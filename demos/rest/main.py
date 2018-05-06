from aiohttp import web
from aiohttp_swagger import setup_swagger
import aiosqlite

DB_NAME = 'sqlite.db'


class MyView(web.View):
    """
    ---
    description: This is test
    tags:
    - Index url
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation
    """

    async def get(self):
        resp = []
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute("SELECT 42;") as cursor:
                async for row in cursor:
                    resp.append(row)

        return web.json_response({'data': resp})


    async def post(self):
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("INSERT INTO some_table VALUES (43)")
            await db.commit()

        return web.json_response({'status_code': 201})



async def init_app():

    app = web.Application()

    app.add_routes([
        web.get('/', MyView),
        web.post('/', MyView)
    ])

    setup_swagger(app)

    return app


def main():
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
