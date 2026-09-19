"""Bulk Import module.

This module handles importing multiple documents or files into Project Atlas.

Responsibilities:
- Coordinate bulk document/file import operations.
- Represent the entry point for the Bulk Import bounded context.
- Provide the package boundary for Bulk Import functionality.

The module must remain focused on bulk import concerns.

Do not place:
- HTTP/API handlers
- CLI commands
- Database-specific implementation
- Storage-provider SDK code
- Document parsing or processing logic
- Knowledge-engineering logic

Those concerns belong to their appropriate modules or layers.
"""
