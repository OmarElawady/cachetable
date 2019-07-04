import pytest
import cache_table
import cache_table_per_entry
import time
def test_cache_table_key_expired():
    table = cache_table.CacheTable(1000)
    table["key1"] = 2
    time.sleep(2)
    assert ("key1" in table) == False, "Key is expired but not removed"

def test_cache_table_key_not_expired():
    table = cache_table.CacheTable(2000)
    table["key"] = 3
    time.sleep(1)
    assert ("key" in table) == True, "Key added and not expired but doesn't exist"


def test_cache_table_len():
    table = cache_table.CacheTable(2000)
    assert len(table) == 0, "Table should be empty"
    table["key1"] = 1
    assert len(table) == 1, "Added one element"
    table["key2"] = 2
    table["key3"] = 3
    assert len(table) == 3, "Added three elements"
    time.sleep(3)
    assert len(table) == 0, "All keys should expire"
    table["key1"] = 1
    time.sleep(1)
    table["key2"] = 2
    time.sleep(1.5)
    assert len(table) == 1, "One key expired and one exist"
    time.sleep(1)
    assert len(table) == 0, "All keys expired"

def test_cache_table_del():
    table = cache_table.CacheTable(2000)
    table["key1"] = 1
    time.sleep(1.5)
    del table["key1"]
    assert ("key1" in table) == False, "Key is not removed"
    table["key1"] = 2
    time.sleep(1)
    assert "key1" in table, "Expired using old expiration time"

def test_cache_table_per_entry():
    table = cache_table_per_entry.CacheTablePerEntry()
    table.set("a", 1, 2000)
    table.set("b", 2, 1000)
    time.sleep(1.5)
    assert table.exists("a"), "a not expired"
    assert not table.exists("b"), "b expired"
