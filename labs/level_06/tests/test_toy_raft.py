from system_design_labs.toy_raft import ToyRaftCluster


def test_elects_leader_with_majority_vote():
    cluster = ToyRaftCluster.with_nodes(["a", "b", "c"])

    assert cluster.elect_leader("a", term=1)
    assert cluster.leader_id == "a"


def test_commits_entry_when_replicated_to_majority():
    cluster = ToyRaftCluster.with_nodes(["a", "b", "c"])
    cluster.elect_leader("a", term=1)

    assert cluster.append("set x=1")
    assert cluster.commit_index == 1
    assert cluster.nodes["b"].log == ["set x=1"]


def test_does_not_commit_without_majority():
    cluster = ToyRaftCluster.with_nodes(["a", "b", "c"])
    cluster.elect_leader("a", term=1)
    cluster.set_online("b", False)
    cluster.set_online("c", False)

    assert not cluster.append("set x=1")
    assert cluster.commit_index == 0
