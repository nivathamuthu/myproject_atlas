"""Domain layer for the Connectors module.

The domain layer contains the core business concepts and rules
associated with external connectors in Project Atlas.

This layer may contain:
- connector entities
- connector value objects
- repository contracts
- connector domain exceptions
- connector business rules

The domain must remain independent from infrastructure technologies.

It must not directly depend on:
- cloud-provider SDKs
- HTTP clients
- database libraries
- filesystem implementations
- external API clients
- message brokers
- authentication provider SDKs

The domain describes what a connector means to Project Atlas,
not how a specific external system implements it.
"""
