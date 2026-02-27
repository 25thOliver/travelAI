import { ExternalLink, AlertCircle, Compass, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "@/types/api";

interface Props {
  message: ChatMessageType;
}

export function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  if (message.error) {
    return (
      <div className="flex gap-3 animate-fade-in px-4 py-3">
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-destructive/20 flex items-center justify-center">
          <AlertCircle className="w-4 h-4 text-destructive" />
        </div>
        <div className="flex-1 rounded-lg bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
          {message.error}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex gap-3 animate-fade-in px-4 py-3 ${isUser ? "" : "bg-chat-assistant"}`}>
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-secondary" : "bg-primary/20"
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-secondary-foreground" />
        ) : (
          <Compass className="w-4 h-4 text-primary" />
        )}
      </div>
      <div className="flex-1 min-w-0 space-y-2">
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-2 pt-1">
            {message.sources.map((src, i) => (
              <a
                key={i}
                href={src}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-primary hover:text-primary/80 bg-primary/10 rounded-md px-2 py-1 transition-colors"
              >
                <ExternalLink className="w-3 h-3" />
                Source {i + 1}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
