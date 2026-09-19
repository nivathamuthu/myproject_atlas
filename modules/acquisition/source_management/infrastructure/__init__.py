"""Infrastructure layer for Source Management.

The infrastructure layer contains technical implementations required
to persist and integrate acquisition source information.

Responsibilities may include:
- database persistence
- ORM mappings
- configuration persistence
- external source metadata integrations
- credential-reference integrations
- provider-specific source configuration

Infrastructure may depend on:
- database libraries
- ORM libraries
- cloud SDKs
- external service clients
- filesystem APIs
- configuration systems

Infrastructure must implement the contracts expected by the
application and domain layers.

Technical details must not leak into domain business logic.
"""
