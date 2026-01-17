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

 
{'Message': '', 'Data': [{'user_id': UUID('f58babf1-d019-4dad-a2a5-9429783268c1'), 'email': 'cmesiti@gmail.com', 'display_name': 'yoda', 'created_at': datetime.datetime(2026, 1, 12, 14, 52, 22, 636905), 'campaigns': [Campaign:
            campaign_id - 4dfdb2d5-2324-4bc4-92fb-85c5b2819ae7
            Title - Campaign1
            Description - None
            Created_By - f58babf1-d019-4dad-a2a5-9429783268c1
]}, {'user_id': UUID('3f270947-4aac-41de-93a7-09530c502f15'), 'email': 'example@example.com', 'display_name': 'tester', 'created_at': datetime.datetime(2026, 1, 14, 19, 39, 42, 670779), 'campaigns': []}]}