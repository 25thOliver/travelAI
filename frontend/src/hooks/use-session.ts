import { useState } from "react";

function generateSessionId(): string {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
}

export function useSession() {
  const [sessionId, setSessionId] = useState<string>(() => {
    const stored = sessionStorage.getItem("travel_ai_session_id");
    if (stored) return stored;
    const id = generateSessionId();
    sessionStorage.setItem("travel_ai_session_id", id);
    return id;
  });

  const newSession = () => {
    const id = generateSessionId();
    sessionStorage.setItem("travel_ai_session_id", id);
    setSessionId(id);
  };

  return { sessionId, newSession };
}
