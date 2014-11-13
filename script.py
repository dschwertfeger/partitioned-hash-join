from io import open
from time import time

NR_OF_BUCKETS = 90
R = 'r10m.txt'  # 'file1.txt'
S = 's10m.txt'  # 'file2.txt'

def init_buckets(name):
    return [open('{}_{}.txt'.format(name, i), 'w') for i in range(NR_OF_BUCKETS)]

def h1(line):
    return int(line[1:3]) % NR_OF_BUCKETS

def make_row(line):
    row = [line[1:10]]
    row.append(line[:1])
    str = ','.join(row)
    return str + '\n'

def get_size(file):
    file.seek(0, 2)
    return file.tell()

def build_hash_table(from_file):
    hash_table = dict()
    with open(from_file.name, 'r') as f:
        for line in f:
            key, value = line.split(',')
            value = value[:1]
            # elimitinate duplicates
            if key in hash_table:
                hash_table[key].add(value)
            else:
                hash_table[key] = set(value)
    return hash_table

def partition(src_file, to):
    with open(src_file, 'rt') as f:
        for line in f:
            bucket = h1(line)
            row = make_row(line)
            to[bucket].write(row)

def join_buckets():
    result = dict()
    for bucket in range(NR_OF_BUCKETS):
        hash_table = build_hash_table(r[bucket])
        part = join(hash_table, s[bucket])
        result.update(part)
        del hash_table
    return result

def join(hash_table, file):
    results = dict()
    with open(file.name, 'r') as f:
        for line in f:
            key, value = line.split(',')
            value = value[:1]
            if key in hash_table:
                results[key] = hash_table[key]
                results[key].add(value)
    return results

def write(result_dict):
    with open('result.txt', 'w') as f:
        for key, values in result_dict.iteritems():
            for v in values:
                f.write(u'{}{}\n'.format(v, key))


if __name__=='__main__':

    start_time = time()
    r = init_buckets('r')
    s = init_buckets('s')
    partition(R, r)
    partition(S, s)
    write(join_buckets())
    elapsed_time = time() - start_time
    print elapsed_time
