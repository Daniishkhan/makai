from threading import Barrier, Thread
import time

from system_design_labs.cache_stampede import CacheAside


def test_single_flight_protects_cache_miss():
    cache = CacheAside(ttl_seconds=10)
    barrier = Barrier(3)
    calls = 0
    results: list[str] = []

    def loader() -> str:
        nonlocal calls
        calls += 1
        time.sleep(0.02)
        return "profile"

    def worker() -> None:
        barrier.wait()
        results.append(cache.get("user:1", now=0, loader=loader))

    threads = [Thread(target=worker) for _ in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results == ["profile", "profile", "profile"]
    assert calls == 1


def test_expired_entry_reloads():
    cache = CacheAside(ttl_seconds=5)
    calls = 0

    def loader() -> str:
        nonlocal calls
        calls += 1
        return f"value-{calls}"

    assert cache.get("key", now=0, loader=loader) == "value-1"
    assert cache.get("key", now=6, loader=loader) == "value-2"
