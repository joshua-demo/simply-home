"use server"
import fs from 'fs';

export async function getStep() {
    // @ts-ignore
    const data = fs.readFileSync("./app/api/step.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });

    return JSON.parse(data).step;
}

export async function setStep(step: number) {
    const jsonData = JSON.stringify({step: step})
    // @ts-ignore
    fs.writeFileSync("./app/api/step.json", jsonData, (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });

    return;
}