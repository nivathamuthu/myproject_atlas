"""Infrastructure layer for the Crawler module.

The infrastructure layer contains technical implementations required
to perform crawling and persist crawler state.

Responsibilities may include:
- HTTP clients
- web crawling libraries
- browser automation
- robots.txt handling
- rate limiting implementation
- retry mechanisms
- external-source communication
- persistence implementations
- provider-specific integrations

Infrastructure may depend on:
- HTTP libraries
- browser automation libraries
- scraping frameworks
- database libraries
- external SDKs
- filesystem APIs

Infrastructure must implement the contracts expected by the
application and domain layers.

Technical details must not leak into domain business logic.
"""
