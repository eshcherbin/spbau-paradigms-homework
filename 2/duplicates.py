import os
import sys
from collections import defaultdict
from hashlib import sha1


CHUNK_SIZE = 4096


def calc_hash(filename):
    hasher = sha1()
    with open(filename, mode='rb') as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(CHUNK_SIZE)
        return hasher.hexdigest()


def find_duplicates(dirname):
    hash2files = defaultdict(list)
    for dirpath, _, filenames in os.walk(dirname):
        for f, f_full in zip(filenames, map(lambda s: os.path.join(dirpath, s),
                                            filenames)):
            if not (f.startswith('.') or f.startswith('~') or
                    os.path.islink(f_full)):
                hash2files[calc_hash(f_full)].append(f_full)
    return hash2files.values()


def main():
    if len(sys.argv) != 2:
        print('usage: python duplicates.py dirname')
        sys.exit(1)

    dirname = sys.argv[1]

    for files in find_duplicates(dirname):
        if len(files) > 1:
            print(*files, sep=':')


if __name__ == '__main__':
    main()
