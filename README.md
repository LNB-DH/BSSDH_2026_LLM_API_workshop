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
| `workshop_session_0.ipynb` | Beginner preparation: Colab, Jupyter notebooks, Markdown, variables, and Python basics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_0.ipynb) |
| `workshop_session_1.ipynb` | LLM and API basics, OpenRouter setup, first API requests, JSON | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_1.ipynb) |
| `workshop_session_2.ipynb` | Latvian Economic Review corpus, named entities, summaries, concept mining, batch processing | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_2.ipynb) |
| `workshop_session_3.ipynb` | **Optional Session 3:** Rigasche Zeitung corpus, historical OCR, translation, and image inputs | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/workshop_session_3.ipynb) |
| `assignment_llm_api.ipynb` | Credit assignment: design a prompt, analyze a fixed historical mini-corpus, and interpret results | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LNB-DH/BSSDH_2026_LLM_API_workshop/blob/main/notebooks/assignment_llm_api.ipynb) |

Participants with no prior experience using Google Colab, Jupyter notebooks, or
Python should complete `workshop_session_0.ipynb` a day or a few days before the
workshop.

During Session 3, most participants should continue from
`workshop_session_2.ipynb` to `assignment_llm_api.ipynb`. The Session 3 notebook
is an optional extension for participants who have finished the assignment or
want additional practice with historical OCR, translation, and multimodal input.

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
locally, see [LOCAL_INSTRUCTIONS.md](LOCAL_INSTRUCTIONS.md) for detailed VS Code
setup notes for Windows, macOS, and Ubuntu Linux.

The local Python packages are listed in [requirements.txt](requirements.txt).
Install them into a virtual environment before running the notebooks locally.

The notebooks download workshop data as needed, so the data files are not stored
directly in this repository.

## Workshop Context

The workshop is part of
[BSSDH 2026](https://digitalhumanities.lv/en/bssdh/2026/), held in Riga at the
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

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Valdis%20Saulespurens-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/valdis-saulespurens/)

## Related Links

- [BSSDH 2026 home page](https://www.digitalhumanities.lv/bssdh/2026/)
- [All BSSDH 2026 lectures and workshops](https://www.digitalhumanities.lv/bssdh/2026/lectures-and-workshops/)
- [2025 workshop repository](https://github.com/ValRCS/BSSDH_2025_workshop_LLM_API)

## Instructor Materials

Organizer-only notebooks for provisioning and emailing workshop API keys are
documented in [notebooks/for_instructors/README.md](notebooks/for_instructors/README.md).
