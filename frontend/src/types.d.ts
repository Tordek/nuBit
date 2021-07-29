export type WeekData = {
    viewingOpen: boolean;
    votingOpen: boolean;
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
    mp3Url: string;
    mp3Format: string;
} & Record<string, any>;

export type AuthenticatedQuery = {
    userstringey: string
}