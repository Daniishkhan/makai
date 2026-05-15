from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    term: int = 0
    voted_for: str | None = None
    log: list[str] = field(default_factory=list)
    online: bool = True


@dataclass
class ToyRaftCluster:
    nodes: dict[str, Node]
    leader_id: str | None = None
    commit_index: int = 0

    @classmethod
    def with_nodes(cls, node_ids: list[str]) -> "ToyRaftCluster":
        return cls(nodes={node_id: Node(node_id) for node_id in node_ids})

    def majority(self) -> int:
        return len(self.nodes) // 2 + 1

    def set_online(self, node_id: str, online: bool) -> None:
        self.nodes[node_id].online = online

    def elect_leader(self, candidate_id: str, term: int) -> bool:
        votes = 0
        for node in self.nodes.values():
            if not node.online:
                continue
            if term >= node.term and node.voted_for in (None, candidate_id):
                node.term = term
                node.voted_for = candidate_id
                votes += 1
        if votes >= self.majority():
            self.leader_id = candidate_id
            return True
        return False

    def append(self, command: str) -> bool:
        if self.leader_id is None:
            raise RuntimeError("no leader")
        leader = self.nodes[self.leader_id]
        if not leader.online:
            raise RuntimeError("leader is offline")

        replicated = 0
        for node in self.nodes.values():
            if node.online:
                node.log.append(command)
                replicated += 1
        if replicated >= self.majority():
            self.commit_index += 1
            return True
        return False
