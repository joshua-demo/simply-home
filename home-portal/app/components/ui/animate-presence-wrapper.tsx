import { cn } from "@/app/utils/cn"
import { motion, AnimatePresence } from "framer-motion"
import { ReactChildren, ReactNode } from "react"

export const AnimatePresenceWrapper = ({ isVisible, children, className} : { isVisible : boolean, children : ReactNode, className? : string }) => (
  <AnimatePresence>
    {isVisible && (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className={className ?? ""}
      >
        { children }
      </motion.div>
    )}
  </AnimatePresence>
)