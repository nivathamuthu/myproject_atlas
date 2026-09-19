"""Persistence implementation for Connectors repositories.

This module contains the infrastructure implementation of the
repository contract defined in:

    domain/repository.py

Responsibilities:
- Persist connector configuration and state.
- Retrieve connector information.
- Update connector lifecycle state.
- Translate between persistence models and domain objects.
- Handle database-specific concerns.

Database-specific implementation belongs here.

Potential concerns include:
- ORM models
- SQL queries
- database sessions
- transaction handling
- persistence mappings

The domain repository contract must remain independent from the
chosen database technology.

Do not move database-specific concerns into the domain layer.
"""
