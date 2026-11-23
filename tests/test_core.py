"""Tests for PromptTreePruner."""
import unittest
from agent_dynamic_prompt_tree_pruner.core import PromptTreePruner

class TestPromptTreePruner(unittest.TestCase):
    def test_prune_low_utility(self):
        p = PromptTreePruner("root", "Initial goal")
        p.add_node("good", "Good step", "root", utility_score=0.9)
        p.add_node("bad", "Bad step", "root", utility_score=0.2)
        p.add_node("bad_child", "Child of bad", "bad", utility_score=0.1)

        pruned = p.prune_branches(min_utility=0.5)
        self.assertEqual(pruned, 1) # bad node triggers subtree
        ctx = p.render_linear_context()
        self.assertIn("Good step", ctx)
        self.assertNotIn("Bad step", ctx)
        self.assertNotIn("Child of bad", ctx)
