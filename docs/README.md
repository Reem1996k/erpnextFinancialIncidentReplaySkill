# ERPNext Financial Incident Replay Skill

## Project Overview
This project is a backend service that integrates with ERPNext and provides
a "Financial Incident Replay" capability.

The system allows a user to input a financial document ID (Invoice, Payment, etc.)
and receive a structured explanation of:
- What happened
- Which business rules were applied
- Why the action was allowed
- Supporting evidence from ERP data

## Tech Stack
- Python 3.12
- FastAPI
- SQLite (local development)
- pytest for testing

## Architecture Principles
- Clear separation of concerns
- Business logic isolated from API layer
- ERPNext access via service layer
- No business logic inside controllers

# Backend Structure

- api/         → HTTP routes (FastAPI routers)
- controllers/ → Request orchestration (no business logic)
- services/    → Core business logic
- rules/       → Business policy evaluation
- models/      → Data models (Pydantic / ORM)
- db/          → Database access and repositories
