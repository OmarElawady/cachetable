from collections import MutableMapping
import time
class CacheTablePerEntry:
    def __init__(self):
        self.data = {}
        self.removalTime = {}
    def get(self, key):
        self.remove_expired()
        return self.data[key]
    def set(self, key, val, ttl):
        self.remove_expired()
        self.data[key] = val
        self.removalTime[key] = self.get_time() + ttl
    def get_time(self):
        return int(round(time.time() * 1000))
    def remove_expired(self):
        for key in list(self.removalTime.keys()):
            if self.is_expired(key):
                self.remove_key(key)
    def is_expired(self, key): 
        return self.get_time() > self.removalTime[key]
    def remove_key(self, key):
        del self.data[key]
        del self.removalTime[key]
    
    def exists(self, key):
        self.remove_expired()
        return key in self.data
if __name__ == "__main__":
    dic = CacheTablePerEntry()
    dic.set("expire", 1, 1000)
    time.sleep(2)
    print(dic.exists("expire"))

    dic.set("persist", 2, 2000)
    time.sleep(1)
    print(dic.exists("persist"))
