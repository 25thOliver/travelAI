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
    <div className="flex flex-col h-screen bg-background relative overflow-hidden">
      {/* Dynamic Background Blurs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-accent/10 blur-[120px] pointer-events-none" />

      {/* Floating Glassmorphic Header */}
      <header className="absolute top-4 left-1/2 -translate-x-1/2 w-full max-w-5xl px-4 z-50">
        <div className="flex items-center justify-between px-5 py-3 rounded-2xl bg-card/60 backdrop-blur-xl border border-white/5 shadow-2xl">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/20 shadow-glow">
              <Compass className="w-5 h-5 text-primary" />
            </div>
            <span className="font-bold tracking-tight text-foreground/90">Travel AI</span>
          </div>

          <div className="flex items-center gap-3">
            <StatusIndicator status={status} error={error} />
            <div className="w-px h-6 bg-border/50 mx-1" />
            <button
              onClick={handleNewConversation}
              className="p-2 rounded-xl text-muted-foreground hover:text-primary hover:bg-primary/10 transition-all duration-300"
              title="New conversation"
            >
              <Plus className="w-4 h-4" />
            </button>
            <SettingsDialog />
          </div>
        </div>
      </header>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin pt-28 pb-32 z-10 relative">
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

      {/* Floating Input */}
      <div className="absolute bottom-6 left-0 w-full px-4 z-50 pointer-events-none">
        <div className="max-w-3xl mx-auto pointer-events-auto">
          <ChatInput onSend={sendMessage} disabled={isLoading} />
        </div>
      </div>
    </div>
  );
};

export default Index;
