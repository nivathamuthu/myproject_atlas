"""Queries for the Source Management application layer.

Queries represent read-only requests concerning acquisition sources.

Potential examples:
- retrieve a source
- list project sources
- list active sources
- retrieve source configuration
- retrieve source status
- retrieve source ownership
- retrieve source acquisition policy
- search registered sources

Responsibilities:
- Define read-only application requests.
- Retrieve source information through repository abstractions.
- Return application-level information.

Queries must not:
- change source state
- perform acquisition
- perform crawling
- directly access provider SDKs
- contain database-specific implementation
- contain presentation logic
"""
