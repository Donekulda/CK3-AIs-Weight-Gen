# Trait Interactions System

The CK3 AI Weight Generator now supports a comprehensive trait interaction system that defines how different character traits interact with each other. These interactions are defined in JSON files alongside the trait definitions, making them easy to configure and extend.

## Overview

Trait interactions allow for more nuanced AI behavior by defining relationships between traits:
- **Synergistic interactions**: Traits that work well together and enhance each other's effects
- **Antagonistic interactions**: Conflicting traits that create internal struggles and reduced effectiveness
- **Conditional interactions**: Traits that have special effects only under certain game conditions

## JSON Structure

Trait interactions are defined in the same JSON files as traits, under an `"interactions"` key:

```json
{
  "traits": {
    // ... trait definitions ...
  },
  "interactions": [
    {
      "trait_combination": ["trait1", "trait2"],
      "interaction_type": "synergy",
      "weight_modifier": 15,
      "description": "Description of the interaction effect"
    },
    {
      "trait_combination": ["trait3", "trait4"],
      "interaction_type": "conditional",
      "weight_modifier": 10,
      "description": "Conditional interaction description",
      "conditions": ["game_condition = value"]
    }
  ]
}
```

## Interaction Fields

### Required Fields

- **`trait_combination`**: Array of trait names that must all be present for the interaction to trigger
- **`interaction_type`**: Type of interaction - `"synergy"`, `"antagonism"`, or `"conditional"`
- **`weight_modifier`**: Integer weight adjustment applied when the interaction is active
- **`description`**: Human-readable description of what the interaction represents

### Optional Fields

- **`conditions`**: Array of CK3 game conditions (only for conditional interactions)

## Interaction Types

### Synergy
Positive interactions between compatible traits that enhance each other.

**Example:**
```json
{
  "trait_combination": ["ambitious", "diligent"],
  "interaction_type": "synergy",
  "weight_modifier": 10,
  "description": "Ambitious and diligent characters work tirelessly toward their goals"
}
```

### Antagonism
Negative interactions between conflicting traits that cause internal conflict.

**Example:**
```json
{
  "trait_combination": ["brave", "craven"],
  "interaction_type": "antagonism",
  "weight_modifier": -20,
  "description": "Conflicting courage traits create internal conflict and indecision"
}
```

### Conditional
Interactions that only apply under specific game conditions.

**Example:**
```json
{
  "trait_combination": ["zealous", "just"],
  "interaction_type": "conditional",
  "weight_modifier": 15,
  "description": "Religious zealots with strong justice are especially effective with same-faith subjects",
  "conditions": ["faith = ROOT.faith"]
}
```

## Current Interactions

### Personality Trait Interactions (personality_traits.json)

**Synergistic Interactions:**
- `ambitious + greedy`: Material gain focus (+15)
- `brave + wrathful`: Combat aggression (+10)
- `patient + calm`: Thoughtful decision-making (+8)
- `generous + just`: Ideal ruler perception (+12)
- `brave + honest`: Loyalty inspiration (+8)
- `ambitious + diligent`: Goal-oriented work (+10)
- `gregarious + generous`: Social network building (+12)

**Antagonistic Interactions:**
- `brave + craven`: Internal courage conflict (-20)
- `generous + greedy`: Generosity contradiction (-15)
- `trusting + paranoid`: Trust level conflict (-18)
- `honest + deceitful`: Honesty contradiction (-16)
- `patient + wrathful`: Temperament opposition (-14)
- `humble + arrogant`: Ego conflict (-18)
- `diligent + lazy`: Work ethic opposition (-20)
- `zealous + cynical`: Religious-cynical conflict (-22)

**Conditional Interactions:**
- `gregarious + shy`: Social conflict at court (-10 when `is_at_court = yes`)
- `zealous + just`: Same-faith effectiveness (+15 when `faith = ROOT.faith`)
- `ambitious + ruthless`: Wartime effectiveness (+12 when `is_at_war = yes`)
- `paranoid + spymaster`: Intrigue focus bonus (+8 when `has_focus = intrigue_focus`)
- `brave + berserker`: Battle effectiveness (+18 when `is_in_battle = yes`)
- `content + just`: Peacetime appreciation (+10 when `is_at_war = no`)

### Education Trait Interactions (education_traits.json)

**Synergistic Interactions:**
- `scholar + historian`: Enhanced learning (+12)
- `diplomat + gregarious`: International relationships (+15)
- `strategist + patient`: Long-term planning (+10)
- `administrator + diligent`: Organizational efficiency (+14)
- `theologian + zealous`: Religious leadership (+16)
- `physician + compassionate`: Patient care (+12)
- `architect + perfectionist`: Exceptional structures (+11)

**Conditional Interactions:**
- `scholar + cynical`: Doctrine questioning (+8 when `has_focus = learning_focus`)
- `diplomat + honest`: Peaceful negotiation trust (+12 when `is_at_war = no`)
- `strategist + ruthless`: Military campaign effectiveness (+15 when `is_at_war = yes`)
- `administrator + just`: Legal reform value (+13 when `is_ruler = yes`)
- `theologian + humble`: Common people acceptance (+10 when `NOT = { is_ruler = yes }`)
- `physician + brave`: Battle medicine (+14 when `is_in_battle = yes`)

## Adding Custom Interactions

### In JSON Files
Add new interactions directly to the JSON files in the `models/Traits/` directory:

```json
{
  "trait_combination": ["your_trait1", "your_trait2"],
  "interaction_type": "synergy",
  "weight_modifier": 8,
  "description": "Your custom interaction description"
}
```

### Programmatically
Add interactions at runtime using the API:

```python
from ai_model_manager import AIModelManager, TraitInteraction

ai_manager = AIModelManager()

custom_interaction = TraitInteraction(
    trait_combination=["trait1", "trait2"],
    interaction_type="synergy",
    weight_modifier=10,
    description="Custom runtime interaction"
)

ai_manager.add_custom_trait_interaction(custom_interaction)
```

## Usage in AI Models

Trait interactions are automatically applied when building unified AI models:

1. The system detects which interactions apply to a character model's traits
2. Synergistic and antagonistic interactions add their weight modifiers directly
3. Conditional interactions add CK3 conditions that are evaluated at runtime
4. All interactions are included in the generated CK3 triggers

## Best Practices

1. **Realistic Interactions**: Base interactions on realistic psychological and social dynamics
2. **Balanced Weights**: Use moderate weight adjustments to avoid overwhelming base trait effects
3. **Clear Descriptions**: Write descriptive text that explains the interaction's narrative purpose
4. **Test Thoroughly**: Validate interactions in actual CK3 gameplay scenarios
5. **Avoid Conflicts**: Ensure trait combinations make logical sense together

## CK3 Condition Examples

Common conditions for conditional interactions:
- `is_ruler = yes/no`
- `is_at_war = yes/no`
- `faith = ROOT.faith`
- `culture = ROOT.culture`
- `has_focus = [focus_type]`
- `is_at_court = yes/no`
- `is_in_battle = yes/no`
- `age >= 30`
- `prestige >= 1000`

## Validation

The system automatically validates trait interactions:
- Checks that all referenced traits exist
- Warns about conflicting trait combinations
- Reports interaction statistics and usage
- Validates weight calculations include interaction effects

Use the validation system to ensure your custom interactions work correctly:

```python
ai_manager = AIModelManager()
validation_results = ai_manager.validate_all_models()
``` 