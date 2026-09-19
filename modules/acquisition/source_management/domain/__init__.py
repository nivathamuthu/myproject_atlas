"""Domain layer for the Source Management module.

The domain layer contains the core business concepts and rules
associated with acquisition sources.

This layer may contain:
- source entities
- source value objects
- repository contracts
- source domain exceptions
- source lifecycle rules
- source configuration rules
- source ownership rules
- acquisition policy rules

The domain must remain independent from infrastructure technologies.

It must not directly depend on:
- databases
- ORM libraries
- HTTP clients
- crawler frameworks
- connector SDKs
- cloud SDKs
- filesystem implementations
- API frameworks

The domain describes what an acquisition source means to Project
Atlas, not how a particular technology stores or communicates with it.
"""
