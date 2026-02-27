export interface AgentRequest {
  session_id: string;
  message: string;
}

export interface AgentResponse {
  answer: string;
  sources: string[];
}

export interface MonitoringStatus {
  status: string;
  uptime_seconds: number;
  dependencies: {
    database: string;
    redis: string;
  };
}

export interface HealthResponse {
  status: string;
}

export interface RateLimitError {
  error: string;
  message: string;
  window_seconds: number;
  max_requests: number;
  remaining_ttl: number;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  error?: string;
  timestamp: Date;
}
