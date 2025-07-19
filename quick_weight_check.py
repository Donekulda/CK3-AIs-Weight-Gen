#!/usr/bin/env python3
"""
Quick CK3 AI Weight Check

Simple script to quickly display current weight values for all AI models.
"""

from ai_model_manager import AIModelManager


def main():
    """Quick weight check for all AI models."""
    print("🔍 CK3 AI Weight Check")
    print("=" * 80)
    
    # Initialize AI model manager
    ai_manager = AIModelManager()
    trait_manager = ai_manager.get_trait_manager()
    
    print(f"📊 Loaded {len(ai_manager.list_character_models())} character models")
    print(f"🎭 Loaded {trait_manager.get_trait_count()} traits")
    print()
    
    # Calculate and display weights for each model
    for model_name in ai_manager.list_character_models():
        character_model = ai_manager.get_character_model(model_name)
        if not character_model:
            continue
        
        # Calculate total weight
        total_weight = character_model.base_weight
        
        # Add positive trait weights
        positive_traits = []
        for trait_name in character_model.traits.get('positive', []):
            trait = trait_manager.get_trait(trait_name)
            if trait:
                total_weight += trait.weight
                positive_traits.append(f"{trait_name}({trait.weight:+d})")
        
        # Subtract negative trait weights (NOT conditions)
        negative_traits = []
        for trait_name in character_model.traits.get('negative', []):
            trait = trait_manager.get_trait(trait_name)
            if trait:
                total_weight -= trait.weight
                negative_traits.append(f"{trait_name}({trait.weight:+d})")
        
        # Subtract opposite trait weights (NOT conditions)
        opposite_traits = []
        for trait_name in character_model.opposite_traits:
            trait = trait_manager.get_trait(trait_name)
            if trait:
                total_weight -= trait.weight
                opposite_traits.append(f"{trait_name}({trait.weight:+d})")
        
        # Add modifier weights
        modifier_total = sum(mod.weight_adjustment for mod in character_model.modifiers)
        total_weight += modifier_total
        
        # Display model information
        print(f"🎯 {model_name.upper()}")
        print(f"   Base Weight: {character_model.base_weight}")
        print(f"   Description: {character_model.description}")
        
        if positive_traits:
            print(f"   ✅ Positive: {', '.join(positive_traits)}")
        if negative_traits:
            print(f"   ❌ Negative: {', '.join(negative_traits)}")
        if opposite_traits:
            print(f"   🚫 Opposite: {', '.join(opposite_traits)}")
        if modifier_total != 0:
            print(f"   ⚙️  Modifiers: {modifier_total:+d}")
        
        # Convert to integer (round down to lowest integer)
        integer_weight = int(total_weight) if isinstance(total_weight, float) else total_weight
        print(f"   🎯 TOTAL: {total_weight} (Integer: {integer_weight})")
        print("-" * 80)


if __name__ == "__main__":
    main() 