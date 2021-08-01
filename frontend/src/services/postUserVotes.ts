import { EntryId, singleVote, VoteData, VoteParam, VoteParamName, VoteReplyEntry, WeekData } from "@/types";

const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

function packVoteData(weekData: WeekData, voteData: VoteData): VoteReplyEntry[] {
    const result: VoteReplyEntry[] = [];

    for (const [entryId, votes] of Object.entries<singleVote>(voteData)) {
        const entry = weekData.entries?.find(({ uuid }) => uuid === entryId)
        if (entry === undefined) continue;
        for (const [voteParam, value] of Object.entries<number | null>(votes)) {
            if (value === null) continue;
            result.push({
                entryUUID: entryId as EntryId,
                voteParam: voteParam as VoteParamName,
                voteForName: entry.entrantName,
                rating: value,
            })
        }
    }

    return result;
}

export default async function (weekData: WeekData, voteData: VoteData): Promise<void> {
    const response = await fetch(`${VUE_APP_API_URL}/api/votes/me`, {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({
            votes: packVoteData(weekData, voteData)
        }),
        headers: {
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        throw new Error("...");
    }
}