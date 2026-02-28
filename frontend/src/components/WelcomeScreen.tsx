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
    <div className="flex-1 flex flex-col items-center justify-center px-4 animate-fade-in">
      <style>{`.toaster, .sonner { display: none !important; }`}</style>
      <div className="w-14 h-14 rounded-2xl bg-primary/15 flex items-center justify-center mb-6">
        <Compass className="w-7 h-7 text-primary" />
      </div>
      <h1 className="text-2xl font-bold mb-2">Travel AI</h1>
      <p className="text-muted-foreground text-sm mb-8 text-center max-w-sm">
        Your intelligent travel companion. Ask about destinations, plan trips,
        and discover hidden gems.
      </p>
      <div className="grid gap-2 w-full max-w-sm">
        {suggestions.map(({ icon: Icon, text }) => (
          <button
            key={text}
            onClick={() => onSuggestion(text)}
            className="flex items-center gap-3 rounded-lg border border-border bg-card hover:bg-secondary px-4 py-3 text-left text-sm transition-colors group"
          >
            <Icon className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
            <span className="text-secondary-foreground">{text}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
