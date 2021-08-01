import { WeekData } from "../types";

const API_URL = process.env.VUE_APP_API_URL;

export type GetWeekRequest = {
  which: string
}

export default async function getWeek({ which }: GetWeekRequest): Promise<WeekData> {
  const request = await fetch(`${API_URL}/api/weeks/${which}`, {
    credentials: "include"
  });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return await request.json();
}