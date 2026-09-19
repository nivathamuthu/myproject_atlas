"""Commands for the Crawler application layer.

Commands represent requests that initiate or change crawler
operations.

Potential examples:
- create a crawl job
- start a crawl
- pause a crawl
- resume a crawl
- cancel a crawl
- schedule a crawl
- retry a failed crawl
- register a crawl source

Responsibilities:
- Represent application intent.
- Define the input required for state-changing operations.
- Remain independent from crawling technologies.
- Remain independent from HTTP and CLI frameworks.

Commands must not:
- directly perform HTTP requests
- directly control browsers
- access databases directly
- contain provider-specific implementation
- contain document processing logic

Execution is coordinated by application services.
"""
