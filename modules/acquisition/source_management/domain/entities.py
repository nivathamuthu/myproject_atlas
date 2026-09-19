"""Domain entities for Source Management.

Entities represent business objects that have identity and lifecycle
within the source management domain.

Potential entities may include:
- AcquisitionSource
- SourceConfiguration
- SourceOwnership
- SourceRegistration

The exact entities should be determined during domain modelling.

Entities are responsible for:
- maintaining meaningful domain state
- enforcing source-related invariants
- representing business identity
- managing source lifecycle
- providing domain behaviour
- maintaining valid source state transitions

Entities must not contain:
- database ORM objects
- HTTP clients
- crawler objects
- connector SDK objects
- API framework models
- cloud provider objects
- infrastructure configuration

Technical implementations belong in infrastructure.
"""
