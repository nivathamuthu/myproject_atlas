"""Crawler module for Project Atlas.

This module is responsible for acquiring content from crawlable
external sources.

Responsibilities:
- Discover crawlable resources.
- Fetch content from permitted sources.
- Manage crawl-related application workflows.
- Represent crawler concepts and rules.
- Provide abstractions for crawl infrastructure.

Crawler output should be handed to the appropriate downstream
processing workflow.

This module must not implement:
- document parsing
- OCR
- normalization
- metadata enrichment
- chunking
- embeddings
- knowledge graph construction
- vector indexing
- retrieval
- API presentation logic

Those responsibilities belong to downstream modules or applications.
"""
