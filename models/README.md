# CK3 AI Models Organization

This directory contains the organized AI models for CK3 AI Weight Generator, structured for better maintainability, reusability, and faster development.

## Directory Structure

```
models/
├── Traits/                    # Individual trait definitions
│   ├── personality_traits.json
│   ├── education_traits.json
│   └── [other_trait_files].json
├── Characters/                # Character models that reference traits
│   ├── character_models.json
│   └── [other_character_files].json
└── README.md                  # This file
```

## System Overview

### Traits System (`Traits/` folder)

Traits are individual character attributes that affect AI behavior. Each trait is defined with:

- **Description**: What the trait represents
- **Weight**: Base influence on AI decisions
- **AI Effects**: How the trait modifies AI behavior in different situations
- **Opposite Traits**: Traits that conflict with this one

#### Trait Structure
```json
{
  "traits": {
    "trait_name": {
      "description": "Description of the trait",
      "weight": 25,
      "ai_effects": {
        "base_weight": 15,
        "modifiers": [
          {
            "condition": "has_education_learning_trigger = yes",
            "weight_adjustment": 10
          }
        ]
      },
      "opposite_traits": ["opposite_trait1", "opposite_trait2"]
    }
  }
}
```

### Character Models System (`Characters/` folder)

Character models define AI behavior patterns by referencing traits. Each model includes:

- **Description**: What type of character this represents
- **Base Weight**: Starting weight for this behavior
- **Traits**: Positive and negative traits that influence this model
- **Opposite Traits**: Traits that would make this model less likely
- **Modifiers**: Additional conditions that affect the model's weight

#### Character Model Structure
```json
{
  "models": {
    "model_name": {
      "description": "Description of the character type",
      "base_weight": 50,
      "traits": {
        "positive": ["trait1", "trait2"],
        "negative": ["trait3", "trait4"]
      },
      "opposite_traits": ["opposite_trait1", "opposite_trait2"],
      "modifiers": [
        {
          "condition": "is_ruler = yes",
          "weight_adjustment": 15
        }
      ]
    }
  }
}
```

## Benefits of This Organization

### 1. **Reusability**
- Traits can be used across multiple character models
- No need to redefine trait effects for each model
- Easy to maintain consistent trait behavior

### 2. **Maintainability**
- Changes to trait effects automatically apply to all models using that trait
- Clear separation of concerns between traits and character models
- Easy to add new traits without modifying existing models

### 3. **Development Speed**
- Quick to create new character models by combining existing traits
- Template system for rapid model creation
- Validation tools to catch missing trait references

### 4. **Organization**
- Logical grouping of related traits
- Clear distinction between individual traits and character archetypes
- Easy to find and modify specific components

## Usage Examples

### Adding a New Trait

1. Create or edit a file in `Traits/` folder
2. Add the trait definition with weight, effects, and opposites
3. The trait is automatically available to all character models

### Creating a New Character Model

1. Create or edit a file in `Characters/` folder
2. Reference existing traits from the Traits folder
3. Define positive/negative trait associations
4. Add specific modifiers for the character type

### Validation

Use the `model_organizer.py` script to:
- Validate that all trait references exist
- Generate documentation
- Create templates for new traits/models
- Check for unused traits

## File Naming Conventions

- **Trait files**: Use descriptive names like `personality_traits.json`, `education_traits.json`
- **Character model files**: Use descriptive names like `character_models.json`, `noble_models.json`
- **All files**: Use lowercase with underscores, `.json` extension

## Best Practices

1. **Trait Organization**: Group related traits in the same file (e.g., all personality traits together)
2. **Opposite Traits**: Always define opposite traits to create logical conflicts
3. **Weight Balance**: Ensure positive and negative traits have balanced weights
4. **Documentation**: Keep trait descriptions clear and concise
5. **Validation**: Run the model organizer regularly to catch issues early

## Migration from Legacy System

The system supports both the new trait-based format and the legacy format. The `AIModelManager` automatically detects which format is being used and loads models accordingly.

To migrate legacy models:
1. Extract individual traits into `Traits/` files
2. Create character models in `Characters/` files that reference those traits
3. Use the validation tools to ensure all references are correct

## Tools and Utilities

- `model_organizer.py`: Main utility for managing and validating the system
- `ai_model_manager.py`: Core manager that loads and provides access to models
- `model_documentation.md`: Auto-generated documentation of all models and traits

For more information, see the main project README and the documentation in the `docs/` folder:
- [Condition Identifier System](../docs/CONDITION_IDENTIFIER_SYSTEM.md)
- [CK3 Syntax Analysis](../docs/CK3_SYNTAX_ANALYSIS.md)
- [Weight Calculator Documentation](../docs/WEIGHT_CALCULATOR_README.md) 