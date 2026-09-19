"""Application layer for the Crawler module.

The application layer coordinates crawler use cases.

Responsibilities:
- Define crawler commands and queries.
- Coordinate crawler domain objects.
- Orchestrate crawl operations.
- Invoke crawler abstractions.
- Coordinate persistence where required.
- Return application-level results.

The application layer must not contain:
- HTTP client implementation
- browser automation implementation
- provider-specific crawling libraries
- database-specific implementation
- document parsing logic
- OCR logic
- embedding logic
- presentation logic

Infrastructure concerns belong in the infrastructure layer.
Core crawler business rules belong in the domain layer.
"""
