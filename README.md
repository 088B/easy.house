# Virtual House Inserter (FastAPI + OpenAI Images Edit)

This simple website lets a user upload a real photo, mark the area where a virtual house should appear, write a description of the house, and then it asks OpenAI's GPT Image model to edit the photo by placing the requested house into the selected region.

Works on macOS. No prior coding knowledge required.

## Quick Start (Mac)
1. Install Homebrew (if you don't have it):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
2. Install Python 3.11:
```
brew install python@3.11
python3 --version
```
3. Create a virtual env and install deps:
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
4. Add your OpenAI key:
- Duplicate `.env.example` to `.env` and paste your key.

5. Run the app:
```
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

See the full README in the ChatGPT message for details.
# easy.house
