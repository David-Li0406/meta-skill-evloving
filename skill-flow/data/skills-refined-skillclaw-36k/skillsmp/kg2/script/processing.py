"""Common processing loop utilities for enrichment and linking."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from .db import Database
    from .models import PaperRow

logger = logging.getLogger(__name__)


def iter_papers(
    db: Database,
    claim_fn: Callable[[], PaperRow | None],
    next_fn: Callable[[], PaperRow | None],
    reset_stale_fn: Callable[[], int],
    parallel: bool,
    watch: bool,
    poll_interval: int,
    max_papers: int | None,
    log_waiting_msg: str,
) -> Iterator[PaperRow]:
    """Iterate over papers for processing.

    Handles:
    - Parallel vs single-process paper acquisition
    - Watch mode polling
    - Stale claim reset at startup
    - max_papers limit

    Args:
        db: Database connection
        claim_fn: Atomic claim function for parallel mode (e.g., db.claim_unenriched_paper)
        next_fn: Simple query function for single mode (e.g., db.next_unenriched_paper)
        reset_stale_fn: Function to reset stale claims (e.g., db.reset_stale_enrichment)
        parallel: Use atomic claims for multi-worker mode
        watch: Poll for new papers instead of exiting when queue empty
        poll_interval: Seconds between polls when watching
        max_papers: Maximum papers to yield (None = unlimited)
        log_waiting_msg: Message to log when waiting for papers

    Yields:
        PaperRow objects to process
    """
    yielded = 0

    # Reset stale claims at startup when running in parallel
    if parallel:
        stale = reset_stale_fn()
        if stale > 0:
            logger.info("Reset %d stale claims", stale)
            db.commit()

    get_paper = claim_fn if parallel else next_fn

    while True:
        if max_papers and yielded >= max_papers:
            break

        row = get_paper()
        if not row:
            if watch:
                logger.info("%s (poll every %ds)", log_waiting_msg, poll_interval)
                time.sleep(poll_interval)
                continue
            break

        yield row
        yielded += 1
