type VoteData = {
    entryUUID: string,
    voteForName: string,
    voteParam: string,
    rating: number | null
};

export type PostUserVotesParams = {
    votes: Array<VoteData>,
    voteKey: string
};

export default async function (voteData: PostUserVotesParams): Promise<void> {
    const response = await fetch("submit_vote", {
        method: "POST",
        body: JSON.stringify(voteData),
        headers: {
            "Content-Type": "application/json"
        }
    });
    if (!response.ok) {
        throw new Error("...");
    }
}