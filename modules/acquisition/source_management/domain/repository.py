"""Repository contracts for Source Management.

This module defines persistence abstractions required by the source
management domain and application layers.

The repository is a contract, not a database implementation.

Responsibilities:
- Define operations for registering sources.
- Define operations for retrieving sources.
- Define operations for updating sources.
- Define operations for changing source status.
- Define operations for managing source ownership.
- Define operations for storing source configuration.
- Define operations for retrieving source policies.

The implementation belongs in:

    infrastructure/repository.py

This module must not depend on:
- PostgreSQL
- SQLAlchemy
- MongoDB
- Redis
- database-specific query syntax
- ORM-specific implementation details

Dependency direction:

    Application / Domain
            |
            v
    Repository Contract
            ^
            |
    Infrastructure Implementation
"""
