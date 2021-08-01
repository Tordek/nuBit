import { Entry } from "@/types";

export type EntryRespone = Entry;

const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

export default async function (): Promise<EntryRespone> {
    const request = await fetch(`${VUE_APP_API_URL}/api/entries/me`,
        {
            credentials: "include"
        });

    if (!request.ok) {
        throw new Error(await request.text());
    }

    return request.json();
}