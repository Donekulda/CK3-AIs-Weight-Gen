#!/usr/bin/env python3
"""
Test script for the new Condition System

This script demonstrates how the ConditionManager can be used to
generate optimized CK3 triggers with proper syntax validation.
"""

from src.ck3_trigger_generator import CK3TriggerGenerator
from src.condition_manager import ConditionManager


def test_condition_manager():
    """Test the ConditionManager functionality."""
    print("Testing ConditionManager...")
    print("=" * 50)
    
    # Initialize the condition manager
    cm = ConditionManager()
    
    # Display basic information
    print(f"Loaded {cm.get_condition_count()} conditions")
    print(f"Categories: {', '.join(cm.list_categories())}")
    
    # Show high relevance conditions
    high_relevance = cm.get_high_relevance_conditions()
    print(f"\nHigh relevance conditions ({len(high_relevance)}):")
    for condition in high_relevance[:10]:  # Show first 10
        print(f"  - {condition.name}: {condition.description}")
    
    # Test condition validation
    print("\nTesting condition validation:")
    test_conditions = [
        ("is_ruler", "yes"),
        ("is_ruler", "maybe"),  # Invalid
        ("has_trait", "ambitious"),
        ("wealth", "< 100"),
        ("wealth", "invalid"),  # Invalid
        ("unknown_condition", "value")  # Unknown
    ]
    
    for condition_name, value in test_conditions:
        is_valid, error_msg = cm.validate_condition_syntax(condition_name, value)
        status = "✅" if is_valid else "❌"
        print(f"  {status} {condition_name} = {value}: {error_msg if not is_valid else 'Valid'}")
    
    # Test condition suggestions for traits
    print("\nTesting trait-based condition suggestions:")
    test_traits = ["ambitious", "brave", "greedy", "scholar"]
    
    for trait in test_traits:
        suggestions = cm.suggest_conditions_for_trait(trait)
        print(f"  {trait}: {', '.join(suggestions)}")


def test_trigger_generator():
    """Test the enhanced CK3TriggerGenerator with ConditionManager."""
    print("\n\nTesting CK3TriggerGenerator with ConditionManager...")
    print("=" * 50)
    
    # Initialize the trigger generator
    generator = CK3TriggerGenerator()
    
    # Test optimized trigger generation for traits
    print("Testing optimized trigger generation for traits:")
    test_traits = ["ambitious", "brave", "greedy"]
    
    for trait in test_traits:
        trigger = generator.generate_optimized_trigger_for_trait(trait, base_weight=75)
        print(f"\n{trait.upper()} trait trigger:")
        print(f"  Model: {trigger.model_name}")
        print(f"  Weight: {trigger.weight}")
        print(f"  Conditions ({len(trigger.conditions)}):")
        for i, condition in enumerate(trigger.conditions, 1):
            print(f"    {i}. {condition}")
    
    # Test condition syntax generation
    print("\nTesting condition syntax generation:")
    test_conditions = [
        ("is_ruler", "yes"),
        ("has_trait", "ambitious"),
        ("wealth", "< 500"),
        ("prestige", "> 1000"),
        ("has_claim_on", "{ title = ROOT }")
    ]
    
    for condition_name, value in test_conditions:
        syntax = generator.condition_manager.generate_condition_syntax(condition_name, value)
        print(f"  {condition_name} = {value} → {syntax}")
    
    # Test available conditions
    print(f"\nAvailable conditions: {len(generator.get_available_conditions())}")
    high_relevance = generator.get_conditions_by_relevance("high")
    print(f"High relevance conditions: {len(high_relevance)}")
    print(f"  Examples: {', '.join(high_relevance[:5])}")


def test_condition_categories():
    """Test condition categories and organization."""
    print("\n\nTesting condition categories...")
    print("=" * 50)
    
    cm = ConditionManager()
    
    for category_name in cm.list_categories():
        category = cm.get_conditions_by_category(category_name)
        if category:
            print(f"\n{category_name.upper()} ({len(category.conditions)} conditions):")
            print(f"  Description: {category.description}")
            
            # Show first few conditions in this category
            for condition_name, condition_def in list(category.conditions.items())[:3]:
                print(f"    - {condition_name}: {condition_def.description}")
                print(f"      Syntax: {condition_def.syntax}")
                print(f"      Type: {condition_def.condition_type}")
                print(f"      AI Relevance: {condition_def.ai_relevance}")


def main():
    """Main test function."""
    print("CK3 Condition System Test")
    print("=" * 60)
    
    try:
        test_condition_manager()
        test_trigger_generator()
        test_condition_categories()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 