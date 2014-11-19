from io import open
from os import makedirs, path
from time import time

NR_OF_BUCKETS = 150

R = 'r10m.txt'  # 'file1.txt'
S = 's10m.txt'  # 'file2.txt'

def init_buckets(name):
    if not path.exists('./tmp'):
        makedirs('./tmp')
    return [open('./tmp/{}_{}.txt'.format(name, i), 'w') for i in xrange(NR_OF_BUCKETS)]

def h1(line):
    return int(line[1:4]) % NR_OF_BUCKETS

def build_hash_table(from_file):
    hash_table = dict()
    with open(from_file.name, 'r') as f:
        for line in f:
            key = line[1:11]
            # elimitinate duplicates
            if key in hash_table:
                hash_table[key].add(line)
            else:
                hash_table[key] = set()
                hash_table[key].add(line)
    return hash_table

def partition(src_file, to):
    with open(src_file, 'rt') as f:
        for line in f:
            bucket = h1(line)
            to[bucket].write(line)

def join_buckets(r, s):
    result = dict()
    for bucket in xrange(NR_OF_BUCKETS):
        hash_table = build_hash_table(r[bucket])
        part = join(hash_table, s[bucket])
        result.update(part)
        del part
        del hash_table
    return result

def join(hash_table, file):
    results = dict()
    with open(file.name, 'r') as f:
        for line in f:
            key = line[1:11]
            if key in hash_table:
                results[key] = hash_table[key]
                results[key].add(line)
    return results

def write(result_dict):
    with open('result.txt', 'w') as f:
        for k, value in result_dict.iteritems():
            for v in value:
                f.write(v)


if __name__=='__main__':

    start_time = time()
    r = init_buckets('r')
    s = init_buckets('s')
    partition(R, r)
    partition(S, s)
    write(join_buckets(r, s))
    elapsed_time = time() - start_time
    print elapsed_time
