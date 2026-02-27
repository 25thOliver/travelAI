import type { AgentResponse, MonitoringStatus, RateLimitError } from "@/types/api";

const getBaseUrl = (): string => {
  const base = import.meta.env.VITE_API_BASE_URL;
  return base !== undefined && base !== null ? String(base) : "http://localhost";
};

const getApiKey = (): string =>
  localStorage.getItem("travel_ai_api_key") || import.meta.env.VITE_API_KEY || "";

export class ApiError extends Error {
  status: number;
  rateLimitInfo?: RateLimitError;

  constructor(status: number, message: string, rateLimitInfo?: RateLimitError) {
    super(message);
    this.status = status;
    this.rateLimitInfo = rateLimitInfo;
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (res.ok) return res.json();

  if (res.status === 401) {
    throw new ApiError(401, "Missing or invalid API key. Check your settings.");
  }

  if (res.status === 429) {
    const body = await res.json().catch(() => ({ detail: "" }));
    let rateLimitInfo: RateLimitError | undefined;
    try {
      rateLimitInfo = typeof body.detail === "string" ? JSON.parse(body.detail) : body.detail;
    } catch {}
    const ttl = rateLimitInfo?.remaining_ttl ?? 60;
    throw new ApiError(429, `Rate limited. Try again in ${ttl}s.`, rateLimitInfo);
  }

  throw new ApiError(res.status, `Server error (${res.status}). Please try again later.`);
}

function authHeaders(): Record<string, string> {
  const key = getApiKey();
  return key ? { "X-API-Key": key, "Content-Type": "application/json" } : { "Content-Type": "application/json" };
}

export async function chat(sessionId: string, message: string): Promise<AgentResponse> {
  const res = await fetch(`${getBaseUrl()}/agent/chat`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ session_id: sessionId, message }),
  });
  return handleResponse<AgentResponse>(res);
}

export async function getMonitoringStatus(): Promise<MonitoringStatus> {
  const res = await fetch(`${getBaseUrl()}/monitoring/status`);
  return handleResponse<MonitoringStatus>(res);
}

export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${getBaseUrl()}/health/`);
  return handleResponse<{ status: string }>(res);
}

export async function rateTest(sessionId: string): Promise<{ ok: boolean }> {
  const res = await fetch(`${getBaseUrl()}/agent/rate-test?session_id=${sessionId}`, {
    headers: authHeaders(),
  });
  return handleResponse<{ ok: boolean }>(res);
}
