import { useState, useEffect, useCallback } from "react";
import type { MonitoringStatus } from "@/types/api";
import { getMonitoringStatus } from "@/services/api";

export function useMonitoring(intervalMs = 30000) {
  const [status, setStatus] = useState<MonitoringStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    try {
      const data = await getMonitoringStatus();
      setStatus(data);
      setError(null);
    } catch {
      setError("Unable to reach backend");
    }
  }, []);

  useEffect(() => {
    fetch();
    const id = setInterval(fetch, intervalMs);
    return () => clearInterval(id);
  }, [fetch, intervalMs]);

  return { status, error, refetch: fetch };
}
