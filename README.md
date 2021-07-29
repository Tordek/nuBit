nuBit
=====

Website to aid the 8BMT Server's Weekly competition, using Vue for a frontend
and FastAPI for a backend.

Configuration
-------------

Make sure to install the proper packages by doing
`pip install -r requirements.txt` for the backend and `npm install` for the
frontend.

Configuration is done through `env` variables or `.env` files.

Frontend settings:
- `VUE_APP_API_URL=` - The URL the server is served at
- `VUE_APP_OAUTH_URL=https://discord.com/api/oauth2/authorize...` - The Discord
    URL the user logs in at. Configure the `redirect_url` for your app.

Backend settings:
- `CLIENT_ID=` - Your Discord App ID
- `CLIENT_SECRET=` - Your Discord App Secret (don't publish it!)
- `SERVER_ID=` - We want to check that the user belongs to the server,
    so put the proper ID here
- `COOKIE_SECRET=` - A random string to encrypt cookies

Running
-------

If you use Visual Studio Code, open the workspace provided in .vscode and you
can use the launch scripts.

To run it manually, the server part is run with `uvicorn src.main:app --reload`
and the client is run with `npm run serve`.

Installing
----------

Run `npm run build` on the frontend, copy it to the backend's `static` directory
and serve.

License
-------

nuBit is released under the GNU GPL v3 License.