import { NextRequest, NextResponse } from "next/server";
import fs from 'fs';
import path from 'path';

const filePath = path.join(process.cwd(), 'app', 'api', 'step.json');

export async function POST(req: NextRequest) {
    const body = await req.json()
    
    const step = JSON.stringify({step: body.step});

    // @ts-ignore
    fs.writeFileSync(filePath, step, (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}