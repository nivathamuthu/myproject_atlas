"""
Application layer for the Project Atlas file upload module.

This layer coordinates file upload use cases.

Application code may:
- receive commands from API, CLI, worker, or other entry points
- orchestrate domain objects and domain rules
- use repository and storage abstractions
- coordinate events for downstream processing

Application code must not contain:
- HTTP or FastAPI route definitions
- database-specific implementation details
- object-storage-provider-specific implementation details
- core business rules that belong to the domain layer
"""
