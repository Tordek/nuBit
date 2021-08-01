export type EntryId = string;
export type VoteParamName = string;

export type WeekData = {
    votingOpen: boolean;
    submissionOpen: boolean;
    entries: Entry[] | null;
    entryCount: number;
    voteParams: VoteParam[];
    theme: string;
    date: string;
};

export type VoteParam = {
    name: VoteParamName;
    description: string;
    helpTips: Record<number, string>;
}

type Result = {
    name: VoteParamName;
    description: string;
    rating;
}

export type Entry = {
    uuid: EntryId;
    entrantName: string;
    entryName: string;
    pdfUrl: string;
    pdfFormat: string;
    mp3Url: string;
    mp3Format: string;
    isValid: boolean;
    entryNotes?: string;
    results?: {
        overall: Result;
        ratings: Result[];
    }
};

export type AuthenticatedQuery = {
    userstringey: string
}

export type UserData = {
    user_id: string,
    username: string,
    avatar: string,
};

export type VoteReplyEntry = {
    entryUUID: EntryId;
    voteParam: VoteParamName;
    voteForName: string;
    rating: number | null;
};

export type singleVote = Record<VoteParamName, number | null>;

export type VoteData = Record<EntryId, singleVote>;