"""Connectors module for Project Atlas.

This module manages connections to external data sources and systems
that can provide documents or other acquisition inputs to Project Atlas.

Responsibilities:
- Define the connector bounded context.
- Coordinate external-source acquisition through application use cases.
- Provide a consistent architectural boundary around external connectors.

The module may later support connectors for:
- cloud storage systems
- enterprise document systems
- external APIs
- repositories
- other supported data sources

Do not place:
- HTTP API endpoints
- CLI presentation logic
- provider SDK implementation
- database-specific code
- document parsing logic
- OCR logic
- chunking or embedding logic

Those concerns belong in their appropriate applications, modules, or layers.
"""
