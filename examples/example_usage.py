"""
Example Usage of CK3 AI Model System

This script demonstrates how to use the new trait-based AI model system
for generating CK3 triggers and understanding character behavior.
"""

from src.ai_model_manager import AIModelManager, TraitManager
from src.model_organizer import ModelOrganizer


def demonstrate_trait_system():
    """Demonstrate how to work with traits."""
    print("=== Trait System Demonstration ===\n")
    
    # Initialize managers
    ai_manager = AIModelManager()
    trait_manager = ai_manager.get_trait_manager()
    
    # List all available traits
    print(f"Available traits ({trait_manager.get_trait_count()} total):")
    for trait_name in trait_manager.list_traits():
        trait = trait_manager.get_trait(trait_name)
        print(f"  - {trait_name}: {trait.description} (Weight: {trait.weight})")
    
    print()
    
    # Show trait details
    print("Example trait details:")
    ambitious_trait = trait_manager.get_trait("ambitious")
    if ambitious_trait:
        print(f"Trait: {ambitious_trait.name}")
        print(f"Description: {ambitious_trait.description}")
        print(f"Weight: {ambitious_trait.weight}")
        print(f"Opposite traits: {', '.join(ambitious_trait.opposite_traits)}")
        print(f"AI effects base weight: {ambitious_trait.ai_effects.get('base_weight', 0)}")
    
    print()


def demonstrate_character_models():
    """Demonstrate how to work with character models."""
    print("=== Character Models Demonstration ===\n")
    
    ai_manager = AIModelManager()
    
    # List all character models
    print(f"Available character models ({len(ai_manager.character_models)} total):")
    for model_name in ai_manager.list_character_models():
        model = ai_manager.get_character_model(model_name)
        print(f"  - {model_name}: {model.description}")
    
    print()
    
    # Show detailed character model
    print("Example character model details:")
    aggressive_model = ai_manager.get_character_model("aggressive")
    if aggressive_model:
        print(f"Model: {aggressive_model.name}")
        print(f"Description: {aggressive_model.description}")
        print(f"Base weight: {aggressive_model.base_weight}")
        print(f"Positive traits: {', '.join(aggressive_model.traits.get('positive', []))}")
        print(f"Negative traits: {', '.join(aggressive_model.traits.get('negative', []))}")
        print(f"Opposite traits: {', '.join(aggressive_model.opposite_traits)}")
        print(f"Modifiers: {len(aggressive_model.modifiers)} conditions")
    
    print()


def demonstrate_weight_calculation():
    """Demonstrate how weights are calculated for a character."""
    print("=== Weight Calculation Demonstration ===\n")
    
    ai_manager = AIModelManager()
    trait_manager = ai_manager.get_trait_manager()
    
    # Example: Calculate weight for an aggressive character with specific traits
    model = ai_manager.get_character_model("aggressive")
    if not model:
        print("Aggressive model not found!")
        return
    
    # Simulate character traits
    character_traits = ["brave", "berserker", "wrathful"]  # Positive traits for aggressive
    character_opposite_traits = ["craven", "content"]  # Opposite traits
    
    print(f"Character with traits: {', '.join(character_traits)}")
    print(f"Character opposite traits: {', '.join(character_opposite_traits)}")
    print(f"Using model: {model.name}")
    print()
    
    # Calculate base weight
    total_weight = model.base_weight
    print(f"Base weight: {total_weight}")
    
    # Add trait contributions
    for trait_name in character_traits:
        trait = trait_manager.get_trait(trait_name)
        if trait:
            if trait_name in model.traits.get('positive', []):
                contribution = trait.weight
                total_weight += contribution
                print(f"  + {trait_name}: {contribution} (positive trait)")
            elif trait_name in model.traits.get('negative', []):
                contribution = -trait.weight
                total_weight += contribution
                print(f"  - {trait_name}: {contribution} (negative trait)")
    
    # Subtract opposite trait penalties
    for trait_name in character_opposite_traits:
        if trait_name in model.opposite_traits:
            trait = trait_manager.get_trait(trait_name)
            if trait:
                penalty = -trait.weight
                total_weight += penalty
                print(f"  - {trait_name}: {penalty} (opposite trait)")
    
    # Add modifier contributions (simplified)
    for modifier in model.modifiers:
        print(f"  + Modifier '{modifier.condition}': {modifier.weight_adjustment}")
        total_weight += modifier.weight_adjustment
    
    print(f"\nFinal calculated weight: {total_weight}")
    print()


def demonstrate_validation():
    """Demonstrate the validation system."""
    print("=== Validation System Demonstration ===\n")
    
    organizer = ModelOrganizer()
    
    # Run validation
    validation = organizer.validate_trait_references()
    
    print("Validation Results:")
    if validation['missing_traits']:
        print("❌ Missing trait references:")
        for issue in validation['missing_traits']:
            print(f"  - {issue['model']}: {', '.join(issue['missing_traits'])}")
    else:
        print("✅ All trait references are valid")
    
    if validation['unused_traits']:
        print(f"⚠️  Unused traits: {', '.join(validation['unused_traits'])}")
    
    print(f"✅ Valid models: {len(validation['valid_models'])}")
    print()


def demonstrate_templates():
    """Demonstrate template creation."""
    print("=== Template Creation Demonstration ===\n")
    
    organizer = ModelOrganizer()
    
    # Create trait template
    print("Creating trait template for 'charismatic':")
    trait_template = organizer.create_trait_template("charismatic")
    print(trait_template)
    print()
    
    # Create character model template
    print("Creating character model template for 'charismatic_leader':")
    model_template = organizer.create_character_model_template("charismatic_leader")
    print(model_template)
    print()


def main():
    """Main demonstration function."""
    print("CK3 AI Model System - Usage Examples\n")
    print("=" * 50)
    
    # Run demonstrations
    demonstrate_trait_system()
    demonstrate_character_models()
    demonstrate_weight_calculation()
    demonstrate_validation()
    demonstrate_templates()
    
    print("=" * 50)
    print("Demonstration complete!")
    print("\nTo use this system in your own code:")
    print("1. Import AIModelManager and TraitManager")
    print("2. Initialize the managers")
    print("3. Use get_trait() and get_character_model() methods")
    print("4. Calculate weights based on character traits and models")
    print("5. Use ModelOrganizer for validation and documentation")


if __name__ == "__main__":
    main() 