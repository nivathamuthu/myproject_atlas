"""Domain layer for the Crawler module.

The domain layer contains the core business concepts and rules
associated with crawling in Project Atlas.

This layer may contain:
- crawl entities
- crawl value objects
- repository contracts
- crawl domain exceptions
- crawl business rules
- crawl lifecycle rules

The domain must remain independent from infrastructure technologies.

It must not directly depend on:
- HTTP clients
- browser automation libraries
- web scraping frameworks
- database libraries
- cloud SDKs
- filesystem implementations
- external service clients

The domain describes what a crawl means to Project Atlas,
not how a particular crawling technology performs it.
"""
