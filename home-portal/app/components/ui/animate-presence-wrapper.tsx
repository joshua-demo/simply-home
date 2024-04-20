import { motion, AnimatePresence } from "framer-motion"
import { ReactChildren, ReactNode } from "react"

export const AnimatePresenceWrapper = ({ isVisible, children } : { isVisible : boolean, children : ReactNode }) => (
  <AnimatePresence>
    {isVisible && (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        { children }
      </motion.div>
    )}
  </AnimatePresence>
)