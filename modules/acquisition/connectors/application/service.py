"""Application services for connector use cases.

Application services orchestrate connector-related workflows.

Responsibilities:
- Receive connector commands or requests.
- Coordinate domain entities and value objects.
- Use domain repository contracts.
- Invoke appropriate connector abstractions.
- Coordinate the sequence of operations required by a use case.
- Translate domain/application results into appropriate responses.

Application services must not become a container for business rules.

They must not:
- directly implement domain invariants
- directly depend on provider SDKs
- contain database implementation
- contain HTTP framework code
- contain CLI presentation logic

Provider-specific behaviour belongs in infrastructure.

Business rules belong in the domain layer.
"""
