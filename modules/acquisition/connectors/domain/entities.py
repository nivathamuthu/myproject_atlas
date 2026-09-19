"""Domain entities for Connectors.

Entities represent business objects within the connector domain.

Potential entities may include:
- Connector
- ConnectorConfiguration
- ConnectorSource
- ConnectorSynchronization

The exact entities should be determined by the connector requirements
and domain model during implementation.

Entities are responsible for:
- maintaining meaningful domain state
- enforcing connector-related invariants
- providing domain behaviour
- representing business identity

Entities must not contain:
- database ORM models
- provider SDK objects
- HTTP request/response models
- network implementation
- external service clients

Persistence and provider-specific representations belong in infrastructure.
"""
