# partitioned-hash-join

This is a homework solution for the following problem.

Given two **1.3 GB** large files with 100 million entries each, find the intersection of those files. The program must not use more than **50 MB** of RAM.

A single entry of the input files is of the format `A1234567890\r\n`. Two entries are equal if the numeric part of the entries are equal. For example is `A1234567890` equal to `B1234567890`.

The zipped input files can be found here:

- [file1.zip](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file1.zip)
- [file2.zip](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file2.zip)

As the name of the project suggests, the problem is solved using a partitioned hash join algorithm. 

# Running the script

First, clone this repo or [download as zip](https://github.com/dschwertfeger/partitioned-hash-join/archive/master.zip):

`$ git clone https://github.com/dschwertfeger/partitioned-hash-join.git`

Then, change into the directory:

`$ cd partitioned-hash-join`

Make sure the script is executable:

`$ chmod +x partitioned_hash_join.py`

The script partitions the input files into many smaller files. This might exceed the default limit for open files on some systems. You can easily increase the number of allowed open files with `ulimit` like this:

`$ ulimit -n 1024` 

Now, you can invoke the script, passing the files it should find the intersection for as arguments:

`$ ./partitioned_hash_join.py -r file1.txt -s file2.txt`

Should the input files not be in the same directory as the script itself, use `path/to/file` instead:

`$ ./partitioned_hash_join.py -r path/to/file1.txt -s path/to/file2.txt`

# How it works

## Partitioning phase

First, both input files are split into 450 smaller *bucket* files using a very simple hash function. The input file is read line by line and the hash function determines in which *bucket* to put this entry based on the first three numbers of an entry.

```python
def h1(line):
    return int(line[1:4]) % NR_OF_BUCKETS
```

This distributes the entries evenly to the smaller *bucket* files and makes sure that all entries of relation R and relation S end up in corresponding buckets. Each of those files has now only a size of 2.7 MB.

## Join phase

During the join phase, the buckets of relation `R` are consecutively read into memory as a `hash_table` and the corresponding buckets of relation `S` are read line-by-line from disk to find a match.

### Desgin of the hash table

Since memory is limited, it is desirable to keep the memory footprint of the `hash_table` small. The `hash_table` is built using Python's [dictionary](https://docs.python.org/2/tutorial/datastructures.html#dictionaries) data type. The keys are the number part of an entry as strings (`'4525879378'`) and the values are integers encoding the presence of letters for that key. A value could look like this `10011` which would encode the letters `A`, `B`, and `E`.

The idea is that a letter has a value of 10 to the power of its index in this list:

```python
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
```

An `A` has a value of `1` while a `J` has a value of `1,000,000,000`.

So, when the `hash_table` is built, we check for every `line` of file `f` if the `key` is already in the `hash_table` and if it is, we add the value for the letter to the already existing value if we haven't seen this letter before.

Here's an example:

```python
hash_table = {
    '4525879378': 1001
}
```

The entries `A4525879378` and `D4525879378` are stored in the `hash_table`. Let's assume the next entry we read is `B4525879378`. Then the value of `B` which is `10` is added to the already existing value, resulting in the new `hash_table`:

```python
hash_table = {
    '4525879378': 1011
}
```

### Joining the buckets

Once the `hash_table` for relation `R` is built, the corresponsing bucket for relation `S` is read from file line by line and joined with the `hash_table` for `R`. This process is very similar to building the `hash_table` for `R`.

### Writiing the results to file

[tbd]


# Memory usage

It turns out that measuring the memory usage of a program is not as easy as it might seem. If we look at the output of command line utilities like `ps`, `top` or `htop`, we usually see values for [*virtual* memory](http://serverfault.com/questions/138427/top-what-does-virtual-memory-size-mean-linux-ubuntu), which are called `VSZ`, `VSIZE`, and `VIRT` respectively, and values for *actual* memory, which are called `RSIZE`, `MEM`, `RES` and sometimes `RSS`. 

So, what does *actual* memory really mean, though? When we start profiling our program with tools like [`memory_profiler`](https://pypi.python.org/pypi/memory_profiler) or [Syrupy](https://github.com/jeetsukumaran/Syrupy), or by manually looking at the outputs of above-mentioned command line tools, we will notice that even the values for *actual* memory differ.

[This SO article](http://stackoverflow.com/a/1954774/1663506) does a pretty good job in explaining what we should look at when we are interested in *real* memory usage. The bottom line is, it is not so easy. 

Anyways, the following sections will assess the memory usage based on the used data structures and partly on profiling with Syrupy.

## Partitioning

The buckets for partitioning the input files are represented by a lists of file descriptors for writing the smaller *bucket* files.

- one list of length 450: 97,368 B
- two lists of length 450: 97,368 B * 2 = 194,763 B (~ 190.2 KB)
- file descriptor uses default write buffer of 8,192 KB
- write buffer for each file descriptor in both lists: 2 * 450 * 8,192 B = 7,372,800 B (~ 7.2 MB)
- Syrupy reports an average of 25 MB during the partitioning phase

## Hash table

To determine the hash table's size, we have to look at the sizes of the individual components the hash table is build of. The hash table is build using Python's `dictionary` data type. The keys are strings of length 10 and the values are simply a single `int`.

>An empty string costs 37 bytes in a 64-bit environment! Memory used by string then linearly grows in the length of the (useful) string. [[deeplearning.net](http://deeplearning.net/software/theano/tutorial/python-memory-management.html)]

One `hash_table` will have 222,222 entries on average because we partition the 100,000,000 entries of the input file into 450 files.

- size of dictionary with 222,222 entries: 12.583.192 B
- 222,222 values with 24 B each: 5,333,328 B
- 222,222 keys with 47 B each: 10,444,434 B
- in total: 28,360,954 B (~ 27 MB)

A recursive version of `sys.getsizeof()` based on this [Python recipe](http://code.activestate.com/recipes/577504/) returns a size of 28,008,230 B (27.6 MB) for a `hash_table` with actual 222,222 entries.

## Join

During the join phase only one `hash_table` is in memory. The corresponding bucket of relation S is read from the partitioned files on disk line by line to check for a match.

Syrupy reports a maximum memory usage of 49,112 KB (~ 48 MB) during this phase.

# Results

- runs in 8 mins 47 secs on delphi
- size of resulting file is 25.1 MB
- RSS profiled with Syrupy does not exceed 49,112 KB
- the [result file](https://dl.dropboxusercontent.com/u/22040079/intersection.txt) `intersection.txt` contains 2,092,935 entries (`$ wc -l intersection.txt`)  

# Development

If you don't want to work on the complete set while developing, you can easily create smaller files with the following command:

`$ cat file1.txt | head -1000000 > 1m.txt`

This creates a file with only 1 million entries. The script runs in a reasonable amount of time with smaller file sizes.
