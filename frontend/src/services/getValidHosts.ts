const VUE_APP_API_URL = process.env['VUE_APP_API_URL']

export default async function (): Promise<Array<string>> {
    const request = await fetch(`${VUE_APP_API_URL}/api/hosts/`);

    if (!request.ok) {
        throw new Error(await request.text());
    }

    return request.json();
}