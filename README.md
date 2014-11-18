partitioned-hash-join
=====================

This script computes the intersection of two 1.3 GB large files with 100 million entries each. The resulting intersection of the two sets is saved in a separate file `result.txt`. 

A single entry of the input file is of the format `A1234567890\r\n`. Two entries are equal if the numeric part of the entries are equal. For example is `A1234567890` equal to `B1234567890`.

The problem is that this program must not use more than 50 MB of RAM.

The zipped input files can be found here:

- [file1.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file1.zip)
- [file2.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file2.zip)

If you don't want to work on the complete set while developing, you can easily create smaller files with the following command:


`$ cat file1.txt | head -1000000 > 1m.txt`

This creates a file with only 1 million entries.


## todo

- make script more generic
  - don't hard-code file names
  - pass files as arguments when invoking the script
- if possible, make it faster
  - try lower number of buckets without hitting memory limit
- test on delphi
- finish README (how to invoke script)
