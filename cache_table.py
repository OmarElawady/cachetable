from collections import deque
from collections import MutableMapping
import time
class EntryTime:
    """A class to store the entry time of the key along with the key"""
    def __init__(self, key, insertion_time):
        """Base of EntryTime

        Arguments:
            key {object} -- the key
            insertion_time -- the time it was inserted in in milliseconds
        """
        self.key = key
        self.insertion_time = insertion_time
class CacheTable(MutableMapping): 
    """A dict-like data structure in which the keys expire after a specific time"""
    def __init__(self, ttl):
        """Base of CachTable

        Arguments:
            ttl -- time to live for the keys in milliseconds
        
        data          {dict}  -- The dict of the stored data
        insertedTimes {deque} -- deque of EntryTime maintained in sorted order
        """
        self.ttl = ttl
        self.data = {}
        self.insertedTimes = deque()
    def __getitem__(self, key):
        """Gets the value of the key

        Arguments:
            key {object} -- the string representing the key

        Raises:
            KeyError -- if the key is expired or doesn't exist

        Returns:
            value of the key
        """
        self.remove_expired()
        return self.data[key]
    def __setitem__(self, key, val):
        self.remove_expired()
        self.data[key] = val
        self.insertedTimes.appendleft(EntryTime(key, self.get_time()))
    def __delitem__(self, key):
        del self.data[key]
    def __len__(self):
        self.remove_expired()
        return len(self.data)
    def __iter__(self):
        self.remove_expired()
        return self
    def get_time(self):
        """Returns the milliseconds since some reference time(this actual time is not relevant)"""
        return int(round(time.time() * 1000))
    def remove_expired(self):
        """Removes the expired key from the table and unmark their insertion time"""
        while len(self.insertedTimes) != 0 and self.is_expired(self.insertedTimes[0]):
                del self.data[self.insertedTimes[0].key]
                self.insertedTimes.popleft()
    def is_expired(self, entry):
        """Checks whether a key is expired

        Arguments:
            entry {EntryTime} -- The objcet in which the insertion_time and the key name is stored

        Returns:
            bool -- true if the key is expired
        """
        return self.get_time() - entry.insertion_time > self.ttl
if __name__ == "__main__":
    data = CacheTable(2000)
    data["expire"] = 1

    time.sleep(3)

    print("expire" in data)
    data["persist"] = 2
    time.sleep(1)
    print("persist" in data)
