"""External content acquisition implementation for the Crawler module.

This module contains technical implementations used to communicate
with crawlable external sources and retrieve their content.

Potential responsibilities include:
- HTTP requests
- connection management
- browser automation
- page retrieval
- response handling
- retry and timeout handling
- rate limiting
- source-specific crawling behaviour
- raw content retrieval

Provider-specific libraries and network implementations belong here.

This module should return data in a form that can be passed to the
appropriate application workflow.

It must not perform downstream processing such as:
- document parsing
- OCR
- normalization
- metadata enrichment
- chunking
- embeddings
- knowledge graph construction
- vector indexing

Those responsibilities belong to the appropriate downstream modules.

When multiple crawling technologies or providers are supported,
their implementations should remain isolated behind appropriate
abstractions.
"""
