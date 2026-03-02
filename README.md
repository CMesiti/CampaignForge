# NarrativeOS
RAG powered TTRPG Assistive Web Application. Need help working through player actions, improvising encounters, balancing random events, or keeping track of campaign notes and details? NarrativeOS supports DMs and players to easily improvise actions and encounters. Upload your notes for a RAG agent chat interface allowing for meaningful responses, related events, DM support, ruleset information and balanced encounters.

<img width="1551" height="901" alt="image" src="https://github.com/user-attachments/assets/18f13e75-6ebe-4435-ad77-4c176b0358b2" />

<img width="1553" height="899" alt="image" src="https://github.com/user-attachments/assets/f6c8d0ad-c25e-4102-90b6-37c63ba5adb6" />

<img width="1553" height="903" alt="image" src="https://github.com/user-attachments/assets/254a655b-1995-47fe-a0a6-44a65e99a580" />


---
# Development Backend Server

### Install uv Package Manager
[UV Installation](https://docs.astral.sh/uv/getting-started/installation/)


### Sync Environment Dependencies
- `cd server`
- `uv sync`

### Run main
- `macOS/Linux: export FLASK_APP=main.py.`
- `Windows (Command Prompt): set FLASK_APP=main.py.`
- `Windows (PowerShell): $env:FLASK_APP="main.py"`
- `flask run`

(Optional For Pip installations)
- `uv pip compile pyproject.toml -o requirements.txt`


## Database (Working on DB Migration Tool Implementation)

### Install PostgreSQL
[PostgreSQL Installation](https://www.postgresql.org/download/)

### Create Local DB
- `CREATE USER campaign_forge_app WITH PASSWORD 'local_password';`
- `CREATE DATABASE campaign_forge_dev OWNER campaign_forge_app;`

### Environment Variables
- `DATABASE_URL=postgresql+psycopg2://campaign_forge_app:local_password@localhost:5432/campaign_forge_dev`

## RAG-Notebook
- Here we are parsing and chunking Rulebook data for clean RAG Retrieval. These methods will be taken further to extract, parse and chunk additional data for the RAG Agent. First POC is clean and efficient rulebook assistant with LLM to guide DM through user interactions with rulebook enhanced decision making
[RAG Colab - Development](https://colab.research.google.com/drive/1R2epbnKPp1cctCzhaBizf6IlZiHq6oTc?usp=sharing)


- END GOAL:
Chat input: Prompt = 
  [Relevant rules from RAG]
  [Relevant campaign facts from RAG]
  [Live session state]
  [User question]

- Returning a relavant output given each of the variables and user questions
