# -*- coding: UTF-8 -*-

import os
import time
import hashlib
import asyncio
from pathlib import Path

import aiohttp

client: aiohttp.ClientSession | None = None


def sign(key: str) -> dict:
    ts = str(int(time.time()))
    signature = hashlib.sha256(f'{key}AS{ts}'.encode('utf-8')).hexdigest()
    return {'signature': signature, 'timestamp': ts}


async def upload(server: str, key: str, path: str, file: bytes):
    global client
    async with client.put(server, headers=sign(key), params={'path': path, 'site': 'data'},
                          data={'file': file}) as r:
        if r.status:
            res = await r.json()
            if res['code'] == 200:
                return True
            else:
                return res['code']
        else:
            return r.status


def scan(path: str = 'target'):
    return [(i.as_posix(), i.as_posix().removeprefix('target/')) for i in Path(path).rglob('*') if i.is_file()]


async def run():
    global client
    client = aiohttp.ClientSession()

    server = os.environ.get('SERVER')
    key = os.environ.get('KEY')

    files = scan()
    y = len(files)
    x = 0

    for path, target in files:
        x += 1

        with open(path, mode='rb') as f:
            res = await upload(server, key, target, f.read())
        if res is True:
            print(f'[{x}/{y}] upload {target} successfully')
        else:
            print(f'[{x}/{y}] upload {target} failed \n{res}')

    async with client.post(server + 'restart', headers=sign(key)) as r:
        resp = await r.json()
        if resp['code'] == 200:
            print('restart server')
        else:
            print('restart failed', resp['data']['code'])
            raise ValueError

    await client.close()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
