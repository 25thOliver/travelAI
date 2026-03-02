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
    <div className="flex items-center gap-2 text-xs">
      <div className="flex items-center gap-2 text-muted-foreground bg-secondary/50 px-2.5 py-1.5 rounded-full">
        <StatusDot ok={status.status === "ok"} />
        <Activity className="w-3 h-3 text-success" />
        <span className="font-medium tracking-wide">System Online</span>
      </div>
    </div>
  );
}
