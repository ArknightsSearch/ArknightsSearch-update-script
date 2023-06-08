import os
from pathlib import Path

data_path = Path('data')
version_path = Path('version')
target_path = Path('target')
hash_path = Path('hash')


def touch_and_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    path.write_bytes(data)


def run():
    update_count = 0

    for path in hash_path.rglob('*.txt'):
        parts = path.parts[1:]
        dst_path = version_path.joinpath(*parts)

        if dst_path.exists() and dst_path.read_bytes() == path.read_bytes():
            continue

        update_count += 1

        version = path.read_text(encoding='utf-8')
        print(f'update {"/".join(parts).removesuffix(".txt")} {version}')
        touch_and_write(dst_path, path.read_bytes())

        parts = path.with_suffix('.json').parts[1:]
        touch_and_write(target_path.joinpath(*parts), data_path.joinpath(*parts).read_bytes())

    if update_count:
        os.system('echo "update=1" >> $GITHUB_ENV')
    else:
        os.system('echo "update=0" >> $GITHUB_ENV')


if __name__ == '__main__':
    run()
