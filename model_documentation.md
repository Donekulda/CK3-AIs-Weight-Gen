# CK3 AI Model Documentation

## Traits

Total traits: 26

### Personality Traits

- **ambitious**: Character is driven by ambition and seeks power (Weight: 50)
  - Opposite: content, humble
- **content**: Character is satisfied with their current position (Weight: -40)
  - Opposite: ambitious, greedy
- **greedy**: Character is motivated by wealth and material gain (Weight: 30)
  - Opposite: content, generous
- **generous**: Character is giving and charitable (Weight: -20)
  - Opposite: greedy, stingy
- **wrathful**: Character is quick to anger and vengeful (Weight: 30)
  - Opposite: calm, patient
- **calm**: Character is composed and level-headed (Weight: -25)
  - Opposite: wrathful, berserker

### Education Traits

- **historian**: Character has scholarly knowledge of history (Weight: 25)
  - Opposite: illiterate, ignorant
- **scholar**: Character is well-educated and learned (Weight: 20)
  - Opposite: illiterate, ignorant
- **diplomat**: Character is skilled in diplomacy and negotiation (Weight: 40)
  - Opposite: shy, awkward
- **zealous**: Character is deeply religious and pious (Weight: -10)
  - Opposite: cynical, skeptical
- **cynical**: Character is skeptical of religion and tradition (Weight: 10)
  - Opposite: zealous, pious

### Combat Traits

- **berserker**: Character is fierce and battle-crazed (Weight: 50)
  - Opposite: craven, calm
- **reckless**: Character acts without considering consequences (Weight: 35)
  - Opposite: cautious, patient
- **patient**: Character is willing to wait and plan carefully (Weight: -30)
  - Opposite: reckless, wrathful
- **brave**: Character is courageous and fearless (Weight: 40)
  - Opposite: craven, paranoid
- **craven**: Character is fearful and avoids danger (Weight: -50)
  - Opposite: brave, berserker

### Social Traits

- **gregarious**: Character is outgoing and sociable (Weight: 25)
  - Opposite: shy, awkward
- **shy**: Character is introverted and uncomfortable in social situations (Weight: -20)
  - Opposite: gregarious, diplomat
- **humble**: Character is modest and unassuming (Weight: -25)
  - Opposite: ambitious, proud
- **paranoid**: Character is suspicious and distrustful (Weight: 25)
  - Opposite: trusting, gregarious
- **trusting**: Character is open and trusting of others (Weight: -20)
  - Opposite: paranoid, suspicious

### Religious Traits

- **zealous**: Character is deeply religious and pious (Weight: -10)
  - Opposite: cynical, skeptical
- **cynical**: Character is skeptical of religion and tradition (Weight: 10)
  - Opposite: zealous, pious

## Character Models

Total character models: 8

### Historical

**Description**: Historical character behavior model - focuses on scholarly and diplomatic pursuits

**Base Weight**: 50

**Positive Traits**: historian, scholar, diplomat, gregarious

**Negative Traits**: zealous, shy, reckless

**Opposite Traits**: illiterate, ignorant, awkward, cynical

**Modifiers**: 2 conditions

### Ambitious

**Description**: Ambitious character behavior model - driven by power and advancement

**Base Weight**: 75

**Positive Traits**: ambitious, greedy, proud

**Negative Traits**: content, humble, patient

**Opposite Traits**: content, humble, generous

**Modifiers**: 2 conditions

### Cautious

**Description**: Cautious character behavior model - careful and risk-averse

**Base Weight**: 60

**Positive Traits**: craven, paranoid, patient

**Negative Traits**: brave, reckless, trusting

**Opposite Traits**: brave, reckless, trusting

**Modifiers**: 2 conditions

### Aggressive

**Description**: Aggressive character behavior model - warlike and confrontational

**Base Weight**: 80

**Positive Traits**: brave, berserker, wrathful, reckless

**Negative Traits**: craven, content, patient

**Opposite Traits**: craven, content, calm

**Modifiers**: 2 conditions

### Diplomatic

**Description**: Diplomatic character behavior model - skilled in negotiation and relationships

**Base Weight**: 70

**Positive Traits**: diplomat, gregarious, trusting, generous

**Negative Traits**: shy, wrathful, paranoid

**Opposite Traits**: shy, wrathful, awkward

**Modifiers**: 2 conditions

### Scholarly

**Description**: Scholarly character behavior model - focused on learning and knowledge

**Base Weight**: 65

**Positive Traits**: historian, scholar, patient, cynical

**Negative Traits**: reckless, zealous, greedy

**Opposite Traits**: illiterate, ignorant, reckless

**Modifiers**: 2 conditions

### Merchant

**Description**: Merchant character behavior model - focused on trade and wealth

**Base Weight**: 55

**Positive Traits**: greedy, gregarious, patient

**Negative Traits**: generous, shy, reckless

**Opposite Traits**: generous, content, humble

**Modifiers**: 2 conditions

### Religious

**Description**: Religious character behavior model - pious and faith-driven

**Base Weight**: 45

**Positive Traits**: zealous, humble, patient

**Negative Traits**: cynical, greedy, wrathful

**Opposite Traits**: cynical, skeptical, greedy

**Modifiers**: 2 conditions

