#!/usr/bin/env bash
set -euo pipefail

echo "📝 Setting up logging..."

pip install structlog

cat > logging_config.py << 'PY'
import structlog

def configure_logging():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

# Usage
configure_logging()
logger = structlog.get_logger()
logger.info("application_started", version="1.0")
PY

echo "✅ Logging configured in logging_config.py"
