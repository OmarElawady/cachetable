Cache table
===========

This is a project that provides a dict like data structure in which the keys expire after a specific time.

The project has two versions:
1. the time to live is specified for all the keys in the cache table.
2. the time to live is specified for each entry individually.

This is the [documentation](https://omarelawady.github.io/cachetable/doc/) of the project.

Sample Usage
============
```python
import cache_table_per_entry
import cache_table
import time

table1 = cache_table.CacheTable(2000)
table1["key1"] = 1
time.sleep(3)
print("key1" in table1) # False
table1["key2"] = 2
time.sleep(1)
print("key2" in table1) # True

dic = cache_table_per_entry.CacheTablePerEntry()
dic.set("expire", 1, 1000)
time.sleep(2)
print(dic.exists("expire")) # False
dic.set("persist", 2, 2000)
time.sleep(1)
print(dic.exists("persist")) # True
```
