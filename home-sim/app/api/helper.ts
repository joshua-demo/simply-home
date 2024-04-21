"use server"
import fs from "fs"

export const cameraAPI = async (item: string) => {
    // @ts-ignore
    const data = fs.readFileSync("./app/api/data.json", {encoding:'utf8', flag:'r'},(err) => {
        throw err;
    });
    const parsedData = JSON.parse(data);

    parsedData.frontHouse.devices.camera.item = item;

    // @ts-ignore
    fs.writeFileSync("./app/api/data.json", JSON.stringify(parsedData), (err) => {
        if (err) {
            console.error("Error writing data to file:", err);
            throw err;
        }
    });
}