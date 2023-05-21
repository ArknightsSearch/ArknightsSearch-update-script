import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta


def calc_version() -> str:
    paths = sorted((i for i in Path('version').rglob('*') if i.is_file()), key=lambda x: x.as_posix())
    return hashlib.md5(b''.join(i.read_bytes() for i in paths)).hexdigest()


utc = datetime.utcnow().replace(tzinfo=timezone.utc)
now = utc.astimezone(timezone(timedelta(hours=8)))
time = now.strftime('%y-%m-%d-%H-%M-%S')

subprocess.run('git config --global user.email noreply@arkfans.top', shell=True)
subprocess.run('git config --global user.name MeeBooBot_v0', shell=True)
subprocess.run('git add version', shell=True)
subprocess.run(f'git commit -m \'[UPDATE] Data:{time}-{calc_version()[7:]}\'', shell=True)
