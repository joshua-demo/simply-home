import fs from "fs"
import { NextRequest, NextResponse } from 'next/server'

// example post body
// {
//     "room":"livingRoom",
//     "sound":"alarm"
// }

export async function POST(req: NextRequest) {
    const body = await req.json()
    
    const room = body.room;
    const sound = body.sound;

    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    const parsedData = JSON.parse(data);

    parsedData[room].devices.speaker.text = sound;
    parsedData[room].devices.speaker.isOn = true;

    // @ts-ignore
    fs.writeFileSync("./app/api/data.json", JSON.stringify(parsedData), (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}