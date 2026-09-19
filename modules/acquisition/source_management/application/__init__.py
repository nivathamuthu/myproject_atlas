"""Application layer for the Source Management module.

The application layer coordinates source management use cases.

Responsibilities:
- Define source management commands and queries.
- Coordinate source domain objects.
- Orchestrate source lifecycle operations.
- Coordinate repository access through domain contracts.
- Validate application-level requests.
- Coordinate interactions with acquisition workflows.

The application layer must not contain:
- database-specific implementation
- provider SDK implementation
- web crawling implementation
- file parsing
- OCR
- document processing
- embedding logic
- API presentation logic

Infrastructure concerns belong in the infrastructure layer.
Source management business rules belong in the domain layer.
"""
