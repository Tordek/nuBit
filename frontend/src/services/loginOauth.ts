import { UserDataResponse } from "./getUserData";

export type OauthRequestParams = {
    authorization_response: string,
};

const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

export default async function (oauthData: OauthRequestParams): Promise<UserDataResponse> {
    const request = await fetch(`${VUE_APP_API_URL}/api/oauth/discord`, {        
        credentials: "include",
        method: "POST",
        body: JSON.stringify(oauthData)
    });

    if (!request.ok) {
        throw new Error(await request.text());
    }

    return request.json();
}