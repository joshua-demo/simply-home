"use client"
import { useState, useEffect } from "react";
import { CameraIcon, LightbulbIcon, LockedIcon, SpeakerIcon, UnlockedIcon } from "./components/icons";

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
    <div className="p-6 m-4 border border-white rounded-xl">
      <h2 className="text-2xl font-semibold text-center">{roomName}</h2>
      <div className="grid grid-cols-2 mt-4 place-items-center">
        <button
          style={{
            backgroundColor: lightOn ? lightColor : "transparent",
            ...(lightOn ? {} : { ":hover": { backgroundColor: "rgb(107 114 128)" } }),
          }}
          className={`rounded-full p-3 border border-gray-800 transition-colors duration-350 ${
            lightOn ? "transparent text-gray-900" : "hover:border-gray-500"
          }`}
          onClick={toggleLight}
        >
          <LightbulbIcon className="w-8 h-8" />
        </button>
        <button
          className={`rounded-xl p-3 border border-gray-800 ${
            speakerOn ? "!border-gray-500" : "hover:border-gray-500"
          }`}
          onClick={toggleSpeaker}
        >
          <SpeakerIcon className="w-8 h-8" />
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
  
  const [frontHouseLock, setFrontHouseLock] = useState(true);
  const [frontHouseCameraItem, setFrontHouseCameraItem ] = useState("package");

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

        setFrontHouseLock(parsedData.frontHouse.devices.lock.isLocked);
        setFrontHouseCameraItem(parsedData.frontHouse.devices.camera.item);
      })
    }
  },[time])

  const formattedTime = time.toLocaleString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
    timeZone: "UTC",
  });

  const toggleLivingRoomLightFunction = async () => {
    if(livingRoomLight){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "livingRoom", device: "light" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "livingRoom", device: "light" }),
      });
    }
    setLivingRoomLight((prevLight) => !prevLight)
  }
  const toggleLivingRoomSpeakerFunction = async () => {
    if(livingRoomSpeaker){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "livingRoom", device: "speaker" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "livingRoom", device: "speaker" }),
      });
    }
    setLivingRoomSpeaker((prevSpeaker) => !prevSpeaker)
  }
  const toggleKitchenLightFunction = async () => {
    if(kitchenLight){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "kitchen", device: "light" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "kitchen", device: "light" }),
      });
    }
    setKitchenLight((prevLight) => !prevLight)
  }
  const toggleKitchenSpeakerFunction = async () => {
    if(kitchenSpeaker){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "kitchen", device: "speaker" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "kitchen", device: "speaker" }),
      });
    }
    setKitchenSpeaker((prevSpeaker) => !prevSpeaker)
  }
  const toggleBedroomLightFunction = async () => {
    if(bedroomLight){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "bedroom", device: "light" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "bedroom", device: "light" }),
      });
    }
    setBedroomLight((prevLight) => !prevLight)
  }
  const toggleBedroomSpeakerFunction = async () => {
    if(bedroomSpeaker){
      await fetch("/api/turnOff", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "bedroom", device: "speaker" }),
      });
    } else {
      await fetch("/api/turnOn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ room: "bedroom", device: "speaker" }),
      });
    }
    setBedroomSpeaker((prevSpeaker) => !prevSpeaker)
  }
  const toggleFrontHouseLockFunction = async () => {
    if(!frontHouseLock){
      await fetch("/api/lockDoor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
    } else {
      await fetch("/api/unlockDoor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
    }
    setFrontHouseLock((prevLock) => !prevLock)
  }

  return (
    <div className="bg-gray-800 min-h-[100vh] text-white/90">
      <h1 className="p-4 text-3xl font-bold text-center">Home Simulator</h1>
      <h2 className="text-xl text-center">Current Time: {formattedTime}</h2>
      
      <div className="flex flex-col max-w-5xl mx-auto">
        <Room
          roomName="Living Room"
          lightOn={livingRoomLight}
          speakerOn={livingRoomSpeaker}
          toggleLight={toggleLivingRoomLightFunction}
          toggleSpeaker={toggleLivingRoomSpeakerFunction}
          lightColor={livingRoomLightColor}
          speakerText={livingRoomSpeakerText}
        />

        <Room
          roomName="Kitchen"
          lightOn={kitchenLight}
          speakerOn={kitchenSpeaker}
          toggleLight={toggleKitchenLightFunction}
          toggleSpeaker={toggleKitchenSpeakerFunction}
          lightColor={kitchenLightColor}
          speakerText={kitchenRoomSpeakerText}
        />

        <Room
          roomName="Bedroom"
          lightOn={bedroomLight}
          speakerOn={bedroomSpeaker}
          toggleLight={toggleBedroomLightFunction}
          toggleSpeaker={toggleBedroomSpeakerFunction}
          lightColor={bedroomLightColor}
          speakerText={bedroomRoomSpeakerText}
        />

        <div>
          <div className="p-6 m-4 border border-white rounded-xl">
            <h2 className="text-2xl font-semibold text-center">Front Of House</h2>
            <div className="grid grid-cols-2 mt-4 place-items-center">
              <button
                className={"rounded-full p-3 border border-gray-800 hover:border-gray-500"}
                onClick={toggleFrontHouseLockFunction}
              >
                {frontHouseLock ? <LockedIcon className="w-8 h-8" /> : <UnlockedIcon className="w-8 h-8" />}
              </button>
              
              <div
                className="p-3 border border-gray-800 rounded-xl"
              >
                <CameraIcon className="w-8 h-8" />
              </div>
              <div>
                {' '}
              </div>
              <div className="p-2 text-center">
                Camera sees {frontHouseCameraItem}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
