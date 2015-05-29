pyZTime
=======

Shows an implementation of distributed time. 
The first ztime node in the network starts decides on a time 0 point. Nodes entering the network after that calculate an offset to their local times from all other peers keeping time. Even if the original node stops, the other nodes keep the original 0 time in effect through their calculated offsets.


Statistics
----------
This implementation uses the statistics module to calculate the median of time-offsets suggested by peers.
On Python 3.2 (eg Raspbian), this is not a standard module so it has to be installed. Unfortunately the current Pypi version of statistics has issues with python3.2, so it needs to be patched

```
sudo pip3 install statistics
sudo 2to3 -w /usr/local/lib/python3.2/dist-packages/statistics/__init__.py
```
