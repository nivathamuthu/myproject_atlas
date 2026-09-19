"""Domain-specific exceptions for the Crawler module.

This module contains exceptions representing business-level failures
within the crawler domain.

Potential examples include:
- invalid crawl state
- invalid crawl configuration
- invalid crawl target
- unsupported crawl operation
- invalid lifecycle transition
- crawl domain invariant violation

Exceptions should describe business meaning rather than technical
implementation details.

Technical failures such as HTTP errors, browser failures, network
timeouts, or provider-specific exceptions belong to infrastructure.

Infrastructure errors may be translated into appropriate
application or domain-level errors where necessary.
"""
