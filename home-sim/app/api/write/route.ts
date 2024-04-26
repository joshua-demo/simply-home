import { NextRequest, NextResponse } from 'next/server'
import fs from "fs"
import path from 'path';

const filePath = path.join(process.cwd(), 'app', 'api', 'data.json');

export async function POST(req: NextRequest) {
    const body = await req.json()

    const jsonData = JSON.stringify(body);
    // @ts-ignore
    fs.writeFileSync(filePath, jsonData, (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return NextResponse.json({ success: true }, { status: 200 });
}
