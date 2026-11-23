"""Core Prompt Tree Pruner implementation."""
from typing import Dict, List, Optional

class TreeNode:
    def __init__(self, node_id: str, content: str, parent_id: Optional[str] = None, utility_score: float = 1.0):
        self.node_id = node_id
        self.content = content
        self.parent_id = parent_id
        self.utility_score = utility_score
        self.children: List[str] = []
        self.pruned = False

class PromptTreePruner:
    def __init__(self, root_id: str, root_content: str):
        self.nodes: Dict[str, TreeNode] = {
            root_id: TreeNode(root_id, root_content, utility_score=1.0)
        }
        self.root_id = root_id

    def add_node(self, node_id: str, content: str, parent_id: str, utility_score: float = 1.0) -> TreeNode:
        if parent_id not in self.nodes:
            raise KeyError(f"Parent {parent_id} does not exist")
        node = TreeNode(node_id, content, parent_id, utility_score)
        self.nodes[node_id] = node
        self.nodes[parent_id].children.append(node_id)
        return node

    def prune_branches(self, min_utility: float = 0.4) -> int:
        pruned_count = 0
        for node_id, node in list(self.nodes.items()):
            if node_id != self.root_id and not node.pruned and node.utility_score < min_utility:
                node.pruned = True
                pruned_count += 1
                self._prune_subtree(node)
        return pruned_count

    def _prune_subtree(self, node: TreeNode):
        for child_id in node.children:
            if child_id in self.nodes:
                self.nodes[child_id].pruned = True
                self._prune_subtree(self.nodes[child_id])

    def render_linear_context(self) -> List[str]:
        result = []
        def dfs(curr_id: str):
            node = self.nodes[curr_id]
            if not node.pruned:
                result.append(node.content)
                for cid in node.children:
                    dfs(cid)
        dfs(self.root_id)
        return result
