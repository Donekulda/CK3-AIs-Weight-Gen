#!/usr/bin/env python3
"""
CK3 AI Weight Calculator

This script calculates and displays the complete weight values for all AI models,
showing the breakdown of base weights, trait contributions, and modifiers.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ai_model_manager import AIModel, AIModelManager, CharacterModel, TraitManager


class WeightCalculator:
    """Calculates and displays complete weight values for AI models."""
    
    def __init__(self):
        """Initialize the weight calculator with AI model manager."""
        self.ai_manager = AIModelManager()
        self.trait_manager = self.ai_manager.get_trait_manager()
    
    def calculate_model_weights(self, model_name: str) -> Dict[str, Any]:
        """
        Calculate complete weight breakdown for a specific model.
        
        Args:
            model_name: Name of the model to calculate weights for
            
        Returns:
            Dictionary containing weight breakdown
        """
        character_model = self.ai_manager.get_character_model(model_name)
        if not character_model:
            return {"error": f"Model '{model_name}' not found"}
        
        # Initialize weight breakdown
        breakdown = {
            "model_name": model_name,
            "description": character_model.description,
            "base_weight": character_model.base_weight,
            "trait_contributions": {
                "positive_traits": {},
                "negative_traits": {},
                "opposite_traits": {}
            },
            "modifiers": [],
            "total_weight": character_model.base_weight
        }
        
        # Calculate positive trait contributions
        for trait_name in character_model.traits.get('positive', []):
            trait = self.trait_manager.get_trait(trait_name)
            if trait:
                trait_weight = trait.weight
                breakdown["trait_contributions"]["positive_traits"][trait_name] = {
                    "weight": trait_weight,
                    "description": trait.description
                }
                breakdown["total_weight"] += trait_weight
                
                # Add trait's AI effects modifiers
                for mod_data in trait.ai_effects.get('modifiers', []):
                    mod_weight = mod_data.get('weight_adjustment', 0)
                    breakdown["modifiers"].append({
                        "source": f"trait_{trait_name}",
                        "condition": mod_data.get('condition', ''),
                        "weight_adjustment": mod_weight
                    })
                    breakdown["total_weight"] += mod_weight
        
        # Calculate negative trait contributions (NOT conditions)
        for trait_name in character_model.traits.get('negative', []):
            trait = self.trait_manager.get_trait(trait_name)
            if trait:
                trait_weight = -trait.weight  # Negative because it's a NOT condition
                breakdown["trait_contributions"]["negative_traits"][trait_name] = {
                    "weight": trait_weight,
                    "description": trait.description,
                    "note": "Applied as NOT condition (reduces weight)"
                }
                breakdown["total_weight"] += trait_weight
        
        # Calculate opposite trait contributions (strong negative)
        for trait_name in character_model.opposite_traits:
            trait = self.trait_manager.get_trait(trait_name)
            if trait:
                trait_weight = -trait.weight  # Negative because it's a NOT condition
                breakdown["trait_contributions"]["opposite_traits"][trait_name] = {
                    "weight": trait_weight,
                    "description": trait.description,
                    "note": "Applied as NOT condition (strongly reduces weight)"
                }
                breakdown["total_weight"] += trait_weight
        
        # Add character model's own modifiers
        for modifier in character_model.modifiers:
            breakdown["modifiers"].append({
                "source": "character_model",
                "condition": modifier.condition,
                "weight_adjustment": modifier.weight_adjustment
            })
            breakdown["total_weight"] += modifier.weight_adjustment
        
        return breakdown
    
    def get_model_weight(self, model_name: str) -> int:
        """
        Get the final weight for a specific model as an integer.
        If the calculated weight is a float, it rounds down to the lowest integer.
        
        Args:
            model_name: Name of the model to get weight for
            
        Returns:
            Integer weight value, or 0 if model not found
        """
        breakdown = self.calculate_model_weights(model_name)
        if "error" in breakdown:
            return 0
        
        # Convert to integer, rounding down to lowest integer
        weight = breakdown["total_weight"]
        if isinstance(weight, float):
            weight = int(weight)  # This rounds down to the lowest integer
        
        return weight
    
    def get_all_model_weights(self) -> Dict[str, int]:
        """
        Get the final weights for all models as integers.
        If any calculated weight is a float, it rounds down to the lowest integer.
        
        Returns:
            Dictionary mapping model names to integer weight values
        """
        weights = {}
        for model_name in self.ai_manager.list_character_models():
            weights[model_name] = self.get_model_weight(model_name)
        return weights
    
    def calculate_all_weights(self) -> Dict[str, Any]:
        """
        Calculate complete weight breakdown for all models.
        
        Returns:
            Dictionary containing weight breakdowns for all models
        """
        all_models = {}
        
        for model_name in self.ai_manager.list_character_models():
            all_models[model_name] = self.calculate_model_weights(model_name)
        
        return all_models
    
    def print_weight_breakdown(self, breakdown: Dict[str, Any], detailed: bool = True) -> None:
        """
        Print a formatted weight breakdown.
        
        Args:
            breakdown: Weight breakdown dictionary
            detailed: Whether to show detailed breakdown
        """
        if "error" in breakdown:
            print(f"❌ {breakdown['error']}")
            return
        
        print(f"\n{'='*80}")
        print(f"📊 AI MODEL: {breakdown['model_name'].upper()}")
        print(f"📝 Description: {breakdown['description']}")
        print(f"{'='*80}")
        
        # Base weight
        print(f"\n🏗️  BASE WEIGHT: {breakdown['base_weight']}")
        
        if detailed:
            # Positive traits
            if breakdown['trait_contributions']['positive_traits']:
                print(f"\n✅ POSITIVE TRAITS:")
                for trait_name, trait_data in breakdown['trait_contributions']['positive_traits'].items():
                    print(f"   • {trait_name}: +{trait_data['weight']} ({trait_data['description']})")
            
            # Negative traits
            if breakdown['trait_contributions']['negative_traits']:
                print(f"\n❌ NEGATIVE TRAITS (NOT conditions):")
                for trait_name, trait_data in breakdown['trait_contributions']['negative_traits'].items():
                    print(f"   • {trait_name}: {trait_data['weight']} ({trait_data['description']})")
            
            # Opposite traits
            if breakdown['trait_contributions']['opposite_traits']:
                print(f"\n🚫 OPPOSITE TRAITS (NOT conditions):")
                for trait_name, trait_data in breakdown['trait_contributions']['opposite_traits'].items():
                    print(f"   • {trait_name}: {trait_data['weight']} ({trait_data['description']})")
            
            # Modifiers
            if breakdown['modifiers']:
                print(f"\n⚙️  MODIFIERS:")
                for modifier in breakdown['modifiers']:
                    sign = "+" if modifier['weight_adjustment'] >= 0 else ""
                    print(f"   • [{modifier['source']}] {modifier['condition']}: {sign}{modifier['weight_adjustment']}")
        
        # Total weight
        print(f"\n{'='*80}")
        print(f"🎯 TOTAL WEIGHT: {breakdown['total_weight']}")
        print(f"{'='*80}")
    
    def print_summary_table(self, all_breakdowns: Dict[str, Any]) -> None:
        """
        Print a summary table of all model weights.
        
        Args:
            all_breakdowns: Dictionary containing all model breakdowns
        """
        print(f"\n{'='*100}")
        print(f"📋 AI MODEL WEIGHT SUMMARY")
        print(f"{'='*100}")
        print(f"{'Model Name':<20} {'Base Weight':<12} {'Trait Total':<12} {'Modifiers':<12} {'Total Weight':<12}")
        print(f"{'-'*100}")
        
        for model_name, breakdown in all_breakdowns.items():
            if "error" in breakdown:
                continue
            
            # Calculate trait total
            trait_total = 0
            for trait_type in breakdown['trait_contributions'].values():
                for trait_data in trait_type.values():
                    trait_total += trait_data['weight']
            
            # Calculate modifiers total
            modifiers_total = sum(mod['weight_adjustment'] for mod in breakdown['modifiers'])
            
            print(f"{model_name:<20} {breakdown['base_weight']:<12} {trait_total:<12} {modifiers_total:<12} {breakdown['total_weight']:<12}")
        
        print(f"{'='*100}")
    
    def export_to_json(self, all_breakdowns: Dict[str, Any], filename: str = "weight_breakdown.json") -> None:
        """
        Export weight breakdowns to JSON file.
        
        Args:
            all_breakdowns: Dictionary containing all model breakdowns
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_breakdowns, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Weight breakdown exported to: {filename}")


def main():
    """Main function to run the weight calculator."""
    print("🔍 CK3 AI Weight Calculator")
    print("Calculating complete weight values for all AI models...")
    
    calculator = WeightCalculator()
    
    # Calculate all weights
    all_breakdowns = calculator.calculate_all_weights()
    
    # Print summary table
    calculator.print_summary_table(all_breakdowns)
    
    # Show integer weights
    print(f"\n🎯 INTEGER WEIGHTS (rounded down):")
    integer_weights = calculator.get_all_model_weights()
    for model_name, weight in integer_weights.items():
        print(f"   {model_name}: {weight}")
    
    # Ask user if they want detailed breakdown
    print(f"\nOptions:")
    print(f"1. Show detailed breakdown for all models")
    print(f"2. Show detailed breakdown for specific model")
    print(f"3. Export to JSON file")
    print(f"4. Get integer weight for specific model")
    print(f"5. Exit")
    
    while True:
        choice = input(f"\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print(f"\n📊 DETAILED BREAKDOWN FOR ALL MODELS")
            for model_name, breakdown in all_breakdowns.items():
                calculator.print_weight_breakdown(breakdown, detailed=True)
            break
        
        elif choice == "2":
            print(f"\nAvailable models:")
            for i, model_name in enumerate(all_breakdowns.keys(), 1):
                print(f"{i}. {model_name}")
            
            try:
                model_choice = int(input(f"\nEnter model number: ")) - 1
                model_names = list(all_breakdowns.keys())
                if 0 <= model_choice < len(model_names):
                    selected_model = model_names[model_choice]
                    calculator.print_weight_breakdown(all_breakdowns[selected_model], detailed=True)
                else:
                    print("❌ Invalid model number")
            except ValueError:
                print("❌ Please enter a valid number")
            break
        
        elif choice == "3":
            filename = input(f"Enter filename (default: weight_breakdown.json): ").strip()
            if not filename:
                filename = "weight_breakdown.json"
            calculator.export_to_json(all_breakdowns, filename)
            break
        
        elif choice == "4":
            print(f"\nAvailable models:")
            for i, model_name in enumerate(integer_weights.keys(), 1):
                print(f"{i}. {model_name}")
            
            try:
                model_choice = int(input(f"\nEnter model number: ")) - 1
                model_names = list(integer_weights.keys())
                if 0 <= model_choice < len(model_names):
                    selected_model = model_names[model_choice]
                    weight = calculator.get_model_weight(selected_model)
                    print(f"\n🎯 {selected_model.upper()} INTEGER WEIGHT: {weight}")
                else:
                    print("❌ Invalid model number")
            except ValueError:
                print("❌ Please enter a valid number")
            break
        
        elif choice == "5":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main() 