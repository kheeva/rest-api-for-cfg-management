import aiopg

from psycopg2 import IntegrityError


async def db_middleware(app, handler):
    async def middleware(request):
        if not app.get('db'):
            app['db'] = await aiopg.create_pool(app['dsn'], maxsize=11)
        request.app['db'] = app['db']
        return await handler(request)
    return middleware


async def store_cfg(request, cfg):
    file = cfg.file.read()
    file_name = cfg.filename.replace(' ', '_')

    with await request.app['db'].cursor() as cursor:
        await cursor.execute(
            '''
            INSERT INTO configurations (file_name, cfg) VALUES (%s, %s) RETURNING id;
            ''',
            (file_name, file,)
        )
        cfg_id, =  await cursor.fetchone()
        return cfg_id


async def get_cfg(request):
    with await request.app['db'].cursor() as cursor:
        await cursor.execute(
            '''
            SELECT file_name, cfg FROM configurations WHERE id=%s;
            ''',
            (request.query['cfg_id'],)
        )
        cfg = await cursor.fetchone()

        if not cfg:
            return None, None

        file_name, file_body = cfg[0], bytes(cfg[1])
        return file_name, file_body


async def get_cfg_list(request):
    with await request.app['db'].cursor() as cursor:
        await cursor.execute(
            '''
            SELECT id, loaded_on, file_name FROM configurations WHERE id IN (
            SELECT cfg_id FROM users_configurations WHERE user_id=(
            SELECT id FROM users WHERE username=%s));
            ''',
            (request.query['username'],)
        )
        return await cursor.fetchall()


async def add_user(request, data):
    with await request.app['db'].cursor() as cursor:
        try:
            await cursor.execute(
                '''
                INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;
                ''',
                (data['username'], data['password'],)
            )
            user_id, =  await cursor.fetchone()
        except IntegrityError:
            user_id = None
        return user_id


async def bind_cfg_to_user(request, data):
    with await request.app['db'].cursor() as cursor:
        try:
            await cursor.execute(
                '''
                INSERT INTO users_configurations (user_id, cfg_id) VALUES
                ((SELECT id FROM users WHERE username=%s), %s);
                ''',
                (data['username'], data['cfg_id'],)
            )
        except IntegrityError:
            status = 'fail'
        else:
            status = 'success'

        return status
