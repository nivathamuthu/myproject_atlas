"""Domain-specific exceptions for Source Management.

This module contains exceptions representing business-level failures
within the source management domain.

Potential examples include:
- source already exists
- source not found
- invalid source configuration
- invalid source type
- invalid source status transition
- source ownership violation
- unsupported acquisition policy
- invalid source lifecycle operation

Exceptions should describe business meaning rather than technical
implementation details.

Technical failures such as database errors, network failures, provider
errors, or SDK-specific exceptions belong to infrastructure.

Infrastructure errors may be translated into appropriate application
or domain-level errors where necessary.
"""
