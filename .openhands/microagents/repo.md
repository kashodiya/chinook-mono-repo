
# Chinook Monorepo Information

## Repository Overview

This is a monorepo containing multiple projects related to the Chinook database system. The monorepo structure allows for shared code, coordinated versioning, and simplified dependency management across projects.

## Projects

### chinook-crud-api-mcp

**Description**: Microservice Control Plane for Chinook CRUD API
**Tech Stack**: Node.js, Express, Docker, Kubernetes
**Purpose**: Provides orchestration, monitoring, and management for the Chinook CRUD API microservices

### chinook-crud-api

**Description**: Core CRUD API for Chinook database
**Tech Stack**: Node.js, Express, PostgreSQL
**Purpose**: Provides RESTful API endpoints for interacting with the Chinook database

## Shared Resources

- Common utilities
- Configuration templates
- Documentation
- CI/CD pipelines

## Development Workflow

1. Clone the repository
2. Install dependencies for the specific project you're working on
3. Make changes
4. Run tests to ensure compatibility across projects
5. Submit pull requests

## Versioning Strategy

The monorepo uses coordinated versioning to ensure compatibility between projects:

- Major version changes: Breaking changes that affect multiple projects
- Minor version changes: New features that maintain backward compatibility
- Patch version changes: Bug fixes and minor improvements

## Deployment

Each project can be deployed independently or as part of a coordinated release.

## Microagents Configuration

This directory contains configuration for automated agents that help maintain and improve the codebase.

