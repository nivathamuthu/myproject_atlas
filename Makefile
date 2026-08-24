# ============================================================
# Project Atlas - Makefile
# ============================================================

.DEFAULT_GOAL := help

# ------------------------------------------------------------
# Variables
# ------------------------------------------------------------

PYTHON := uv run python
PYTEST := uv run pytest
RUFF := uv run ruff
MYPY := uv run mypy


# ------------------------------------------------------------
# Help
# ------------------------------------------------------------

help:
	@echo "Project Atlas development commands:"
	@echo ""
	@echo "  make setup       Install project dependencies"
	@echo "  make lint        Run Ruff linting"
	@echo "  make format      Format Python code"
	@echo "  make format-check Check formatting without changing files"
	@echo "  make typecheck   Run MyPy type checking"
	@echo "  make test        Run test suite"
	@echo "  make check       Run lint + format check + typecheck + tests"
	@echo "  make run         Start FastAPI development server"


# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------

setup:
	uv sync


# ------------------------------------------------------------
# Code Quality
# ------------------------------------------------------------

lint:
	$(RUFF) check .


format:
	$(RUFF) format .


format-check:
	$(RUFF) format --check .


typecheck:
	$(MYPY) .


# ------------------------------------------------------------
# Testing
# ------------------------------------------------------------

test:
	$(PYTEST)


# ------------------------------------------------------------
# Full Validation
# ------------------------------------------------------------

check:
	$(RUFF) check .
	$(RUFF) format --check .
	$(MYPY) .
	$(PYTEST)


# ------------------------------------------------------------
# Development Server
# ------------------------------------------------------------

run:
	$(PYTHON) -m uvicorn atlas_api.main:app --reload --host 0.0.0.0 --port 8000