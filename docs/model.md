# Tables: (View Raw File)

## Users Table:
users
id              UUID (PK)
email           TEXT UNIQUE NOT NULL
password_hash   TEXT NOT NULL
display_name    TEXT
created_at      TIMESTAMP

--------

## Campaigns Table:
campaigns:
id              UUID (PK)
name            TEXT NOT NULL
description     TEXT
created_by      UUID (FK → users.id)
created_at      TIMESTAMP

---------

## Campaign Members Table:
campaign_members
id              UUID (PK)
campaign_id     UUID (FK → campaigns.id)
user_id         UUID (FK → users.id)
role            TEXT CHECK (role IN ('DM', 'PLAYER'))
joined_at       TIMESTAMP

---------

## Player Characters Table:
player_characters
id              UUID (PK)
user_id         UUID (FK → users.id)
campaign_id     UUID (FK → campaigns.id)

name            TEXT NOT NULL
class           TEXT
level           INTEGER
race            TEXT

stats           JSONB
hit_points      INTEGER

created_at      TIMESTAMP

---------

## Relationship Summary:
User
 ├── CampaignMember ── Campaign
 └── PlayerCharacter ── Campaign
