// ─── Auth ────────────────────────────────────────────────────────────────────
// POST /auth/login
export interface LoginPayload {
  email: string;
  password: string;
}

// POST /v1/users/
export interface RegisterPayload {
  email: string;
  password: string;
  username: string;
}

export interface AuthResponse {
  access_token: string;
}

// ─── User ────────────────────────────────────────────────────────────────────
export interface User {
  user_id: string;
  username: string;
  email: string;
}

// ─── Campaign ────────────────────────────────────────────────────────────────
// GET /v1/campaigns/ → { campaign_data: Campaign[] }
// POST /v1/campaigns/create → { campaign_data: Campaign }
// POST /v1/campaigns/enroll/:campaign_id
// PUT /v1/campaigns/:campaign_id
// DELETE /v1/campaigns/:campaign_id
export interface Campaign {
  campaign_id: string;
  title: string;
  description: string;
  status: "active" | "recruiting" | "paused";
  dm_username: string;
  player_count: number;
  max_players: number;
  session_count: number;
}

export interface CreateCampaignPayload {
  title: string;
  description: string;
}

// ─── Player Character ────────────────────────────────────────────────────────
// GET  /v1/player-characters/:campaign_id → { player_data: PlayerCharacter[] }
// POST /v1/player-characters/:campaign_id → { player_data: PlayerCharacter }
// PUT  /v1/player-characters/:character_id
// DELETE /v1/player-characters/:character_id
export interface PlayerCharacter {
  character_id: string;
  campaign_id: string;
  user_id: string;
  player_name: string;
  character_name: string;
  race: string;
  char_class: string;
  background: string;
  alignment: string;
  level: number;
  ability_scores: AbilityScores;
}

export interface AbilityScores {
  strength: number;
  dexterity: number;
  constitution: number;
  intelligence: number;
  wisdom: number;
  charisma: number;
}

export type CreateCharacterPayload = Omit<PlayerCharacter, "character_id" | "campaign_id" | "user_id">;

// ─── Agent ───────────────────────────────────────────────────────────────────
// POST /agent/query/:campaign_id → streaming Response
export interface AgentQueryPayload {
  user_query: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}
