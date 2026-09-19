"""
Project Atlas file upload module.

This module is responsible for acquiring documents through manual file uploads.

The file upload capability is the entry point for supported enterprise
documents provided directly to Project Atlas.

Primary responsibilities:
- accept file upload requests through application interfaces
- represent uploaded files as domain concepts
- validate file-upload-specific business rules
- coordinate persistence of upload metadata
- coordinate storage of uploaded file content
- prepare accepted uploads for downstream processing

Typical downstream flow:

File Upload
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
Metadata / OCR
    |
    v
Knowledge Engineering

Layer responsibilities are defined in:
- application/
- domain/
- infrastructure/

This package must not contain API route definitions. Transport-specific code
belongs in the appropriate application entry point under apps/.
"""
