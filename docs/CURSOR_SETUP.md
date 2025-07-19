# Cursor IDE Setup for CK3 AI Weight Generator

This document provides comprehensive setup instructions for using Cursor IDE with the CK3 AI Weight Generator project, optimized for CK3 modding development.

## Quick Start

1. **Open the project in Cursor IDE**
2. **Install recommended extensions** (Cursor will prompt you)
3. **Set up the Python environment** using the provided tasks
4. **Start developing!**

## Project Structure

The Cursor IDE setup includes the following configuration files:

```
CK3-AIs-Weight-Gen/
├── .cursorrules                    # AI assistant rules for CK3 modding
├── .vscode/
│   ├── settings.json              # Editor settings and preferences
│   ├── extensions.json            # Recommended extensions
│   ├── launch.json                # Debug configurations
│   ├── tasks.json                 # Build and development tasks
│   ├── snippets/
│   │   └── python.json           # CK3-specific code snippets
│   └── workspace.code-workspace  # Complete workspace configuration
├── schemas/
│   ├── config.schema.json        # Configuration validation schema
│   └── models.schema.json        # AI model validation schema
├── pyproject.toml                # Modern Python project configuration
└── .pre-commit-config.yaml       # Automated code quality checks
```

## Key Features

### 1. AI Assistant Integration (`.cursorrules`)

The `.cursorrules` file provides context-aware assistance for CK3 modding:

- **Project Context**: Understands CK3 modding concepts and requirements
- **Code Standards**: Enforces Python 3.7+ syntax and PEP 8 guidelines
- **CK3-Specific Guidelines**: Validates CK3 syntax and game compatibility
- **Development Priorities**: Focuses on accuracy, performance, and usability

### 2. Editor Configuration (`.vscode/settings.json`)

Optimized settings for CK3 modding development:

- **Python Environment**: Automatic virtual environment detection
- **File Associations**: Proper handling of CK3 event files (.txt) and JSON models
- **Code Formatting**: Black formatter with 88-character line length
- **Import Sorting**: isort integration for clean imports
- **Linting**: flake8 for code quality checks
- **JSON Validation**: Schema-based validation for configuration and model files

### 3. Recommended Extensions (`.vscode/extensions.json`)

Essential extensions for CK3 modding:

#### Python Development
- **Python**: Core Python support
- **Pylance**: Advanced Python language server
- **Black Formatter**: Code formatting
- **Flake8**: Linting
- **isort**: Import sorting
- **MyPy**: Type checking

#### CK3 Modding Specific
- **Material Icon Theme**: Visual file organization
- **Path Intellisense**: Smart path completion
- **Auto Rename Tag**: XML/JSON tag management
- **Code Spell Checker**: Spelling validation

#### Productivity
- **GitLens**: Enhanced Git integration
- **Markdown All in One**: Documentation support
- **JSON Tools**: JSON file management

### 4. Debug Configurations (`.vscode/launch.json`)

Multiple debug scenarios for development:

- **Debug CK3 AI Weight Generator**: Main program debugging
- **Debug with Test Events**: Testing with sample event files
- **Debug Event Parser**: Focused debugging of event parsing
- **Debug AI Model Manager**: Model management debugging
- **Debug Trigger Generator**: Trigger generation debugging
- **Debug Tests**: Test suite debugging

### 5. Development Tasks (`.vscode/tasks.json`)

Automated workflows for common development tasks:

#### Setup Tasks
- **Setup Environment**: Initialize Python environment
- **Run Menu System**: Launch the interactive menu
- **Create Config**: Generate configuration files

#### Code Quality Tasks
- **Format Python Code**: Apply Black formatting
- **Sort Imports**: Organize imports with isort
- **Lint Code**: Run flake8 linting
- **Type Check**: Run MyPy type checking
- **Validate JSON Models**: Check model file validity

#### Testing Tasks
- **Run Tests**: Execute test suite
- **Quick Weight Check**: Validate AI weights
- **Run All Checks**: Complete quality check pipeline

### 6. Code Snippets (`.vscode/snippets/python.json`)

CK3-specific code templates:

- **CK3 AI Model Class**: Template for AI model classes
- **CK3 Trait Definition**: Template for trait definitions
- **CK3 Event Parser**: Template for event parsing
- **CK3 Trigger Generator**: Template for trigger generation
- **CK3 Test Case**: Template for test cases
- **CK3 Configuration**: Template for configuration management
- **CK3 JSON Model**: Template for JSON model definitions
- **CK3 JSON Trait**: Template for JSON trait definitions

### 7. JSON Schema Validation (`.vscode/schemas/`)

Schema-based validation for configuration and model files:

- **config.schema.json**: Validates configuration files
- **models.schema.json**: Validates AI model definitions

### 8. Modern Python Configuration (`pyproject.toml`)

Comprehensive project configuration:

- **Build System**: Modern setuptools configuration
- **Dependencies**: Core and optional dependencies
- **Development Tools**: Black, flake8, isort, MyPy, pytest
- **Pre-commit Hooks**: Automated code quality checks

### 9. Pre-commit Hooks (`.pre-commit-config.yaml`)

Automated code quality enforcement:

- **Code Formatting**: Black and isort
- **Linting**: flake8 and MyPy
- **Security**: Bandit security checks
- **CK3-Specific**: JSON validation and CK3 syntax checks

## Getting Started

### 1. Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd CK3-AIs-Weight-Gen

# Open in Cursor IDE
cursor .

# Install recommended extensions when prompted
```

### 2. Environment Setup

```bash
# Use the provided task (Ctrl+Shift+P -> Tasks: Run Task)
# Or run manually:
./run.sh
```

### 3. Configuration

```bash
# Create your configuration
python3 create_config.py

# Or use the menu system
./menu.sh
```

### 4. Development Workflow

1. **Write Code**: Use the provided snippets and AI assistance
2. **Format Code**: `Ctrl+Shift+P` -> `Tasks: Run Task` -> `Format Python Code`
3. **Run Tests**: `Ctrl+Shift+P` -> `Tasks: Run Task` -> `Run Tests`
4. **Debug**: Use the debug configurations in the Run and Debug panel
5. **Commit**: Pre-commit hooks will automatically format and validate your code

## Keyboard Shortcuts

### Development Tasks
- `Ctrl+Shift+P` -> `Tasks: Run Task`: Execute development tasks
- `Ctrl+Shift+P` -> `Tasks: Run Build Task`: Run build tasks
- `Ctrl+Shift+P` -> `Tasks: Run Test Task`: Run test tasks

### Code Quality
- `Shift+Alt+F`: Format document
- `Ctrl+Shift+P` -> `Python: Sort Imports`: Sort imports
- `Ctrl+Shift+P` -> `Python: Select Linter`: Choose linter

### Debugging
- `F5`: Start debugging
- `Ctrl+F5`: Start without debugging
- `F9`: Toggle breakpoint
- `F10`: Step over
- `F11`: Step into
- `Shift+F11`: Step out

### File Management
- `Ctrl+P`: Quick file open
- `Ctrl+Shift+F`: Search in files
- `Ctrl+Shift+E`: Explorer
- `Ctrl+Shift+G`: Source control

## Best Practices

### 1. Use AI Assistance
- The `.cursorrules` file provides context-aware assistance
- Ask for help with CK3-specific syntax and patterns
- Use the AI to generate boilerplate code

### 2. Follow Code Standards
- Use the provided formatting and linting tools
- Follow the established naming conventions
- Write comprehensive docstrings

### 3. Validate Your Work
- Use the JSON schema validation for model files
- Run tests regularly
- Use the pre-commit hooks

### 4. Debug Effectively
- Use the provided debug configurations
- Set breakpoints in strategic locations
- Use the debug console for exploration

### 5. Document Changes
- Update documentation when adding new features
- Use meaningful commit messages
- Keep the README updated

## Troubleshooting

### Common Issues

1. **Python Interpreter Not Found**
   - Ensure the virtual environment is created: `./run.sh`
   - Check the Python path in settings

2. **Extensions Not Working**
   - Install recommended extensions when prompted
   - Reload the window after installation

3. **JSON Validation Errors**
   - Check the schema files in `schemas/`
   - Validate your JSON files manually

4. **Pre-commit Hooks Failing**
   - Install pre-commit: `pip install pre-commit`
   - Install hooks: `pre-commit install`

5. **Debug Configuration Issues**
   - Check that the virtual environment is activated
   - Verify file paths in launch configurations

### Getting Help

- Check the project documentation in `docs/`
- Review the README.md file
- Use the AI assistant for context-aware help
- Check the test files for examples

## Contributing

When contributing to the project:

1. **Follow the established patterns**
2. **Use the provided tools and configurations**
3. **Write tests for new features**
4. **Update documentation as needed**
5. **Use the pre-commit hooks**

The Cursor IDE setup is designed to make CK3 modding development efficient and enjoyable. The AI assistant will help you understand CK3-specific concepts and generate appropriate code patterns. 