import { UserDataResponse } from "./getUserData";

export type SubmitRequest = {
  name: string,
  pdfFile?: File,
  mp3File?: File,
  mp3Link?: string,
};

const API_URL = process.env['VUE_APP_API_URL']

export default async function (entry: SubmitRequest): Promise<UserDataResponse> {
  const formData = new FormData();

  formData.append("name", entry.name);

  if (entry.pdfFile !== undefined) {
    formData.append("pdfFile", entry.pdfFile, entry.pdfFile.name);
  }

  if (entry.mp3File !== undefined) {
    formData.append("mp3File", entry.mp3File, entry.mp3File.name);
  }

  if (entry.mp3Link !== undefined) {
    formData.append("mp3Link", entry.mp3Link);
  }

  const request = await fetch(`${API_URL}/api/entries/me`, {
    credentials: "include",
    method: "PUT",
    body: formData,
  });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return request.json();
}