export type EntryId = string & { readonly __tag: unique symbol };
export type VoteParamName = string & { readonly __tag: unique symbol };

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
};

export type AuthenticatedQuery = {
    userstringey: string
}

export type UserData = {
    user_id: string,
    username: string,
    avatar: string,
};

export type VoteData = Record<EntryId, Record<VoteParamName, number | null>>;