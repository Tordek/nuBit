export type AuthUrlRequest = {
  redirectUri: string,
};

export type AuthUrlResponse = {
  authUrl: string,
};

const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

export default async function ({ redirectUri }: AuthUrlRequest): Promise<AuthUrlResponse> {
  const request = await fetch(`${VUE_APP_API_URL}/api/auth/discord?redirectUri=${encodeURIComponent(redirectUri)}`,
    {
      credentials: "include"
    });

  if (!request.ok) {
    throw new Error(await request.text());
  }

  return request.json();
}