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
- `uv run main.py`

(Optional For Pip installations)
`uv pip compile pyproject.toml -o requirements.txt`


# Database

### Install PostgreSQL


### Create Local DB
`CREATE USER campaign_forge_app WITH PASSWORD 'local_password';`
`CREATE DATABASE campaign_forge_dev OWNER campaign_forge_app;`

### Environment Variables
`DATABASE_URL=postgresql://campaign_forge_app:local_password@localhost:5432/campaign_forge_dev`

