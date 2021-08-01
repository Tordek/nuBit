type VoteData = {
    entryUUID: string,
    voteForName: string,
    voteParam: string,
    rating: number | null
};

export type PostUserVotesParams = {
    votes: VoteData[],
};

export default async function (voteData: PostUserVotesParams): Promise<void> {
    const response = await fetch("submit_vote", {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(voteData),
        headers: {
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        throw new Error("...");
    }
}