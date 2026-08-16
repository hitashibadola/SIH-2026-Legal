"use client";

import { useRef, useState } from "react";
import { cn } from "@/lib/utils";
import { useAutoResizeTextarea } from "@/hooks/use-auto-resize-textarea";
import { CornerDownLeft, FileText, X, Paperclip } from "lucide-react";

const DOCUMENT_TYPES = ["Auto-detect", "Rent Agreement", "Offer Letter", "T&C Link"];

export default function RuixenPromptBox() {
  const [input, setInput] = useState("");
  const [fileName, setFileName] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState("Auto-detect");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { textareaRef } = useAutoResizeTextarea(input, {
    minHeight: 24,
    maxHeight: 200,
  });

  const handleSend = () => {
    console.log("Submitting:", { input, fileName, docType: selectedType });
    setInput("");
    setFileName(null);
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileName(file.name);
    }
  };

  return (
    <div className="w-full px-4 py-6">
      <div className="w-full mx-auto">
        <div className="rounded-2xl border border-border bg-background shadow-sm p-3 focus-within:ring-1 focus-within:ring-border transition-all">

          {fileName && (
            <div className="flex items-center gap-2 bg-muted/50 border border-border/50 px-3 py-1.5 rounded-lg w-fit text-sm shadow-sm mb-3 animate-in fade-in slide-in-from-bottom-2">
              <FileText className="w-4 h-4 text-primary" />
              <span className="font-medium truncate max-w-[200px]">{fileName}</span>
              <button
                onClick={() => setFileName(null)}
                className="hover:bg-muted p-0.5 rounded-full transition-colors"
              >
                <X className="w-3.5 h-3.5 text-muted-foreground" />
              </button>
            </div>
          )}

          <textarea
            ref={textareaRef}
            placeholder={fileName ? "Add an optional message..." : "What would you like to know?"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (input.trim() || fileName) handleSend();
              }
            }}
            className={cn(
              "w-full resize-none bg-transparent border-none text-foreground text-sm",
              "focus:outline-none focus:ring-0 placeholder:text-muted-foreground",
              "min-h-[24px] max-h-[200px] p-0"
            )}
          />

          <div className="flex items-center justify-between mt-2 pt-1">
            <div className="flex items-center gap-3">
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept=".pdf"
                className="hidden"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-muted-foreground hover:text-foreground bg-muted/40 hover:bg-muted rounded-lg transition-colors border border-border/50"
              >
                <Paperclip className="w-3.5 h-3.5" />
                <span>Attach Document</span>
              </button>

              <div className="hidden sm:flex items-center gap-1 bg-muted/30 p-1 rounded-lg border border-border/50">
                {DOCUMENT_TYPES.map((type) => (
                  <button
                    key={type}
                    type="button"
                    onClick={() => setSelectedType(type)}
                    className={cn(
                      "px-2.5 py-1 text-[11px] font-medium rounded-md transition-all",
                      selectedType === type
                        ? "bg-background text-foreground shadow-sm border border-border/50"
                        : "text-muted-foreground hover:text-foreground hover:bg-muted/50 border border-transparent"
                    )}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSend}
              className={cn(
                "flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200 shrink-0",
                (input.trim() || fileName)
                  ? "bg-primary text-primary-foreground hover:bg-primary/90"
                  : "bg-primary text-primary-foreground"
              )}
              disabled={!input.trim() && !fileName}
              type="button"
            >
              <CornerDownLeft className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
