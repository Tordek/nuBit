export type WeekData = {
    votingOpen: boolean;
    submissionOpen: boolean;
    entries: Entry[];
    voteParams: VoteParam[];
    theme: string;
    date: string;
};

export type VoteParam = {
    name: string;
    description: string;
    helpTipDefs: Record<number, string>;
}

export type Entry = {
    uuid: string;
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