"""Value objects for the Source Management domain.

Value objects represent source concepts defined by their values rather
than independent identity.

Potential examples include:
- SourceId
- SourceName
- SourceType
- SourceStatus
- SourceUri
- SourceConfiguration
- SourceOwner
- ProjectId
- AcquisitionPolicy
- SourceSchedule
- CredentialReference

Value objects should:
- express meaningful domain concepts
- validate domain-level constraints
- be immutable where appropriate
- prevent invalid source configuration
- remain independent from infrastructure technologies

Do not place:
- ORM types
- database-specific types
- HTTP request objects
- provider SDK objects
- API framework models

in this module.
"""
