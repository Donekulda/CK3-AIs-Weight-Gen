# CK3 Condition Identifier System

## Overview

The Condition Identifier System is a new architecture that separates CK3 condition definitions from character models, making conditions self-editable and more flexible. This system uses condition identifiers, input values, custom triggers, and dollar symbol variables to create a more maintainable and extensible condition system.

## Key Features

### 1. Condition Identifiers
Instead of hardcoding conditions in character models, conditions are now referenced by identifiers:

**Old Format:**
```json
{
  "condition": "is_ruler = yes",
  "weight_adjustment": 15
}
```

**New Format:**
```json
{
  "condition_identifier": "IS_RULER",
  "condition_values": {"yes": "yes"},
  "weight_adjustment": 15
}
```

### 2. Input Values with Validation
Conditions can accept input values that are validated for correctness:

```json
{
  "condition_identifier": "WEALTH",
  "condition_values": {
    "operator": "<",
    "wealth_threshold": "500"
  },
  "weight_adjustment": 15
}
```

### 3. Custom Triggers
Predefined trigger combinations for common scenarios:

```json
{
  "condition_identifier": "WEALTH",
  "condition_values": {"poor": "poor"},
  "weight_adjustment": 15
}
```

This generates: `wealth < 100`

### 4. Dollar Symbol Variables
Dynamic variable replacement in condition syntax:

```json
{
  "syntax": "wealth $operator $wealth_threshold",
  "input_values": {
    "operator": "<, <=, =, !=, >, >=",
    "wealth_threshold": "Numeric threshold value"
  }
}
```

## Condition Categories

### Character Status Conditions
- `IS_RULER` - Is the character a ruler?
- `IS_HEIR` - Is the character an heir?
- `IS_COMMANDER` - Is the character a commander?
- `IS_AT_WAR` - Is the character at war?

### Character Trait Conditions
- `HAS_TRAIT` - Does the character have a specific trait?

### Character Resource Conditions
- `WEALTH` - Character's wealth amount
- `PRESTIGE` - Character's prestige amount
- `PIETY` - Character's piety amount

### Character Skill Conditions
- `DIPLOMACY` - Character's diplomacy skill
- `MARTIAL` - Character's martial skill
- `STEWARDSHIP` - Character's stewardship skill
- `INTRIGUE` - Character's intrigue skill
- `LEARNING` - Character's learning skill

### Character Claim Conditions
- `HAS_CLAIM_ON` - Does the character have a claim on a title?

### Character Relationship Conditions
- `HAS_RIVAL` - Does the character have a rival?
- `HAS_ENEMY` - Does the character have an enemy?

### Character Education Conditions
- `HAS_EDUCATION_LEARNING` - Does the character have learning education?
- `HAS_EDUCATION_DIPLOMACY` - Does the character have diplomacy education?
- `HAS_EDUCATION_MARTIAL` - Does the character have martial education?
- `HAS_EDUCATION_STEWARDSHIP` - Does the character have stewardship education?
- `HAS_EDUCATION_INTRIGUE` - Does the character have intrigue education?

### Character Court Conditions
- `IS_COURT_CHANCELLOR` - Is the character a court chancellor?
- `IS_COURT_CHAPLAIN` - Is the character a court chaplain?
- `IS_COURT_SPYMASTER` - Is the character a court spymaster?
- `IS_COURT_PHYSICIAN` - Is the character a court physician?

## Usage Examples

### Basic Boolean Conditions
```json
{
  "condition_identifier": "IS_RULER",
  "condition_values": {"yes": "yes"},
  "weight_adjustment": 15
}
```
Generates: `is_ruler = yes`

### Trait Conditions
```json
{
  "condition_identifier": "HAS_TRAIT",
  "condition_values": {"trait_name": "ambitious"},
  "weight_adjustment": 20
}
```
Generates: `has_trait = ambitious`

### Comparison Conditions
```json
{
  "condition_identifier": "WEALTH",
  "condition_values": {
    "operator": "<",
    "wealth_threshold": "500"
  },
  "weight_adjustment": 15
}
```
Generates: `wealth < 500`

### Custom Triggers
```json
{
  "condition_identifier": "WEALTH",
  "condition_values": {"rich": "rich"},
  "weight_adjustment": 15
}
```
Generates: `wealth > 5000`

### Complex Conditions
```json
{
  "condition_identifier": "HAS_CLAIM_ON",
  "condition_values": {"title_scope": "ROOT"},
  "weight_adjustment": 20
}
```
Generates: `has_claim_on = { title = ROOT }`

## Custom Triggers Available

### WEALTH Custom Triggers
- `poor` → `wealth < 100`
- `modest` → `wealth < 500`
- `wealthy` → `wealth > 1000`
- `rich` → `wealth > 5000`

### PRESTIGE Custom Triggers
- `low_prestige` → `prestige < 100`
- `modest_prestige` → `prestige < 1000`
- `high_prestige` → `prestige > 1000`
- `legendary_prestige` → `prestige > 5000`

### HAS_TRAIT Custom Triggers
- `ambitious`, `content`, `brave`, `craven`, `greedy`, `generous`
- `wrathful`, `calm`, `paranoid`, `trusting`, `proud`, `humble`
- `patient`, `reckless`, `zealous`, `cynical`, `scholar`, `diplomat`
- `merchant`, `berserker`

### Skill Custom Triggers
For each skill (DIPLOMACY, MARTIAL, STEWARDSHIP, INTRIGUE, LEARNING):
- `low_[skill]` → `[skill] < 5`
- `modest_[skill]` → `[skill] < 10`
- `high_[skill]` → `[skill] > 10`
- `master_[skill]` → `[skill] > 15`

## Adding New Conditions

To add a new condition:

1. **Add to condition_models.json:**
```json
{
  "conditions": {
    "character_new_category": {
      "description": "New category description",
      "conditions": {
        "NEW_CONDITION": {
          "description": "Description of the new condition",
          "syntax": "ck3_syntax_with_$variables",
          "input_values": {
            "variable_name": "Description of the variable"
          },
          "custom_triggers": {
            "trigger_name": "predefined_trigger_syntax"
          },
          "supported_scopes": ["character"],
          "ai_relevance": "high|medium|low",
          "condition_type": "boolean|comparison|trait|claim|complex"
        }
      }
    }
  }
}
```

2. **Use in character models:**
```json
{
  "condition_identifier": "NEW_CONDITION",
  "condition_values": {"variable_name": "value"},
  "weight_adjustment": 10
}
```

## Benefits

### 1. Separation of Concerns
- Conditions are defined separately from character models
- Easy to modify conditions without touching character models
- Centralized condition management

### 2. Self-Editable
- Conditions can be edited independently
- No need to modify code to add new conditions
- JSON-based configuration

### 3. Validation
- Input values are validated for correctness
- Prevents invalid condition syntax
- Better error messages

### 4. Custom Triggers
- Predefined common trigger combinations
- Reduces repetition in character models
- Easy to use common scenarios

### 5. Dollar Symbol Variables
- Dynamic value replacement
- Flexible condition syntax
- Support for complex conditions

### 6. Extensibility
- Easy to add new conditions
- Easy to add new custom triggers
- Backward compatible with legacy format

## Migration from Legacy Format

The system maintains backward compatibility. Character models can still use the old format:

```json
{
  "condition": "is_ruler = yes",
  "weight_adjustment": 15
}
```

But it's recommended to migrate to the new format for better maintainability.

## Testing

Use the test script to verify the system:

```bash
python test_condition_identifiers.py
```

This will test:
- Condition identifier generation
- Custom trigger usage
- Dollar symbol variable replacement
- Validation
- Integration with character models

## File Structure

```
models/
├── Conditions/
│   └── condition_models.json    # Condition definitions
├── Characters/
│   └── character_models.json    # Character models (updated)
└── Traits/
    ├── personality_traits.json
    └── education_traits.json
```

## API Reference

### ConditionManager Methods

- `get_condition_by_identifier(identifier)` - Get condition by ID
- `generate_condition_from_identifier(identifier, **kwargs)` - Generate condition string
- `validate_condition_identifier(identifier, **kwargs)` - Validate condition
- `get_custom_triggers_for_condition(identifier)` - Get custom triggers
- `list_condition_identifiers_by_type(type)` - List conditions by type

### CK3TriggerGenerator Methods

- `generate_trigger_from_model(model)` - Generate trigger from model
- `get_available_conditions()` - Get all available conditions
- `get_conditions_by_relevance(relevance)` - Get conditions by relevance

## Conclusion

The Condition Identifier System provides a more flexible, maintainable, and extensible way to handle CK3 conditions. It separates concerns, provides validation, supports custom triggers, and uses dollar symbol variables for dynamic content. This makes the system much easier to maintain and extend while providing better error checking and user experience. 