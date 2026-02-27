import { Activity, Database, Server } from "lucide-react";
import type { MonitoringStatus } from "@/types/api";

function formatUptime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m ${s}s`;
}

function StatusDot({ ok }: { ok: boolean }) {
  return (
    <span className={`inline-block w-2 h-2 rounded-full ${ok ? "bg-success" : "bg-destructive"}`} />
  );
}

interface Props {
  status: MonitoringStatus | null;
  error: string | null;
}

export function StatusIndicator({ status, error }: Props) {
  if (error) {
    return (
      <div className="flex items-center gap-2 text-xs text-destructive">
        <span className="w-2 h-2 rounded-full bg-destructive" />
        Offline
      </div>
    );
  }

  if (!status) {
    return (
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse" />
        Connecting...
      </div>
    );
  }

  return (
    <div className="space-y-2 text-xs">
      <div className="flex items-center gap-2 text-muted-foreground">
        <StatusDot ok={status.status === "ok"} />
        <Activity className="w-3 h-3" />
        <span>Up {formatUptime(status.uptime_seconds)}</span>
      </div>
      <div className="flex gap-3">
        <span className="flex items-center gap-1.5 text-muted-foreground">
          <StatusDot ok={status.dependencies.database === "ok"} />
          <Database className="w-3 h-3" />
          DB
        </span>
        <span className="flex items-center gap-1.5 text-muted-foreground">
          <StatusDot ok={status.dependencies.redis === "ok"} />
          <Server className="w-3 h-3" />
          Redis
        </span>
      </div>
    </div>
  );
}
