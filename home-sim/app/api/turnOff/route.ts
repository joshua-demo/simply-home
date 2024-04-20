import fs from "fs"
import { NextRequest, NextResponse } from 'next/server'

// example post body
// {
//     "room":"livingRoom",
//     "device":"light"
// }

export async function POST(req: NextRequest) {
    const body = await req.json()
    
    const room = body.room;
    const device = body.device;

    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    const parsedData = JSON.parse(data);

    parsedData[room].devices[device].isOn = false;

    // @ts-ignore
    fs.writeFileSync("./app/api/data.json", JSON.stringify(parsedData), (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}