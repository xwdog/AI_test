# AI\_test

AI-powered test case generator.



\## Structure

\- `app/`: orchestrator code (pipeline)

\- `prompts/`: prompt templates for the LLM

\- `tests/`: generated + manual tests

\- `.env`: local secrets (not tracked)



\## Quick start 



1\. Create `.env` with `OPENAI\_API\_KEY` and `OPENAI\_MODEL`.

2\. Create venv: `python -m venv .venv` then `.\\.venv\\Scripts\\activate`

3\. Install deps: `pip install -r requirements.txt`

4\. Run: `python app\\pipeline.py









(more in-depth explanation)

0\. Clone this repository and move into the folder:

&nbsp;  ```bash

&nbsp;  git clone <your-repo-url>

&nbsp;  cd AI\_test



1. Create .env with OPENAI\_API\_KEY and OPENAI\_MODEL.



2\. Create venv:



bash



python -m venv .venv

.\\.venv\\Scripts\\activate



3\. Install deps:



bash



pip install -r requirements.txt



4\. Run:



bash



python app\\pipeline.py



---



🔑 Notes:

\- Step 0 makes it clear to \*anyone else\* (or “future you”) how to start from zero.  

\- I formatted commands as fenced code blocks so it’s easy to read and copy.  

\- I also removed the word \*Optional\* from Step 2 → always use a venv.  

