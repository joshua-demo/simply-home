import fs from "fs"
import { NextResponse } from 'next/server'

export async function GET() {

    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    const parsedData = JSON.parse(data);

    return NextResponse.json({data: parsedData.frontHouse.devices.camera.item, success: true }, { status: 200 });
}