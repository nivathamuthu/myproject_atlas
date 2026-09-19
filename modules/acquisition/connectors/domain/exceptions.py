"""Domain-specific exceptions for Connectors.

This module contains exceptions representing business-level failures
within the Connectors domain.

Potential examples include:
- invalid connector state
- invalid connector configuration
- unsupported connector type
- invalid connector lifecycle transition
- connector domain invariant violation

Exceptions should describe business meaning rather than technical
implementation details.

Provider-specific or infrastructure-specific failures should remain
in the infrastructure layer and be translated into appropriate
application or domain-level errors where necessary.
"""
