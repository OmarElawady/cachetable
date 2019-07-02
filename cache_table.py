from collections import deque
from collections import MutableMapping
import time
class EntryTime:
    def __init__(self, key, insertion_time):
        self.key = key
        self.insertion_time = insertion_time
class CacheTable(MutableMapping): 
    def __init__(self, ttl):
        self.ttl = ttl
        self.data = {}
        self.insertedTimes = deque()
    def __getitem__(self, key):
        self.remove_expired()
        return self.data[key]
    def __setitem__(self, key, val):
        self.remove_expired()
        self.data[key] = val
        self.insertedTimes.appendleft(EntryTime(key, self.get_time()))
    def __delitem__(self, key):
        del self.data[key]
    def __len__(self):
        return len(self.data)
    def __iter__(self):
        return self
    def get_time(self):
        return int(round(time.time() * 1000))
    def remove_expired(self):
        while len(self.insertedTimes) != 0 and self.is_expired(self.insertedTimes[0]):
                del self.data[self.insertedTimes[0].key]
                self.insertedTimes.popleft()
    def is_expired(self, entry):
        return self.get_time() - entry.insertion_time > self.ttl

data = CacheTable(2000)
data["expire"] = 1
time.sleep(3)
print "exopire" in data
data["persist"] = 2
time.sleep(1)
print "persist" in data
