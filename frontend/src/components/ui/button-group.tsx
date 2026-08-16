import * as React from "react"
import { cn } from "@/lib/utils"

const ButtonGroup = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex items-center space-x-1 rounded-md bg-secondary/20 p-1 backdrop-blur-md border border-white/5", className)}
      {...props}
    />
  )
)
ButtonGroup.displayName = "ButtonGroup"

const ButtonGroupText = React.forwardRef<HTMLSpanElement, React.HTMLAttributes<HTMLSpanElement>>(
  ({ className, ...props }, ref) => (
    <span
      ref={ref}
      className={cn("px-2 text-xs font-medium text-muted-foreground", className)}
      {...props}
    />
  )
)
ButtonGroupText.displayName = "ButtonGroupText"

export { ButtonGroup, ButtonGroupText }
