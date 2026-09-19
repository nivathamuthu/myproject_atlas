"""Commands for the Source Management application layer.

Commands represent state-changing requests related to acquisition
sources.

Potential examples:
- register a source
- update a source
- enable a source
- disable a source
- archive a source
- activate a source
- update source configuration
- assign a source to a project
- update source acquisition policy

Responsibilities:
- Represent application intent.
- Define input required for state-changing operations.
- Remain independent from infrastructure technologies.
- Express operations in application/domain language.

Commands must not:
- directly access databases
- perform HTTP requests
- perform crawling
- upload files
- call provider SDKs
- parse documents
- perform OCR
- perform downstream knowledge engineering

Execution is coordinated by application services.
"""
