#!/usr/bin/env python3
"""
Example: Using Integer Weight Functions

This script demonstrates how to use the new integer weight functions
from the WeightCalculator class.
"""

from src.weight_calculator import WeightCalculator


def main():
    """Demonstrate integer weight functions."""
    print("🔢 CK3 AI Integer Weight Example")
    print("=" * 50)
    
    # Initialize calculator
    calculator = WeightCalculator()
    
    # Get integer weights for all models
    print("\n📊 All Model Integer Weights:")
    integer_weights = calculator.get_all_model_weights()
    for model_name, weight in integer_weights.items():
        print(f"   {model_name}: {weight}")
    
    # Get integer weight for specific model
    print(f"\n🎯 Specific Model Examples:")
    
    # Example 1: Historical model
    historical_weight = calculator.get_model_weight("historical")
    print(f"   Historical: {historical_weight}")
    
    # Example 2: Aggressive model
    aggressive_weight = calculator.get_model_weight("aggressive")
    print(f"   Aggressive: {aggressive_weight}")
    
    # Example 3: Religious model
    religious_weight = calculator.get_model_weight("religious")
    print(f"   Religious: {religious_weight}")
    
    # Demonstrate float handling (if any weights were floats)
    print(f"\n🔍 Float Handling Test:")
    test_weights = [290.7, 405.2, -100.9, 505.1]
    for weight in test_weights:
        integer_weight = int(weight)  # Rounds down to lowest integer
        print(f"   {weight} -> {integer_weight}")
    
    print(f"\n✅ Example completed!")


if __name__ == "__main__":
    main() 