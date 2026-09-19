"""Commands for the Connectors application layer.

Commands represent requests that may change connector state or
initiate connector operations.

Potential examples:
- register a connector
- enable a connector
- disable a connector
- trigger a connector synchronization
- remove a connector
- refresh connector credentials or configuration

Responsibilities:
- Define the input required for a state-changing operation.
- Represent application intent.
- Remain independent of external provider SDKs.
- Remain independent of HTTP and CLI frameworks.

Commands must not:
- contain provider-specific implementation
- access databases directly
- call external APIs directly
- contain presentation logic
- implement infrastructure behaviour

Business rules must be enforced by the domain layer.
"""
