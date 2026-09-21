import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from data.rule_engine import RuleEngine


_rule_engine = RuleEngine()


def recommend_learning_resources(*args, **kwargs):
    """Compatibility wrapper for callers using the former backend import."""
    return _rule_engine.recommend_learning_resources(*args, **kwargs)