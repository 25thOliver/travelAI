import { useRef, useEffect } from "react";
import { Plus, Compass } from "lucide-react";
import { useSession } from "@/hooks/use-session";
import { useChat } from "@/hooks/use-chat";
import { useMonitoring } from "@/hooks/use-monitoring";
import { ChatMessage } from "@/components/ChatMessage";
import { ChatInput } from "@/components/ChatInput";
import { ThinkingIndicator } from "@/components/ThinkingIndicator";
import { StatusIndicator } from "@/components/StatusIndicator";
import { SettingsDialog } from "@/components/SettingsDialog";
import { WelcomeScreen } from "@/components/WelcomeScreen";

const Index = () => {
  const { sessionId, newSession } = useSession();
  const { messages, isLoading, sendMessage, clearMessages } = useChat(sessionId);
  const { status, error } = useMonitoring();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isLoading]);

  const handleNewConversation = () => {
    newSession();
    clearMessages();
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <header className="flex items-center justify-between border-b border-border px-4 py-3 bg-card">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/15 flex items-center justify-center">
            <Compass className="w-4 h-4 text-primary" />
          </div>
          <span className="font-semibold text-sm">Travel AI</span>
        </div>

        <div className="flex items-center gap-2">
          <StatusIndicator status={status} error={error} />
          <div className="w-px h-5 bg-border mx-1" />
          <button
            onClick={handleNewConversation}
            className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
            title="New conversation"
          >
            <Plus className="w-4 h-4" />
          </button>
          <SettingsDialog />
        </div>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin">
        {messages.length === 0 && !isLoading ? (
          <WelcomeScreen onSuggestion={sendMessage} />
        ) : (
          <div className="max-w-3xl mx-auto py-4">
            {messages.map((msg) => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {isLoading && <ThinkingIndicator />}
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
};

export default Index;
