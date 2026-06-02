# BSSDH 2026 LLM API Workshop

Materials for the Baltic Summer School of Digital Humanities 2026 workshop
**Using LLMs in Humanities Research via API**.

This repository contains hands-on notebooks for working with large language
models through APIs, with a focus on batch processing humanities data,
prompting for structured analysis, named entity recognition, concept mining,
OCR quality issues, translation, and multimodal analysis of historical sources.

## Start Here

Most participants should use Google Colab. Colab runs the notebooks in a web
browser, so you do not need to install Python before the workshop.

Tip: right-click a Colab badge and open it in a new tab so this README stays
available while you work.

| Notebook | Topic | Open in Colab |
| --- | --- | --- |
| `workshop_session_1.ipynb` | LLM and API basics, OpenRouter setup, first API requests, JSON | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_1.ipynb) |
| `workshop_session_2.ipynb` | Latvian Economic Review corpus, named entities, summaries, concept mining, batch processing | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_2.ipynb) |
| `workshop_session_3.ipynb` | Rigasche Zeitung corpus, historical OCR, translation, and image inputs | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_3.ipynb) |

An introductory notebook for first-time Google Colab, Jupyter, and Python users
is planned and will be added before the workshop.

## Participant Preparation

Please prepare:

- A Google account for opening and running notebooks in Google Colab.
- A workshop API key. This will be provided to each participant before the
  session, either by email or through another workshop communication channel.

Do not paste your API key into notebook text cells, screenshots, shared documents,
or public code. The notebooks use hidden input prompts for keys.

Participants do not need to create an OpenRouter account or add OpenRouter
credit for this session.

## Optional Local Use

Colab is the expected environment for the workshop. If you prefer to work
locally, you can use VS Code with the Jupyter extension and a Python environment
that includes the packages used by the notebooks, especially:

- `requests`
- `tqdm`
- `python-dotenv`
- `openai`
- `ipykernel`

The notebooks download workshop data as needed, so the data files are not stored
directly in this repository.

## Workshop Context

The workshop is part of
[BSSDH 2026](https://www.digitalhumanities.lv/bssdh/2026/), held in Riga at the
National Library of Latvia from 3-7 August 2026. The 2026 theme is
**Cultural Data Analytics and Meaning**.

[Lectures and workshops](https://www.digitalhumanities.lv/bssdh/2026/lectures-and-workshops/)
include an updated version of the LLM API workshop from the 2025 programme.

## Data

The notebooks use the public workshop data repository:

- [LNB-DH/BSSDH_2025_workshop_data](https://github.com/LNB-DH/BSSDH_2025_workshop_data)

Main corpora used in the exercises:

- `Latvian_Economic_Review_1936_1940.zip` - English-language economic review
  corpus for entity extraction, summarization, and concept mining.
- `Rigasche_Zeitung_1918_1919.zip` and `RigascheZeitung_samples.zip` -
  German-language historical newspaper data for OCR, translation, and
  multimodal experiments.

## Workshop Description

Participants will learn how to access large language models through APIs and
use them for practical humanities data analysis in Python. Through guided
examples, we will explore prompt engineering, structured responses, batch
processing, named entity recognition, concept mining, historical OCR problems,
translation, and model comparison.

The workshop is designed for humanities researchers, students, librarians,
archivists, data analysts, and digital humanities practitioners. No advanced
programming background is expected. The materials are written for participants
who may be using Jupyter notebooks and Python for the first time.

## Instructor

Valdis Saulespurens works as a researcher and developer at the National Library
of Latvia. He is also a lecturer at Riga Technical University, where he teaches
Python, JavaScript, and other computer science subjects. His work focuses on
machine learning, data analysis, and turning disordered data into structured
knowledge.

Contact: valdis.saulespurens at lnb.lv

## Related Links

- [BSSDH 2026 home page](https://www.digitalhumanities.lv/bssdh/2026/)
- [All BSSDH 2026 lectures and workshops](https://www.digitalhumanities.lv/bssdh/2026/lectures-and-workshops/)
- [2025 workshop repository](https://github.com/ValRCS/BSSDH_2025_workshop_LLM_API)
