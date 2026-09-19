"""Application services for crawler use cases.

Application services orchestrate crawler-related workflows.

Responsibilities:
- Coordinate crawler commands.
- Coordinate domain entities and value objects.
- Invoke crawler abstractions.
- Manage crawl job lifecycle workflows.
- Coordinate persistence through repository contracts.
- Coordinate delivery of acquired content to downstream processing.

Application services must not become a container for low-level
crawling implementation.

They must not:
- implement HTTP clients
- implement browser automation
- contain database implementation
- contain document parsing
- contain OCR
- contain chunking or embedding logic
- contain API presentation logic

Technical implementations belong in infrastructure.
Business rules belong in the domain layer.
"""
