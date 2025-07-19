# CK3 AI Weight Calculator

This directory contains scripts to calculate and display the complete weight values for all AI models in the CK3 AI Weight Generator system.

## Scripts Overview

### 1. `quick_weight_check.py` - Quick Weight Overview
A simple script that quickly displays the current weight values for all AI models without interactive prompts.

**Usage:**
```bash
python quick_weight_check.py
```

**Output:**
- Shows base weight, trait contributions, modifiers, and total weight for each model
- Displays positive traits (✅), negative traits (❌), opposite traits (🚫), and modifiers (⚙️)
- Provides a quick overview of all 8 character models

### 2. `weight_calculator.py` - Detailed Weight Calculator
A comprehensive interactive script that provides detailed weight breakdowns and export options.

**Usage:**
```bash
python weight_calculator.py
```

**Features:**
- Interactive menu with options to:
  1. Show detailed breakdown for all models
  2. Show detailed breakdown for specific model
  3. Export to JSON file
  4. Exit
- Detailed breakdown showing:
  - Base weight
  - Individual trait contributions with descriptions
  - Modifier breakdowns with conditions
  - Total calculated weight

### 3. `check_weights.sh` - Shell Script Wrapper
A convenient shell script that handles virtual environment activation and runs the quick weight check.

**Usage:**
```bash
./check_weights.sh
```

## Weight Calculation Logic

The weight calculation follows this formula:

```
Total Weight = Base Weight + Positive Traits + Modifiers - Negative Traits - Opposite Traits
```

### Components:

1. **Base Weight**: The starting weight defined in the character model
2. **Positive Traits**: Traits that increase the weight when present
3. **Negative Traits**: Traits that decrease the weight (applied as NOT conditions)
4. **Opposite Traits**: Traits that strongly decrease the weight (applied as NOT conditions)
5. **Modifiers**: Conditional weight adjustments from both character models and traits

### Example Calculation:

For the "Historical" model:
- Base Weight: 50
- Positive Traits: historian(+25) + scholar(+20) + diplomat(+40) + gregarious(+25) = +110
- Negative Traits: zealous(-10) + shy(-20) + reckless(+35) = +5 (NOT conditions)
- Opposite Traits: illiterate(-50) + ignorant(-40) + awkward(-30) + cynical(+10) = -110 (NOT conditions)
- Modifiers: +25
- **Total: 50 + 110 + 5 - 110 + 25 = 290**

## Current Model Weights

Based on the current configuration:

| Model | Base Weight | Total Weight | Description |
|-------|-------------|--------------|-------------|
| Historical | 50 | 290 | Scholarly and diplomatic pursuits |
| Ambitious | 75 | 405 | Power and advancement driven |
| Cautious | 60 | -100 | Careful and risk-averse |
| Aggressive | 80 | 505 | Warlike and confrontational |
| Diplomatic | 70 | 105 | Negotiation and relationships |
| Scholarly | 65 | 120 | Learning and knowledge focused |
| Merchant | 55 | 205 | Trade and wealth focused |
| Religious | 45 | -135 | Pious and faith-driven |

## Files Used

The scripts read from these configuration files:
- `models/Characters/character_models.json` - Character model definitions
- `models/Traits/personality_traits.json` - Personality trait definitions
- `models/Traits/education_traits.json` - Education trait definitions

## Troubleshooting

1. **Import Errors**: Make sure you're running from the project root directory
2. **File Not Found**: Ensure all model and trait JSON files exist
3. **Virtual Environment**: Use `./check_weights.sh` to automatically activate the virtual environment

## Output Formats

### Quick Check Format:
```
🎯 MODEL_NAME
   Base Weight: 50
   Description: Model description
   ✅ Positive: trait1(+25), trait2(+20)
   ❌ Negative: trait3(-10), trait4(-20)
   🚫 Opposite: trait5(-30), trait6(-40)
   ⚙️  Modifiers: +25
   🎯 TOTAL: 290
```

### JSON Export Format:
```json
{
  "model_name": "historical",
  "description": "Historical character behavior model",
  "base_weight": 50,
  "trait_contributions": {
    "positive_traits": {...},
    "negative_traits": {...},
    "opposite_traits": {...}
  },
  "modifiers": [...],
  "total_weight": 290
}
``` 