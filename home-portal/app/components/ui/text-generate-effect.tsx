"use client";
import { Dispatch, SetStateAction, useEffect } from "react";
import { motion, stagger, useAnimate, useMotionValue, useMotionValueEvent } from "framer-motion";
import { cn } from "@/app/utils/cn";

export const TextGenerateEffect = ({
  words,
  className,
  setLoading
}: {
  words: string;
  className?: string;
  setLoading: Dispatch<SetStateAction<boolean>>;
}) => {
  const [scope, animate] = useAnimate();
  let wordsArray = words.split(" ");
  useEffect(() => {
    const animation = animate(
      "span",
      {
        opacity: 1,
      },
      {
        duration: 2,
        delay: stagger(0.2),
      }
    );
    animation.then(() => setLoading(false));
  }, [scope.current]);

  const renderWords = () => {
    return (
      <motion.div ref={scope} >
        {wordsArray.map((word, idx) => {
          return (
            <motion.span
              key={word + idx}
              className="text-white opacity-0"
            >
              {word}{" "}
            </motion.span>
          );
        })}
      </motion.div>
    );
  };

  return (
    <div className={cn("font-bold", className)}>
      <div className="mt-4">
        <div className="leading-snug tracking-wide text-3xl md:text-7xl text-transparent bg-clip-text drop-shadow-2xl bg-gradient-to-b from-white to-white/10">
          {renderWords()}
        </div>
      </div>
    </div>
  );
};
