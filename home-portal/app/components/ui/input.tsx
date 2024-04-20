import { cn } from '@/app/utils/cn';
import React, { useState, useEffect, useRef } from 'react';
import MicSVG from '../svg/mic';
import SendSVG from '../svg/send';

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
        className={"w-full m-0 text-center bg-transparent focus:outline-none text-2xl overflow-visible resize-none max-h-[60vh]"}
        onChange={(e) => setText(e.target.value)}
      />
      {/* Mic button */}
      <button className='p-3'>
        <MicSVG />
      </button>
        {/* Send button */}
      <button className='pr-1'>
        <SendSVG />
      </button>
    </div>
  );
};

export default Input;
