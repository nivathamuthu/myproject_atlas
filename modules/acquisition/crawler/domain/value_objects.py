"""Value objects for the Crawler domain.

Value objects represent crawler concepts that are defined by their
values rather than independent identity.

Potential examples include:
- CrawlJobId
- CrawlSourceId
- CrawlTarget
- CrawlUrl
- CrawlDepth
- CrawlStatus
- CrawlPriority
- CrawlConfiguration
- CrawlSchedule

Value objects should:
- express meaningful domain concepts
- validate domain-level constraints
- be immutable where appropriate
- remain independent from infrastructure technologies

Do not place:
- HTTP request objects
- browser objects
- database types
- ORM objects
- scraping framework objects
- provider-specific objects

in this module.
"""
