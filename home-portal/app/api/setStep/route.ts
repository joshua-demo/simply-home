import { NextRequest, NextResponse } from "next/server";
import fs from 'fs';

export async function POST(req: NextRequest) {
    const body = await req.json()
    
    const step = JSON.stringify({step: body.step});

    // @ts-ignore
    fs.writeFileSync("./app/api/step.json", step, (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}