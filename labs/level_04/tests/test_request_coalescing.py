from threading import Barrier, Thread
import time

from system_design_labs.request_coalescing import RequestCoalescer


def test_collapses_identical_in_flight_requests():
    coalescer = RequestCoalescer()
    barrier = Barrier(3)
    calls = 0
    results: list[str] = []

    def loader() -> str:
        nonlocal calls
        calls += 1
        time.sleep(0.02)
        return "value"

    def worker() -> None:
        barrier.wait()
        results.append(coalescer.get("cache-key", loader))

    threads = [Thread(target=worker) for _ in range(3)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results == ["value", "value", "value"]
    assert calls == 1
