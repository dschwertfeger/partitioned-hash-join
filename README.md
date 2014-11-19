partitioned-hash-join
=====================

This is a homework solution for the following problem.

Given two **1.3 GB** large files with 100 million entries each, find the intersection of those files. The program must not use more than **50 MB** of RAM.

A single entry of the input files is of the format `A1234567890\r\n`. Two entries are equal if the numeric part of the entries are equal. For example is `A1234567890` equal to `B1234567890`.

The zipped input files can be found here:

- [file1.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file1.zip)
- [file2.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file2.zip)

As the name of the project suggests, the problem is solved using a partitioned hash join algorithm. 

# Running the script

Make sure the script is executable:

`$ chmod +x partitioned_hash_join.py`

Invoke the script, passing the files it should find the intersection for as arguments:

`$ ./partitioned_hash_join.py -r file1.txt -s file2.txt`

Optionally, you can pass the number of buckets for the partitioning step with the `-b` flag. The default is 150. Here's an example:

`$ ./partitioned_hash_join.py -r file1.txt -s file2.txt -b 123`

# Development

If you don't want to work on the complete set while developing, you can easily create smaller files with the following command:

`$ cat file1.txt | head -1000000 > 1m.txt`

This creates a file with only 1 million entries. The script runs in a reasonable amount of time with smaller file sizes.
