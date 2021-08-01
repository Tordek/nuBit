import { Entry } from "@/types";

const VUE_APP_API_URL = process.env['VUE_APP_API_URL'];

export type GetEntryRequest = {
  which: string
}


export default async function ({ which }: GetEntryRequest): Promise<Entry> {
  const request = await fetch(`${VUE_APP_API_URL}/api/entries/me/${which}`,
    {
      credentials: "include"
    });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return request.json();
}