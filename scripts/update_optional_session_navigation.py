import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
old_row = "| `workshop_session_3.ipynb` | Rigasche Zeitung corpus, historical OCR, translation, and image inputs |"
new_row = "| `workshop_session_3.ipynb` | **Optional Session 3:** Rigasche Zeitung corpus, historical OCR, translation, and image inputs |"
if old_row not in readme:
    raise RuntimeError("Expected Session 3 README row not found")
readme = readme.replace(old_row, new_row, 1)

anchor = (
    "Participants with no prior experience using Google Colab, Jupyter notebooks, or\n"
    "Python should complete `workshop_session_0.ipynb` a day or a few days before the\n"
    "workshop.\n"
)
addition = (
    anchor
    + "\nDuring Session 3, most participants should continue from\n"
    + "`workshop_session_2.ipynb` to `assignment_llm_api.ipynb`. The Session 3 notebook\n"
    + "is an optional extension for participants who have finished the assignment or\n"
    + "want additional practice with historical OCR, translation, and multimodal input.\n"
)
if anchor not in readme:
    raise RuntimeError("Expected README participant-preparation anchor not found")
readme = readme.replace(anchor, addition, 1)
readme_path.write_text(readme, encoding="utf-8")

assignment_path = ROOT / "notebooks" / "assignment_llm_api.ipynb"
assignment = json.loads(assignment_path.read_text(encoding="utf-8"))
optional_cell = next(
    cell
    for cell in assignment["cells"]
    if cell["cell_type"] == "markdown"
    and "# ⭐ Optional extensions" in "".join(cell["source"])
)
optional_source = "".join(optional_cell["source"])
old_bullet = "- investigate whether the model treats statistical and rhetorical evidence differently.\n"
new_bullets = (
    "- investigate whether the model treats statistical and rhetorical evidence differently;\n"
    "- continue with the optional [`workshop_session_3.ipynb`](workshop_session_3.ipynb) "
    "for historical OCR, translation, and image-input experiments.\n"
)
if old_bullet not in optional_source:
    raise RuntimeError("Expected assignment optional-extension bullet not found")
optional_source = optional_source.replace(old_bullet, new_bullets, 1)
optional_cell["source"] = optional_source.splitlines(keepends=True)
assignment_path.write_text(
    json.dumps(assignment, indent=1, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

print("Updated README and assignment navigation")
