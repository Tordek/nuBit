export type UserDataResponse = {
    user_id: string,
    username: string,
    avatar: string,
};

const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

export default async function (): Promise<UserDataResponse> {
    const request = await fetch(`${VUE_APP_API_URL}/api/auth/me`,
        {
            credentials: "include"
        });

    if (!request.ok) {
        throw new Error(await request.text());
    }

    return request.json();
}