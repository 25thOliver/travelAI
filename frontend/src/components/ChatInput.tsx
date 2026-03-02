import { useState, useRef, useEffect } from "react";
import { Send } from "lucide-react";

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export function ChatInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!disabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [disabled]);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = () => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = Math.min(el.scrollHeight, 160) + "px";
    }
  };

  return (
    <div className="w-full pb-4">
      <div className="flex gap-3 items-end bg-card/80 backdrop-blur-xl border border-white/10 p-3 rounded-3xl shadow-2xl transition-all duration-300 focus-within:border-primary/50 focus-within:shadow-glow">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder="Ask about a destination..."
          rows={1}
          disabled={disabled}
          className="flex-1 resize-none bg-transparent border-0 px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-0 min-h-[44px] max-h-[160px] scrollbar-thin transition-opacity disabled:opacity-50"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          className="flex-shrink-0 h-11 w-11 rounded-full bg-primary text-primary-foreground flex items-center justify-center hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-300 shadow-md hover:shadow-lg hover:scale-105 active:scale-95"
        >
          <Send className="w-4 h-4 ml-0.5" />
        </button>
      </div>
    </div>
  );
}
