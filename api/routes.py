from views import cfg, user, bind


def setup_routes(app):
    app.router.add_route('*', '/cfg', cfg)
    app.router.add_route('*', '/user', user)
    app.router.add_post('/bind', bind)
