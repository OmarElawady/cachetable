from collections import MutableMapping
import time
class CacheTablePerEntry:
    """This is a cache table which is a dict with diffrent expiration time for each key"""
    def __init__(self):
        """Base for CacheTablePerEntry
        
        data        {dict} -- the dictionary in which the table is stored
        removalTime {dict} -- the dictionary which marks the expiration time for each key
        """
        self.data = {}
        self.removalTime = {}

    def get(self, key):
        """Gets the value of the key if it exists and not expired

        Arguments:
            key {object} -- the name of the key

        Raises:
            KeyError -- if the key expired or doesn't exist

        Returns:
            val -- the value associated with the key
        """
        self.remove_expired()
        return self.data[key]
    
    def set(self, key, val, ttl):
        """Adds or override the key with the given val to expire in ttl milliseconds

        Arguments:
            key {object} -- the name of the key
            val {object} -- the value associated with the key
            ttl {int}    -- time to live in milliseconds

        """
        self.remove_expired()
        self.data[key] = val
        self.removalTime[key] = self.get_time() + ttl
    
    def get_time(self):
        """Gets the milliseconds with respect to some reference time(the reference is not important).

        Returns:
            int -- milliseconds since the reference time
        """
        return int(round(time.time() * 1000))
    
    def remove_expired(self):
        """passes over all keys and revoves the one that passes its expiration time"""
        for key in list(self.removalTime.keys()):
            if self.is_expired(key):
                self.remove_key(key)
    
    def is_expired(self, key): 
        """Checks whether the given key is expired
        
        Arguments:
            key {objcet} -- the key to be checked

        Returns:
            bool -- true if the key passed its expiration time
        """
        return self.get_time() > self.removalTime[key]
    
    def remove_key(self, key):
        """Removes the key from the dict and unmark its expiration time

        Arguments:
            key {object} -- the key to be removed
        """
        del self.data[key]
        del self.removalTime[key]
    
    def exists(self, key):
        """Checks whether key exists in the stored data

        Arguments:
            key {object} -- the key to be checked

        Returns:
            bool -- false if the key is not stored or expired, true otherwise
        """
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
