"use client"

import { ChevronLeftIcon, ChevronRightIcon, PaperclipIcon, XIcon } from "lucide-react"
import type { ComponentProps, HTMLAttributes, ReactElement } from "react"
import { createContext, memo, useContext, useEffect, useState } from "react"
/* 
import { Button } from "@/components/ui/button"
import { ButtonGroup, ButtonGroupText } from "@/components/ui/button-group"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip" 
*/
import { cn } from "@/lib/utils"
import {
  AnalysisResults,
  AnalysisHeader,
  AnalysisSummary,
  AnalysisRiskLevel,
  AnalysisContent,
  ClauseCard,
  ClauseHeader,
  ClauseContent,
  ClauseOriginalText,
  ClauseMeaning,
  ClauseReasoning,
  ClauseStatuteBlock,
} from "../analysis/analysis-results"

export type MessageProps = HTMLAttributes<HTMLDivElement> & {
  from: "user" | "assistant"
}

export const Message = ({ className, from, ...props }: MessageProps) => (
  <div
    className={cn(
      "group flex w-full max-w-[95%] flex-col gap-2",
      from === "user" ? "is-user ml-auto justify-end" : "is-assistant",
      className,
    )}
    {...props}
  />
)

export type MessageContentProps = HTMLAttributes<HTMLDivElement>

export const MessageContent = ({ children, className, ...props }: MessageContentProps) => (
  <div
    className={cn(
      "is-user:dark flex w-fit max-w-full min-w-0 flex-col gap-2 overflow-hidden text-sm",
      "group-[.is-user]:ml-auto group-[.is-user]:rounded-lg group-[.is-user]:bg-secondary group-[.is-user]:px-4 group-[.is-user]:py-3 group-[.is-user]:text-foreground",
      "group-[.is-assistant]:text-foreground",
      className,
    )}
    {...props}
  >
    {children}
  </div>
)

/*
 * TODO [TECH DEBT]: We've commented out the following components (MessageBranch, MessageAction, MessageAttachment, etc.).
 * for ChatGPT-style message regeneration, pagination, and multi-modal attachments.
 * Keeping them around for now in case we need branch navigation in a future iteration, but they are currently unused.
 */
/*
export type MessageActionsProps = ComponentProps<"div">

export const MessageActions = ({ className, children, ...props }: MessageActionsProps) => (
  <div className={cn("flex items-center gap-1", className)} {...props}>
    {children}
  </div>
)

export type MessageActionProps = ComponentProps<typeof Button> & {
  tooltip?: string
  label?: string
}

export const MessageAction = ({
  tooltip,
  children,
  label,
  variant = "ghost",
  size = "icon",
  ...props
}: MessageActionProps) => {
  const button = (
    <Button size={size} type="button" variant={variant} {...props}>
      {children}
      <span className="sr-only">{label || tooltip}</span>
    </Button>
  )

  if (tooltip) {
    return (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>{button}</TooltipTrigger>
          <TooltipContent>
            <p>{tooltip}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    )
  }

  return button
}

interface MessageBranchContextType {
  currentBranch: number
  totalBranches: number
  goToPrevious: () => void
  goToNext: () => void
  branches: ReactElement[]
  setBranches: (branches: ReactElement[]) => void
}

const MessageBranchContext = createContext<MessageBranchContextType | null>(null)

const useMessageBranch = () => {
  const context = useContext(MessageBranchContext)

  if (!context) {
    throw new Error("MessageBranch components must be used within MessageBranch")
  }

  return context
}

export type MessageBranchProps = HTMLAttributes<HTMLDivElement> & {
  defaultBranch?: number
  onBranchChange?: (branchIndex: number) => void
}

export const MessageBranch = ({
  defaultBranch = 0,
  onBranchChange,
  className,
  ...props
}: MessageBranchProps) => {
  const [currentBranch, setCurrentBranch] = useState(defaultBranch)
  const [branches, setBranches] = useState<ReactElement[]>([])

  const handleBranchChange = (newBranch: number) => {
    setCurrentBranch(newBranch)
    onBranchChange?.(newBranch)
  }

  const goToPrevious = () => {
    const newBranch = currentBranch > 0 ? currentBranch - 1 : branches.length - 1
    handleBranchChange(newBranch)
  }

  const goToNext = () => {
    const newBranch = currentBranch < branches.length - 1 ? currentBranch + 1 : 0
    handleBranchChange(newBranch)
  }

  const contextValue: MessageBranchContextType = {
    currentBranch,
    totalBranches: branches.length,
    goToPrevious,
    goToNext,
    branches,
    setBranches,
  }

  return (
    <MessageBranchContext.Provider value={contextValue}>
      <div className={cn("grid w-full gap-2 [&>div]:pb-0", className)} {...props} />
    </MessageBranchContext.Provider>
  )
}

export type MessageBranchContentProps = HTMLAttributes<HTMLDivElement>

export const MessageBranchContent = ({ children, ...props }: MessageBranchContentProps) => {
  const { currentBranch, setBranches, branches } = useMessageBranch()
  const childrenArray = Array.isArray(children) ? children : [children]

  // Use useEffect to update branches when they change
  useEffect(() => {
    if (branches.length !== childrenArray.length) {
      setBranches(childrenArray)
    }
  }, [childrenArray, branches, setBranches])

  return childrenArray.map((branch, index) => (
    <div
      className={cn(
        "grid gap-2 overflow-hidden [&>div]:pb-0",
        index === currentBranch ? "block" : "hidden",
      )}
      key={branch.key}
      {...props}
    >
      {branch}
    </div>
  ))
}

export type MessageBranchSelectorProps = HTMLAttributes<HTMLDivElement> & {
  from: UIMessage["role"]
}

export const MessageBranchSelector = ({
  className,
  from,
  ...props
}: MessageBranchSelectorProps) => {
  const { totalBranches } = useMessageBranch()

  // Don't render if there's only one branch
  if (totalBranches <= 1) {
    return null
  }

  return (
    <ButtonGroup
      className="[&>*:not(:first-child)]:rounded-l-md [&>*:not(:last-child)]:rounded-r-md"
      {...props}
    />
  )
}

export type MessageBranchPreviousProps = ComponentProps<typeof Button>

export const MessageBranchPrevious = ({ children, ...props }: MessageBranchPreviousProps) => {
  const { goToPrevious, totalBranches } = useMessageBranch()

  return (
    <Button
      aria-label="Previous branch"
      disabled={totalBranches <= 1}
      onClick={goToPrevious}
      size="icon"
      type="button"
      variant="ghost"
      {...props}
    >
      {children ?? <ChevronLeftIcon size={14} />}
    </Button>
  )
}

export type MessageBranchNextProps = ComponentProps<typeof Button>

export const MessageBranchNext = ({ children, className, ...props }: MessageBranchNextProps) => {
  const { goToNext, totalBranches } = useMessageBranch()

  return (
    <Button
      aria-label="Next branch"
      disabled={totalBranches <= 1}
      onClick={goToNext}
      size="icon"
      type="button"
      variant="ghost"
      {...props}
    >
      {children ?? <ChevronRightIcon size={14} />}
    </Button>
  )
}

export type MessageBranchPageProps = HTMLAttributes<HTMLSpanElement>

export const MessageBranchPage = ({ className, ...props }: MessageBranchPageProps) => {
  const { currentBranch, totalBranches } = useMessageBranch()

  return (
    <ButtonGroupText
      className={cn("border-none bg-transparent text-muted-foreground shadow-none", className)}
      {...props}
    >
      {currentBranch + 1} of {totalBranches}
    </ButtonGroupText>
  )
}

export type MessageResponseProps = ComponentProps<typeof Streamdown>

export const MessageResponse = memo(
  ({ className, ...props }: MessageResponseProps) => (
    <Streamdown
      className={cn(
        "size-full [&>*:first-child]:mt-0 [&>*:last-child]:mb-0",
        "[&_code]:bg-muted/80 [&_code]:rounded-md [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.9em]",
        className
      )}
      {...props}
    />
  ),
  (prevProps, nextProps) => prevProps.children === nextProps.children,
)

MessageResponse.displayName = "MessageResponse"

export type MessageAttachmentProps = HTMLAttributes<HTMLDivElement> & {
  data: FileUIPart
  className?: string
  onRemove?: () => void
}

export function MessageAttachment({ data, className, onRemove, ...props }: MessageAttachmentProps) {
  const filename = data.filename || ""
  const mediaType = data.mediaType?.startsWith("image/") && data.url ? "image" : "file"
  const isImage = mediaType === "image"
  const attachmentLabel = filename || (isImage ? "Image" : "Attachment")

  return (
    <div className={cn("group relative size-24 overflow-hidden rounded-lg", className)} {...props}>
      {isImage ? (
        <>
          <img
            alt={filename || "attachment"}
            className="size-full object-cover"
            height={100}
            src={data.url}
            width={100}
          />
          {onRemove && (
            <Button
              aria-label="Remove attachment"
              className="absolute top-2 right-2 size-6 rounded-full bg-background/80 p-0 opacity-0 backdrop-blur-sm transition-opacity hover:bg-background group-hover:opacity-100 [&>svg]:size-3"
              onClick={e => {
                e.stopPropagation()
                onRemove()
              }}
              type="button"
              variant="ghost"
            >
              <XIcon />
              <span className="sr-only">Remove</span>
            </Button>
          )}
        </>
      ) : (
        <>
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="flex size-full shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
                <PaperclipIcon className="size-4" />
              </div>
            </TooltipTrigger>
            <TooltipContent>
              <p>{attachmentLabel}</p>
            </TooltipContent>
          </Tooltip>
          {onRemove && (
            <Button
              aria-label="Remove attachment"
              className="size-6 shrink-0 rounded-full p-0 opacity-0 transition-opacity hover:bg-accent group-hover:opacity-100 [&>svg]:size-3"
              onClick={e => {
                e.stopPropagation()
                onRemove()
              }}
              type="button"
              variant="ghost"
            >
              <XIcon />
              <span className="sr-only">Remove</span>
            </Button>
          )}
        </>
      )}
    </div>
  )
}

export type MessageAttachmentsProps = ComponentProps<"div">

export function MessageAttachments({ children, className, ...props }: MessageAttachmentsProps) {
  if (!children) {
    return null
  }

  return (
    <div className={cn("ml-auto flex w-fit flex-wrap items-start gap-2", className)} {...props}>
      {children}
    </div>
  )
}

export type MessageToolbarProps = ComponentProps<"div">

export const MessageToolbar = ({ className, children, ...props }: MessageToolbarProps) => (
  <div className={cn("mt-4 flex w-full items-center justify-between gap-4", className)} {...props}>
    {children}
  </div>
)
*/

/** Demo component for preview */
export default function MessageDemo() {
  const summary = { safe: 15, negotiate: 2, risk: 1, total: 18, riskLevel: "High" as const }

  return (
    <div className="flex w-full mx-auto flex-col gap-6 px-4 py-6">
      <Message from="user">
        <MessageContent>
          <p>I just uploaded my employment offer letter. Can you check if there are any red flags?</p>
        </MessageContent>
      </Message>
      <Message from="assistant">
        <MessageContent className="w-full max-w-2xl bg-transparent p-0">
          <div className="text-foreground text-sm mb-3">
            I've analyzed the offer letter. I found one **High-Risk** clause and a few missing terms you should be aware of:
          </div>

          <AnalysisResults summary={summary}>
            <AnalysisHeader>
              <AnalysisRiskLevel />
              <AnalysisSummary />
            </AnalysisHeader>

            <AnalysisContent>
              <ClauseCard name="Clause 4.2 — Non-compete for 2 years" status="risk" defaultOpen>
                <ClauseHeader />
                <ClauseContent>
                  <ClauseOriginalText>
                    4.2 The employee agrees not to engage in competing business for 2 years post-termination, anywhere in the territory of India.
                  </ClauseOriginalText>
                  <ClauseMeaning>
                    The contract states you cannot work in the same industry for 2 years after leaving the company.
                  </ClauseMeaning>
                  <ClauseReasoning>
                    This is a blanket restraint of trade. Under Indian law, post-employment non-compete clauses are generally unenforceable unless they involve the sale of business goodwill.
                  </ClauseReasoning>
                  <ClauseStatuteBlock
                    statute="Indian Contract Act 1872, Section 27"
                    text="Every agreement by which any one is restrained from exercising a lawful profession, trade or business of any kind, is to that extent void."
                  />
                </ClauseContent>
              </ClauseCard>

              <ClauseCard name="Missing: Dispute Resolution Clause" status="negotiate">
                <ClauseHeader />
                <ClauseContent>
                  <ClauseOriginalText>
                    No dispute resolution or arbitration clause was found in the provided document.
                  </ClauseOriginalText>
                  <ClauseMeaning>
                    The contract does not specify how legal disputes will be resolved between you and the employer.
                  </ClauseMeaning>
                  <ClauseReasoning>
                    Without a clear arbitration or jurisdiction clause, any legal disagreement could default to lengthy and expensive standard court litigation in an unspecified jurisdiction.
                  </ClauseReasoning>
                  <ClauseStatuteBlock
                    statute="Standard Contractual Practice"
                    text="It is highly recommended to include an arbitration clause under the Arbitration and Conciliation Act, 1996, specifying the seat of arbitration."
                  />
                </ClauseContent>
              </ClauseCard>

              <ClauseCard name="Clause 7 — Standard Termination" status="safe">
                <ClauseHeader />
                <ClauseContent>
                  <ClauseOriginalText>
                    7.1 Either party may terminate this agreement at any time by providing a 30-day prior written notice to the other party.
                  </ClauseOriginalText>
                  <ClauseMeaning>
                    Either party can terminate the contract with a 30-day written notice.
                  </ClauseMeaning>
                  <ClauseReasoning>
                    This is a standard and balanced mutual termination clause commonly found in Indian employment contracts.
                  </ClauseReasoning>
                </ClauseContent>
              </ClauseCard>
            </AnalysisContent>
          </AnalysisResults>

          <div className="text-foreground text-sm mt-4">
            Would you like me to explain how to negotiate the non-compete clause with your employer?
          </div>
        </MessageContent>
      </Message>
    </div>
  )
}
