from system_design_labs.mini_lsm import MiniLSM


def test_reads_newest_value_across_memtable_and_sstables():
    lsm = MiniLSM(flush_threshold=2)
    lsm.put("a", "1")
    lsm.put("b", "2")
    lsm.put("a", "3")

    assert lsm.get("a") == "3"
    assert len(lsm.sstables) == 1


def test_delete_tombstone_hides_old_value_after_flush():
    lsm = MiniLSM(flush_threshold=1)
    lsm.put("a", "1")
    lsm.delete("a")

    assert lsm.get("a") is None


def test_compaction_keeps_newest_live_values():
    lsm = MiniLSM(flush_threshold=1)
    lsm.put("a", "1")
    lsm.put("a", "2")
    lsm.delete("b")

    lsm.compact()

    assert lsm.sstables == [{"a": "2"}]
