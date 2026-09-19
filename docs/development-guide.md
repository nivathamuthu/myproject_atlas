# Project Atlas Development Guide

## 1. Purpose

This document defines the development rules for Project Atlas.

The goal is to ensure that every developer follows the same architecture, coding standards, module boundaries, testing strategy, and Git workflow.

Developers must read this document and `docs/architecture.md` before implementing a new module or feature.

---

# 2. Core Development Principle

Project Atlas uses a modular layered architecture.

The primary rule is:

> Business logic must not depend directly on infrastructure technologies.

Business rules belong in the domain layer.

Use cases belong in the application layer.

External technologies belong in the infrastructure layer.

Provider-specific implementations belong behind provider interfaces.

---

# 3. Repository Structure

The main repository structure is:

```text
project-atlas/
│
├── apps/
│   ├── api/
│   ├── cli/
│   ├── web/
│   └── worker/
│
├── core/
│   ├── config/
│   ├── database/
│   ├── errors/
│   ├── events/
│   ├── llm/
│   ├── logging/
│   ├── security/
│   ├── storage/
│   └── types/
│
├── modules/
│   ├── acquisition/
│   ├── audit/
│   ├── authentication/
│   ├── evaluation/
│   ├── knowledge_engineering/
│   ├── monitoring/
│   ├── processing/
│   ├── project_management/
│   └── retrieval/
│
├── workflows/
│   ├── document_ingestion/
│   ├── document_processing/
│   ├── knowledge_pipeline/
│   └── reprocessing/
│
├── infrastructure/
├── tests/
├── docs/
└── scripts/
```
This structure is intentional.

Developers should not create arbitrary top-level folders without an architectural reason.

---

# 4. Layered Module Structure

Most business modules should follow this structure:

modules/
└── module/
    ├── application/
    ├── domain/
    └── infrastructure/
    If a module requires multiple interchangeable external providers, it may also contain:

modules/
└── module/
    ├── application/
    ├── domain/
    ├── infrastructure/
    └── providers/

The exact structure may vary slightly depending on the responsibility of the module, but the dependency direction must remain consistent.

---

# 5. Domain Layer

Location:

modules/<module>/domain/

The domain layer contains business concepts and business rules.

Examples include:

entities
value objects
domain services
domain rules
domain exceptions
repository interfaces
provider interfaces
business policies

Example:

modules/processing/validation/domain/
├── entities.py
├── exceptions.py
├── repositories.py
└── services.py

The domain layer should remain independent of infrastructure technologies whenever practical.

The domain layer should NOT directly depend on:

FastAPI
PostgreSQL
SQLAlchemy
Qdrant
Neo4j
Kafka
Temporal
MinIO
cloud SDKs
HTTP clients
specific LLM providers
specific embedding providers

For example, do not write business rules that directly execute a Qdrant query.

Instead, define an interface and let infrastructure implement it.

# 6. Application Layer

Location:

modules/<module>/application/

The application layer contains use cases and application orchestration.

The application layer coordinates domain objects, repositories, providers, and other required services.

Typical responsibilities include:

Receive input.
Validate application-level requirements.
Call domain logic.
Coordinate repositories.
Coordinate providers.
Publish events when required.
Return application results.

Examples:

UploadDocumentUseCase
ValidateDocumentUseCase
ProcessDocumentUseCase
CreateEmbeddingUseCase
SearchKnowledgeUseCase
CreateProjectUseCase

Example structure:

modules/acquisition/file_upload/application/
├── commands.py
├── dto.py
└── use_cases.py

The application layer should not contain HTTP-specific logic.

For example, an application use case should not return JSONResponse.

# 7. Infrastructure Layer

Location:

modules/<module>/infrastructure/

The infrastructure layer contains implementations that communicate with external systems.

Examples include:

PostgreSQL repositories
SQL queries
Qdrant implementations
Neo4j implementations
Kafka publishers
Kafka consumers
MinIO storage adapters
external API clients
filesystem implementations
database adapters
provider implementations

Example:

modules/knowledge_engineering/vector_index/infrastructure/
├── qdrant_repository.py
└── qdrant_client.py

Infrastructure code may depend on external libraries and technologies.

The important rule is that infrastructure-specific dependencies should not leak unnecessarily into the domain layer.

# 8. Provider Layer

Some Atlas capabilities may have multiple implementations.

Examples:

OCR
embeddings
LLMs
document parsers
web crawlers
vector databases

For these cases, use provider abstractions.

Example:

modules/knowledge_engineering/embeddings/
├── application/
├── domain/
├── infrastructure/
└── providers/
    ├── local/
    └── ...

The application should depend on a stable provider contract rather than a specific provider.

For example:

EmbeddingProvider
       |
       +── LocalEmbeddingProvider
       |
       +── OtherEmbeddingProvider

This allows Atlas to change providers without rewriting the entire application.

# 9. Dependency Direction

The general dependency direction is:

Applications / API / Worker / CLI
              |
              v
        Application Layer
              |
              v
         Domain Layer
              ^
              |
      Infrastructure Layer

Infrastructure implements interfaces defined by inner layers where appropriate.

The domain layer should not import infrastructure implementations.

Avoid:

domain -> Qdrant
domain -> PostgreSQL
domain -> Kafka
domain -> Neo4j

Prefer:

domain
  |
  v
interface
  ^
  |
infrastructure implementation

# 10. Core Directory

The core/ directory contains cross-cutting capabilities shared by the platform.

Current areas include:

core/
├── config/
├── database/
├── errors/
├── events/
├── llm/
├── logging/
├── security/
├── storage/
└── types/

Examples:

core/config/

Application configuration and environment settings.

core/database/

Database connection foundations and shared database infrastructure.

core/errors/

Common application errors and error-handling primitives.

core/events/

Shared event contracts and event infrastructure.

core/llm/

Shared LLM abstractions where appropriate.

core/logging/

Centralized logging configuration.

core/security/

Cross-cutting security functionality.

core/storage/

Shared storage abstractions.

core/types/

Common types that are genuinely shared across multiple modules.

# 11. Core vs Modules

Use core/ for platform-wide concerns.

Use modules/ for business capabilities.

For example:

Authentication business logic
        ↓
modules/authentication/

while:

JWT configuration
password hashing utilities
security primitives
        ↓
core/security/

Do not place module-specific business logic into core/ simply because multiple modules currently use it.

A capability belongs in core/ only when it is genuinely cross-cutting.

# 12. Apps Directory

The apps/ directory contains executable application entry points.

apps/
├── api/
├── cli/
├── web/
└── worker/
apps/api/

Contains the FastAPI application.

Responsibilities include:

HTTP routing
request parsing
authentication dependencies
authorization dependencies
response mapping
API middleware
API configuration

API routes should remain thin.

Do not place complex business logic directly inside API routes.

# 13. Worker Application

apps/worker/ contains background worker entry points.

Workers may consume:

Kafka events
workflow tasks
background jobs

Workers should call application use cases and workflows rather than implementing large amounts of business logic directly.

# 14. CLI Application

apps/cli/ contains command-line functionality.

CLI commands should delegate to application services/use cases.

Do not duplicate business logic inside CLI commands.

# 15. Web Application

apps/web/ is reserved for the Atlas web application if one is implemented.

The web layer should communicate with backend APIs rather than directly accessing internal module infrastructure.

# 16. Workflows

The workflows/ directory contains long-running or multi-step orchestration.

Current workflows include:

workflows/
├── document_ingestion/
├── document_processing/
├── knowledge_pipeline/
└── reprocessing/

Examples:

Document ingestion
Upload
  ↓
Validate
  ↓
Store
  ↓
Publish event
Document processing
Parse
  ↓
Normalize
  ↓
Extract metadata
  ↓
OCR if required
  ↓
Chunk
Knowledge pipeline
Chunk
  ↓
Embed
  ↓
Enrich
  ↓
Knowledge Graph
  ↓
Vector Index

Workflow code should coordinate activities.

Business rules should remain inside the relevant modules.

# 17. Module Responsibilities

Each module should have one clear business responsibility.

Current major modules are:

acquisition
audit
authentication
evaluation
knowledge_engineering
monitoring
processing
project_management
retrieval
# 18. Acquisition Module

Location:

modules/acquisition/

Responsible for bringing data into Atlas.

Current areas:

acquisition/
├── bulk_import/
├── connectors/
├── crawler/
├── file_upload/
└── source_management/

Examples:

file uploads
bulk imports
external connectors
web crawling
source configuration

Acquisition should focus on getting data into the platform.

It should not contain downstream document processing logic.

# 19. Processing Module

Location:

modules/processing/

Responsible for transforming raw input into normalized and processable content.

Current areas:

processing/
├── deduplication/
├── metadata/
├── normalization/
├── ocr/
├── parsing/
└── validation/

Examples:

file validation
parsing
OCR
metadata extraction
normalization
duplicate detection
# 20. Knowledge Engineering Module

Location:

modules/knowledge_engineering/

Responsible for converting processed information into searchable knowledge.

Current areas:

knowledge_engineering/
├── chunking/
├── embeddings/
├── enrichment/
├── knowledge_graph/
└── vector_index/

Typical flow:

Processed Document
        |
        v
     Chunking
        |
        v
    Embeddings
        |
        +------> Vector Index
        |
        v
    Enrichment
        |
        v
 Knowledge Graph

Each area should remain independently testable and replaceable.

# 21. Retrieval Module

Location:

modules/retrieval/

Responsible for retrieving knowledge for applications and AI workflows.

Potential responsibilities include:

keyword search
semantic search
hybrid search
filtering
ranking
retrieval orchestration
RAG context preparation

Retrieval should not directly contain document ingestion logic.

# 22. Authentication Module

Location:

modules/authentication/

Responsible for business-level authentication and authorization functionality.

Examples:

user authentication
access policies
roles
permissions
project access

Security primitives that are shared across the system may belong in:

core/security/
# 23. Project Management Module

Location:

modules/project_management/

Responsible for project-level business concepts.

Examples:

projects
project membership
project configuration
project ownership
project-level access

This module should provide the business rules required to isolate different Atlas projects.

# 24. Audit Module

Location:

modules/audit/

Responsible for tracking important user and system actions.

Examples:

document uploaded
document deleted
project created
permission changed
processing started
processing completed
authentication events

Audit records should be designed so that important actions can be traced later.

# 25. Evaluation Module

Location:

modules/evaluation/

Responsible for evaluating retrieval and AI-related behavior.

Potential areas include:

evaluation datasets
retrieval evaluation
ranking evaluation
RAG evaluation
regression tests
quality metrics

Evaluation should help ensure that changes do not silently reduce system quality.

# 26. Monitoring Module

Location:

modules/monitoring/

Responsible for application and platform observability.

Current areas include:

monitoring/
├── application/
├── collectors/
├── infrastructure/
├── metrics/
└── tracing/

Monitoring should provide visibility into:

failures
latency
throughput
workflow status
processing performance
system health
# 27. API Development Rules

API routes should remain thin.

A typical route should:

authenticate the request
authorize access
validate request input
call an application use case
map the result to an HTTP response

Example flow:

HTTP Request
     |
     v
API Router
     |
     v
Authentication / Authorization
     |
     v
Application Use Case
     |
     v
Domain
     |
     v
Infrastructure
     |
     v
Response

Do not place the following directly inside API routes:

complex business rules
database queries
embedding generation
document parsing
OCR
long-running workflows
complex retrieval logic
# 28. Database Rules

Database-specific code belongs in infrastructure.

Database technologies may include:

PostgreSQL
Neo4j
Qdrant
other approved storage systems

Do not spread raw database queries throughout application/domain code.

Prefer repository interfaces.

Example:

Domain
   |
   v
DocumentRepository
   ^
   |
PostgresDocumentRepository

This keeps the business layer independent from the database implementation.

# 29. External Service Rules

External services must be treated as replaceable dependencies whenever practical.

Examples:

PostgreSQL
Neo4j
Qdrant
MinIO
Kafka
Temporal
OCR providers
Embedding providers
LLM providers
Crawler providers

Do not hard-code:

credentials
API keys
passwords
URLs
environment-specific configuration

Use configuration management and environment variables.

# 30. Free-First Technology Policy

Project Atlas follows a free/open-source-first development policy.

The preferred approach is:

Free and open-source technology
Self-hosted technology
Local development tools
Local AI models where practical
Free tiers where appropriate
Paid services only when explicitly approved

The initial project should not depend on paid services.

Provider abstraction should allow paid services to be added later without redesigning the architecture.

# 31. Configuration and Secrets

Local configuration should use .env.

The repository contains:

.env.example

The example file contains placeholders only.

Never commit:

.env
API keys
passwords
JWT secrets
private keys
cloud credentials
database credentials
tokens

Before committing, verify that no secret has been added.

# 32. Environment Configuration

Configuration should be accessed through a centralized configuration mechanism.

Do not scatter:

os.getenv(...)

throughout the business logic.

Prefer a centralized configuration object under:

core/config/

This provides:

validation
consistent configuration
typed settings
environment separation
easier testing
# 33. Naming Conventions

Python files:

snake_case.py

Classes:

PascalCase

Functions:

snake_case()

Variables:

snake_case

Constants:

UPPER_SNAKE_CASE

Examples:

Document
DocumentRepository
UploadDocumentUseCase
parse_document()
MAX_FILE_SIZE_MB

Names should describe the responsibility clearly.

Avoid vague names such as:

utils.py
helpers.py
misc.py
stuff.py
common.py

unless the purpose is genuinely broad and justified.

# 34. File Placement Rules

Before creating a new file, ask:

Question 1

Is this business logic?

Put it in:

domain/
Question 2

Is this a use case or application orchestration?

Put it in:

application/
Question 3

Does it communicate with an external technology?

Put it in:

infrastructure/
Question 4

Is it an interchangeable provider?

Put it in:

providers/
Question 5

Is it genuinely shared across the platform?

Consider:

core/
Question 6

Is it an executable entry point?

Consider:

apps/
Question 7

Is it long-running multi-step orchestration?

Consider:

workflows/

Do not create arbitrary folders.

# 35. Cross-Module Communication

Modules should communicate through explicit contracts.

Prefer:

application use cases
domain interfaces
events
shared contracts
clearly defined service boundaries

Avoid reaching directly into another module's internal implementation.

For example, do not do this:

Module A
   |
   +----> Module B infrastructure

Prefer:

Module A
   |
   v
Module B public contract
   |
   v
Module B

This protects module ownership and makes future team development easier.

# 36. Events

Events should be used when asynchronous or loosely coupled communication is appropriate.

Examples:

DocumentUploaded
DocumentValidated
DocumentParsed
DocumentProcessed
EmbeddingsCreated
KnowledgeGraphUpdated
DocumentProcessingFailed

Events should contain clear and stable contracts.

Where necessary, event contracts should be versioned.

Kafka may be used as the event transport layer.

The business meaning of an event should not depend on Kafka-specific implementation details.

# 37. Error Handling

Use structured application and domain errors.

Do not expose internal implementation details through APIs.

Never expose:

database stack traces
passwords
API keys
internal credentials
sensitive document contents
internal infrastructure details

The API layer should translate internal errors into appropriate HTTP responses.

Example:

Domain Error
     |
     v
Application Error
     |
     v
API Error Response
# 38. Logging

Use centralized logging.

Logs should contain useful context where appropriate, such as:

request_id
project_id
document_id
workflow_id
operation
status
duration

Never log:

passwords
API keys
JWT tokens
private keys
sensitive document contents

Logging should support debugging without creating a security risk.

# 39. Observability

Atlas should be designed for observability from the beginning.

Important areas include:

application logs
metrics
tracing
workflow visibility
error tracking
processing latency
queue/event status
retrieval performance

Observability should be implemented as a cross-cutting concern rather than duplicated inside every module.

# 40. Security Rules

Security is a cross-cutting concern.

Apply:

authentication
authorization
input validation
secure secret handling
least-privilege access
safe error responses
audit logging
secure communication

Never trust authorization information supplied directly by a client.

Authorization must be verified by the backend.

# 41. Document Security

Documents may contain sensitive enterprise information.

Therefore:

validate uploads
restrict file sizes
validate file types
prevent path traversal
avoid logging document contents
control document access
enforce project-level permissions
store files using controlled storage
track important document actions through audit events
# 42. Testing Strategy

Every meaningful feature should include tests.

Testing may include:

Unit Tests
Integration Tests
Application Tests
API Tests
Workflow Tests
End-to-End Tests

Tests should verify behavior rather than implementation details.

Tests belong under:

tests/

Example:

tests/
├── unit/
├── integration/
├── api/
└── workflows/

The exact test structure may evolve as the project grows.

# 43. Unit Tests

Unit tests should test isolated business behavior.

Examples:

validation rules
chunking behavior
domain entities
ranking logic
authorization rules
metadata transformations

Unit tests should be fast and should avoid requiring external infrastructure whenever possible.

# 44. Integration Tests

Integration tests verify interaction with real or test instances of infrastructure.

Examples:

PostgreSQL repositories
Qdrant repositories
Neo4j repositories
MinIO storage
Kafka event publishing

Use test infrastructure rather than production systems.

# 45. API Tests

API tests should verify:

request validation
authentication
authorization
HTTP status codes
response schemas
error responses
API behavior

Do not rely only on manual testing.

# 46. Workflow Tests

Workflow tests should verify:

workflow starts correctly
activities execute correctly
failures are handled
retries work as expected
workflow state is maintained
processing completes successfully

Long-running workflows should be designed to be deterministic where the workflow technology requires it.

# 47. Code Quality Checks

Before pushing code, run:

uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest

Or:

make check

All checks should pass before opening a pull request.

# 48. Python Version

Project Atlas currently targets:

Python 3.12

The version is defined by:

.python-version

and:

pyproject.toml

Do not change the supported Python version without an explicit project decision.

# 49. Dependency Management

Project Atlas uses uv for Python dependency management.

Install/synchronize dependencies using:

uv sync

Run Python through the project environment using:

uv run python

Run tests using:

uv run pytest

Run tools using:

uv run ruff check .
uv run mypy .

Do not manually install project dependencies globally unless there is a specific reason.

# 50. Adding Dependencies

Before adding a dependency:

Confirm it is required.
Check whether the Python standard library can solve the problem.
Prefer well-maintained open-source libraries.
Check licensing.
Consider security and maintenance.
Avoid unnecessary duplicate libraries.
Update the lock file through uv.

Dependencies should be added intentionally.

# 51. Git Branching Strategy

Project Atlas uses the following branching model:

main
  |
  v
develop
  |
  +---- feature/bridget
  |
  +---- feature/<developer-name>
  |
  +---- feature/<future-developer>

Branch responsibilities:

main

Production/stable branch.

This branch should contain production-ready code.

develop

Shared development/integration branch.

This is where completed feature work is integrated before being promoted to production.

feature/*

Individual development branches.

Each developer should work on their own feature branch.

# 52. Current Developer Branch

The initial developer branch is:

feature/bridget

Future developers should receive their own branches, for example:

feature/alex
feature/john
feature/sarah

Do not create another developer branch until that developer joins the project.

# 53. Pull Request Flow

The normal development flow is:

feature/<developer>
        |
        v
     develop
        |
        v
       main

Regular feature work should normally create a pull request:

feature/bridget -> develop

After features are integrated, tested, and considered stable:

develop -> main

This keeps main production-ready while develop acts as the shared development branch.

Do not normally create:

feature/bridget -> main

for ordinary feature development.

# 54. Developer Workflow

A developer should normally follow this process:

1. Clone repository
        |
        v
2. Checkout develop
        |
        v
3. Pull latest develop
        |
        v
4. Create feature branch
        |
        v
5. Implement assigned work
        |
        v
6. Run tests and quality checks
        |
        v
7. Commit changes
        |
        v
8. Push feature branch
        |
        v
9. Create PR into develop
        |
        v
10. Review
        |
        v
11. Merge into develop
# 55. Creating a Feature Branch

Example:

git checkout develop
git pull origin develop
git checkout -b feature/bridget

For another developer:

git checkout develop
git pull origin develop
git checkout -b feature/alex

The feature branch should be created from the latest develop.

# 56. Keeping a Feature Branch Updated

If develop has advanced while you are working:

git checkout develop
git pull origin develop
git checkout feature/bridget
git merge develop

Resolve conflicts carefully.

Run the complete test and quality checks after resolving conflicts.

# 57. Commit Message Convention

Use clear conventional commit messages.

Examples:

feat: add document validation use case
fix: handle invalid PDF metadata
refactor: simplify embedding provider interface
test: add document validation tests
docs: update architecture guide
chore: update development dependencies

Common prefixes:

feat
fix
refactor
test
docs
chore

Keep commits focused and understandable.

# 58. Commit Guidelines

A good commit should:

represent one logical change
have a clear message
avoid unrelated changes
not contain secrets
not contain generated local files
be easy to review

Avoid huge commits that combine unrelated work.

# 59. Pull Request Rules

A pull request should clearly describe:

what was changed
why it was changed
affected module
affected layers
tests performed
architecture decisions
configuration changes
migration requirements
known limitations

Example:

Title:
feat: add document validation module

Summary:
Adds document validation domain rules and application use case.

Affected:
modules/processing/validation/

Tests:
- unit tests
- application tests
- ruff
- mypy
# 60. Feature Ownership

Each developer should work inside an assigned module or feature area.

Example:

feature/bridget
        |
        v
modules/knowledge_engineering/embeddings/

A developer should avoid modifying another developer's module unless the change is required and coordinated.

Cross-module changes must be clearly explained in the pull request.

# 61. Example Developer Assignment

A developer working on embeddings may receive:

Module:
Knowledge Engineering

Area:
Embeddings

Branch:
feature/bridget

Allowed area:

modules/knowledge_engineering/embeddings/
├── application/
├── domain/
├── infrastructure/
└── providers/

The developer should understand exactly where each type of code belongs before implementation begins.

# 62. Example Embedding Architecture

The intended structure could look like:

modules/knowledge_engineering/embeddings/

├── application/
│   ├── dto.py
│   └── use_cases.py
│
├── domain/
│   ├── entities.py
│   ├── interfaces.py
│   └── services.py
│
├── infrastructure/
│   └── ...
│
└── providers/
    └── local/
        └── ...

The exact files can be introduced as implementation begins.

Do not create unnecessary empty files only for visual completeness.

Create files when they have a clear architectural purpose.

# 63. Adding a New Module

Before creating a new module:

Identify the business capability.
Confirm that it belongs under modules/.
Define its responsibility.
Determine its domain concepts.
Determine its application use cases.
Determine required infrastructure.
Define provider interfaces if required.
Add tests.
Update documentation if architecture changes.
Create a feature branch.
Implement the feature.
Run quality checks.
Open a PR into develop.
# 64. Adding a New Provider

When adding an external provider:

Define the required capability.
Define a stable interface.
Keep the interface independent from the provider.
Implement the provider.
Add configuration.
Add tests.
Add error handling.
Add observability.
Document provider-specific behavior.
Verify that provider-specific types do not leak into domain logic.

Example:

EmbeddingProvider
       |
       +---- LocalEmbeddingProvider
       |
       +---- FutureHostedEmbeddingProvider
# 65. Provider Replacement

The architecture should allow a provider to be replaced without rewriting business logic.

For example:

Application
     |
     v
EmbeddingProvider
     ^
     |
     +---- Local Provider
     |
     +---- Future Provider

The application should not care which provider implementation is used.

Configuration should decide which implementation is active.

# 66. Document Processing Flow

A typical Atlas document flow is:

Document Source
      |
      v
Acquisition
      |
      v
Validation
      |
      v
Deduplication
      |
      v
Parsing
      |
      v
Normalization
      |
      v
Metadata
      |
      v
OCR if required
      |
      v
Chunking
      |
      v
Embeddings
      |
      +----------------+
      |                |
      v                v
Vector Index      Enrichment
                       |
                       v
                Knowledge Graph
                       |
                       v
                   Retrieval
                       |
                       v
                 API / RAG

The actual implementation may evolve, but responsibilities should remain separated.

# 67. RAG Responsibilities

RAG-related logic should not be scattered across the application.

A typical flow is:

User Query
    |
    v
Authentication
    |
    v
Retrieval Application
    |
    v
Query Processing
    |
    v
Vector / Keyword / Graph Retrieval
    |
    v
Ranking
    |
    v
Context Preparation
    |
    v
LLM
    |
    v
Response

Retrieval logic belongs under:

modules/retrieval/

Knowledge creation belongs under:

modules/knowledge_engineering/
# 68. LLM Rules

LLM providers should be abstracted.

Do not make business logic depend directly on one provider.

Prefer:

LLM interface
      |
      +---- Local model
      |
      +---- Future provider

Configuration should select the implementation.

This supports the project's free-first approach and future provider changes.

# 69. Embedding Rules

Embedding generation belongs under:

modules/knowledge_engineering/embeddings/

Embedding storage belongs under:

modules/knowledge_engineering/vector_index/

Do not combine embedding generation and vector database persistence into one large class.

Keep responsibilities separated.

# 70. Knowledge Graph Rules

Knowledge graph business concepts belong under:

modules/knowledge_engineering/knowledge_graph/

Neo4j-specific implementation belongs in infrastructure/provider code.

Business logic should not directly construct Neo4j-specific queries unless that code is explicitly part of infrastructure.

# 71. Vector Index Rules

Vector indexing belongs under:

modules/knowledge_engineering/vector_index/

Qdrant-specific code belongs in infrastructure/provider implementation.

Retrieval should consume a stable interface rather than depending directly on Qdrant wherever practical.

# 72. OCR Rules

OCR belongs under:

modules/processing/ocr/

OCR provider implementations should be replaceable.

Development may use free/local OCR technologies.

Commercial OCR services should not be required for the core project.

# 73. Parsing Rules

Document parsing belongs under:

modules/processing/parsing/

Different document formats may require different parser providers.

Examples:

PDF
DOCX
PPTX
XLSX
CSV
XML
JSON
HTML
Markdown
TXT
Images

Parser-specific code belongs in appropriate infrastructure/provider implementations.

# 74. Crawling Rules

Crawler functionality belongs under:

modules/acquisition/crawler/

Crawler implementations should be replaceable.

Do not mix crawler logic with document parsing or knowledge engineering.

The crawler's responsibility is acquisition.

# 75. Storage Rules

Object/document storage should use controlled storage abstractions.

Potential development storage:

MinIO

The business layer should not directly depend on MinIO-specific APIs.

Prefer:

Storage interface
      ^
      |
MinIO implementation
# 76. Messaging Rules

Kafka may be used for asynchronous event communication.

Kafka-specific code belongs in infrastructure/event implementation.

Business modules should work with event contracts rather than raw Kafka client behavior wherever practical.

# 77. Workflow Orchestration Rules

Temporal may be used for durable workflow orchestration.

Workflow definitions should coordinate activities and application use cases.

Do not place all business logic inside Temporal workflow definitions.

Separate:

Workflow orchestration

from:

Business logic
# 78. Docker Rules

Docker configuration should be designed for reproducible development and deployment.

Do not place secrets inside Dockerfiles.

Do not copy:

.env
.venv
.git

into container images.

Keep images minimal where practical.

# 79. Local Development

The project should be runnable locally using free/open-source technologies.

Typical setup:

Python
uv
FastAPI
PostgreSQL
Neo4j
Qdrant
MinIO
Kafka
Temporal
Tesseract
Local embedding model
Local LLM where practical

Not every service must be running during every development task.

Developers should only start the infrastructure required for their assigned work.

# 80. Documentation Rules

Important architecture documentation belongs in:

docs/

Current documents include:

docs/
├── architecture.md
└── development-guide.md

When architecture changes materially, update the relevant documentation.

Documentation should be committed together with architectural changes when practical.

# 81. Architecture Decision Rules

Before introducing a significant architectural change, consider:

Why is the change required?
Which module owns the responsibility?
Which layer should contain the code?
Does the change introduce coupling?
Can the dependency be abstracted?
Does it affect other modules?
Does documentation need updating?
Does it affect existing developers?
Does it affect deployment?
Does it introduce a paid dependency?

Large architectural changes should be discussed before implementation.

# 82. Avoid Overengineering

Production-oriented architecture does not mean creating unnecessary abstractions.

Use abstractions when they provide a clear benefit such as:

replaceability
testability
separation of concerns
module ownership
external dependency isolation

Do not create interfaces, factories, services, or files without a clear reason.

Prefer simple code with clear boundaries.

# 83. Empty Folders and Placeholder Files

Git does not track empty directories.

Do not create large numbers of meaningless placeholder files just to make the repository tree look complete.

Create directories and files when there is an architectural or implementation reason.

If a directory must exist before implementation begins, a clearly named placeholder may be used when necessary, but it should be removed once real implementation files are added.

# 84. Generated Files

Do not commit local generated files such as:

.pytest_cache/
.ruff_cache/
.mypy_cache/
.venv/
__pycache__/

These are already handled by .gitignore.

Do not commit temporary processing data, local database files, logs, or generated artifacts unless they are intentionally part of the project.

# 85. Before Opening a Pull Request

Run:

git status

Then:

uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest

Review:

git diff

Check for secrets.

Then commit:

git add .
git commit -m "feat: ..."

Push:

git push origin feature/<developer-name>

Then open the pull request into:

develop
# 86. Definition of Done

A feature is considered complete when:

implementation follows the architecture
correct module owns the code
correct layer contains the code
dependencies follow the intended direction
tests are included
Ruff passes
formatting passes
MyPy passes
tests pass
secrets are not committed
documentation is updated when required
configuration is documented
commit messages are clear
PR description is complete
feature branch is pushed
PR is ready for review
PR targets develop
# 87. Golden Rules

The following rules should always be remembered:

Keep business logic in the domain layer.
Keep use cases in the application layer.
Keep external technology in infrastructure.
Use provider interfaces for replaceable external services.
Keep API routes thin.
Keep workflows focused on orchestration.
Do not put module-specific business logic into core/.
Do not commit secrets.
Write tests for meaningful behavior.
Run quality checks before opening a PR.
Feature branches merge into develop.
develop is the shared integration branch.
main represents production/stable code.
Keep modules independently understandable.
Respect module ownership.
Avoid unnecessary cross-module coupling.
Prefer free/open-source technologies for the project.
Update architecture documentation when architectural decisions change.
Do not bypass the architecture simply to implement something faster.
When uncertain where code belongs, discuss the responsibility and layer before implementing it.
# 88. Final Architecture Rule

When deciding where new code belongs, use this simple rule:

What does the code do?
        |
        +------------------------------+
        |                              |
        v                              v
Business rule?                  External technology?
        |                              |
        v                              v
    DOMAIN                       INFRASTRUCTURE
        |
        |
Use case / orchestration?
        |
        v
  APPLICATION

Replaceable provider?
        |
        v
    PROVIDER

Cross-cutting platform capability?
        |
        v
      CORE

Executable entry point?
        |
        v
      APPS

Long-running multi-step process?
        |
        v
    WORKFLOWS

The architecture exists to make Project Atlas easier to develop as a team.

Every developer should be able to look at the repository and understand:

what each folder is responsible for
where their code belongs
what they are allowed to change
what dependencies they may use
how their module communicates with other modules
how their work reaches develop
how stable code eventually reaches main

This consistency is more important than simply creating code quickly.