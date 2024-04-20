"use client"
import { BackgroundGradientAnimation } from "@/app/components/ui/background-gradient-animation";
import { BackgroundGradient } from "./components/ui/background-gradient";
import Image from "next/image";
import { TextGenerateEffect } from "./components/ui/text-generate-effect";
import { useState } from "react";

export default function Home() {
  // checks for the page background and text generation effect to be loaded
  const [loading, setLoading] = useState(true);

  return (
    <BackgroundGradientAnimation className="w-full, h-full flex items-center justify-center mx-5 sm:mx-20">
      <div className="flex flex-col m-0 p-10 rounded-3xl bg-zinc-900 items-center">
        <TextGenerateEffect
          words="Hi, how can I help you?"
          className="text-center font-bold text-transparent bg-clip-text drop-shadow-2xl bg-gradient-to-b from-white to-white/10"
        />
        <BackgroundGradient
          className="rounded-[22px] bg-white dark:bg-zinc-900 !p-1"
          containerClassName="w-[50%] min-w-100px mt-10"
        >
          <textarea
            placeholder="What would you like your smart home to do?"
            className="w-full m-0 text-center bg-transparent focus:outline-none text-2xl overflow-visible"
          />
          {/* Add microphone button */}

        </BackgroundGradient>
      </div>
    </BackgroundGradientAnimation>
  );
}
