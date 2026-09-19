"""Queries for the Crawler application layer.

Queries represent read-only requests related to crawler state,
crawl jobs, sources, and crawl results.

Potential examples:
- retrieve crawl job details
- list crawl jobs
- retrieve crawl status
- retrieve crawl source configuration
- retrieve crawl statistics
- retrieve crawl history

Responsibilities:
- Define read-only application requests.
- Coordinate retrieval through appropriate abstractions.
- Return application-level information.

Queries must not:
- change crawler state
- directly perform crawling
- directly access provider SDKs
- contain database-specific implementation
- contain presentation logic
"""
