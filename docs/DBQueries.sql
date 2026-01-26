-- Table Blueprints and outlines for references, documenting my process developing the database

--Ensure current user is set to development user.
SELECT current_user;
SET ROLE campaign_user_app
CREATE EXTENSION IF NOT EXISTS pgcrypto;

--Create users table
CREATE TABLE IF NOT EXISTS users(
	user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	email VARCHAR (355) UNIQUE NOT NULL,
	pass_hash VARCHAR(50) NOT NULL,
	display_name VARCHAR(50),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Create campaigns table
CREATE TABLE IF NOT EXISTS campaigns(
	campaign_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	title VARCHAR(100) NOT NULL, 
	description TEXT,
	created_by UUID REFERENCES users (user_id),
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alterations
ALTER TABLE campaigns
DROP CONSTRAINT campaigns_created_by_fkey;

ALTER TABLE campaigns 
ADD CONSTRAINT campaigns_created_by_fkey FOREIGN KEY (created_by)
REFERENCES users (user_id)
ON DELETE CASCADE;

-- Add Contraints to tables when needed
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;


--Create Relationship tables
-- CREATE TYPE USER_ROLE AS ENUM('DM', 'Player', 'Viewer')
CREATE TABLE IF NOT EXISTS campaign_members (
	campaign_id UUID NOT NULL,
	user_id UUID NOT NULL, 
	user_role USER_ROLE NOT NULL,
	joined_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT campaign_user_pk 
		PRIMARY KEY (campaign_id, user_id), 
	CONSTRAINT members_campaign_fk 
		FOREIGN KEY (campaign_id)
		REFERENCES campaigns(campaign_id)
		ON DELETE CASCADE,
	CONSTRAINT members_user_fk 
		FOREIGN KEY (user_id) 
		REFERENCES users(user_id)
		ON DELETE CASCADE
)


-- player characters table:
CREATE TABLE IF NOT EXISTS player_characters (
	character_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
	campaign_id UUID NOT NULL, 
	user_id UUID NOT NULL, 
	character_name VARCHAR(50) NOT NULL, 
	character_class JSONB, 
	character_stats JSONB,
	character_level INTEGER CHECK (character_level >= 1),
	character_hitpoints INTEGER CHECK (character_hitpoints > 0), 
	created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT character_campaign_fk
		FOREIGN KEY (campaign_id) 
		REFERENCES campaigns(campaign_id)
		ON DELETE CASCADE, 
	CONSTRAINT character_user_fk
		FOREIGN KEY (user_id)
		REFERENCES users(user_id)
		ON DELETE CASCADE
)



-- Insert Mock data for testing purposes.
INSERT INTO users (email, pass_hash, display_name) 
VALUES (
	'cmesiti@gmail.com', 'mypass123', 'yoda'
)

INSERT INTO campaigns (title, created_by)
SELECT 'Campaign1', user_id
FROM users
WHERE email = 'cmesiti@gmail.com';

