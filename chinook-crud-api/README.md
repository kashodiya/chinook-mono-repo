
# Chinook CRUD API

A RESTful API for the Chinook database system.

## Overview

This project provides a comprehensive CRUD API for interacting with the Chinook database, which represents a digital media store including tables for artists, albums, media tracks, invoices, and customers.

## Features

- Full CRUD operations for all Chinook entities
- Authentication and authorization
- Rate limiting
- Comprehensive API documentation
- Filtering, sorting, and pagination

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL 14+

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/chinook-mono-repo.git

# Navigate to the project directory
cd chinook-mono-repo/chinook-crud-api

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### Database Setup

```bash
# Run database migrations
npm run migrate

# Seed the database with sample data
npm run seed
```

## Usage

```bash
# Start the server
npm start

# The API will be available at http://localhost:3000
```

## API Documentation

API documentation is available at `/api-docs` when the server is running.

## Development

```bash
# Run in development mode with hot reloading
npm run dev

# Run tests
npm test
```

## License

MIT
