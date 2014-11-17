partitioned-hash-join
=====================

This script computes the intersection of two 1.3 GB large files with 100 million entries each. The resulting intersection of the two sets is saved in separate file a `results.txt`. 

An entry of the input file is of the format `A1234567890\r\n`. Two entries are equal if the numeric part of the entries are equal. For example is `A1234567890` equal to `B1234567890`.

The problem is that this program must not use more than 50 MB of RAM.

The zipped input files can be found here:

- [file1.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file1.zip)
- [file2.txt](http://www2.informatik.hu-berlin.de/~wandelt/DWDM/file2.zip)
