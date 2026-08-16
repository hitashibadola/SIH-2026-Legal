import { useLayoutEffect, useRef } from "react"

interface UseAutoResizeTextareaProps {
  minHeight?: number
  maxHeight?: number
}

export function useAutoResizeTextarea(
  value: string,
  { minHeight = 24, maxHeight = 200 }: UseAutoResizeTextareaProps = {}
) {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useLayoutEffect(() => {
    const textarea = textareaRef.current
    if (!textarea) return

    // Reset height to minHeight to measure true scrollHeight
    textarea.style.height = `${minHeight}px`
    const scrollHeight = textarea.scrollHeight
    
    if (scrollHeight > maxHeight) {
      textarea.style.height = `${maxHeight}px`
      textarea.style.overflowY = "auto"
    } else {
      textarea.style.height = `${Math.max(scrollHeight, minHeight)}px`
      textarea.style.overflowY = "hidden"
    }
  }, [value, minHeight, maxHeight])

  return { textareaRef }
}
