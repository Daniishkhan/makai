from threading import Barrier, Thread

from system_design_labs.concurrent_withdrawal import Account


def test_naive_withdraw_allows_two_successes_from_one_balance():
    account = Account(100)
    barrier = Barrier(2)
    results: list[bool] = []

    threads = [
        Thread(target=lambda: results.append(account.naive_withdraw(80, barrier))),
        Thread(target=lambda: results.append(account.naive_withdraw(80, barrier))),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results == [True, True]
    assert account.balance_cents == 20


def test_locked_withdraw_preserves_the_invariant():
    account = Account(100)
    results: list[bool] = []

    threads = [
        Thread(target=lambda: results.append(account.locked_withdraw(80))),
        Thread(target=lambda: results.append(account.locked_withdraw(80))),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert sorted(results) == [False, True]
    assert account.balance_cents == 20
