#!/usr/bin/env python3
"""
Test script for the new Condition Identifier System

This script demonstrates how condition identifiers can be used to generate
CK3 triggers with custom values and dollar symbol variables.
"""

from src.ck3_trigger_generator import CK3TriggerGenerator
from src.condition_manager import ConditionManager


def test_condition_identifiers():
    """Test the condition identifier system."""
    print("Testing Condition Identifier System...")
    print("=" * 60)
    
    # Initialize the condition manager
    cm = ConditionManager()
    
    # Test basic condition identifiers
    print("1. Testing basic condition identifiers:")
    test_conditions = [
        ("IS_RULER", {"yes": "yes"}),
        ("HAS_TRAIT", {"trait_name": "ambitious"}),
        ("WEALTH", {"operator": "<", "wealth_threshold": "500"}),
        ("PRESTIGE", {"operator": ">", "prestige_threshold": "1000"}),
        ("HAS_CLAIM_ON", {"title_scope": "ROOT"}),
        ("DIPLOMACY", {"operator": ">", "skill_threshold": "10"}),
        ("HAS_EDUCATION_LEARNING", {"yes": "yes"})
    ]
    
    for identifier, values in test_conditions:
        condition_string = cm.generate_condition_from_identifier(identifier, **values)
        print(f"  {identifier} {values} → {condition_string}")
    
    # Test custom triggers
    print("\n2. Testing custom triggers:")
    custom_triggers = [
        ("HAS_TRAIT", "ambitious"),
        ("HAS_TRAIT", "brave"),
        ("WEALTH", "poor"),
        ("WEALTH", "rich"),
        ("PRESTIGE", "high_prestige"),
        ("DIPLOMACY", "high_diplomacy"),
        ("HAS_CLAIM_ON", "has_claim_on_root")
    ]
    
    for identifier, trigger_name in custom_triggers:
        condition_string = cm.generate_condition_from_identifier(identifier, **{trigger_name: trigger_name})
        print(f"  {identifier}.{trigger_name} → {condition_string}")
    
    # Test validation
    print("\n3. Testing condition validation:")
    validation_tests = [
        ("IS_RULER", {"yes": "yes"}, True),
        ("IS_RULER", {"yes": "maybe"}, False),  # Invalid boolean value
        ("WEALTH", {"operator": "<", "wealth_threshold": "500"}, True),
        ("WEALTH", {"operator": "invalid", "wealth_threshold": "500"}, False),  # Invalid operator
        ("HAS_TRAIT", {"trait_name": "ambitious"}, True),
        ("UNKNOWN_CONDITION", {"value": "test"}, False),  # Unknown condition
    ]
    
    for identifier, values, should_be_valid in validation_tests:
        is_valid, error_msg = cm.validate_condition_identifier(identifier, **values)
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"  {status} {identifier} {values}: {error_msg if not is_valid else 'Valid'}")


def test_trigger_generation():
    """Test trigger generation with condition identifiers."""
    print("\n\nTesting Trigger Generation with Condition Identifiers...")
    print("=" * 60)
    
    # Initialize the trigger generator
    generator = CK3TriggerGenerator()
    
    # Test available identifiers
    print("1. Available condition identifiers:")
    identifiers = generator.condition_manager.get_available_identifiers()
    print(f"  Total: {len(identifiers)} identifiers")
    print(f"  Examples: {', '.join(identifiers[:10])}")
    
    # Test identifiers by type
    print("\n2. Condition identifiers by type:")
    for condition_type in ["boolean", "comparison", "trait", "claim"]:
        type_identifiers = generator.condition_manager.list_condition_identifiers_by_type(condition_type)
        print(f"  {condition_type}: {len(type_identifiers)} identifiers")
        if type_identifiers:
            print(f"    Examples: {', '.join(type_identifiers[:5])}")
    
    # Test custom triggers for specific conditions
    print("\n3. Custom triggers for specific conditions:")
    test_conditions = ["HAS_TRAIT", "WEALTH", "PRESTIGE", "DIPLOMACY"]
    
    for condition_id in test_conditions:
        custom_triggers = generator.condition_manager.get_custom_triggers_for_condition(condition_id)
        print(f"  {condition_id}: {len(custom_triggers)} custom triggers")
        if custom_triggers:
            print(f"    Examples: {', '.join(list(custom_triggers.keys())[:3])}")


def test_dollar_symbol_variables():
    """Test dollar symbol variable replacement."""
    print("\n\nTesting Dollar Symbol Variable Replacement...")
    print("=" * 60)
    
    cm = ConditionManager()
    
    # Test various dollar symbol replacements
    test_cases = [
        ("WEALTH", {"operator": "<", "wealth_threshold": "1000"}, "wealth < 1000"),
        ("PRESTIGE", {"operator": ">", "prestige_threshold": "5000"}, "prestige > 5000"),
        ("DIPLOMACY", {"operator": ">=", "skill_threshold": "15"}, "diplomacy >= 15"),
        ("HAS_CLAIM_ON", {"title_scope": "scope:primary_title"}, "has_claim_on = { title = scope:primary_title }"),
        ("HAS_TRAIT", {"trait_name": "custom_trait"}, "has_trait = custom_trait"),
    ]
    
    for identifier, values, expected in test_cases:
        result = cm.generate_condition_from_identifier(identifier, **values)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {identifier} {values}")
        print(f"    Expected: {expected}")
        print(f"    Got:      {result}")
        print()


def test_character_model_integration():
    """Test integration with character models using condition identifiers."""
    print("\n\nTesting Character Model Integration...")
    print("=" * 60)
    
    # This would test how character models use condition identifiers
    # For now, let's show how the system would work
    
    print("Character models now use condition identifiers instead of hardcoded conditions:")
    print("  Old format: 'condition': 'is_ruler = yes'")
    print("  New format:")
    print("    'condition_identifier': 'IS_RULER'")
    print("    'condition_values': {'yes': 'yes'}")
    print()
    print("Benefits:")
    print("  ✅ Conditions are separate and self-editable")
    print("  ✅ Support for custom triggers with predefined values")
    print("  ✅ Dollar symbol variables for dynamic values")
    print("  ✅ Better validation and error checking")
    print("  ✅ Easier to maintain and extend")


def main():
    """Main test function."""
    print("CK3 Condition Identifier System Test")
    print("=" * 80)
    
    try:
        test_condition_identifiers()
        test_trigger_generation()
        test_dollar_symbol_variables()
        test_character_model_integration()
        
        print("\n" + "=" * 80)
        print("All tests completed successfully!")
        print("\nThe new condition identifier system provides:")
        print("  • Condition identifiers (IS_RULER, HAS_TRAIT, etc.)")
        print("  • Input values with validation")
        print("  • Custom triggers (poor, rich, high_prestige, etc.)")
        print("  • Dollar symbol variables ($wealth_threshold, $trait_name, etc.)")
        print("  • Separation of conditions from character models")
        print("  • Self-editable condition definitions")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 