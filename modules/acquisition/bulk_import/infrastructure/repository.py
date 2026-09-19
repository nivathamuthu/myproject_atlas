"""Persistence implementation for Bulk Import repositories.

This module contains the infrastructure implementation of the
repository contract defined in:

    domain/repository.py

Responsibilities:
- Persist Bulk Import domain information.
- Retrieve Bulk Import information.
- Translate between persistence representations and domain objects.
- Handle database-specific concerns.

Database-specific code belongs here.

Examples may include:
- ORM models
- SQL queries
- database sessions
- transaction handling
- persistence mappings

Do not move database-specific implementation into the domain layer.

The infrastructure repository should satisfy the domain repository
contract rather than changing the domain to accommodate a database.
"""
