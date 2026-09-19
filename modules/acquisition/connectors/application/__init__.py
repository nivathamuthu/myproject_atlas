"""Application layer for the Connectors module.

The application layer coordinates connector-related use cases.

Responsibilities:
- Define application commands and queries.
- Coordinate connector domain objects.
- Invoke connector abstractions and repository contracts.
- Orchestrate connector operations.
- Return application-level results.

The application layer must not contain:
- provider-specific SDK implementation
- database-specific implementation
- HTTP framework logic
- CLI presentation logic
- low-level network implementation
- core connector business rules

Business rules belong in the domain layer.

External technology implementations belong in the infrastructure layer.
"""
