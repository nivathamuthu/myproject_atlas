"""Repository contracts for the Crawler domain.

This module defines persistence abstractions required by the
Crawler domain and application layers.

The repository is a contract, not a database implementation.

Responsibilities:
- Define operations required to store crawl jobs.
- Define operations required to retrieve crawl jobs.
- Define operations required to update crawl state.
- Define operations required to persist crawl metadata.
- Express persistence requirements using domain language.

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
