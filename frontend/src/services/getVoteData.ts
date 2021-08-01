import { EntryId, VoteData, VoteParam, VoteParamName, WeekData } from "@/types";

const API_URL = process.env.VUE_APP_API_URL;

function buildVoteData(weekData: WeekData, voteData: VoteReplyEntry[]): VoteData {
  if (weekData.entries === null) return {};

  const votes: VoteData = {};
  for (const entry of weekData.entries) {
    votes[entry.uuid] = {};

    for (const voteParam of weekData.voteParams) {
      votes[entry.uuid][voteParam.name] = null;
    }
  }

  for (const vote of voteData) {
    votes[vote.entryUUID][vote.voteParam] = vote.rating;
  }

  return votes;
}

export default async function (weekData: WeekData): Promise<VoteData> {

  const request = await fetch(`${API_URL}/api/votes/me`, {
    credentials: "include"
  });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return Promise.resolve(buildVoteData(weekData, await request.json()));
}