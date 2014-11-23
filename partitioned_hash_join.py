#! /usr/bin/env python
"""This script computes the intersection of two files.

Usage:
  ./partitioned_hash_join.py -s file1 -r file2

Example Usage:
  ./partitioned_hash_join.py -r file1.txt -s file2.txt

This computes the intersection of the specified files and saves the result in a file called intersection.txt

Options:
  -h, --help    show these help docs
  -r, --file1   specify the first file
  -s, --file2   specify the second file
"""
from getopt import getopt, GetoptError
from io import open
from os import makedirs, path
from sys import argv, exit
from time import time

NR_OF_BUCKETS = 900

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

def h1(line):
    return int(line[1:4]) % NR_OF_BUCKETS

def init_buckets(name):
    if not path.exists('./tmp'):
        makedirs('./tmp')
    return [open('./tmp/{}_{}.txt'.format(name, i), 'w')
            for i in xrange(NR_OF_BUCKETS)]

def join_buckets(r, s):
    result = dict()
    for bucket in xrange(NR_OF_BUCKETS):
        hash_table = build_hash_table(r[bucket])
        part = join(hash_table, s[bucket])
        result.update(part)
        r[bucket].close()
        s[bucket].close()
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

def partition(src_file, to):
    with open(src_file, 'rt') as f:
        for line in f:
            bucket = h1(line)
            to[bucket].write(line)
    [to[x].close for x in xrange(NR_OF_BUCKETS)]

def write(result_dict):
    with open('intersection.txt', 'w') as f:
        for k, value in result_dict.iteritems():
            for v in value:
                f.write(v)

def usage():
    print __doc__

def main(argv):
    R = None
    S = None
    try:
        opts, args = getopt(argv, 'hr:s:b:', ['help', 'file1=', 'file2=', 'buckets='])
    except GetoptError as err:
        print str(err)
        usage()
        exit(2)
    if not opts:
        print 'You need to specify the files you would like to to find the intersection for!\n'
        usage()
        exit(2)
    for opt, arg, in opts:
        if opt in ('-h', '--help'):
            usage()
            exit()
        elif opt in ('-r', '--file1'):
            R = arg
        elif opt in ('-s', '--file2'):
            S = arg

    start_time = time()
    r = init_buckets('r')
    s = init_buckets('s')
    partition(R, r)
    partition(S, s)
    write(join_buckets(r, s))
    elapsed_time = time() - start_time
    print elapsed_time


if __name__=='__main__':
    main(argv[1:])
