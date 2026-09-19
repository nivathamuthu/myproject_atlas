"""Infrastructure layer for the Connectors module.

The infrastructure layer contains technical implementations used by
the Connectors application and domain layers.

Responsibilities may include:
- external-system integrations
- provider-specific connector implementations
- persistence implementations
- network clients
- authentication with external sources
- source-specific data acquisition

Infrastructure may depend on:
- provider SDKs
- HTTP clients
- database libraries
- filesystem APIs
- external service clients

Infrastructure must implement the contracts expected by the
application and domain layers.

Provider-specific details must not leak into domain business logic.
"""
