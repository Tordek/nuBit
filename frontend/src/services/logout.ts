const API_URL = process.env['VUE_APP_API_URL']

export default async function () {
  const request = await fetch(`${API_URL}/api/auth/logout`, {
    credentials: "include",
    method: "POST",
  });

  if (!request.ok) {
    throw new Error(await request.text());
  }
}