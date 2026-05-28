"""Entry point: ``python -m benchmark`` forwards to ranking CLI."""

import sys

from benchmark.AgentSkillOS_bench.ranking.rank import main

sys.exit(main())
