import { Compass } from "lucide-react";

export function ThinkingIndicator() {
  return (
    <div className="flex gap-3 animate-fade-in px-4 py-3 bg-chat-assistant">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
        <Compass className="w-4 h-4 text-primary animate-spin" style={{ animationDuration: "3s" }} />
      </div>
      <div className="flex items-center gap-1.5 pt-2">
        <span className="thinking-dot w-2 h-2 rounded-full bg-primary" />
        <span className="thinking-dot w-2 h-2 rounded-full bg-primary" />
        <span className="thinking-dot w-2 h-2 rounded-full bg-primary" />
      </div>
    </div>
  );
}
