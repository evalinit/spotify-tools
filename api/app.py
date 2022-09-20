import binascii
import json
import os
from webbrowser import get

from aiohttp import web, ClientSession, BasicAuth


SONG_URL = 'https://open.spotify.com/track/0C0XkZtNBEJMzwtXJfgJxj?si=4a874b19613b4ddc'

SPOTIFY_CLIENT = ''


async def get_client_access_token(id, secret):
    url = 'https://accounts.spotify.com/api/token'
    auth = BasicAuth(id, secret)
    payload = {'grant_type': 'client_credentials'}
    async with ClientSession() as client:
        async with client.post(url, auth=auth, data=payload) as resp:
            print('asdfasdfasdfasdf')
            print(await resp.text())
            return (await resp.json())['access_token']


def get_id_from_url(url):
    split_url = url.split('/')
    track_id_str = split_url[-1]
    track_id = track_id_str.split('?')[0]
    return track_id


async def fetch(url, id, secret):
    async with ClientSession() as client:
        access_token = await get_client_access_token(id, secret)
        print('access_token', access_token)
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        async with client.get(url, headers=headers) as resp:
            return await resp.json()


# app
async def create_app():
    app = web.Application()
    app['config'] = {
        'debug': json.loads(os.environ.get('DEBUG', 'false')),
        'secret': os.environ.get('SECRET', 'devsecret'),
        'spotify_id': os.environ.get('SPOTIFY_ID'),
        'spotify_secret': os.environ.get('SPOTIFY_SECRET')
    }

    app.add_routes([
        web.get('/recommend', recommend)
    ])

    if app['config']['debug']:
        import aiohttp_debugtoolbar
        aiohttp_debugtoolbar.setup(app)

    async def startup(app):
        print(get_id_from_url(SONG_URL))

    async def shutdown(app):
        print('shutting down')

    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)

    return app


# routes
async def recommend(request):
    # TODO: secure this route
    track_id = get_id_from_url(SONG_URL)
    url = 'https://api.spotify.com/v1/audio-features/{}'.format(track_id)
    print('url', url)
    track_info = await fetch(url, request.app['config']['spotify_id'], request.app['config']['spotify_secret'])
    from pprint import pprint
    pprint(track_info)
    return web.json_response(track_info)
    

if __name__ == '__main__':
    web.run_app(create_app())
