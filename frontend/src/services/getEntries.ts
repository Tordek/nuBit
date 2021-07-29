import { WeekData } from "../types";

const VUE_APP_URL = process.env.VUE_APP_URL;

export type GetEntriesParameter = {
    userKey?: string
}

// Necessary for Vue reactivity
function ensureFormat(week: WeekData): WeekData {
    for (const entry of week.entries) {
        for (const voteParam of week.voteParams) {
            if (!Object.prototype.hasOwnProperty.call(entry, voteParam.name)) {
                entry[voteParam.name] = null;
            }
        }
    }

    return week;
}

export default async function getEntries({ userKey }: GetEntriesParameter): Promise<WeekData> {
    return Promise.resolve({
        viewingOpen: true,
        votingOpen: true,
        entries: [{
            entrantName: "Tordek",
            entryName: "Test",
            mp3Format: "mp3",
            mp3Url: "http://127.0.0.1",
            pdfUrl: "http://127.0.0.1",
            uuid: "123",
            prompt: 1
        }],
        voteParams: [{
            name: "prompt",
            description: "Overall use of prompt",
            helpTipDefs: ["a", "b", "c", "d", "e"]
        }],
        date: Date(),
        theme: "test"
    })

    const options = {} as RequestInit;
    if (userKey !== undefined) {
        options.headers = {
            Authorization: 'Bearer ' + userKey
        }
    }
    const request = await fetch(`${VUE_APP_URL}/api/entries`, options);

    if (!request.ok) {
        throw new Error(await request.text());
    }

    const rawResponse = await request.json();

    return ensureFormat(rawResponse);
}