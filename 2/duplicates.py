import os
import sys
from collections import defaultdict
from hashlib import sha1


CHUNK_SIZE = 4096


def calc_hash(filename):
    hasher = sha1()
    with open(filename, mode='rb') as f:
        chunk = f.read(CHUNK_SIZE)
        while chunk != b'':
            hasher.update(chunk)
            chunk = f.read(CHUNK_SIZE)
    return hasher.hexdigest()


def main():
    if len(sys.argv) != 2:
        print('usage: python duplicates.py dirname')
        sys.exit(1)

    dirname = os.path.abspath(sys.argv[1])

    hash2files = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            if not (f.startswith('.') or f.startswith('~')):
                f = os.path.join(dirpath, f)
                hash2files[calc_hash(f)].append(f)

    for files in hash2files.values():
        if len(files) > 1:
            print(':'.join(map(str, files)))


if __name__ == '__main__':
    main()
