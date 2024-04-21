"use client";
import { BackgroundGradientAnimation } from "@/app/components/ui/background-gradient-animation";
import { BackgroundGradient } from "./components/ui/background-gradient";
import { TextGenerateEffect } from "./components/ui/text-generate-effect";
import { useState } from "react";
import { AnimatePresenceWrapper } from "./components/ui/animate-presence-wrapper";
import { motion } from "framer-motion";
import Input from "./components/ui/input";
import { MultiStepLoader } from "./components/ui/multi-step-loader";
import { IconSquareRoundedX } from "@tabler/icons-react";

export default function Home() {
  // checks for the page background and text generation effect to be loaded
  const [loading, setLoading] = useState(true);
  const [showToast, setToast] = useState(false);
  const [multiStepLoading, setMultiStepLoading] = useState(false);
  const loadingStates = [
    { text: "Identifying Tasks" },
    { text: "Building Tool" },
    { text: "Evaluating Tool" },
    { text: "Running Command" },
  ];

  return (
    <BackgroundGradientAnimation className="absolute h-screen w-screen flex items-center justify-center">
      <MultiStepLoader loadingStates={loadingStates} loading={multiStepLoading} setLoading={setMultiStepLoading} duration={1000} setToast={setToast} />
      <motion.div className="flex flex-col m-0 p-10 rounded-3xl bg-zinc-900 items-center !z-[1000]">
        <TextGenerateEffect
          words="Hi, how can I help you?"
          className="text-center font-bold text-transparent bg-clip-text drop-shadow-2xl bg-gradient-to-b from-white to-white/10"
          setLoading={setLoading}
        />
        <AnimatePresenceWrapper isVisible={!loading} className="mt-10">
          <BackgroundGradient
            className="rounded-[22px] bg-white dark:bg-zinc-900 !p-1"
            containerClassName="w-full md:w-[600px]"
          >
            <Input setToast={setToast} setMultiStepLoading={setMultiStepLoading}/>
          </BackgroundGradient>
        </AnimatePresenceWrapper>
        <AnimatePresenceWrapper isVisible={showToast}>
          <p className="text-red-500 mt-3">
            Error sending command. Please try again in a few seconds.
            Darn api rate limits.
          </p>
        </AnimatePresenceWrapper>
      </motion.div>
      {multiStepLoading && (
        <button
          className="fixed top-4 right-4 text-black dark:text-white z-[1002]"
          onClick={() => setMultiStepLoading(false)}
        >
          <IconSquareRoundedX className="h-10 w-10" />
        </button>
      )}
    </BackgroundGradientAnimation>
  );
}
