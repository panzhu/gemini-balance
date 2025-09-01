# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

**Local Development:**
- Install dependencies: `pip install -r requirements.txt`
- Run application with hot-reloading: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

**Production Environment (Uvicorn):**
- Create virtual environment: `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run application: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --loop uvloop --http httptools`

**Production Environment (Gunicorn + Uvicorn):**
- Run application: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

**Docker:**
- Build and run with Docker Compose: `docker-compose up -d`
- Pull Docker image: `docker pull ghcr.io/snailyp/gemini-balance:latest`
- Run Docker container: `docker run -d -p 8000:8000 --name gemini-balance -v ./data:/app/data --env-file .env ghcr.io/snailyp/gemini-balance:latest`

## High-Level Code Architecture

The project `Gemini Balance` is a Python FastAPI application that acts as a proxy and load balancer for the Google Gemini API. It supports multiple Gemini API Keys, key rotation, authentication, model filtering, and status monitoring. It also integrates image generation and multiple image hosting upload functions, and supports proxying in the OpenAI API format.

The main application structure is as follows:

-   `app/`: Contains the core application logic.
    -   `config/`: Configuration management.
    -   `core/`: Core application logic (FastAPI instance creation, middleware).
    -   `database/`: Database models and connections.
    -   `domain/`: Business domain objects.
    -   `exception/`: Custom exceptions.
    -   `handler/`: Request handlers.
    -   `log/`: Logging configuration.
    -   `main.py`: Application entry point.
    -   `middleware/`: FastAPI middleware.
    -   `router/`: API routes (Gemini, OpenAI, status page).
    -   `scheduler/`: Scheduled tasks (e.g., Key status check).
    -   `service/`: Business logic services (chat, Key management, statistics).
    -   `static/`: Static files (CSS, JS).
    -   `templates/`: HTML templates (e.g., Key status page).
    -   `utils/`: Utility functions.
