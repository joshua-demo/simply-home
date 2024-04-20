"use client"
import { useState, useEffect } from "react";
import { LightbulbIcon, SpeakerIcon } from "./components/icons";

type RoomProps = {
  roomName: string;
  lightOn: boolean;
  speakerOn: boolean;
  toggleLight: () => void;
  toggleSpeaker: () => void;
  lightColor: string;
  speakerText: string;
};

function Room({ roomName, lightOn, speakerOn, toggleLight, toggleSpeaker, lightColor, speakerText }: RoomProps) {
  return (
    <div className="border rounded-xl border-black p-6 m-4">
      <h2 className="font-semibold text-2xl text-center">{roomName}</h2>
      <div className="grid grid-cols-2 place-items-center mt-4">
        <button
          style={{ backgroundColor: lightOn ? lightColor : "transparent" }}
          className={`rounded-full p-3 ${
            lightOn ? "shadow-md" : "hover:shadow-md"
          }`}
          onClick={toggleLight}
        >
          <LightbulbIcon className="h-8 w-8" />
        </button>
        <button
          className={`rounded-xl p-3 ${
            speakerOn ? "bg-slate-200" : "hover:bg-slate-200"
          }`}
          onClick={toggleSpeaker}
        >
          <SpeakerIcon className="h-8 w-8" />
        </button>
        <div>
          {' '}
        </div>
        {speakerOn ? (
          <div className="p-2 text-center">
            {speakerText}
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default function Home() {
  const [livingRoomLight, setLivingRoomLight] = useState(false);
  const [kitchenLight, setKitchenLight] = useState(false);
  const [bedroomLight, setBedroomLight] = useState(false);

  const [livingRoomSpeaker, setLivingRoomSpeaker] = useState(false);
  const [kitchenSpeaker, setKitchenSpeaker] = useState(false);
  const [bedroomSpeaker, setBedroomSpeaker] = useState(false);

  const [livingRoomLightColor, setLivingRoomLightColor] = useState("yellow");
  const [kitchenLightColor, setKitchenLightColor] = useState("yellow");
  const [bedroomLightColor, setBedroomLightColor] = useState("yellow");

  const [livingRoomSpeakerText, setLivingRoomSpeakerText] = useState("living room speaker playing sound");
  const [kitchenRoomSpeakerText, setKitchenRoomSpeakerText] = useState("kitchen speaker playing sound");
  const [bedroomRoomSpeakerText, setBedroomRoomSpeakerText] = useState("bedroom speaker playing sound");
  
  const [time, setTime] = useState(new Date(0));

  {/* manual clock */}
  useEffect(() => {
    const interval = setInterval(() => {
      const newTime = new Date(time.getTime() + 15 * 60000);
      setTime(newTime);
    }, 1000);

    return () => clearInterval(interval);
  }, [time]);

  useEffect(() => {
    if((time.getTime()/60000) % 30){
      console.log("getting data")
      fetch("/api/read")
      .then((res) => res.json())
      .then((data) => {
        const parsedData = JSON.parse(data);
        setLivingRoomLight(parsedData.livingRoom.devices.light.isOn);
        setKitchenLight(parsedData.kitchen.devices.light.isOn);
        setBedroomLight(parsedData.bedroom.devices.light.isOn);
        
        setLivingRoomSpeaker(parsedData.livingRoom.devices.speaker.isOn);
        setKitchenSpeaker(parsedData.kitchen.devices.speaker.isOn);
        setBedroomSpeaker(parsedData.bedroom.devices.speaker.isOn);

        setLivingRoomLightColor(parsedData.livingRoom.devices.light.color);
        setKitchenLightColor(parsedData.kitchen.devices.light.color);
        setBedroomLightColor(parsedData.bedroom.devices.light.color);

        setLivingRoomSpeakerText(parsedData.livingRoom.devices.speaker.text);
        setKitchenRoomSpeakerText(parsedData.kitchen.devices.speaker.text);
        setBedroomRoomSpeakerText(parsedData.bedroom.devices.speaker.text);
      })
    }
  },[time])

  const formattedTime = time.toLocaleString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
    timeZone: "UTC",
  });

  return (
    <div>
      <h1 className="text-center text-3xl font-bold p-4">Home Simulator</h1>
      <h2 className="text-center text-xl">Current Time: {formattedTime}</h2>
      
      <div className="max-w-5xl flex flex-col mx-auto">
        <Room
          roomName="Living Room"
          lightOn={livingRoomLight}
          speakerOn={livingRoomSpeaker}
          toggleLight={() => setLivingRoomLight((prevLight) => !prevLight)}
          toggleSpeaker={() => setLivingRoomSpeaker((prevSpeaker) => !prevSpeaker)}
          lightColor={livingRoomLightColor}
          speakerText={livingRoomSpeakerText}
        />

        <Room
          roomName="Kitchen"
          lightOn={kitchenLight}
          speakerOn={kitchenSpeaker}
          toggleLight={() => setKitchenLight((prevLight) => !prevLight)}
          toggleSpeaker={() => setKitchenSpeaker((prevSpeaker) => !prevSpeaker)}
          lightColor={kitchenLightColor}
          speakerText={kitchenRoomSpeakerText}
        />

        <Room
          roomName="Bedroom"
          lightOn={bedroomLight}
          speakerOn={bedroomSpeaker}
          toggleLight={() => setBedroomLight((prevLight) => !prevLight)}
          toggleSpeaker={() => setBedroomSpeaker((prevSpeaker) => !prevSpeaker)}
          lightColor={bedroomLightColor}
          speakerText={bedroomRoomSpeakerText}
        />
      </div>
    </div>
  );
}
