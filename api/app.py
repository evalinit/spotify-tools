import binascii
import json
import os

from aiohttp import web, ClientSession



# app
async def create_app():
    app = web.Application()
    app['config'] = {
        'debug': json.loads(os.environ.get('DEBUG', 'false')),
        'secret': os.environ.get('SECRET', 'devsecret')
    }

    app.add_routes([
        web.get('/recommend', recommend)
    ])

    if app['config']['debug']:
        import aiohttp_debugtoolbar
        aiohttp_debugtoolbar.setup(app)

    async def startup(app):
        print('starting up')

    async def shutdown(app):
        print('shutting down')

    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)

    return app


# routes
async def recommend(request):
    # TODO: secure this route
    return web.json_response({'spotify_url': 'this would be a url'})
    

if __name__ == '__main__':
    web.run_app(create_app())
