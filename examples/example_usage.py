#!/usr/bin/env python3
"""
Enhanced CK3 AI Weight Generator - Example Usage

This example demonstrates the comprehensive trait integration system
including validation, interactions, and advanced AI model generation.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from ai_model_manager import AIModelManager, TraitInteraction
    from ck3_trigger_generator import CK3TriggerGenerator
    from model_organizer import ModelOrganizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run this script from the project root directory")
    sys.exit(1)


def main():
    """Demonstrate the enhanced trait integration system."""
    print("=== Enhanced CK3 AI Weight Generator - Trait Integration Demo ===\n")
    
    # Initialize the system
    print("1. Initializing AI Model Manager with trait system...")
    ai_manager = AIModelManager()
    
    # Show cache information
    cache_info = ai_manager.get_cache_info()
    print(f"Cache Info: {cache_info}")
    
    # Show trait interaction loading from JSON
    print(f"Loaded {ai_manager.trait_manager.get_interaction_count()} trait interactions from JSON files")
    all_interactions = ai_manager.get_trait_interactions()
    
    # Show breakdown by interaction type
    synergies = [i for i in all_interactions if i.interaction_type == "synergy"]
    antagonisms = [i for i in all_interactions if i.interaction_type == "antagonism"]
    conditionals = [i for i in all_interactions if i.interaction_type == "conditional"]
    
    print(f"  - {len(synergies)} synergistic interactions")
    print(f"  - {len(antagonisms)} antagonistic interactions")
    print(f"  - {len(conditionals)} conditional interactions")
    
    # Show some example interactions
    print("\nExample interactions loaded from JSON:")
    for i, interaction in enumerate(all_interactions[:5]):
        print(f"  {i+1}. {' + '.join(interaction.trait_combination)} ({interaction.interaction_type})")
        print(f"     {interaction.description} ({interaction.weight_modifier:+d})")
    
    if len(all_interactions) > 5:
        print(f"     ... and {len(all_interactions) - 5} more interactions")
    
    print()
    
    # Demonstrate trait validation
    print("2. Validating character models and traits...")
    validation_results = ai_manager.validate_all_models()
    
    for model_name, result in validation_results.items():
        print(f"\nModel: {model_name}")
        print(f"  Valid: {'✅' if result.is_valid else '❌'}")
        print(f"  Total Weight: {result.total_trait_weight}")
        
        if result.missing_traits:
            print(f"  Missing Traits: {', '.join(result.missing_traits)}")
        
        if result.conflicting_traits:
            print("  Conflicts:")
            for conflict in result.conflicting_traits:
                print(f"    - {conflict[0]} vs {conflict[1]}: {conflict[2]}")
        
        if result.trait_interactions:
            print(f"  Trait Interactions: {len(result.trait_interactions)}")
            for interaction in result.trait_interactions:
                print(f"    - {interaction.interaction_type}: {interaction.description} ({interaction.weight_modifier:+d})")
        
        if result.warnings:
            print("  Warnings:")
            for warning in result.warnings:
                print(f"    - {warning}")
    
    print("\n" + "="*60)
    
    # Demonstrate trait usage statistics
    print("\n3. Analyzing trait usage across models...")
    stats = ai_manager.get_trait_usage_statistics()
    
    print("Trait Usage Summary:")
    print(f"  Total Traits: {stats['summary']['total_traits']}")
    print(f"  Used Traits: {stats['summary']['used_traits']}")
    print(f"  Unused Traits: {stats['summary']['unused_traits']}")
    print(f"  Usage Rate: {stats['summary']['usage_rate']:.1f}%")
    
    # Show most and least used traits
    trait_usage = stats['trait_usage']
    used_traits = [(name, data['total_usage']) for name, data in trait_usage.items() if data['total_usage'] > 0]
    used_traits.sort(key=lambda x: x[1], reverse=True)
    
    if used_traits:
        print("\nMost Used Traits:")
        for trait_name, usage in used_traits[:5]:
            print(f"  - {trait_name}: {usage} models ({trait_usage[trait_name]['usage_percentage']:.1f}%)")
    
    print("\n" + "="*60)
    
    # Demonstrate custom trait interaction
    print("\n4. Adding custom trait interaction to JSON-based system...")
    
    # Show current interaction count
    print(f"Current interactions from JSON: {ai_manager.trait_manager.get_interaction_count()}")
    
    custom_interaction = TraitInteraction(
        trait_combination=["ambitious", "scholar"],
        interaction_type="synergy",
        weight_modifier=12,
        description="Ambitious scholars seek knowledge to gain power"
    )
    ai_manager.add_custom_trait_interaction(custom_interaction)
    print(f"Added custom interaction: {custom_interaction.description}")
    print(f"New total interactions: {ai_manager.trait_manager.get_interaction_count()}")
    
    # Rebuild models to include the new interaction
    ai_manager.rebuild_models(force=True)
    
    print("\n" + "="*60)
    
    # Demonstrate enhanced trigger generation
    print("\n5. Generating enhanced CK3 triggers...")
    trigger_generator = CK3TriggerGenerator()
    
    # Generate triggers for all models
    for model_name in ai_manager.list_models():
        model = ai_manager.get_model(model_name)
        if model:
            print(f"\n--- Trigger for {model_name.upper()} ---")
            trigger = trigger_generator.generate_comprehensive_trigger(model, ai_manager)
            
            # Display trigger information
            print(f"Model: {trigger.model_name}")
            print(f"Total Weight: {trigger.weight}")
            print(f"Description: {trigger.description}")
            
            if trigger.trait_conditions:
                print(f"Trait Conditions ({len(trigger.trait_conditions)}):")
                for condition in trigger.trait_conditions[:3]:  # Show first 3
                    print(f"  - {condition}")
                if len(trigger.trait_conditions) > 3:
                    print(f"  ... and {len(trigger.trait_conditions) - 3} more")
            
            if trigger.interaction_conditions:
                print(f"Interaction Conditions ({len(trigger.interaction_conditions)}):")
                for condition in trigger.interaction_conditions[:2]:  # Show first 2
                    print(f"  - {condition}")
                if len(trigger.interaction_conditions) > 2:
                    print(f"  ... and {len(trigger.interaction_conditions) - 2} more")
            
            # Show formatted trigger block
            print("\nFormatted CK3 Trigger:")
            formatted_trigger = trigger_generator.format_trigger_block(trigger, f"{model_name}_event")
            print(formatted_trigger[:400] + "..." if len(formatted_trigger) > 400 else formatted_trigger)
            print()
    
    print("\n" + "="*60)
    
    # Demonstrate model organizer integration
    print("\n6. Using enhanced model organizer...")
    organizer = ModelOrganizer()
    
    # Validate trait references with new system
    validation = organizer.validate_trait_references()
    print("Model Validation Summary:")
    print(f"  Valid Models: {len(validation['valid_models'])}")
    print(f"  Models with Missing Traits: {len(validation['missing_traits'])}")
    print(f"  Unused Traits: {len(validation['unused_traits'])}")
    
    # Export enhanced documentation
    print("\n7. Exporting enhanced documentation...")
    organizer.export_model_documentation("enhanced_model_documentation.md")
    
    # Show performance information
    final_cache_info = ai_manager.get_cache_info()
    print(f"\nFinal Cache Info: {final_cache_info}")
    
    print("\n" + "="*60)
    print("\n🎉 Enhanced trait integration demonstration completed!")
    print("\nKey improvements implemented:")
    print("✅ Comprehensive trait validation and conflict detection")
    print("✅ Dynamic trait interaction system (synergistic and antagonistic effects)")
    print("✅ Enhanced CK3 trigger generation with trait-specific conditions")
    print("✅ Performance caching system for unified models")
    print("✅ Detailed documentation and usage statistics")
    
    print("\nGenerated files:")
    print("- enhanced_model_documentation.md (comprehensive model documentation)")


if __name__ == "__main__":
    main() 