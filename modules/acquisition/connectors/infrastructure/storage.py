"""External-source and storage implementations for Connectors.

This module contains infrastructure implementations required to
communicate with external connector sources.

Depending on the connector type, implementations may eventually
interact with:
- cloud storage
- remote file systems
- external document repositories
- third-party APIs
- enterprise systems
- other supported acquisition sources

Responsibilities:
- establish communication with external sources
- retrieve source data
- handle provider-specific authentication
- handle provider-specific errors
- translate external representations into Atlas-compatible forms

Provider SDKs and HTTP clients belong in this layer.

The domain and application layers must not directly depend on
provider-specific SDKs.

When multiple providers are supported, provider-specific implementations
should remain isolated behind appropriate abstractions.
"""
