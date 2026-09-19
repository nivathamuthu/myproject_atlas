"""Infrastructure storage and configuration support for Source Management.

This module contains technical storage implementations required for
source-related configuration and acquisition metadata.

Potential responsibilities include:
- storing source configuration
- retrieving source configuration
- storing source metadata
- managing credential references
- integrating with configuration stores
- integrating with secret-management systems
- handling provider-specific configuration storage

This module must not perform the actual acquisition of content.

It must not implement:
- web crawling
- file uploading
- bulk importing
- document parsing
- OCR
- normalization
- chunking
- embeddings
- knowledge graph construction
- vector indexing
- retrieval

Actual acquisition belongs to the appropriate acquisition module.

Sensitive credentials must not be stored directly in source entities
or committed to the repository. Use appropriate secret-management
abstractions and store references where required.
"""
