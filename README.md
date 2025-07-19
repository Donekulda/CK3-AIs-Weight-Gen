# CK3 AI Weight Generator

[![License: Custom](https://img.shields.io/badge/License-Custom-blue.svg)](LICENSE)

A Python tool for automatically generating CK3 AI modifiers based on a unified trait-based AI model system. This tool processes CK3 event files and replaces AI model references with appropriate CK3 triggers that consider character traits, education, personality, and situational modifiers.

## Features

- **Unified Trait-Based System**: Combines individual traits and character models into cohesive AI models
- **Automatic Event Parsing**: Scans CK3 event files for AI model references
- **CK3 Mod Folder Support**: Works with Steam Workshop and Paradox mods
- **Mod Discovery & Management**: Interactive mod discovery and configuration
- **Descriptor.mod Integration**: Automatic configuration from mod descriptor files
- **Trait Management**: Loads and validates trait definitions with weights and effects
- **Character Model System**: Defines character archetypes that reference traits
- **Trigger Generation**: Converts unified AI models into CK3 trigger code
- **File Modification**: Automatically applies generated triggers back to event files
- **Validation**: Validates generated triggers and trait references
- **Documentation**: Auto-generates comprehensive model documentation
- **Development Tools**: Utilities for managing and organizing AI models

## Requirements

- Python 3.7 or higher
- Linux/macOS/Windows with bash support
- CK3 installed (for mod folder access)

## Installation and Usage

### Menu System

The CK3 AI Weight Generator includes an enhanced interactive menu system (`menu.sh`) that provides:

#### Main Menu Options
1. **Run CK3 AI Weight Generator** - Execute the main program with configuration status
2. **Run CK3 Parser** - Execute the new unified parser (extensible for future file types)
3. **CK3 Mod Manager** - Discover and manage CK3 mods interactively
4. **Setup Configuration** - Interactive configuration setup with mod support
5. **Run Test Suite** - Execute all tests with detailed results
6. **Setup Environment Only** - Install dependencies without running the program
7. **Configuration Management** - Manage configuration files and settings
8. **Show Configuration Status** - Display current configuration information
9. **Exit** - Close the menu

#### Configuration Management Submenu
- **Create User Configuration** - Copy default config to user config
- **Setup from Mod Directory** - Parse descriptor.mod and auto-configure
- **Show Current Configuration Status** - Display detailed config information
- **Edit Configuration File** - Open config.json in your preferred editor
- **Reset to Default Configuration** - Remove user config and use defaults
- **Test Configuration System** - Run configuration validation tests
- **Back to Main Menu** - Return to main menu

#### Features
- **Color-coded output** for better readability
- **Configuration validation** before program execution
- **Multiple editor support** (nano, vim, gedit, custom)
- **Automatic environment setup**
- **Comprehensive status reporting**
- **Mod discovery and management**
- **Descriptor.mod parsing**

### Quick Start

1. **Run the menu script** (recommended):
   ```bash
   ./menu.sh
   ```

This script provides an interactive menu with:
- Environment setup and dependency installation
- Configuration management with mod support
- Main program execution
- CK3 mod discovery and management
- Test suite execution
- Helpful status information

2. **Alternative: Run the setup script directly**:
   ```bash
   ./run.sh
   ```

This script will:
- Create a Python virtual environment
- Install required dependencies
- Run the CK3 AI Weight Generator

### Manual Setup

If you prefer to set up manually:

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration** (optional):
   ```bash
   python3 setup_config.py
   ```

4. **Run the program**:
   ```bash
   python3 main.py
   ```

## CK3 Mod Folder Support

The tool now supports working with CK3 mods from both Steam Workshop and Paradox mods directories.

### Automatic Mod Discovery

The tool can automatically discover CK3 mods in:
- **Steam Workshop**: `~/.steam/steam/steamapps/workshop/content/1158310`
- **Paradox Mods**: `~/.local/share/Paradox Interactive/Crusader Kings III/mod`

### Setup from Mod Directory

You can set up the tool to work with a specific mod:

```bash
# Interactive setup
python3 setup_config.py

# Setup from a specific mod directory
python3 setup_config.py /path/to/mod
```

The tool will automatically:
- Parse the mod's `descriptor.mod` file
- Extract mod information (name, version, description)
- Configure the tool to work with that mod
- Set up appropriate paths and settings

### Mod Manager

Use the interactive mod manager to discover and configure mods:

```bash
python3 ck3_mod_manager.py
```

Features:
- Browse all available CK3 mods
- View mod details and structure
- Generate configuration snippets
- Interactive mod selection

### Configuration Structure

The new configuration system uses a unified `mod_config` section:

```json
{
  "mod_config": {
    "name": "Your Mod Name",
    "version": "1.0.0",
    "description": "Mod description",
    "project_group": "default",
    "author": "Mod Author",
    "steam_workshop_path": "~/.steam/steam/steamapps/workshop/content/1158310",
    "paradox_mod_path": "~/.local/share/Paradox Interactive/Crusader Kings III/mod",
    "mod_folder_name": "your_mod_name",
    "use_steam_workshop": true,
    "use_paradox_mods": false,
    "auto_detect_mods": true,
    "backup_mod_files": true,
    "mod_backup_suffix": ".ai_backup"
  }
}
```

## Directory Structure

```
CK3-AIs-Weight-Gen/
├── main.py                 # Main program entry point
├── ck3_parser.py           # New unified parser (extensible)
├── ck3_mod_manager.py      # Interactive mod discovery and management
├── setup_config.py         # Enhanced configuration setup
├── test_config.py          # Configuration system tests
├── config_manager.py       # Configuration management
├── ai_model_manager.py     # AI model management classes
├── event_parser.py         # CK3 event file parser
├── ck3_trigger_generator.py # CK3 trigger generation
├── model_organizer.py      # Model organization and validation tools
├── examples/               # Example scripts and demonstrations
│   ├── example_usage.py    # Usage examples and demonstrations
│   └── example_integer_weights.py # Integer weight function examples
├── requirements.txt        # Python dependencies
├── run.sh                  # Setup and run script
├── menu.sh                 # Enhanced interactive menu system
├── README.md              # This file
├── config.default.json     # Default configuration (version controlled)
├── config.json            # User configuration (ignored by git)
├── docs/                  # Documentation files
│   ├── README.md                      # Documentation index
│   ├── CONDITION_IDENTIFIER_SYSTEM.md # Condition system documentation
│   ├── CK3_SYNTAX_ANALYSIS.md         # CK3 syntax analysis
│   └── WEIGHT_CALCULATOR_README.md    # Weight calculator documentation
├── events/                # CK3 event files to process
│   ├── *.txt             # Event files with AI model references
├── models/               # AI model definitions (organized structure)
│   ├── README.md         # Model organization documentation
│   ├── Traits/           # Individual trait definitions
│   │   ├── personality_traits.json
│   │   ├── education_traits.json
│   │   └── [other_trait_files].json
│   └── Characters/       # Character model definitions
│       ├── character_models.json
│       └── [other_character_files].json
└── venv/                 # Python virtual environment (created by script)
```

## System Architecture

### Unified Trait-Based System

The CK3 AI Weight Generator uses a sophisticated three-tier architecture:

1. **Traits** (`models/Traits/`): Individual character attributes with weights and effects
2. **Character Models** (`models/Characters/`): Character archetypes that reference traits
3. **Unified AI Models**: Automatically built by combining traits and character models

This architecture provides:
- **Reusability**: Traits can be used across multiple character models
- **Maintainability**: Changes to traits automatically apply everywhere
- **Development Speed**: Quick creation of new character models by combining traits
- **Organization**: Clear separation of concerns and logical grouping

### CK3 Mod Integration

The system now includes comprehensive CK3 mod support:

1. **Mod Discovery**: Automatically finds CK3 mods in Steam Workshop and Paradox directories
2. **Descriptor Parsing**: Reads mod information from `descriptor.mod` files
3. **Path Resolution**: Intelligently resolves target paths based on configuration
4. **Backup Management**: Separate backup handling for mod files vs local files
5. **Configuration Auto-Population**: Automatically fills configuration from mod metadata

### Trait System

Traits are individual character attributes that affect AI behavior. Each trait includes:

- **Description**: What the trait represents
- **Weight**: Base influence on AI decisions
- **AI Effects**: How the trait modifies AI behavior in different situations
- **Opposite Traits**: Traits that conflict with this one

#### Example Trait Definition

```json
{
  "traits": {
    "ambitious": {
      "description": "Character is driven by ambition and seeks power",
      "weight": 50,
      "ai_effects": {
        "base_weight": 25,
        "modifiers": [
          {
            "condition": "is_ruler = yes",
            "weight_adjustment": 15
          },
          {
            "condition": "has_claim = yes",
            "weight_adjustment": 20
          }
        ]
      },
      "opposite_traits": ["content", "humble"]
    }
  }
}
```

### Character Model System

Character models define AI behavior patterns by referencing traits. Each model includes:

- **Description**: What type of character this represents
- **Base Weight**: Starting weight for this behavior
- **Traits**: Positive and negative traits that influence this model
- **Opposite Traits**: Traits that would make this model less likely
- **Modifiers**: Additional conditions that affect the model's weight

#### Example Character Model

```json
{
  "models": {
    "ambitious": {
      "description": "Ambitious character behavior model - driven by power and advancement",
      "base_weight": 75,
      "traits": {
        "positive": ["ambitious", "greedy", "proud"],
        "negative": ["content", "humble", "patient"]
      },
      "opposite_traits": ["content", "humble", "generous"],
      "modifiers": [
        {
          "condition": "is_ruler = yes",
          "weight_adjustment": 15
        },
        {
          "condition": "has_claim = yes",
          "weight_adjustment": 20
        }
      ]
    }
  }
}
```

### Unified AI Models

The system automatically builds unified `AIModel` instances that combine:
- Character model base weights and modifiers
- Trait-based conditions and weight adjustments
- Opposite trait penalties
- All necessary CK3 trigger conditions

## Configuration

The program uses a two-tier configuration system:

1. **`config.default.json`**: Default configuration file (version controlled, updated with releases)
2. **`config.json`**: User configuration file (ignored by git, for custom settings)

### Configuration Setup

#### First Time Setup
If you don't have a `config.json` file, the program will automatically use `config.default.json` and display instructions for creating your own config.

#### Creating Your Own Configuration
To create your own configuration file:

1. **Automatic method** (recommended):
   ```bash
   python3 setup_config.py
   ```

2. **Setup from mod directory**:
   ```bash
   python3 setup_config.py /path/to/mod
   ```

3. **Manual method**:
   ```bash
   cp config.default.json config.json
   ```

4. **Edit the file** with your custom settings using any text editor.

### Configuration Priority
- If `config.json` exists, it will be used
- If `config.json` doesn't exist, `config.default.json` will be used as fallback
- The program will inform you which configuration file is being used

### Program Configuration

The configuration file contains:

- **Mod Information**: Name, version, description, project group, author
- **CK3 Paths**: Steam Workshop and Paradox mods directories
- **Directories**: Paths to events and models directories
- **File Extensions**: Which file types to process
- **AI Markers**: Customizable markers for AI blocks
- **Processing Options**: Comment preservation, backup settings, etc.
- **Output Settings**: Indentation, validation, logging options

### Example Configuration

```json
{
  "mod_config": {
    "name": "My CK3 Mod",
    "version": "1.0.0",
    "description": "My custom CK3 mod",
    "project_group": "default",
    "author": "Mod Author",
    "steam_workshop_path": "~/.steam/steam/steamapps/workshop/content/1158310",
    "paradox_mod_path": "~/.local/share/Paradox Interactive/Crusader Kings III/mod",
    "mod_folder_name": "my_mod",
    "use_steam_workshop": true,
    "use_paradox_mods": false,
    "auto_detect_mods": true,
    "backup_mod_files": true,
    "mod_backup_suffix": ".ai_backup"
  },
  "program_config": {
    "events_directory": "events",
    "models_directory": "models",
    "models_file": "models/ai_models.json",
    "file_extensions": [".txt"],
    "ai_markers": {
      "library_marker": "# AI-MODEL-LIB",
      "start_marker": "# AI-START",
      "end_marker": "# AI-END",
      "model_pattern": "using:\\s*\\{([^}]+)\\}",
      "comment_pattern": "#\\s*(.+)"
    },
    "processing": {
      "preserve_comments": true,
      "delete_markers": false,
      "backup_files": true,
      "backup_suffix": ".backup"
    },
    "output": {
      "indent_level": 2,
      "validate_triggers": true,
      "show_summary": true,
      "verbose_logging": false
    },
    "target": {
      "events_directory": "events",
      "mod_folder": "",
      "should_use_mod_folder": false,
      "is_parent": false
    }
  }
}
```

### Target Configuration

The `target` section controls where the program processes event files:

- **`events_directory`**: Name of the events folder (default: "events")
- **`mod_folder`**: Path to the mod folder (empty string if not using mod)
- **`should_use_mod_folder`**: Whether to use a mod folder structure (default: false)
- **`is_parent`**: Whether the mod folder is in the parent directory (default: false)

#### Target Path Examples

1. **Local events folder** (default):
   ```json
   "target": {
     "events_directory": "events",
     "mod_folder": "",
     "should_use_mod_folder": false,
     "is_parent": false
   }
   ```
   Result: `./events/`

2. **Mod folder in current directory**:
   ```json
   "target": {
     "events_directory": "events",
     "mod_folder": "my_mod",
     "should_use_mod_folder": true,
     "is_parent": false
   }
   ```
   Result: `./my_mod/events/`

3. **Mod folder in parent directory**:
   ```json
   "target": {
     "events_directory": "events",
     "mod_folder": "my_mod",
     "should_use_mod_folder": true,
     "is_parent": true
   }
   ```
   Result: `../my_mod/events/`

4. **Absolute mod path**:
   ```json
   "target": {
     "events_directory": "events",
     "mod_folder": "/path/to/my_mod",
     "should_use_mod_folder": true,
     "is_parent": false
   }
   ```
   Result: `/path/to/my_mod/events/`

## CK3 Event File Format

The tool looks for specific markers in CK3 event files:

1. **AI-MODEL-LIB**: Marks files that use AI models
2. **AI-START**: Begins an AI block
3. **AI-END**: Ends an AI block

### Example Event File

```txt
# this file will use AI-Models generator
#################
## AI-MODEL-LIB 
#################

my_event.0001 = {
    type = character_event
    title = my_event.0001.t
    
    option = {
        name = my_event.0001.a
        
        ai_chance = {
            # AI-START
            # using: {ambitious}
            # AI-END
        }
    }
}
```

## How It Works

1. **Configuration Setup**: Loads configuration and determines target paths
2. **Mod Discovery**: If enabled, discovers available CK3 mods
3. **Trait Loading**: Loads all trait definitions from `models/Traits/`
4. **Character Model Loading**: Loads character models from `models/Characters/`
5. **Unified Model Building**: Automatically combines traits and character models
6. **File Scanning**: Scans all `.txt` files in the configured events directory (local or mod folder)
7. **AI Model Detection**: Looks for files with `# AI-MODEL-LIB` marker
8. **Block Extraction**: Extracts AI blocks marked with `# AI-START` and `# AI-STOP`
9. **Model Resolution**: Maps model names to unified AI models
10. **Trigger Generation**: Converts unified AI models into CK3 trigger code
11. **File Modification**: Replaces AI blocks with generated triggers
12. **Validation**: Checks generated triggers and trait references

## Generated Output

The tool replaces AI blocks with proper CK3 trigger code that considers all traits and conditions.

**Before:**
```txt
ai_chance = {
    # AI-START
    # using: {ambitious}
    # This is a preserved comment
    # AI-END
}
```

**After (with unified trait-based system):**
```txt
ai_chance = {
    # This is a preserved comment
    base = 75
    modifier = {
        add = 50
        has_trait = ambitious
    }
    modifier = {
        add = 30
        has_trait = greedy
    }
    modifier = {
        add = 35
        has_trait = proud
    }
    modifier = {
        add = -40
        NOT = { has_trait = content }
    }
    modifier = {
        add = -25
        NOT = { has_trait = humble }
    }
    modifier = {
        add = 15
        is_ruler = yes
    }
    modifier = {
        add = 20
        has_claim = yes
    }
}
```

## Available AI Models

The tool comes with a comprehensive set of predefined models:

### Character Models

- **historical**: Historical character behavior - focuses on scholarly and diplomatic pursuits
- **ambitious**: Ambitious character behavior - driven by power and advancement
- **cautious**: Cautious character behavior - careful and risk-averse
- **aggressive**: Aggressive character behavior - warlike and confrontational
- **diplomatic**: Diplomatic character behavior - skilled in negotiation and relationships
- **scholarly**: Scholarly character behavior - focused on learning and knowledge
- **merchant**: Merchant character behavior - focused on trade and wealth
- **religious**: Religious character behavior - pious and faith-driven

### Trait Categories

#### Personality Traits
- **ambitious**: Driven by ambition and seeks power (Weight: 50)
- **content**: Satisfied with current position (Weight: -40)
- **brave**: Courageous and fearless (Weight: 40)
- **craven**: Fearful and avoids danger (Weight: -50)
- **greedy**: Motivated by wealth (Weight: 30)
- **generous**: Giving and charitable (Weight: -20)
- **wrathful**: Quick to anger and vengeful (Weight: 30)
- **calm**: Composed and level-headed (Weight: -25)
- **paranoid**: Suspicious and distrustful (Weight: 25)
- **trusting**: Open and trusting of others (Weight: -20)
- **proud**: Values status and reputation (Weight: 35)
- **skeptical**: Questions authority and tradition (Weight: 15)

#### Education Traits
- **historian**: Scholarly knowledge of history (Weight: 25)
- **scholar**: Well-educated and learned (Weight: 20)
- **diplomat**: Skilled in diplomacy and negotiation (Weight: 40)
- **zealous**: Deeply religious and pious (Weight: -10)
- **cynical**: Skeptical of religion and tradition (Weight: 10)
- **gregarious**: Outgoing and sociable (Weight: 25)
- **shy**: Introverted and uncomfortable socially (Weight: -20)
- **awkward**: Socially awkward and lacks grace (Weight: -30)
- **ignorant**: Lacks education and knowledge (Weight: -40)
- **illiterate**: Cannot read or write (Weight: -50)
- **humble**: Modest and unassuming (Weight: -25)
- **berserker**: Fierce and battle-crazed (Weight: 50)
- **reckless**: Acts without considering consequences (Weight: 35)
- **patient**: Willing to wait and plan carefully (Weight: -30)

## Documentation

The project includes comprehensive documentation organized in the `docs/` folder:

### Documentation Index

- **[Documentation Overview](docs/README.md)**: Complete index of all available documentation

### Available Documentation

- **[Condition Identifier System](docs/CONDITION_IDENTIFIER_SYSTEM.md)**: Detailed guide to the condition system architecture, including condition identifiers, input values, custom triggers, and dollar symbol variables
- **[CK3 Syntax Analysis](docs/CK3_SYNTAX_ANALYSIS.md)**: Analysis of CK3 AI chance trigger syntax and validation of generated code
- **[Weight Calculator Documentation](docs/WEIGHT_CALCULATOR_README.md)**: Guide to the weight calculation system and available scripts

### Model Documentation

The system also auto-generates model documentation:
- **Auto-generated**: `model_documentation.md` - Comprehensive documentation of all models and traits
- **Model Organization**: `models/README.md` - Guide to the model organization system

## Development Tools

### Model Organizer

The `model_organizer.py` script provides utilities for managing the AI model system:

```bash
python model_organizer.py
```

**Features:**
- **Validation**: Check that all trait references exist
- **Documentation**: Generate comprehensive model documentation
- **Templates**: Create templates for new traits and character models
- **Summary**: Get overview of all models and traits

### CK3 Mod Manager

The `ck3_mod_manager.py` script provides interactive mod discovery and management:

```bash
python ck3_mod_manager.py
```

**Features:**
- **Mod Discovery**: Find all available CK3 mods
- **Mod Details**: View mod information and structure
- **Configuration Snippets**: Generate configuration for specific mods
- **Interactive Selection**: Browse and select mods

### Configuration Setup

The `setup_config.py` script provides enhanced configuration setup:

```bash
# Interactive setup
python setup_config.py

# Setup from mod directory
python setup_config.py /path/to/mod
```

**Features:**
- **Interactive Setup**: Guided configuration creation
- **Mod Integration**: Automatic setup from descriptor.mod files
- **Path Detection**: Auto-detect CK3 installation paths
- **Configuration Testing**: Validate configuration settings

### Example Usage

The `examples/example_usage.py` script demonstrates how to use the system:

```bash
python examples/example_usage.py
```

**Demonstrations:**
- Trait system usage
- Character model management
- Weight calculation examples
- Validation system
- Template creation

## Customization

### Adding New Traits

1. Create or edit a file in `models/Traits/` (e.g., `models/Traits/personality_traits.json`)
2. Add the trait definition with weight, effects, and opposites
3. The trait is automatically available to all character models

**Example:**
```json
{
  "traits": {
    "charismatic": {
      "description": "Character has natural charm and leadership",
      "weight": 45,
      "ai_effects": {
        "base_weight": 25,
        "modifiers": [
          {
            "condition": "is_ruler = yes",
            "weight_adjustment": 20
          }
        ]
      },
      "opposite_traits": ["shy", "awkward"]
    }
  }
}
```

### Creating New Character Models

1. Create or edit a file in `models/Characters/` (e.g., `models/Characters/character_models.json`)
2. Reference existing traits from the Traits folder
3. Define positive/negative trait associations
4. Add specific modifiers for the character type

**Example:**
```json
{
  "models": {
    "charismatic_leader": {
      "description": "Charismatic leader character model",
      "base_weight": 60,
      "traits": {
        "positive": ["charismatic", "gregarious", "diplomat"],
        "negative": ["shy", "awkward", "paranoid"]
      },
      "opposite_traits": ["shy", "awkward"],
      "modifiers": [
        {
          "condition": "is_ruler = yes",
          "weight_adjustment": 25
        }
      ]
    }
  }
}
```

### Using Templates

The model organizer provides template creation:

```python
from model_organizer import ModelOrganizer

organizer = ModelOrganizer()

# Create trait template
trait_template = organizer.create_trait_template("new_trait")

# Create character model template
model_template = organizer.create_character_model_template("new_model")
```

## Validation and Quality Assurance

### Trait Reference Validation

The system automatically validates that all trait references in character models exist:

```bash
python model_organizer.py
```

**Validation checks:**
- All referenced traits exist in trait files
- No missing trait definitions
- Consistent trait naming

### Configuration Validation

The system includes configuration validation:

```bash
python test_config.py
```

**Validation checks:**
- Configuration file loading
- Descriptor.mod parsing
- Path resolution
- Mod discovery

### Trigger Validation

Generated triggers are validated for common issues:

- Negative weights
- Empty conditions
- Invalid CK3 condition formats
- Zero weight adjustments

### Documentation Generation

Auto-generated documentation includes:

- Complete trait listings with descriptions and weights
- Character model details and trait associations
- Usage statistics and validation results
- Template examples for new development

## Advanced Usage

### Programmatic Access

```python
from ai_model_manager import AIModelManager
from config_manager import ConfigManager

# Initialize managers
config_manager = ConfigManager("config.json")
model_manager = AIModelManager(config_manager)

# Access traits
trait_manager = model_manager.get_trait_manager()
ambitious_trait = trait_manager.get_trait("ambitious")

# Access character models
character_model = model_manager.get_character_model("ambitious")

# Access unified models
unified_model = model_manager.get_model("ambitious")

# Generate triggers
from ck3_trigger_generator import CK3TriggerGenerator
generator = CK3TriggerGenerator(config_manager)
trigger = generator.generate_trigger_from_model(unified_model)
```

### CK3 Parser Usage

The new unified parser provides extensible file processing:

```python
from ck3_parser import CK3Parser

# Initialize parser
parser = CK3Parser("config.json")

# Setup environment
parser.setup_environment()

# Parse all supported file types
summary = parser.parse_all()

# Apply changes
parser.apply_changes(summary)

# Print summary
parser.print_summary(summary)
```

### Weight Calculation

The system automatically calculates weights based on:

1. **Base Weight**: Character model's base weight
2. **Positive Traits**: Add trait weights when character has positive traits
3. **Negative Traits**: Subtract trait weights when character lacks negative traits
4. **Opposite Traits**: Strongly subtract weights when character has opposite traits
5. **Modifiers**: Add conditional weight adjustments

### Condition Generation

The system generates CK3 conditions for:

- **Positive Traits**: `has_trait = trait_name`
- **Negative Traits**: `NOT = { has_trait = trait_name }`
- **Opposite Traits**: `NOT = { has_trait = trait_name }`
- **Modifiers**: Custom conditions from character models and traits

## Troubleshooting

### Common Issues

1. **"Trait not found"**: Ensure trait exists in `models/Traits/` files
2. **"Character model not found"**: Check `models/Characters/` files
3. **"Validation failed"**: Run `model_organizer.py` to identify issues
4. **"Unknown model"**: Verify model names in event files match character model names
5. **"Mod not found"**: Check CK3 installation paths in configuration
6. **"Descriptor.mod parsing failed"**: Ensure mod directory contains valid descriptor.mod file

### Validation Errors

Common validation issues and solutions:

- **Missing traits**: Add missing trait definitions to trait files
- **Invalid conditions**: Check CK3 condition syntax (see [CK3 Syntax Analysis](docs/CK3_SYNTAX_ANALYSIS.md))
- **Negative weights**: Review trait weight values
- **Empty conditions**: Ensure all modifiers have conditions
- **Path resolution issues**: Check target configuration settings

### Debugging

Enable detailed logging by modifying `config.json`:

```json
{
  "program_config": {
    "output": {
      "validate_triggers": true,
      "show_summary": true,
      "verbose_logging": true
    }
  }
}
```

### Documentation References

For detailed information on specific systems:
- **Condition System**: See [Condition Identifier System](docs/CONDITION_IDENTIFIER_SYSTEM.md)
- **Weight Calculation**: See [Weight Calculator Documentation](docs/WEIGHT_CALCULATOR_README.md)
- **CK3 Syntax**: See [CK3 Syntax Analysis](docs/CK3_SYNTAX_ANALYSIS.md)

## Performance and Scalability

### Model Loading

- **Traits**: Loaded once at startup
- **Character Models**: Loaded once at startup
- **Unified Models**: Built automatically from traits and character models
- **Caching**: All models cached in memory for fast access

### File Processing

- **Parallel Processing**: Event files can be processed in parallel
- **Memory Efficient**: Large trait sets handled efficiently
- **Incremental Updates**: Only modified files are reprocessed

### Mod Discovery

- **Cached Discovery**: Mod information cached for faster subsequent runs
- **Incremental Scanning**: Only scans for changes in mod directories
- **Efficient Parsing**: Fast descriptor.mod parsing with regex optimization

### Optimization Tips

1. **Group Related Traits**: Keep related traits in the same file
2. **Reuse Traits**: Reference existing traits rather than creating duplicates
3. **Validate Early**: Run validation before processing large event sets
4. **Use Templates**: Leverage template system for consistent development
5. **Configure Paths**: Set up proper CK3 paths for faster mod discovery

## Contributing

To add new features or fix bugs:

1. **Fork the repository**
2. **Create a feature branch**
3. **Follow the trait-based architecture**:
   - Add traits to appropriate `models/Traits/` files
   - Create character models in `models/Characters/` files
   - Ensure all trait references are valid
4. **Test thoroughly**:
   - Run `model_organizer.py` for validation
   - Run `test_config.py` for configuration validation
   - Test with example event files
   - Verify trigger generation
   - Test with CK3 mods
5. **Submit a pull request**

### Development Guidelines

- **Trait Organization**: Group related traits logically
- **Naming Conventions**: Use descriptive, consistent names
- **Documentation**: Update documentation for new features
- **Validation**: Ensure all changes pass validation
- **Testing**: Test with various event file formats and mod structures
- **CK3 Compatibility**: Ensure generated triggers work with current CK3 versions

## License

This project is licensed under a custom license that allows free use and commercial purposes but prevents selling of the software.

### License Terms

- **Free Use**: Anyone can use the software without charge
- **Commercial Use Allowed**: Can be used in commercial projects and businesses
- **No Selling**: Explicitly prohibits selling the software itself
- **Attribution Required**: Ensures proper credit to original authors
- **Modification Allowed**: Users can modify and distribute the software
- **License Control**: Donekulda maintains full control and ownership rights over this license and software

### Contact

For questions about this license, please contact Donekulda (mikulas.stnaek@protonmail.com).

See the [LICENSE](LICENSE) file for complete license terms.

## Support

For issues or questions:

1. **Check the troubleshooting section**
2. **Review the example files**
3. **Run validation tools**: 
   - `python model_organizer.py`
   - `python test_config.py`
4. **Check documentation**: 
   - [Model Organization](models/README.md)
   - [Condition System](docs/CONDITION_IDENTIFIER_SYSTEM.md)
   - [CK3 Syntax](docs/CK3_SYNTAX_ANALYSIS.md)
   - [Weight Calculator](docs/WEIGHT_CALCULATOR_README.md)
5. **Ensure your CK3 event files follow the expected format**
6. **Verify CK3 mod paths are correctly configured**

## Version History

### v3.0 - CK3 Mod Folder Support
- **New**: Full CK3 mod folder support (Steam Workshop & Paradox Mods)
- **New**: Interactive mod discovery and management
- **New**: Descriptor.mod parsing and auto-configuration
- **New**: Enhanced menu system with mod support
- **New**: Unified parser for future extensibility
- **New**: Configuration testing and validation
- **Improved**: Enhanced path resolution and target handling
- **Improved**: Better mod integration and backup management

### v2.0 - Unified Trait-Based System
- **New**: Trait-based architecture with organized model structure
- **New**: Character models that reference traits
- **New**: Automatic unified model building
- **New**: Comprehensive validation system
- **New**: Model organizer and documentation tools
- **Improved**: Better organization and maintainability
- **Improved**: Enhanced development speed and reusability

### v1.0 - Legacy System
- Basic AI model management
- Simple JSON-based model definitions
- Event file processing
- Trigger generation 