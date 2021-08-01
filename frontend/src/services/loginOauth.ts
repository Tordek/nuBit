import { UserDataResponse } from "./getUserData";

export type OauthRequestParams = {
  code: string,
  state: string,
  redirectUri: string,
};

const API_URL = process.env['VUE_APP_API_URL']

export default async function (oauthData: OauthRequestParams): Promise<UserDataResponse> {
  const request = await fetch(`${API_URL}/api/auth/discord`, {
    credentials: "include",
    method: "POST",
    body: JSON.stringify(oauthData),
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return request.json();
}