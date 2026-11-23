"""CLI for Agent Dynamic Prompt Tree Pruner."""
import argparse
from .core import PromptTreePruner

def main():
    parser = argparse.ArgumentParser(description="Agent Dynamic Prompt Tree Pruner CLI")
    parser.add_argument("--demo", action="store_true", help="Run prompt pruning demonstration")
    args = parser.parse_args()

    pruner = PromptTreePruner("root", "User: Deploy payment gateway.")
    pruner.add_node("step1", "Agent: Trying deprecated API v1.", "root", utility_score=0.2)
    pruner.add_node("step1_err", "Error: 410 Gone.", "step1", utility_score=0.1)
    pruner.add_node("step2", "Agent: Migrating to API v2 with webhook verification.", "root", utility_score=0.95)
    pruner.add_node("step2_ok", "Payment gateway deployed successfully.", "step2", utility_score=1.0)

    print("Before Pruning Context Items:", len(pruner.render_linear_context()))
    pruned = pruner.prune_branches(min_utility=0.5)
    print(f"Pruned {pruned} low-utility nodes.")
    print("Cleaned Linear Context:")
    for line in pruner.render_linear_context():
        print(f"  * {line}")

if __name__ == "__main__":
    main()
