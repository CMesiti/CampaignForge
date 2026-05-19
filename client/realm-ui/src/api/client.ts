import type {
  LoginPayload,
  RegisterPayload,
  AuthResponse,
  Campaign,
  CreateCampaignPayload,
  PlayerCharacter,
  CreateCharacterPayload,
  AgentQueryPayload,
} from "../types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

function authHeaders(): HeadersInit {
  const token = getToken();
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function handleResponse<T>(res: Response): Promise<T> {
  const json = await res.json();
  if (!res.ok) throw new Error(json.ERROR ?? "Request failed");
  return json as T;
}

// ─── Auth ────────────────────────────────────────────────────────────────────

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<AuthResponse>(res);
}

// ─── Users ───────────────────────────────────────────────────────────────────

export async function registerUser(payload: RegisterPayload): Promise<{ user_data: unknown }> {
  const res = await fetch(`${BASE_URL}/v1/users/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

// ─── Campaigns ───────────────────────────────────────────────────────────────

export async function getCampaigns(): Promise<{ campaign_data: Campaign[] }> {
  const res = await fetch(`${BASE_URL}/v1/campaigns/`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function createCampaign(payload: CreateCampaignPayload): Promise<{ campaign_data: Campaign }> {
  const res = await fetch(`${BASE_URL}/v1/campaigns/create`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function joinCampaign(campaignId: string): Promise<{ campaign_data: string }> {
  const res = await fetch(`${BASE_URL}/v1/campaigns/enroll/${campaignId}`, {
    method: "POST",
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function updateCampaign(
  campaignId: string,
  payload: Partial<CreateCampaignPayload>
): Promise<{ campaign_data: Campaign }> {
  const res = await fetch(`${BASE_URL}/v1/campaigns/${campaignId}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteCampaign(campaignId: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/v1/campaigns/${campaignId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) {
    const json = await res.json();
    throw new Error(json.ERROR ?? "Delete failed");
  }
}

// ─── Player Characters ───────────────────────────────────────────────────────

export async function getPlayerCharacters(campaignId: string): Promise<{ player_data: PlayerCharacter[] }> {
  const res = await fetch(`${BASE_URL}/v1/player-characters/${campaignId}`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function createPlayerCharacter(
  campaignId: string,
  payload: CreateCharacterPayload
): Promise<{ player_data: PlayerCharacter }> {
  const res = await fetch(`${BASE_URL}/v1/player-characters/${campaignId}`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function updatePlayerCharacter(
  characterId: string,
  payload: Partial<CreateCharacterPayload>
): Promise<{ player_data: PlayerCharacter }> {
  const res = await fetch(`${BASE_URL}/v1/player-characters/${characterId}`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deletePlayerCharacter(characterId: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/v1/player-characters/${characterId}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (!res.ok) {
    const json = await res.json();
    throw new Error(json.ERROR ?? "Delete failed");
  }
}

// ─── Agent (streaming) ───────────────────────────────────────────────────────

/**
 * Streams the RAG agent response token-by-token.
 * Pass an `onChunk` callback to receive each text fragment.
 * POST /agent/query/:campaign_id
 */
export async function queryAgent(
  campaignId: string,
  payload: AgentQueryPayload,
  onChunk: (chunk: string) => void
): Promise<void> {
  const res = await fetch(`${BASE_URL}/agent/query/${campaignId}`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(payload),
  });

  if (!res.ok || !res.body) {
    const json = await res.json();
    throw new Error(json.ERROR ?? "Agent request failed");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    onChunk(decoder.decode(value, { stream: true }));
  }
}
