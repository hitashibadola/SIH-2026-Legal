import MessageDemo from "@/components/chat/message";
import RuixenPromptBox from "@/components/chat/prompt-box";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-background text-foreground bg-dot-pattern">
      {/* Header */}
      <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-border/40 bg-background/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <h1 className="text-lg font-semibold tracking-tight">Phylax</h1>
      </header>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col items-center overflow-y-auto pb-40 pt-10">
        <div className="w-full max-w-4xl">
          <MessageDemo />
        </div>
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-background via-background/90 to-transparent pt-6 pb-6">
        <div className="w-full max-w-4xl mx-auto">
          <RuixenPromptBox />
        </div>
      </div>
    </main>
  );
}
