import { NextRequest, NextResponse } from 'next/server'
import fs from "fs"
import path from 'path';

const filePath = path.join(process.cwd(), 'app', 'api', 'data.json');

export async function GET() {

    // @ts-ignore
    const data = fs.readFileSync(filePath, {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    return NextResponse.json(data, { status: 200 });
}
