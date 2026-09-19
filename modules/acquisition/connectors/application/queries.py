"""Queries for the Connectors application layer.

Queries represent read-only requests related to configured connectors
and their acquisition status.

Potential examples:
- retrieve connector details
- list configured connectors
- retrieve connector status
- retrieve synchronization information
- retrieve connector health information

Responsibilities:
- Define read-only application requests.
- Coordinate retrieval through appropriate abstractions.
- Return application-level information.

Queries must not:
- change connector state
- directly access provider SDKs
- contain database-specific implementation
- contain HTTP endpoint logic
- contain CLI presentation logic
"""
