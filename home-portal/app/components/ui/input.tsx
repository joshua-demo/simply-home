import { cn } from '@/app/utils/cn';
import React, { useState, useEffect, useRef } from 'react';
import MicSVG from '../svg/mic';
import SendSVG from '../svg/send';

interface InputProps {} // Optional interface for future props

const Input: React.FC<InputProps> = () => {
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [text, setText] = useState("");
  const bodyMaker = (command : string) => {return {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({"command": command}), // body data type must match "Content-Type" header
  }}
  const url = "http://localhost:5000/command";
  
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
        rows={1}
        placeholder="What would you like your smart home to do?"
        className={"p-4 w-full text-center bg-transparent focus:outline-none text-2xl resize-none max-h-[60vh]"}
        onChange={(e) => setText(e.target.value)}
      />
      {/* TODO: support text to speech */}
      {/* <button className='p-3'>
        <MicSVG />
      </button> */}
      <button className='pr-1' onClick={() => {fetch(url, bodyMaker(text))}}>
        <SendSVG />
      </button>
    </div>
  );
};

export default Input;
