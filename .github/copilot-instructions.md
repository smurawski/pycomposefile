# pycomposefile

pycomposefile is a Python library for structured deserialization of Docker Compose files. It provides a structured way to parse, validate, and manipulate Docker Compose YAML configurations in Python applications.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- **Required Python version**: 3.9 or higher (tested with 3.10-3.14)
- **Network Dependencies**: Most pip commands require PyPI access and may timeout in sandboxed environments
- **Initial setup** (if pip access works): `python -m pip install -U pip` then `python -m pip install --group dev`
- **Dependencies**: pyyaml>=6.0, build>=0.7, ruff==0.12.5, timeout-decorator==0.5.0
- **If network issues**: Dependencies may already be installed; verify with `python -m ruff --version`

### Development Workflow Commands
- **Lint code**: `python -m ruff check` (takes <1 second) - **ALWAYS run before committing**
- **Format code**: `python -m ruff format` (takes <1 second) - Auto-formats Python code 
- **Check formatting**: `python -m ruff format --check` (takes <1 second) - **WARNING: Currently shows 31 files would be reformatted - this is normal for this codebase**
- **Run tests**: `python -m unittest discover -v -s . -p "test*.py"` (takes <1 second, 85 tests, 1 typically skipped)
- **Build package**: `python -m build` - **NETWORK DEPENDENT: Will fail with PyPI timeout in sandboxed environments. Use manual testing instead.**

### Key Project Structure
```
/pycomposefile/           # Main library code
  __init__.py            # Exports ComposeFile class
  compose_file.py        # Core ComposeFile class
  compose_element/       # Compose element parsing utilities
  service/              # Service-specific parsing
  secrets/              # Secret management
/tests/                  # Test suite (unittest framework)
  compose_file/         # Tests for compose file parsing
  service/              # Tests for service parsing
  environment_variable_evaluation/  # Tests for env var handling
  compose_generator/    # Test data generators
/sample/                 # Sample files for testing
  test.env, common.env  # Environment files for testing
  my_secret.txt         # Sample secret file
  apps/web.env          # Application-specific env vars
```

## Validation

### Manual Functionality Testing
Always test the core library functionality after making changes:

```python
import sys
sys.path.insert(0, '.')
from pycomposefile import ComposeFile
import yaml

# Test basic parsing
compose_yaml = '''
version: '3'
services:
  web:
    image: nginx:latest
    ports:
      - '80:80'
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
'''
parsed = yaml.load(compose_yaml, Loader=yaml.Loader)
compose_file = ComposeFile(parsed)
print(f'Version: {compose_file.version}')
print(f'Services: {list(compose_file.services.keys())}')
```

### Test Environment Variable Processing
```python
from tests.compose_generator import ComposeGenerator
# Test environment files
compose = ComposeGenerator.get_compose_with_environment_file_list()
# Test service dependencies  
compose = ComposeGenerator.get_compose_with_service_dependencies()
# Test secrets
compose = ComposeGenerator.get_compose_with_one_secret()
```

### CI Validation Steps
Always run these commands before committing (matches .github/workflows/build.yaml):
1. `python -m ruff check` - Must pass with no errors  
2. `python -m unittest discover -v -s . -p "test*.py"` - All tests must pass (85 tests, 1 may be skipped)

**Note on formatting**: `python -m ruff format --check` shows 31 files would be reformatted, which is the current state of the codebase. Focus on ensuring your changes don't introduce new linting errors.

**Build command limitations**: The `python -m build` command requires network access to PyPI and will timeout in sandboxed environments. Use manual functionality testing instead.

## Important Development Notes

### Network Dependencies
- **PyPI Access Required**: Package building and some pip commands require downloading from PyPI
- **Timeout Issues**: In sandboxed environments, pip and build commands frequently fail with "Read timed out" errors
- **Workarounds**: 
  - Test core functionality directly with Python imports instead of relying on package building
  - Dependencies are often pre-installed in development environments
  - Focus on linting, testing, and manual functionality validation
  - Use `python -m ruff --version` to verify ruff is available

### Code Quality Requirements
- **Linting**: All code must pass `ruff check` without warnings
- **Formatting**: Code must be formatted with `ruff format` 
- **Testing**: All new functionality must have corresponding unittest tests
- **Coverage**: Tests are comprehensive with 85+ test cases covering all major functionality

### Common File Locations
- **Configuration**: `pyproject.toml` (build config, dependencies, ruff settings)
- **Main API**: `pycomposefile/__init__.py` (exports ComposeFile)
- **Core Logic**: `pycomposefile/compose_file.py` (main parsing logic)
- **Test Data**: `tests/compose_generator/__init__.py` (ComposeGenerator with test YAML)
- **Sample Files**: `sample/` directory (test.env, common.env, my_secret.txt)

### Testing Framework Details
- **Framework**: Python unittest (not pytest)
- **Test Discovery**: Use `python -m unittest discover -v`
- **Test Organization**: Tests are organized by functionality in separate directories
- **Test Data**: ComposeGenerator class provides Docker Compose YAML snippets for testing
- **Expected Results**: 85 tests run, typically 1 skipped, all others should pass

### Environment & Dependencies
- **Build Backend**: flit_core (defined in pyproject.toml)
- **Main Dependency**: pyyaml for YAML parsing
- **Dev Dependencies**: build, ruff, timeout-decorator
- **Python Support**: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14 (per CI matrix)

### Development Container Support
- **DevContainer**: `.devcontainer/devcontainer.json` with Python 3 setup
- **Post-Create Script**: `.devcontainer/postCreate.sh` sets up virtual environment
- **VSCode Config**: Configured for Python development with unittest integration

Always validate your changes by running the full development workflow: install dependencies, lint, format-check, and run tests.