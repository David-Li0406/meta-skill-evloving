"""Allow ``python -m benchmark.AgentSkillOS_bench.ranking`` as an alias for ``python -m benchmark.AgentSkillOS_bench.ranking.rank``."""
from .rank import main
import sys

sys.exit(main())
