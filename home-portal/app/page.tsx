"use client"
import { BackgroundGradientAnimation } from "@/app/components/ui/background-gradient-animation";
import { BackgroundGradient } from "./components/ui/background-gradient";
import { TextGenerateEffect } from "./components/ui/text-generate-effect";
import { useState } from "react";
import { AnimatePresenceWrapper } from "./components/ui/animate-presence-wrapper";
import { motion } from "framer-motion";
import Input from "./components/ui/input";

export default function Home() {
  // checks for the page background and text generation effect to be loaded
  const [loading, setLoading] = useState(true);
  const [showToast, setToast] = useState(false);

  return (
    <BackgroundGradientAnimation className="absolute h-screen w-screen flex items-center justify-center">
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
            <Input setToast={setToast} />
          </BackgroundGradient>
        </AnimatePresenceWrapper>
        <AnimatePresenceWrapper isVisible={showToast}>
          <p className="text-lime-400 mt-3">Got your request! This may take a minute.</p>
        </AnimatePresenceWrapper>
      </motion.div>
    </BackgroundGradientAnimation>
  );
}
