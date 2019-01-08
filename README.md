# rest-api-for-cfg-management
Async HTTP-REST-API based on aiohttp-server, aiopg and postgresql.
For now supports default aiohttp file size ~ 1mb.

# Installation
At first, install and run docker engine.
After that do several steps:

1) get code from github
`git clone https://github.com/kheeva/rest-api-for-cfg-management.git`

`cd rest-api-for-cfg-management/`

2) build docker containers
```buildoutcfg
sudo docker-compose up -d --build
```

By default http server starts on 0.0.0.0:8888,
postgresql uses 127.0.0.1:5432

# Use the app
**Add new user**:

    url: `http://127.0.0.1:8888/user`
    
    Send POST request to url with data fields:
     - `username`,
     - `password`.
    Field 'username' must be `unique`.

form example:
```html
<form action="http://127.0.0.1:8888/user" method="post" accept-charset="utf-8"
      enctype="multipart/form-data">

    <label for="add_user">add_user</label>
    <input id="username" name="username" type="hidden" value="kheeva" />
    <input id="password" name="password" type="hidden" value="123123" />
    <input type="submit" value="submit" />
</form>
```

**Get list of aviable configurations for a user**:

    url: `http://127.0.0.1:8888/user?username=username`
    
    Send GET request to url with query parameter username.

**Load a cfg to server**:

    url: `http://127.0.0.1:8888/cfg`
    
    Send POST request with field `type=file` and `name=cfg`

form example:
```html
<form action="http://127.0.0.1:8888/cfg" method="post" accept-charset="utf-8"
      enctype="multipart/form-data">

    <label for="cfg">load configuration</label>
    <input id="cfg" name="cfg" type="file" value="" />
    <input type="submit" value="submit" />
</form>
```

**Get a cfg from a server**:

    url: `http://127.0.0.1:8888/cfg?cfg_id={id}`
    id - positive integer
    Send GET request to url.

**Bind a cfg to a user**:

    url: `http://127.0.0.1:8888/bind`
    
    Send POST request with data fields:
    - username (varchar)
    - cfg_id (positive integer)
    
Example POST from:
```html
<form action="http://127.0.0.1:8888/bind" method="post" accept-charset="utf-8"
      enctype="multipart/form-data">

    <label for="cfg_bind">bind cfg to user</label>
    <input id="username" name="username" type="hidden" value="kheeva" />
    <input id="cfg_id" name="cfg_id" type="hidden" value="1" />

    <input type="submit" value="submit" />
</form>
```
You can customize .env, Dockerfile and docker-compose.yml if you want to change app behaviour.


**TO DO**:
 - Stream loading for big files;
 - Tests;
 - Logging;
 - PyDoc

# Project Goals

The code is written for educational purposes.
