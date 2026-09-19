"""Domain entities for the Crawler module.

Entities represent business objects within the crawler domain.

Potential entities may include:
- CrawlJob
- CrawlSource
- CrawlTarget
- CrawlResult
- CrawlSchedule

The exact entities should be determined during domain modelling.

Entities are responsible for:
- maintaining meaningful domain state
- enforcing crawler-related invariants
- representing business identity
- providing domain behaviour
- managing valid lifecycle transitions

Entities must not contain:
- HTTP client objects
- browser instances
- scraping framework objects
- database ORM models
- API framework models
- provider-specific SDK objects

Technical implementations belong in infrastructure.
"""
