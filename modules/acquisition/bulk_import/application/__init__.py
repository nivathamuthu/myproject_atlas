"""Application layer for the Bulk Import module.

The application layer coordinates Bulk Import use cases.

Responsibilities:
- Define application-level commands and queries.
- Coordinate domain objects and domain services.
- Call repository and infrastructure abstractions through defined contracts.
- Control the flow of a Bulk Import use case.

The application layer must not contain:
- Core business rules
- Database-specific implementation
- Storage-provider SDK code
- HTTP framework code
- Provider-specific infrastructure logic

Business rules belong in the domain layer.
"""
