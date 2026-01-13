CREATE TABLE IF NOT EXISTS users(
	user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	email VARCHAR (355) UNIQUE NOT NULL,
	pass_hash VARCHAR(50) NOT NULL,
	display_name VARCHAR(50),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaigns(
	campaign_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	title VARCHAR(100) NOT NULL, 
	description TEXT,
	created_by UUID REFERENCES users (user_id),
	create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ALTER TABLE users ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;

-- INSERT INTO users (email, pass_hash, display_name) 
-- VALUES (
-- 	'cmesiti@gmail.com', 'mypass123', 'yoda'
-- )

INSERT INTO campaigns (title, created_by)
SELECT 'Campaign1', user_id
FROM users
WHERE email = 'cmesiti@gmail.com';

