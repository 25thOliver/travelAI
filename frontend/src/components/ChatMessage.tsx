import { ExternalLink, AlertCircle, Compass, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "@/types/api";

interface Props {
  message: ChatMessageType;
}

// Simple markdown renderer for common patterns
function renderMarkdown(text: string) {
  // Replace bold text (**text**)
  text = text.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  
  // Replace italic text (*text* but not ** or **)
  text = text.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  
  // Replace headers (# Header)
  text = text.replace(/^### ([^\n]+)/gm, "<h3 className='font-semibold text-sm mt-3 mb-1'>$1</h3>");
  text = text.replace(/^## ([^\n]+)/gm, "<h2 className='font-bold text-base mt-3 mb-2'>$1</h2>");
  text = text.replace(/^# ([^\n]+)/gm, "<h1 className='font-bold text-lg mt-3 mb-2'>$1</h1>");
  
  // Replace bullet lists (* item)
  text = text.replace(/^\* ([^\n]+)/gm, "<li className='ml-4'>$1</li>");
  text = text.replace(/(<li[^>]*>.*?<\/li>)/s, "<ul className='list-disc'>$1</ul>");
  
  // Replace line breaks
  text = text.replace(/\n\n/g, "</p><p>");
  
  return text;
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

  const renderedContent = renderMarkdown(message.content);

  return (
    <div className={`flex gap-3 animate-fade-in px-4 py-3 ${isUser ? "" : "bg-chat-assistant"}`}>
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-secondary-foreground" />
        ) : (
          <Compass className="w-4 h-4 text-primary" />
        )}
      </div>
      <div className="flex-1 min-w-0 space-y-2">
        <div 
          className="text-sm leading-relaxed" 
          dangerouslySetInnerHTML={{ __html: renderedContent }}
        />
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
