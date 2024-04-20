import { NextRequest, NextResponse } from 'next/server'
import fs from "fs"

export async function POST(req: NextRequest) {
    const body = await req.json()

    const jsonData = JSON.stringify(body);
    // @ts-ignore
    fs.writeFileSync("./app/api/data.json", jsonData, (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}
