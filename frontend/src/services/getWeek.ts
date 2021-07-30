import { WeekData } from "../types";

const VUE_APP_URL = process.env.VUE_APP_URL;

export type GetWeekRequest = {
    which: string
}

export default async function getWeek({ which }: GetWeekRequest): Promise<WeekData> {
    return Promise.resolve({
        submissionOpen: true,
        votingOpen: true,
        entries: [{
            entrantName: "Tordek",
            entryName: "Test",
            mp3Format: "mp3",
            mp3Url: "http://127.0.0.1",
            pdfUrl: "http://127.0.0.1",
            pdfFormat: "pdf",
            uuid: "123",
            prompt: 1,
            isValid: true,
        }],
        voteParams: [{
            name: "prompt",
            description: "Overall use of prompt",
            helpTipDefs: ["a", "b", "c", "d", "e"]
        }],
        date: Date(),
        theme: "test"
    })

    const request = await fetch(`${VUE_APP_URL}/api/entries/${which}`, {
        credentials: "include"
    });

    if (!request.ok) {
        throw new Error(await request.text());
    }

    return await request.json();
}