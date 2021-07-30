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
- `VUE_APP_APP_URL=` - The URL prefix the client is served at
- `VUE_APP_API_URL=` - The URL prefix the server is served at

Backend settings:
- `CLIENT_ID=` - Your Discord App ID
- `CLIENT_SECRET=` - Your Discord App Secret (don't publish it!)
- `SERVER_ID=` - We want to check that the user belongs to the server,
    so put the proper ID here
- `COOKIE_SECRET=` - A random string to encrypt cookies
- `BOT_TOKEN=` - The Discord Bot token
- `ADMIN_ROLE_ID=` - ID for the Role given to admins on the server.
- `COMMAND_PREFIXES=` - Space-separated list of valid command prefixes
- `NOTIFY_ADMINS_CHANNEL=` - ID for the channel where admin notifications are
    sent
- `URL_BASE=` - Base URL assets will be served from.
- `TIMEZONE_OFFSET=` - Timezone delta between the server and the display.

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

Implementation details
----------------------
- Since Discord uses huge numbers for its ids, and Javascript doesn't play well
    with them, we store them as strings whenever possible and convert them to
    `int` whenever interacting with the bot.

License
-------

nuBit is released under the GNU GPL v3 License.