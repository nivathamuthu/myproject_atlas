"""Persistence implementation for Crawler repositories.

This module contains the infrastructure implementation of the
repository contract defined in:

    domain/repository.py

Responsibilities:
- Persist crawl jobs.
- Retrieve crawl jobs.
- Update crawl status.
- Store crawl configuration and metadata.
- Persist crawl history where required.
- Translate between persistence models and domain objects.
- Handle database-specific concerns.

Database-specific implementation belongs here.

Potential concerns include:
- ORM models
- SQL queries
- database sessions
- transactions
- persistence mappings
- indexes and database-specific optimizations

The domain repository contract must remain independent from the
chosen persistence technology.
"""
