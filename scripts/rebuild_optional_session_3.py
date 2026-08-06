import hashlib
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks" / "workshop_session_3.ipynb"


def normalized(text):
    return dedent(text).strip() + "\n"


cells = []


def add_cell(cell_type, source):
    source = normalized(source)
    cell_id = hashlib.sha1(
        f"{len(cells)}:{cell_type}:{source}".encode("utf-8")
    ).hexdigest()[:8]
    cell = {
        "cell_type": cell_type,
        "id": cell_id,
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    cells.append(cell)


add_cell("markdown", r'''
    # Using LLMs in Humanities Research via API

    ## Optional Session 3 (15.40–17.10) — Historical OCR, translation, and image input

    **BSSDH 2026 · Riga · 6 August 2026**

    [![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_3.ipynb)

    > **This notebook is optional.** Most participants should continue from Session 2 to the assessed [`assignment_llm_api.ipynb`](assignment_llm_api.ipynb). Use this notebook if you have finished the assignment, want an additional challenge, or are exploring historical OCR and multimodal research workflows after the workshop.

    We reuse the 2025 *Rigasche Zeitung* data and the same core activities—corpus inspection, OCR normalization, translation, and image input—but run them as a shorter, auditable 2026 extension.
''')

add_cell("markdown", r'''
    ## Choose your route

    | Route | Recommended for | Time | Model calls |
    |---|---|---:|---:|
    | **Primary: assignment** | Most participants | 60–90 minutes | Normally 6 |
    | **Optional quick path: this notebook** | Participants wanting an OCR/multimodal extension | 25–45 minutes | Normally 3 |
    | **Additional Latvian translation** | Participants with time or language interest | +5–10 minutes | +1 |
    | **Full-corpus inventory** | Post-workshop exploration | Variable | 0 |

    The quick path makes one German normalization call, one English translation call, and one image-based call. Every call requires you to type `RUN`; rerunning a cell reuses a successful response when its prompt ID is unchanged.

    Do **not** send the complete 4,597-document corpus to a model merely because a loop could do so. Sampling, cost estimation, source rights, and validation are research-design decisions.
''')

add_cell("markdown", r'''
    ## Learning goals

    By the end of the optional path, you should be able to:

    - inspect a fixed historical source before asking a model to transform it;
    - distinguish OCR transcription, language normalization, and translation;
    - send text and a local page image through the OpenRouter API;
    - retain model, prompt, source, usage, and timing metadata;
    - identify plausible-looking corrections that are not supported by the scan; and
    - explain why an LLM output is a research object to validate, not a recovered ground truth.

    **Prerequisite:** complete Sessions 1 and 2, or be comfortable running notebook cells and reading basic Python dictionaries and functions.
''')

add_cell("markdown", r'''
    ## 1. Reusing the 2025 *Rigasche Zeitung* corpus

    The data remains in the public [BSSDH 2025 workshop data repository](https://github.com/LNB-DH/BSSDH_2025_workshop_data). Keeping the same fixed source makes it possible to compare teaching examples across workshop years; the repository year is part of the data provenance and should not be changed to 2026.

    *Rigasche Zeitung* was a German-language Riga newspaper printed in Fraktur. The full 1918–1919 archive contains 4,597 OCR-derived text segments from 359 issues. The OCR was produced with an older workflow and was deliberately not normalized in the workshop data.

    The main path uses `RigascheZeitung_samples.zip`, containing four issues, 38 text files, 21 page images, and three small database files. We focus on issue 62 from 15 March 1918 and compare one page image with its first OCR segment.

    Data and historical overview: [LNB-DH/BSSDH_2025_workshop_data](https://github.com/LNB-DH/BSSDH_2025_workshop_data). Periodical record: [periodika.lv](https://periodika.lv/#periodicalMeta:234;-1).
''')

add_cell("markdown", r'''
    ## 2. Prepare the runtime

    The next cell installs the same OpenAI-compatible Python client used earlier in the workshop. Installation downloads software; it does not send a historical source or make a model request.
''')

add_cell("code", r'''
    %pip install -q "openai>=1.58,<3"
''')

add_cell("code", r'''
    # Imports and fixed configuration used throughout the optional notebook.
    from io import BytesIO
    from pathlib import Path
    from zipfile import ZipFile
    import base64
    import getpass
    import hashlib
    import json
    import mimetypes
    import time

    import openai
    import requests
    from IPython.display import Image, Markdown, display
    from openai import OpenAI

    SAMPLE_DATA_URL = (
        "https://raw.githubusercontent.com/LNB-DH/"
        "BSSDH_2025_workshop_data/main/data/RigascheZeitung_samples.zip"
    )
    SAMPLE_ARCHIVE_SHA256 = "12ab25a762d3f20b823e705e0fd5b086a5a1cb6fc12280609ea45bdbe5ca9ff1"
    EXPECTED_SAMPLE_TEXTS = 38
    EXPECTED_SAMPLE_IMAGES = 21

    DATA_DIR = Path("data")
    SAMPLE_DIR = DATA_DIR / "RigascheZeitung_samples"
    ISSUE_DIR = SAMPLE_DIR / "1918" / "rzei1918s01n062"
    SELECTED_TEXT_PATH = ISSUE_DIR / "rzei1918s01n062_001_plaintext_s01.txt"
    SELECTED_IMAGE_PATH = ISSUE_DIR / "rzei1918s01n062_001.jpg"

    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    MODEL_ID = "google/gemini-3.5-flash-lite"
    MODEL_CATALOG_CHECKED = "2026-08-06"

    print(f"OpenAI SDK: {openai.__version__}")
    print(f"Requested model: {MODEL_ID} (catalog checked {MODEL_CATALOG_CHECKED})")
    print(f"Sample directory: {SAMPLE_DIR}")
    print("No model request has been sent.")
''')

add_cell("markdown", r'''
    ## 3. Download and verify the fixed sample

    A reproducible workflow checks more than whether a folder exists. The prepared code:

    - reuses a complete cached sample when available;
    - checks the SHA-256 checksum after a fresh download;
    - rejects unsafe archive paths before extraction;
    - verifies the expected text and image counts; and
    - checks that the selected source pair exists.

    If the checksum or counts change, stop and investigate the data version instead of silently continuing.
''')

add_cell("code", r'''
    def safe_extract_zip(archive_bytes, destination):
        """Extract a ZIP only when every member remains inside destination."""
        destination.mkdir(parents=True, exist_ok=True)
        destination_root = destination.resolve()
        with ZipFile(BytesIO(archive_bytes)) as archive:
            for member in archive.infolist():
                target = (destination / member.filename).resolve()
                if not target.is_relative_to(destination_root):
                    raise ValueError(f"Unsafe archive path: {member.filename}")
            archive.extractall(destination)


    def sample_inventory():
        text_files = sorted(SAMPLE_DIR.rglob("*.txt")) if SAMPLE_DIR.exists() else []
        image_files = (
            sorted(SAMPLE_DIR.rglob("*.jpg"))
            + sorted(SAMPLE_DIR.rglob("*.jpeg"))
            + sorted(SAMPLE_DIR.rglob("*.png"))
            if SAMPLE_DIR.exists()
            else []
        )
        return text_files, image_files


    sample_text_files, sample_image_files = sample_inventory()
    sample_ready = (
        len(sample_text_files) == EXPECTED_SAMPLE_TEXTS
        and len(sample_image_files) == EXPECTED_SAMPLE_IMAGES
        and SELECTED_TEXT_PATH.exists()
        and SELECTED_IMAGE_PATH.exists()
    )

    if sample_ready:
        print("Using the already available, complete sample directory.")
    else:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Downloading: {SAMPLE_DATA_URL}")
        download = requests.get(SAMPLE_DATA_URL, timeout=120)
        download.raise_for_status()
        archive_bytes = download.content
        archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()
        if archive_sha256 != SAMPLE_ARCHIVE_SHA256:
            raise ValueError(
                "Sample archive checksum mismatch. Stop and verify whether the public "
                "workshop data has changed."
            )
        safe_extract_zip(archive_bytes, DATA_DIR)
        print("Download checksum: PASS")

    sample_text_files, sample_image_files = sample_inventory()
    if len(sample_text_files) != EXPECTED_SAMPLE_TEXTS:
        raise ValueError(
            f"Expected {EXPECTED_SAMPLE_TEXTS} sample text files, "
            f"found {len(sample_text_files)}. Restart with a clean runtime."
        )
    if len(sample_image_files) != EXPECTED_SAMPLE_IMAGES:
        raise ValueError(
            f"Expected {EXPECTED_SAMPLE_IMAGES} sample images, "
            f"found {len(sample_image_files)}. Restart with a clean runtime."
        )
    if not SELECTED_TEXT_PATH.exists() or not SELECTED_IMAGE_PATH.exists():
        raise FileNotFoundError("The fixed issue-62 source pair is missing.")

    print(f"Sample verification: PASS ({len(sample_text_files)} texts, {len(sample_image_files)} images)")
    print(f"Selected OCR: {SELECTED_TEXT_PATH.name}")
    print(f"Selected scan: {SELECTED_IMAGE_PATH.name}")
''')

add_cell("code", r'''
    # Summarize the four sampled issues without treating file counts as OCR quality.
    issue_directories = sorted(
        path for path in SAMPLE_DIR.glob("*/*") if path.is_dir()
    )

    print("SAMPLE INVENTORY")
    print("=" * 72)
    for issue_path in issue_directories:
        text_count = len(list(issue_path.glob("*.txt")))
        image_count = sum(
            len(list(issue_path.glob(pattern)))
            for pattern in ("*.jpg", "*.jpeg", "*.png")
        )
        print(
            f"{issue_path.relative_to(SAMPLE_DIR)!s:34} "
            f"texts={text_count:2d}  images={image_count:2d}"
        )
''')

add_cell("markdown", r'''
    ## 4. Inspect one fixed source pair

    We use a documented source rather than an arbitrary list position:

    - issue: `rzei1918s01n062`, Friday, 15 March 1918;
    - page scan: `rzei1918s01n062_001.jpg`;
    - OCR segment: `rzei1918s01n062_001_plaintext_s01.txt`, *Die Befreiung Revals*.

    The working excerpt is lines 7–32 of the OCR file. It contains recognizable language as well as uncertain characters, broken words, and corrupted numbers. Keeping the excerpt fixed makes the later calls easier to compare.
''')

add_cell("code", r'''
    selected_document = SELECTED_TEXT_PATH.read_text(encoding="utf-8")
    selected_lines = selected_document.splitlines()
    working_excerpt = "\n".join(selected_lines[6:32]).strip()
    source_sha256 = hashlib.sha256(selected_document.encode("utf-8")).hexdigest()
    excerpt_sha256 = hashlib.sha256(working_excerpt.encode("utf-8")).hexdigest()

    print("SOURCE METADATA")
    print("=" * 72)
    print("\n".join(selected_lines[:3]))
    print(f"Source characters: {len(selected_document):,}")
    print(f"Source SHA-256: {source_sha256}")
    print(f"Working excerpt SHA-256: {excerpt_sha256}")
    display(Markdown(f"### Fixed OCR excerpt\n\n```text\n{working_excerpt}\n```"))
''')

add_cell("code", r'''
    print(f"Displaying: {SELECTED_IMAGE_PATH}")
    display(Image(filename=str(SELECTED_IMAGE_PATH), width=900))
''')

add_cell("markdown", r'''
    ### Source criticism before model use

    Record brief observations before making a request:

    1. Which words or characters in the OCR excerpt appear uncertain?
    2. Find the line containing `Ъ% 22, 20 und 8,7 Kilometer`. Can the first value be recovered confidently from the OCR text alone?
    3. Which features of the page image may make automatic recognition difficult: Fraktur, column layout, font size, skew, contrast, or physical damage?
    4. What would count as a correction, and what would count as an unsupported rewrite?

    Visual inspection can suggest problems, but claims such as scan DPI, OCR accuracy, or “perfect alignment” require metadata or measurement. Digit density and punctuation counts are descriptive features, not valid OCR-accuracy scores. A formal evaluation would compare the OCR with a manually corrected reference using character or word error rate and documented error categories.
''')

add_cell("markdown", r'''
    ## 5. Configure the 2026 OpenRouter client

    The optional notebook now uses [Google Gemini 3.5 Flash Lite](https://openrouter.ai/google/gemini-3.5-flash-lite), matching the model selected in Session 2. As checked on 6 August 2026, it accepts both text and image input.

    The core API pattern has not changed: OpenRouter still offers an OpenAI-compatible chat-completions endpoint, and a local image can be supplied as a base64 `image_url`. Model availability, supported parameters, routing, and pricing can change, so the model ID and check date remain visible configuration.

    The key is requested with hidden input and kept only in runtime memory. Do not send confidential, personal, culturally sensitive, unpublished, or rights-restricted material without authority and a review of [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection) and provider policies.
''')

add_cell("code", r'''
    OPENROUTER_API_KEY = getpass.getpass("Paste your OpenRouter API key (hidden): ").strip()
    if not OPENROUTER_API_KEY:
        raise ValueError("No API key was entered.")

    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": "https://digitalhumanities.lv/en/bssdh/2026/",
            "X-OpenRouter-Title": "BSSDH 2026 LLM API Workshop",
        },
    )

    if "api_records" not in globals():
        api_records = {}


    def build_prompt_id(*parts):
        joined = "\n\n".join(str(part) for part in parts)
        return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


    def run_confirmed(
        record_key,
        prompt_id,
        messages,
        request_label,
        *,
        max_completion_tokens=1400,
    ):
        """Make one confirmed call, or reuse a successful matching response."""
        existing = api_records.get(record_key)
        same_successful_request = (
            existing is not None
            and existing.get("prompt_id") == prompt_id
            and existing.get("request_status") == "received"
        )

        if same_successful_request:
            action = input(
                "Press Enter to reuse this response, or type RUN to replace it: "
            )
            if action.strip().upper() != "RUN":
                print("Reusing the successful response for this prompt ID.")
                return existing
        else:
            action = input(
                f"Type RUN to make one API call for {request_label}, "
                "or press Enter to cancel: "
            )
            if action.strip().upper() != "RUN":
                print("No API call was made.")
                return None

        started = time.perf_counter()
        try:
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=messages,
                max_completion_tokens=max_completion_tokens,
            )
            response_text = response.choices[0].message.content or ""
            if not response_text.strip():
                raise RuntimeError("The API returned no generated text.")
            usage = response.usage.model_dump(mode="json") if response.usage else {}
            record = {
                "record_key": record_key,
                "prompt_id": prompt_id,
                "request_status": "received",
                "request_error": "",
                "source_name": SELECTED_TEXT_PATH.name,
                "source_sha256": source_sha256,
                "excerpt_sha256": excerpt_sha256,
                "requested_model": MODEL_ID,
                "returned_model": response.model,
                "response_id": response.id,
                "raw_response": response_text,
                "usage": usage,
                "elapsed_seconds": round(time.perf_counter() - started, 2),
            }
        except Exception as exc:
            record = {
                "record_key": record_key,
                "prompt_id": prompt_id,
                "request_status": "failed",
                "request_error": f"{type(exc).__name__}: {exc}",
                "source_name": SELECTED_TEXT_PATH.name,
                "source_sha256": source_sha256,
                "excerpt_sha256": excerpt_sha256,
                "requested_model": MODEL_ID,
                "returned_model": "",
                "response_id": "",
                "raw_response": "",
                "usage": {},
                "elapsed_seconds": round(time.perf_counter() - started, 2),
            }

        api_records[record_key] = record
        print(f"Request status: {record['request_status']}")
        if record["request_status"] == "failed":
            print(record["request_error"])
        return record


    def show_record(record):
        if not record:
            print("No current response to display.")
            return
        if record["request_status"] == "failed":
            print("Request failed:", record["request_error"])
            return
        usage = record.get("usage") or {}
        print(f"Prompt ID:       {record['prompt_id']}")
        print(f"Requested model: {record['requested_model']}")
        print(f"Returned model:  {record['returned_model']}")
        print(f"Response ID:     {record['response_id']}")
        print(f"Elapsed:         {record['elapsed_seconds']} seconds")
        print(f"Input tokens:    {usage.get('prompt_tokens', 'not returned')}")
        print(f"Output tokens:   {usage.get('completion_tokens', 'not returned')}")
        print(f"Reported cost:   {usage.get('cost', 'not returned')}")
        print("\nMODEL OUTPUT\n" + "-" * 72)
        print(record["raw_response"])


    print("API helper ready. No model request has been sent yet.")
''')

add_cell("markdown", r'''
    ## 6. Call 1 — OCR-aware normalization into modern German

    OCR transcription and language normalization are different transformations. This prompt asks for readable modern German while requiring the model to preserve names and numbers, mark uncertainty, and avoid silent invention.

    Read the prompt preview before authorizing the call. Afterward, compare the result with the OCR and scan rather than asking only whether the result sounds fluent.
''')

add_cell("code", r'''
    NORMALIZE_SYSTEM = """
    You are a careful editor of historical German OCR. Work only from the supplied
    OCR excerpt. Produce readable modern German while preserving meaning, names,
    quantities, and the distinction between what is visible and what is uncertain.
    Correct an OCR form only when the supplied text supports the correction. Never
    silently guess missing characters or numbers. Mark an uncertain reading as
    [UNSICHER: original OCR]. Return exactly two sections titled NORMALISIERTER TEXT
    and UNSICHERE STELLEN. Do not add historical facts or commentary.
    """.strip()

    NORMALIZE_TASK = f"""
    SOURCE ID: {SELECTED_TEXT_PATH.name}

    OCR EXCERPT:
    {working_excerpt}

    TASK:
    Normalize this excerpt into readable modern German under the stated rules.
    """.strip()

    normalization_messages = [
        {"role": "system", "content": NORMALIZE_SYSTEM},
        {"role": "user", "content": NORMALIZE_TASK},
    ]
    normalization_prompt_id = build_prompt_id(
        MODEL_ID, NORMALIZE_SYSTEM, NORMALIZE_TASK, excerpt_sha256
    )

    print(f"Prompt ID: {normalization_prompt_id}")
    print(json.dumps(normalization_messages, indent=2, ensure_ascii=False))
''')

add_cell("code", r'''
    normalization_record = run_confirmed(
        "german_normalization",
        normalization_prompt_id,
        normalization_messages,
        "German OCR normalization",
    )
    show_record(normalization_record)
''')

add_cell("markdown", r'''
    ## 7. Call 2 — Translate the original OCR into English

    The translation deliberately starts from the original OCR, not the model's German normalization. This keeps the two calls independent and exposes places where a fluent translation may hide a different guess.

    Check names, distances, dates, and other specific details. Fluency is not evidence that a damaged reading is correct.
''')

add_cell("code", r'''
    ENGLISH_SYSTEM = """
    You are a careful translator of historical German OCR into modern English. Work
    only from the supplied OCR excerpt. Preserve names, quantities, uncertainty, and
    the source's viewpoint. Do not silently repair unreadable characters or add facts.
    Mark an uncertain source reading as [UNCERTAIN: original OCR]. Return exactly two
    sections titled ENGLISH TRANSLATION and UNCERTAIN READINGS.
    """.strip()

    ENGLISH_TASK = f"""
    SOURCE ID: {SELECTED_TEXT_PATH.name}

    OCR EXCERPT:
    {working_excerpt}

    TASK:
    Translate this excerpt into modern English under the stated rules.
    """.strip()

    english_messages = [
        {"role": "system", "content": ENGLISH_SYSTEM},
        {"role": "user", "content": ENGLISH_TASK},
    ]
    english_prompt_id = build_prompt_id(
        MODEL_ID, ENGLISH_SYSTEM, ENGLISH_TASK, excerpt_sha256
    )

    english_record = run_confirmed(
        "english_translation",
        english_prompt_id,
        english_messages,
        "English translation",
    )
    show_record(english_record)
''')

add_cell("markdown", r'''
    ## ⭐ Optional Call — Translate the original OCR into Latvian

    The core optional path does not require this call. Use it if you want to compare how the same model handles a less common target language. The evaluation question remains source fidelity, not which output sounds most polished.
''')

add_cell("code", r'''
    LATVIAN_SYSTEM = """
    You are a careful translator of historical German OCR into modern Latvian. Work
    only from the supplied OCR excerpt. Preserve names, quantities, uncertainty, and
    the source's viewpoint. Do not silently repair unreadable characters or add facts.
    Mark an uncertain source reading as [NESKAIDRS: original OCR]. Return exactly two
    sections titled TULKOJUMS LATVIEŠU VALODĀ and NESKAIDRĀS VIETAS.
    """.strip()

    LATVIAN_TASK = f"""
    SOURCE ID: {SELECTED_TEXT_PATH.name}

    OCR EXCERPT:
    {working_excerpt}

    TASK:
    Translate this excerpt into modern Latvian under the stated rules.
    """.strip()

    latvian_messages = [
        {"role": "system", "content": LATVIAN_SYSTEM},
        {"role": "user", "content": LATVIAN_TASK},
    ]
    latvian_prompt_id = build_prompt_id(
        MODEL_ID, LATVIAN_SYSTEM, LATVIAN_TASK, excerpt_sha256
    )

    latvian_record = run_confirmed(
        "latvian_translation",
        latvian_prompt_id,
        latvian_messages,
        "optional Latvian translation",
    )
    show_record(latvian_record)
''')

add_cell("markdown", r'''
    ## 8. Call 3 — Supply the page image and OCR together

    A multimodal model can inspect the scan, but it does not automatically become a reliable OCR engine. The task is deliberately narrow: examine the headline and opening paragraph corresponding to the fixed excerpt, propose a transcription, and separate visible readings from uncertain ones.

    The user message contains both a text instruction and a base64-encoded local image. Base64 is transport encoding, not encryption; the image is still sent to OpenRouter and the selected provider.
''')

add_cell("code", r'''
    mime_type, _ = mimetypes.guess_type(SELECTED_IMAGE_PATH)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError(f"Unsupported image type: {SELECTED_IMAGE_PATH}")

    image_bytes = SELECTED_IMAGE_PATH.read_bytes()
    image_sha256 = hashlib.sha256(image_bytes).hexdigest()
    image_data_url = (
        f"data:{mime_type};base64," + base64.b64encode(image_bytes).decode("ascii")
    )

    VISION_SYSTEM = """
    You are a careful researcher transcribing a historical German newspaper scan.
    Report only what is supported by the supplied image and comparison OCR. Focus on
    the article titled 'Die Befreiung Revals.' Preserve original spelling in the
    transcription. Mark unreadable characters as [?] and uncertain readings with
    [?word]. Do not infer a damaged number from context. Return exactly three sections:
    IMAGE-BASED TRANSCRIPTION, DIFFERENCES FROM SUPPLIED OCR, and UNCERTAINTIES.
    """.strip()

    VISION_TASK = f"""
    Inspect the headline and opening paragraph of the article 'Die Befreiung Revals.'
    on this page. Transcribe the corresponding passage through the sentence ending
    'Kilometer zurückgelegt.' Then compare it with this supplied OCR excerpt:

    {working_excerpt}
    """.strip()

    vision_messages = [
        {"role": "system", "content": VISION_SYSTEM},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": VISION_TASK},
                {
                    "type": "image_url",
                    "image_url": {"url": image_data_url, "detail": "high"},
                },
            ],
        },
    ]
    vision_prompt_id = build_prompt_id(
        MODEL_ID, VISION_SYSTEM, VISION_TASK, excerpt_sha256, image_sha256
    )

    print(f"Image: {SELECTED_IMAGE_PATH.name}")
    print(f"Image bytes: {len(image_bytes):,}")
    print(f"Image SHA-256: {image_sha256}")
    print(f"Prompt ID: {vision_prompt_id}")
    print("Multimodal request prepared; the base64 payload is intentionally not printed.")
''')

add_cell("code", r'''
    vision_record = run_confirmed(
        "image_transcription",
        vision_prompt_id,
        vision_messages,
        "image-based transcription",
        max_completion_tokens=1800,
    )
    show_record(vision_record)
''')

add_cell("markdown", r'''
    ## 9. Compare the source and generated transformations

    Last year's saved notebook outputs reconstructed the damaged distance differently across languages. That disagreement is useful evidence: a model can turn uncertainty into several different fluent answers.

    Focus especially on:

    - `.I»k«l« Anzeigers"` and `Eronheim`;
    - `Große Kursürst` and `da» Haff`;
    - `Ъ% 22, 20 und 8,7 Kilometer`; and
    - `bis zu 7b Kilo., meter täglich`.

    The next cell gathers any responses you chose to run. It does not score them automatically; source interpretation remains a research task.
''')

add_cell("code", r'''
    focus_excerpt = "\n".join(selected_lines[6:32])
    display(Markdown(f"### Original OCR for comparison\n\n```text\n{focus_excerpt}\n```"))

    comparison_keys = [
        ("German normalization", "german_normalization"),
        ("English translation", "english_translation"),
        ("Latvian translation (optional)", "latvian_translation"),
        ("Image-based transcription", "image_transcription"),
    ]

    for label, record_key in comparison_keys:
        record = api_records.get(record_key)
        if record and record.get("request_status") == "received":
            display(Markdown(f"### {label}\n\n{record['raw_response']}"))
        else:
            print(f"{label}: not run or no successful response")
''')

add_cell("markdown", r'''
    ### Debrief: what counts as success?

    Complete a small comparison in your own notes:

    | Source span | Model reading | Supported by image? | Error or uncertainty type | Researcher decision |
    |---|---|---|---|---|
    | `[copy one OCR span]` | `[copy the generated reading]` | yes / no / unclear | character, word boundary, number, name, translation, omission | accept / reject / retain uncertainty |

    Discuss:

    1. Did each output preserve uncertainty, or silently choose a plausible reading?
    2. Did modernization alter historical rhetoric or only spelling and OCR errors?
    3. Did translation introduce a more specific claim than the German source supports?
    4. Did the image-based call improve the OCR, and how did you verify that?
    5. What manually corrected sample would you need before making a corpus-level accuracy claim?

    A successful API response is not automatically a valid research result. Preserve the source, document every transformation, validate a defensible sample, and report unresolved ambiguity.
''')

add_cell("markdown", r'''
    ## What changed since the 2025 notebook?

    - **Workshop role:** Session 3 is now explicitly optional because most participants use this block for the independent assignment.
    - **Model:** the notebook now requests `google/gemini-3.5-flash-lite`; the model ID and catalog-check date are centralized.
    - **Stable core API:** OpenRouter's OpenAI-compatible chat-completions shape and base64 `image_url` input remain suitable for the original exercises.
    - **Better audit trail:** each call retains source and excerpt hashes, prompt ID, requested and returned model, response ID, timing, usage, and reported cost when available.
    - **Research framing:** OCR diagnostics are no longer presented as accuracy scores, and prompts must preserve uncertainty rather than silently repair it.
    - **Current optional features:** compatible models can use API-level [structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs). Add them only after the source-grounded workflow is understood; valid JSON does not establish historical correctness.
    - **Privacy controls:** provider logging, retention, training, and Zero Data Retention routing require explicit review for real research data. See [OpenRouter privacy documentation](https://openrouter.ai/docs/guides/privacy/data-collection).
''')

add_cell("markdown", r'''
    ## ⭐ Advanced extension — inventory the full corpus

    The sample is sufficient for every exercise above. The next cell optionally downloads the complete 1918–1919 text corpus and verifies all 4,597 files. It makes no model requests.

    Only run it if you deliberately want to explore corpus structure after the workshop. The full corpus still needs a documented sampling plan before API processing.
''')

add_cell("code", r'''
    FULL_CORPUS_URL = (
        "https://raw.githubusercontent.com/LNB-DH/"
        "BSSDH_2025_workshop_data/main/data/Rigasche_Zeitung_1918_1919.zip"
    )
    FULL_ARCHIVE_SHA256 = "5e73bb2b120911f010c2fea6c90718f97cdae15bbb635c7826c15faded6362a2"
    EXPECTED_FULL_TEXTS = 4597
    FULL_CORPUS_DIR = DATA_DIR / "Rigasche_Zeitung_1918_1919"

    full_text_files = (
        sorted(FULL_CORPUS_DIR.rglob("*.txt"))
        if FULL_CORPUS_DIR.exists()
        else []
    )

    if len(full_text_files) == EXPECTED_FULL_TEXTS:
        print(f"Full corpus already available: {len(full_text_files):,} text files.")
    else:
        confirmation = input(
            "Type DOWNLOAD FULL CORPUS to download and extract it, "
            "or press Enter to cancel: "
        )
        if confirmation.strip() == "DOWNLOAD FULL CORPUS":
            response = requests.get(FULL_CORPUS_URL, timeout=120)
            response.raise_for_status()
            full_archive_bytes = response.content
            full_archive_sha256 = hashlib.sha256(full_archive_bytes).hexdigest()
            if full_archive_sha256 != FULL_ARCHIVE_SHA256:
                raise ValueError(
                    "Full-corpus checksum mismatch. Stop and verify the data version."
                )
            safe_extract_zip(full_archive_bytes, DATA_DIR)
            full_text_files = sorted(FULL_CORPUS_DIR.rglob("*.txt"))
            if len(full_text_files) != EXPECTED_FULL_TEXTS:
                raise ValueError(
                    f"Expected {EXPECTED_FULL_TEXTS:,} full-corpus texts, "
                    f"found {len(full_text_files):,}."
                )
            print("Full-corpus checksum: PASS")
            print(f"Full corpus verified: {len(full_text_files):,} text files")
            sizes = [path.stat().st_size for path in full_text_files]
            print(f"Total text bytes: {sum(sizes):,}")
            print(f"Smallest/largest file: {min(sizes):,} / {max(sizes):,} bytes")
        else:
            print("Full-corpus download cancelled.")
''')

add_cell("markdown", r'''
    ## Finish or return to the primary route

    Before leaving this optional notebook, confirm:

    - [ ] I compared generated readings with the OCR and page image.
    - [ ] I treated unresolved characters and numbers as uncertainty rather than filling them silently.
    - [ ] I can identify the requested and returned model for each call.
    - [ ] I inspected token usage and reported cost when available.
    - [ ] My API key is not visible in any cell or output.
    - [ ] I did not interpret a fluent translation as automatic historical accuracy.

    Most participants should now continue or return to [`assignment_llm_api.ipynb`](assignment_llm_api.ipynb). The assignment uses a separate fixed mini-corpus and asks you to make your own analytical decisions.

    Further references: [OpenRouter quickstart](https://openrouter.ai/docs/quickstart), [API reference](https://openrouter.ai/docs/api_reference/overview), [multimodal overview](https://openrouter.ai/docs/guides/overview/multimodal/overview), [structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs), and [errors and debugging](https://openrouter.ai/docs/api/reference/errors-and-debugging).
''')


notebook = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

NOTEBOOK_PATH.write_text(
    json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(f"Wrote {NOTEBOOK_PATH} with {len(cells)} cells")
