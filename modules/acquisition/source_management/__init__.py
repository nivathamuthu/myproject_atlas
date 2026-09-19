"""Source Management module for Project Atlas.

This module manages the lifecycle and configuration of sources from
which Project Atlas may acquire content.

Responsibilities:
- Register acquisition sources.
- Maintain source configuration.
- Manage source lifecycle and status.
- Manage source ownership and project association.
- Maintain acquisition policies and settings.
- Provide source information to acquisition workflows.

This module defines WHAT acquisition sources exist and HOW they are
configured.

It does not perform the actual acquisition of content.

Actual acquisition belongs to modules such as:
- file_upload
- bulk_import
- connectors
- crawler

This module must not implement:
- file parsing
- OCR
- document normalization
- web crawling
- connector-specific communication
- chunking
- embeddings
- knowledge graph construction
- vector indexing
- retrieval
"""
