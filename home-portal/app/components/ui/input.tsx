import { cn } from '@/app/utils/cn';
import React, { useState, useEffect, useRef } from 'react';

interface InputProps {} // Optional interface for future props

const Input: React.FC<InputProps> = () => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [text, setText] = useState("");

  useEffect(() => {
    const textArea = textAreaRef.current;
    if (textArea) {
        textAreaRef.current.style.height = "auto";
        textAreaRef.current.style.height = textArea.scrollHeight + "px";
    }
  }, [text]);

  return (
    <div className="w-full flex flex-row">
      <textarea
        ref={textAreaRef}
        placeholder="What would you like your smart home to do?"
        className={"w-full m-0 text-center bg-transparent focus:outline-none text-2xl overflow-visible resize-none"}
        onChange={(e) => setText(e.target.value)}
      />
    </div>
  );
};

export default Input;
