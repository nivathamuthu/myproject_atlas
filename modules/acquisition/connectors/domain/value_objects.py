"""Value objects for the Connectors domain.

Value objects represent connector concepts that are defined by their
values rather than by independent identity.

Potential examples include:
- ConnectorId
- ConnectorType
- ConnectorName
- ConnectorStatus
- SourceIdentifier
- ConnectorConfiguration values

Value objects should:
- express meaningful domain concepts
- validate domain-level constraints
- be immutable where appropriate
- remain independent from infrastructure

Do not place:
- database-specific types
- ORM objects
- provider SDK objects
- HTTP models
- external API response models

in this module.
"""
