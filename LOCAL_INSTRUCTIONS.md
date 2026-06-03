# Local Setup Instructions

These instructions are for participants or instructors who want to run the
BSSDH 2026 LLM API Workshop notebooks locally in Visual Studio Code instead of
Google Colab. Colab remains the expected workshop environment. Local setup is
useful if you already work in VS Code, want files to stay on your computer, or
want to continue the exercises after the workshop.

The guidance below is written for current VS Code Desktop users as of summer
2026. It assumes a normal personal laptop or desktop and a fresh clone or
download of this repository.

## What You Need

- Visual Studio Code Desktop for Windows, macOS, or Linux.
- Python 3.11 or newer. Python 3.12, 3.13, or 3.14 are all suitable for these
  notebooks. If you already have Python 3.11+ working, you do not need to
  reinstall Python just to use the newest release.
- Git, if you want to clone the repository from the command line. Downloading a
  ZIP file from GitHub also works.
- Internet access. The notebooks call LLM APIs and download public workshop
  data from GitHub.
- A workshop OpenRouter API key. Workshop participants receive this key before
  the session. You do not need to create your own OpenRouter account for the
  workshop exercises.

Recommended VS Code extensions:

- `Python` by Microsoft (`ms-python.python`)
- `Jupyter` by Microsoft (`ms-toolsai.jupyter`)
- `Pylance` by Microsoft (`ms-python.vscode-pylance`)

Optional extensions:

- `GitHub Pull Requests` if you work with GitHub inside VS Code.
- `WSL` if you are on Windows and deliberately choose to run the Linux/Ubuntu
  path in Windows Subsystem for Linux.

GitHub Copilot and other AI coding extensions are not required for this
workshop.

Official reference pages:

- [Python in VS Code](https://code.visualstudio.com/docs/languages/python)
- [Jupyter notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- [VS Code setup overview](https://code.visualstudio.com/docs/setup/setup-overview)
- [Python virtual environments](https://docs.python.org/3/library/venv.html)
- [Python setup and usage](https://docs.python.org/3/using/index.html)

## Get the Repository

If you use Git:

```powershell
git clone https://github.com/LNB-DH/BSSDH_2026_LLM_API_workshop.git
cd BSSDH_2026_LLM_API_workshop
code .
```

If you do not use Git, download the repository ZIP file from GitHub, extract it,
then open the extracted folder in VS Code with `File > Open Folder`.

Open the repository folder, not only an individual notebook file. VS Code uses
the open folder to find `.venv`, `requirements.txt`, images, and downloaded
data paths.

## Windows Path

Use this path for a normal native Windows setup with PowerShell.

1. Install VS Code.

   Use the official Windows User setup unless your organization requires a
   system-wide install:
   [Installing VS Code on Windows](https://code.visualstudio.com/docs/setup/windows).

2. Install Python.

   Current Python for Windows documentation recommends the Python install
   manager from `python.org/downloads` or the Microsoft Store. After
   installation, open a new PowerShell terminal and check:

   ```powershell
   python --version
   py --version
   ```

   At least one of those commands should show Python 3.11 or newer. If both
   fail, restart the terminal or check whether Python was added to your user
   path.

3. Open the repository folder in VS Code.

   In VS Code, open `Terminal > New Terminal`. The default terminal is usually
   PowerShell.

4. Create a virtual environment.

   ```powershell
   py -m venv .venv
   ```

   If `py` is not available but `python` works, use:

   ```powershell
   python -m venv .venv
   ```

5. Activate the environment.

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation with an execution policy error, either run
   this one-time command for your Windows user:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

   Then open a new terminal and activate again. If you cannot change the policy,
   you can skip activation and run the venv Python directly:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

6. Install the libraries.

   With the environment activated:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

7. Register a clear notebook kernel name.

   ```powershell
   python -m ipykernel install --user --name bssdh-2026 --display-name "Python (BSSDH 2026)"
   ```

8. Install VS Code extensions.

   Use the Extensions view in VS Code and install `Python`, `Jupyter`, and
   `Pylance` by Microsoft. If the `code` command is available, this also works:

   ```powershell
   code --install-extension ms-python.python
   code --install-extension ms-toolsai.jupyter
   code --install-extension ms-python.vscode-pylance
   ```

## macOS Path

Use this path for a normal macOS setup with Terminal or the VS Code integrated
terminal. Current macOS uses `zsh` by default.

1. Install VS Code.

   Download the macOS build and drag `Visual Studio Code.app` to Applications:
   [Installing VS Code on macOS](https://code.visualstudio.com/docs/setup/mac).

   To make the `code` command available, open VS Code, press
   `Cmd+Shift+P`, run `Shell Command: Install 'code' command in PATH`, then
   restart Terminal.

2. Install Python.

   Install a recent Python 3 release from
   [python.org/downloads](https://www.python.org/downloads/) or use Homebrew if
   that is already your normal package manager:

   ```zsh
   brew install python
   ```

   Check the version:

   ```zsh
   python3 --version
   ```

   It should show Python 3.11 or newer.

3. Open the repository folder in VS Code.

   ```zsh
   cd BSSDH_2026_LLM_API_workshop
   code .
   ```

4. Create and activate a virtual environment.

   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install the libraries.

   ```zsh
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

6. Register a clear notebook kernel name.

   ```zsh
   python -m ipykernel install --user --name bssdh-2026 --display-name "Python (BSSDH 2026)"
   ```

7. Install VS Code extensions.

   Use the Extensions view in VS Code and install `Python`, `Jupyter`, and
   `Pylance` by Microsoft. If the `code` command is available:

   ```zsh
   code --install-extension ms-python.python
   code --install-extension ms-toolsai.jupyter
   code --install-extension ms-python.vscode-pylance
   ```

If HTTPS downloads fail from Python on macOS with certificate errors after a
python.org install, open the Python folder in Applications and run
`Install Certificates.command`.

## Ubuntu Linux Path

Ubuntu is optional for this workshop, but it is a good path for Linux users and
for Windows users who intentionally work through WSL.

1. Install system packages.

   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip git
   ```

2. Install VS Code.

   Use the official `.deb` package or the Snap package:
   [Installing VS Code on Linux](https://code.visualstudio.com/docs/setup/linux).
   For Snap:

   ```bash
   sudo snap install --classic code
   ```

3. Open the repository folder.

   ```bash
   git clone https://github.com/LNB-DH/BSSDH_2026_LLM_API_workshop.git
   cd BSSDH_2026_LLM_API_workshop
   code .
   ```

4. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install the libraries.

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

6. Register a clear notebook kernel name.

   ```bash
   python -m ipykernel install --user --name bssdh-2026 --display-name "Python (BSSDH 2026)"
   ```

7. Install VS Code extensions.

   ```bash
   code --install-extension ms-python.python
   code --install-extension ms-toolsai.jupyter
   code --install-extension ms-python.vscode-pylance
   ```

If Ubuntu reports that `ensurepip` or `venv` is missing, install
`python3-venv` and recreate `.venv`. Avoid `sudo pip install`; use the virtual
environment instead.

## Check the Installation

After installing requirements, run this inside the activated `.venv`:

```bash
python -c "import openai, requests, tqdm, dotenv, IPython; print('Workshop Python environment OK')"
```

On Windows PowerShell, the same command works:

```powershell
python -c "import openai, requests, tqdm, dotenv, IPython; print('Workshop Python environment OK')"
```

If this command prints `Workshop Python environment OK`, the participant
notebooks have the required libraries.

The instructor notebooks also use `pandas`, `openpyxl`, and `sendgrid`, which
are included in `requirements.txt`.

## Running the Notebooks in VS Code

1. Open the repository folder in VS Code.
2. Open `notebooks/workshop_session_0.ipynb` first if you are new to Python,
   notebooks, or Markdown.
3. Click `Select Kernel` in the upper-right area of the notebook editor.
4. Choose `Python (BSSDH 2026)` if you registered the kernel name above. If it
   is not listed, choose the interpreter inside `.venv`.
5. Run cells one at a time with the play button next to each cell, or use
   `Run All` after you are comfortable with the notebook.

The first session notebooks are designed to be run top to bottom. Later cells
often depend on variables created in earlier cells.

## API Keys and `.env`

The notebooks use OpenRouter. During the workshop, participants receive an API
key from the organizers.

The safest beginner path is to paste the key only into the hidden prompt shown
by the notebook. Do not paste an API key into a Markdown cell, a code cell that
will be committed, a screenshot, or a shared document.

For local work, you may also create a file named `.env` in the repository root:

```text
OPENROUTER_API_KEY=your_key_here
```

The repository `.gitignore` already excludes `.env`, so it should not be
committed. Still, treat it as a private file.

Instructor-only notebooks use additional private environment variables:

```text
OPEN_ROUTER_BSSDH_PROVISIONER=your_admin_key_here
SENDGRID_API=your_sendgrid_key_here
SENDGRID_FROM_EMAIL=verified_sender@example.org
```

Do not use instructor notebooks unless you are preparing workshop keys or
participant email messages.

## Files Created Locally

The notebooks may create local folders or files for downloaded data, extracted
corpora, generated responses, temporary spreadsheets, and `.env` settings. These
are intentionally not stored in the repository.

Do not commit:

- `.env`
- `.venv`
- `temp` folders
- downloaded corpus ZIP files
- participant spreadsheets
- executed notebook outputs that show private data or API responses you do not
  want to share

Before sharing a notebook, use `Clear All Outputs` in VS Code if it contains
private paths, keys, participant data, or expensive API responses.

## Troubleshooting

`python` or `py` is not found on Windows:

Install Python from `python.org/downloads` or the Microsoft Store, restart
PowerShell, and try again. If Windows opens the Store instead of Python, check
Windows App Execution Aliases and disable old broken Python aliases.

PowerShell says `Activate.ps1 cannot be loaded`:

Use `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then open a new
terminal and activate again. If you cannot change policy, call
`.\.venv\Scripts\python.exe -m pip ...` directly.

VS Code cannot see the `.venv` environment:

Restart VS Code, open the repository folder, then run `Python: Select
Interpreter` from the Command Palette and choose the `.venv` interpreter.

The notebook says `No module named requests`, `openai`, `dotenv`, or `tqdm`:

The notebook is probably using the wrong kernel. Select `Python (BSSDH 2026)`
or the `.venv` interpreter, then rerun the cell. If needed, reinstall with
`python -m pip install -r requirements.txt` while `.venv` is active.

VS Code asks to install `ipykernel`:

Use the terminal in the activated `.venv` and run:

```bash
python -m pip install ipykernel
```

Then select the kernel again.

Ubuntu shows an `externally-managed-environment` pip error:

You are trying to install packages into the system Python. Create and activate
`.venv`, then run pip from inside it.

Notebook data download fails:

Check internet access and whether your network blocks GitHub downloads. On
macOS with python.org Python, certificate errors may be fixed by running
`Install Certificates.command` from the Python Applications folder.

API calls fail with `401` or authentication errors:

Check that your OpenRouter API key has no extra spaces, is still active, and
was pasted into the hidden prompt or stored as `OPENROUTER_API_KEY` in `.env`.

API calls fail with rate-limit or budget errors:

Pause before retrying. Repeated reruns can spend credit quickly. For workshop
assignments, process a small sample first before running larger batches.

## Resetting the Local Environment

If the local Python environment becomes confusing, delete `.venv` and recreate
it. Do not delete notebooks or workshop data unless you mean to remove your
work.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS or Linux:

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Only remove `.venv`. Do not run broad cleanup commands in the repository unless
you understand exactly which files they will delete.
