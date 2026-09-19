"""Repository contracts for the Connectors domain.

This module defines the persistence abstractions required by the
Connectors domain and application layers.

The repository is a contract, not a database implementation.

Responsibilities:
- Define operations required to store connector information.
- Define operations required to retrieve connector information.
- Express persistence requirements in domain language.
- Keep the domain independent of database technology.

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
