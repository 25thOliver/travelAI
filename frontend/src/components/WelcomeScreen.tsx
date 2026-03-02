import { Compass, MapPin, Plane, Palmtree } from "lucide-react";

const suggestions = [
  { icon: MapPin, text: "Tell me about Hell's Gate in Kenya" },
  {
    icon: Plane,
    text: "Plan a 7-day trip across Kenya (Nairobi → Maasai Mara → Diani Beach)",
  },
  { icon: Palmtree, text: "Best beaches in Kenya (Diani, Watamu, Lamu)" },
];

interface Props {
  onSuggestion: (text: string) => void;
}

export function WelcomeScreen({ onSuggestion }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-4 animate-fade-in relative z-10">
      <style>{`.toaster, .sonner { display: none !important; }`}</style>

      {/* Decorative Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-primary/20 rounded-full blur-[100px] pointer-events-none" />

      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-6 border border-primary/20 shadow-glow relative">
        <Compass className="w-8 h-8 text-primary" />
      </div>

      <h1 className="text-4xl font-extrabold tracking-tight mb-3 bg-clip-text text-transparent bg-gradient-hero">
        Travel AI
      </h1>

      <p className="text-muted-foreground text-base mb-10 text-center max-w-sm leading-relaxed">
        Your intelligent travel companion. Ask about destinations, plan trips,
        and discover hidden gems matching your vibe.
      </p>

      <div className="grid gap-3 w-full max-w-md">
        {suggestions.map(({ icon: Icon, text }) => (
          <button
            key={text}
            onClick={() => onSuggestion(text)}
            className="flex items-center gap-4 rounded-xl border border-white/5 bg-card/40 backdrop-blur-sm hover:bg-secondary/80 hover:border-primary/30 px-5 py-4 text-left transition-all duration-300 group shadow-sm hover:shadow-md hover:-translate-y-0.5"
          >
            <div className="p-2 rounded-lg bg-secondary group-hover:bg-primary/10 transition-colors">
              <Icon className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
            </div>
            <span className="text-sm font-medium text-secondary-foreground/90 group-hover:text-foreground transition-colors">{text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
