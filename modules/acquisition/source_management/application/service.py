"""Application services for Source Management use cases.

Application services coordinate source management workflows.

Responsibilities:
- Register acquisition sources.
- Update source configuration.
- Manage source lifecycle.
- Coordinate source ownership and project association.
- Coordinate repository operations.
- Enforce application-level workflow rules.
- Provide source information to acquisition processes.

Application services must not become a container for infrastructure
implementation.

They must not:
- implement database access
- implement web crawling
- implement connector clients
- upload files
- parse documents
- perform OCR
- generate embeddings
- build knowledge graphs
- implement API presentation logic

Technical implementations belong in infrastructure.
Core source management rules belong in the domain layer.
"""
