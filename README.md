# CampaignForge
Dungeon Master Assistant to help guide a DM through random encounters, NPC responses, and improving player experience with unique dynamic improvised encounters.

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


## Database

### Install PostgreSQL
[PostgreSQL Installation](https://www.postgresql.org/download/)

### Create Local DB
- `CREATE USER campaign_forge_app WITH PASSWORD 'local_password';`
- `CREATE DATABASE campaign_forge_dev OWNER campaign_forge_app;`

### Environment Variables
- `DATABASE_URL=postgresql+psycopg2://campaign_forge_app:local_password@localhost:5432/campaign_forge_dev`
