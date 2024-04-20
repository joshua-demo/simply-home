import fs from "fs"
import { NextResponse } from 'next/server'

// no post body

export async function POST() {

    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    const parsedData = JSON.parse(data);

    parsedData.frontHouse.devices.lock.isLocked = true;

    // @ts-ignore
    fs.writeFileSync("./app/api/data.json", JSON.stringify(parsedData), (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}