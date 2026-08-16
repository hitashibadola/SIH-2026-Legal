"use client"

import {
  CheckCircle2Icon,
  ChevronRightIcon,
  AlertTriangleIcon,
  XCircleIcon,
  InfoIcon,
  ScaleIcon,
  ShieldAlertIcon,
  HelpCircleIcon
} from "lucide-react"
import { createContext, type HTMLAttributes, useContext, useState } from "react"
import { cn } from "@/lib/utils"

// --- Inline Badge Component ---
const Badge = ({ className, ...props }: HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors", className)} {...props} />
)

export type ClauseStatus = "safe" | "negotiate" | "risk"

interface AnalysisSummaryType {
  safe: number
  negotiate: number
  risk: number
  total: number
  riskLevel: "Low" | "Medium" | "High"
}

interface AnalysisContextType {
  summary?: AnalysisSummaryType
}

const AnalysisContext = createContext<AnalysisContextType>({})

export type AnalysisResultsProps = HTMLAttributes<HTMLDivElement> & {
  summary?: AnalysisSummaryType
}

export const AnalysisResults = ({ summary, className, children, ...props }: AnalysisResultsProps) => (
  <AnalysisContext.Provider value={{ summary }}>
    <div className={cn("flex flex-col gap-4 w-full", className)} {...props}>
      {children}
    </div>
  </AnalysisContext.Provider>
)

export type AnalysisHeaderProps = HTMLAttributes<HTMLDivElement>

export const AnalysisHeader = ({ className, children, ...props }: AnalysisHeaderProps) => (
  <div className={cn("flex flex-col sm:flex-row sm:items-center justify-between border rounded-xl bg-background shadow-sm px-4 py-3.5 gap-3", className)} {...props}>
    {children}
  </div>
)

export type AnalysisSummaryProps = HTMLAttributes<HTMLDivElement>

export const AnalysisSummary = ({ className, children, ...props }: AnalysisSummaryProps) => {
  const { summary } = useContext(AnalysisContext)

  if (!summary) return null

  return (
    <div className={cn("flex items-center flex-wrap gap-2", className)} {...props}>
      {children ?? (
        <>
          {summary.safe > 0 && (
            <Badge className="gap-1.5 bg-emerald-100 border-emerald-300 text-emerald-800 hover:bg-emerald-200 font-medium px-2.5 py-0.5 shadow-none">
              <CheckCircle2Icon className="w-3.5 h-3.5" />
              {summary.safe} Standard
            </Badge>
          )}
          {summary.negotiate > 0 && (
            <Badge className="gap-1.5 bg-amber-100 border-amber-300 text-amber-800 hover:bg-amber-200 font-medium px-2.5 py-0.5 shadow-none">
              <AlertTriangleIcon className="w-3.5 h-3.5" />
              {summary.negotiate} Negotiate
            </Badge>
          )}
          {summary.risk > 0 && (
            <Badge className="gap-1.5 bg-rose-100 border-rose-300 text-rose-800 hover:bg-rose-200 font-medium px-2.5 py-0.5 shadow-none">
              <XCircleIcon className="w-3.5 h-3.5" />
              {summary.risk} High Risk
            </Badge>
          )}
        </>
      )}
    </div>
  )
}

export type AnalysisRiskLevelProps = HTMLAttributes<HTMLDivElement>

export const AnalysisRiskLevel = ({ className, children, ...props }: AnalysisRiskLevelProps) => {
  const { summary } = useContext(AnalysisContext)

  if (!summary) return null

  const getRiskColor = (level: string) => {
    switch (level) {
      case "High": return "text-rose-600"
      case "Medium": return "text-amber-600"
      case "Low": return "text-emerald-600"
      default: return "text-muted-foreground"
    }
  }

  return (
    <div className={cn("flex items-center gap-1.5 text-sm font-medium", getRiskColor(summary.riskLevel), className)} {...props}>
      {children ?? (
        <>
          <ShieldAlertIcon className="w-4 h-4" />
          <span>{summary.riskLevel} Risk Document</span>
        </>
      )}
    </div>
  )
}

export type AnalysisContentProps = HTMLAttributes<HTMLDivElement>

export const AnalysisContent = ({ className, children, ...props }: AnalysisContentProps) => (
  <div className={cn("flex flex-col gap-3", className)} {...props}>
    {children}
  </div>
)

interface ClauseContextType {
  name: string
  status: ClauseStatus
  isOpen: boolean
  setIsOpen: (open: boolean) => void
}

const ClauseContext = createContext<ClauseContextType>({ name: "", status: "safe", isOpen: false, setIsOpen: () => { } })

export type ClauseCardProps = HTMLAttributes<HTMLDivElement> & {
  name: string
  status: ClauseStatus
  defaultOpen?: boolean
}

export const ClauseCard = ({ name, status, defaultOpen = false, className, children, ...props }: ClauseCardProps) => {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  return (
    <ClauseContext.Provider value={{ name, status, isOpen, setIsOpen }}>
      <div className={cn("rounded-xl border bg-background shadow-sm overflow-hidden transition-all", isOpen ? "ring-1 ring-border" : "", className)} {...props}>
        {children}
      </div>
    </ClauseContext.Provider>
  )
}

export type ClauseHeaderProps = HTMLAttributes<HTMLButtonElement>

export const ClauseHeader = ({ className, children, ...props }: ClauseHeaderProps) => {
  const { name, status, isOpen, setIsOpen } = useContext(ClauseContext)

  return (
    <button
      type="button"
      onClick={() => setIsOpen(!isOpen)}
      data-state={isOpen ? "open" : "closed"}
      className={cn(
        "group flex w-full items-center gap-3 px-4 py-3.5 text-left transition-colors hover:bg-muted/30 focus-visible:outline-none focus-visible:bg-muted/50 cursor-pointer",
        className,
      )}
      {...props}
    >
      <ChevronRightIcon className="size-4 shrink-0 text-muted-foreground transition-transform duration-200 group-data-[state=open]:rotate-90" />
      <ClauseStatusIcon status={status} />
      <span className="font-medium text-sm text-foreground">{children ?? name}</span>
    </button>
  )
}

export type ClauseContentProps = HTMLAttributes<HTMLDivElement>

export const ClauseContent = ({ className, children, ...props }: ClauseContentProps) => {
  const { isOpen } = useContext(ClauseContext)

  if (!isOpen) return null

  return (
    <div className={cn("overflow-hidden", className)} {...props}>
      <div className="px-4 pb-4 pt-1 ml-6 space-y-4">
        {children}
      </div>
    </div>
  )
}

const statusStyles: Record<ClauseStatus, string> = {
  safe: "text-emerald-600",
  negotiate: "text-amber-600",
  risk: "text-rose-600",
}

const statusIcons: Record<ClauseStatus, React.ReactNode> = {
  safe: <CheckCircle2Icon className="size-4.5" />,
  negotiate: <AlertTriangleIcon className="size-4.5" />,
  risk: <XCircleIcon className="size-4.5" />,
}

const ClauseStatusIcon = ({ status }: { status: ClauseStatus }) => (
  <span className={cn("shrink-0", statusStyles[status])}>{statusIcons[status]}</span>
)

// Detail sections inside a clause

export const ClauseDetailItem = ({
  icon: Icon,
  title,
  children
}: {
  icon: React.ElementType,
  title: string,
  children: React.ReactNode
}) => (
  <div className="flex gap-2.5">
    <Icon className="w-4 h-4 text-muted-foreground shrink-0 mt-0.5" />
    <div className="space-y-1">
      <h4 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">{title}</h4>
      <div className="text-sm text-foreground leading-relaxed">{children}</div>
    </div>
  </div>
)

export const ClauseOriginalText = ({ children }: { children: React.ReactNode }) => (
  <div className="mb-2 p-3.5 rounded-lg bg-muted/30 border border-muted/50 text-sm text-foreground italic">
    <div className="text-[10px] font-bold tracking-wider uppercase text-muted-foreground mb-1.5 not-italic">Original Document Text</div>
    "{children}"
  </div>
)

export const ClauseMeaning = ({ children }: { children: React.ReactNode }) => (
  <ClauseDetailItem icon={InfoIcon} title="What this means">
    {children}
  </ClauseDetailItem>
)

export const ClauseReasoning = ({ children }: { children: React.ReactNode }) => (
  <ClauseDetailItem icon={HelpCircleIcon} title="Why it's flagged">
    {children}
  </ClauseDetailItem>
)

export const ClauseStatuteBlock = ({ statute, text }: { statute: string, text: string }) => (
  <div className="mt-3 rounded-md bg-muted/30 border p-3.5 space-y-2">
    <div className="flex items-center gap-2 text-xs font-semibold text-primary">
      <ScaleIcon className="w-3.5 h-3.5" />
      <span>{statute}</span>
    </div>
    <div className="font-mono text-xs text-muted-foreground leading-relaxed pl-5 border-l-2 border-primary/20">
      {text}
    </div>
  </div>
)


