from aiohttp import web
from db import store_cfg, get_cfg, add_user, bind_cfg_to_user, get_cfg_list


async def cfg(request):
    if request.method == 'GET' and request.query.get('cfg_id'):
        file_name, cfg = await get_cfg(request)
        if not file_name or not cfg:
            return web.json_response({'status': 'fail'})

        headers = {
            "Content-disposition": "attachment; filename={file_name}".format(
                file_name=file_name)
        }

        return web.Response(body=cfg, headers=headers)
    elif request.method == 'POST':
        post_parameters = await request.post()
        if post_parameters.get('cfg'):

            stored_cfg_id = await store_cfg(request, post_parameters['cfg'])

            if stored_cfg_id:
                response = {'status': 'success', 'cfg_id': stored_cfg_id}
            else:
                response = {'status': 'fail', 'cfg_id': None}

            return web.json_response(response)
        else:
            return web.Response(text='Bad request', status=400)

    return web.Response(text='Forbidden', status=403)


async def user(request):
    if request.method == 'GET' and request.query.get('username'):
        cfg_list = await get_cfg_list(request)

        if not cfg_list:
            return web.json_response({'status': 'fail'})

        response = {'status': 'success', 'configurations': []}

        for cfg in cfg_list:
            cfg_id, loaded_on, file_name = cfg
            loaded_on = loaded_on.strftime('%d-%m-%Y %H:%M:%S')
            response['configurations'].append({
                'cfg_id': cfg_id,
                'loaded_on': loaded_on,
                'file_name': file_name
            }
            )
        return web.json_response(response)
    elif request.method == 'POST':
        post_parameters = await request.post()
        if post_parameters.get('username') and post_parameters.get('password'):
            user_id = await add_user(request, post_parameters)

            if user_id:
                response = {'status': 'success', 'user_id': user_id}
                return web.json_response(response)
            else:
                return web.json_response({'status': 'fail'})
        else:
            return web.Response(text='Bad request', status=400)

    return web.Response(text='Forbidden', status=403)


async def bind(request):
    post_parameters = await request.post()
    if post_parameters.get('username') and post_parameters.get('cfg_id'):
        bind_status = await bind_cfg_to_user(request, post_parameters)
        return web.json_response({'status': bind_status})
    else:
        return web.Response(text='Bad request', status=400)
