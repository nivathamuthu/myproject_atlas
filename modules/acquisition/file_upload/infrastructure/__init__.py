"""
Infrastructure layer for the Project Atlas file upload module.

This layer contains concrete implementations of external dependencies
required by the file upload capability.

Infrastructure implementations may include:
- upload metadata persistence
- object storage integration
- provider-specific adapters

This layer may depend on external technologies and provider SDKs.

Examples may include:
- PostgreSQL
- MinIO
- S3-compatible storage

Infrastructure code implements contracts required by higher layers.

Business rules must not be moved into this layer merely because an
infrastructure operation is involved.
"""
