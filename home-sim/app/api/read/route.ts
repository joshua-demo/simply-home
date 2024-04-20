import { NextRequest, NextResponse } from 'next/server'
import fs from "fs"

export async function GET() {

    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    return NextResponse.json(data, { status: 200 });
}
