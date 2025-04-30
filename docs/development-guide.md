# WeHolo Development Guide

This guide provides information for developers working on the WeHolo project, including coding standards, workflow, and best practices.

## Development Environment Setup

Follow the instructions in the [Getting Started](./getting-started.md) guide to set up your development environment.

## Development Workflow

### 1. Issue Tracking

All development work should be tied to an issue in the issue tracker. If you're working on something that doesn't have an issue yet, create one first.

### 2. Branching Strategy

We follow a feature branch workflow:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/<feature-name>`: Feature branches
- `bugfix/<bug-name>`: Bug fix branches
- `hotfix/<fix-name>`: Hot fixes for production

### 3. Development Process

1. Create a new branch from `develop` for your feature or bug fix
2. Implement your changes with appropriate tests
3. Run tests locally to ensure they pass
4. Submit a pull request to merge your branch into `develop`
5. After code review and approval, your changes will be merged

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following additions:

- Line length: 88 characters (compatible with Black formatter)
- Use double quotes for strings unless single quotes avoid backslashes
- Use type hints for function parameters and return values

### Code Formatting

We use the following tools to maintain code quality:

- **Black**: For code formatting
- **isort**: For import sorting
- **flake8**: For linting
- **mypy**: For type checking

You can run these tools with:

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Lint code
flake8 app tests

# Type check
mypy app
```

### Docstrings

Use Google-style docstrings for functions and classes:

```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.
    
    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.
    
    Returns:
        bool: The return value. True for success, False otherwise.
    
    Raises:
        ValueError: If param1 is negative.
    """
    if param1 < 0:
        raise ValueError("param1 must be positive")
    return param1 > len(param2)
```

## Project Structure

Maintain the project structure as described in the [Architecture](./architecture.md) document.

### Adding New Features

When adding new features:

1. Create appropriate models in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Implement API endpoints in `app/api/endpoints/`
4. Add tests in the `tests/` directory

### Database Changes

When making database changes:

1. Update the SQLAlchemy models in `app/models/`
2. Generate a migration with Alembic:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```
3. Review the generated migration to ensure it's correct
4. Apply the migration:
   ```bash
   alembic upgrade head
   ```

## Testing

### Test Structure

Tests are organized in the `tests/` directory with a structure that mirrors the application:

```
tests/
├── api/
│   └── endpoints/
│       ├── test_users.py
│       └── ...
├── core/
│   ├── test_config.py
│   └── ...
└── conftest.py
```

### Writing Tests

- Use pytest for all tests
- Create fixtures in `conftest.py` for reusable test components
- Aim for high test coverage, especially for critical paths
- Write both unit tests and integration tests

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app

# Run specific tests
pytest tests/api/endpoints/test_users.py
```

## API Development

### API Design Principles

- Follow RESTful principles
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate HTTP status codes
- Use consistent response formats
- Document all endpoints

### Adding New Endpoints

When adding new endpoints:

1. Create a new file in `app/api/endpoints/` if needed
2. Define the endpoint using FastAPI's router
3. Add appropriate dependencies for authentication and database access
4. Validate input using Pydantic schemas
5. Implement the business logic
6. Return a properly formatted response
7. Add the router to `main.py`

Example:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.some_schema import SomeSchema

router = APIRouter()

@router.post("/", response_model=SomeSchema)
def create_something(
    *,
    db: Session = Depends(get_db),
    data_in: SomeSchema,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new something.
    """
    # Implementation here
    return result
```

## Dependency Management

- Add new dependencies to `requirements.txt`
- Pin dependency versions to ensure reproducibility
- Use virtual environments to isolate dependencies

## Logging

- Use the standard Python logging module
- Configure logging in `app/core/logging.py`
- Use appropriate log levels:
  - DEBUG: Detailed information for debugging
  - INFO: Confirmation that things are working as expected
  - WARNING: Something unexpected happened, but the application still works
  - ERROR: Something failed, but the application can continue
  - CRITICAL: The application cannot continue

Example:

```python
import logging

logger = logging.getLogger(__name__)

def some_function():
    logger.debug("Detailed debug information")
    try:
        # Some operation
        logger.info("Operation completed successfully")
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}", exc_info=True)
```

## Error Handling

- Use FastAPI's HTTPException for API errors
- Return appropriate HTTP status codes
- Provide clear error messages
- Log errors with sufficient context

Example:

```python
from fastapi import HTTPException, status

def get_item(item_id: int, db: Session):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        logger.warning(f"Item with ID {item_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item
```

## Security Best Practices

- Never store sensitive information (passwords, API keys) in code
- Use environment variables for configuration
- Always validate and sanitize user input
- Use parameterized queries to prevent SQL injection
- Keep dependencies up to date to avoid security vulnerabilities
- Follow the principle of least privilege

## Performance Considerations

- Use database indexes for frequently queried fields
- Implement pagination for endpoints that return lists
- Use async/await for I/O-bound operations
- Consider caching for expensive operations
- Profile and optimize critical paths

## Documentation

- Document all code with appropriate docstrings
- Keep API documentation up to date
- Document architectural decisions
- Update the README.md with any significant changes

## Continuous Integration

We use GitHub Actions for continuous integration:

- Automated tests run on every pull request
- Code quality checks (linting, formatting)
- Security scanning
- Build and deployment for production

## Getting Help

If you need help with development:

- Check the existing documentation
- Look at the code for similar features
- Ask questions in the team chat
- Create an issue for larger problems or feature requests