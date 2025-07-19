"""
Model Organizer for CK3 AI Weight Generator

This utility script helps organize and manage the trait-based AI model system.
It provides functions to validate, list, and manage traits and character models.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .ai_model_manager import AIModelManager, TraitManager


class ModelOrganizer:
    """Utility class for organizing and managing AI models and traits."""
    
    def __init__(self):
        """Initialize the model organizer."""
        self.ai_manager = AIModelManager()
        self.trait_manager = self.ai_manager.get_trait_manager()
    
    def validate_trait_references(self) -> Dict[str, List[str]]:
        """
        Validate that all trait references in character models exist.
        
        Returns:
            Dictionary with validation results
        """
        results: Dict[str, Any] = {
            'missing_traits': [],
            'unused_traits': [],
            'valid_models': []
        }
        
        # Get all available traits
        available_traits = set(self.trait_manager.list_traits())
        
        # Check character models
        for model_name, model in self.ai_manager.character_models.items():
            model_traits = set()
            
            # Collect all traits referenced in this model
            for trait_list in model.traits.values():
                model_traits.update(trait_list)
            model_traits.update(model.opposite_traits)
            
            # Check for missing traits
            missing = model_traits - available_traits
            if missing:
                results['missing_traits'].append({
                    'model': model_name,
                    'missing_traits': list(missing)
                })
            else:
                results['valid_models'].append(model_name)
        
        # Find unused traits
        used_traits = set()
        for model in self.ai_manager.character_models.values():
            for trait_list in model.traits.values():
                used_traits.update(trait_list)
            used_traits.update(model.opposite_traits)
        
        results['unused_traits'] = list(available_traits - used_traits)
        
        return results
    
    def list_model_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of all models and traits.
        
        Returns:
            Dictionary with summary information
        """
        summary = {
            'traits': {
                'total_count': self.trait_manager.get_trait_count(),
                'categories': self._get_trait_categories(),
                'list': self.trait_manager.list_traits()
            },
            'character_models': {
                'total_count': len(self.ai_manager.character_models),
                'list': self.ai_manager.list_character_models(),
                'details': {}
            },
            'legacy_models': {
                'total_count': len(self.ai_manager.models),
                'list': list(self.ai_manager.models.keys())
            }
        }
        
        # Add details for each character model
        for model_name, model in self.ai_manager.character_models.items():
            summary['character_models']['details'][model_name] = {
                'description': model.description,
                'base_weight': model.base_weight,
                'positive_traits': model.traits.get('positive', []),
                'negative_traits': model.traits.get('negative', []),
                'opposite_traits': model.opposite_traits,
                'modifier_count': len(model.modifiers)
            }
        
        return summary
    
    def _get_trait_categories(self) -> Dict[str, List[str]]:
        """Categorize traits based on their characteristics."""
        categories: Dict[str, List[str]] = {
            'personality': [],
            'education': [],
            'combat': [],
            'social': [],
            'religious': []
        }
        
        # Define trait categories
        personality_traits = ['ambitious', 'content', 'greedy', 'generous', 'wrathful', 'calm']
        education_traits = ['historian', 'scholar', 'diplomat', 'zealous', 'cynical']
        combat_traits = ['brave', 'craven', 'berserker', 'reckless', 'patient']
        social_traits = ['gregarious', 'shy', 'paranoid', 'trusting', 'humble']
        religious_traits = ['zealous', 'cynical']
        
        for trait_name in self.trait_manager.list_traits():
            if trait_name in personality_traits:
                categories['personality'].append(trait_name)
            if trait_name in education_traits:
                categories['education'].append(trait_name)
            if trait_name in combat_traits:
                categories['combat'].append(trait_name)
            if trait_name in social_traits:
                categories['social'].append(trait_name)
            if trait_name in religious_traits:
                categories['religious'].append(trait_name)
        
        return categories
    
    def export_model_documentation(self, output_file: str = "model_documentation.md") -> None:
        """
        Export model documentation to a markdown file.
        
        Args:
            output_file: Path to the output markdown file
        """
        summary = self.list_model_summary()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# CK3 AI Model Documentation\n\n")
            
            # Traits section
            f.write("## Traits\n\n")
            f.write(f"Total traits: {summary['traits']['total_count']}\n\n")
            
            for category, traits in summary['traits']['categories'].items():
                if traits:
                    f.write(f"### {category.title()} Traits\n\n")
                    for trait_name in traits:
                        trait = self.trait_manager.get_trait(trait_name)
                        if trait:
                            f.write(f"- **{trait_name}**: {trait.description} (Weight: {trait.weight})\n")
                            if trait.opposite_traits:
                                f.write(f"  - Opposite: {', '.join(trait.opposite_traits)}\n")
                    f.write("\n")
            
            # Character Models section
            f.write("## Character Models\n\n")
            f.write(f"Total character models: {summary['character_models']['total_count']}\n\n")
            
            for model_name, details in summary['character_models']['details'].items():
                f.write(f"### {model_name.title()}\n\n")
                f.write(f"**Description**: {details['description']}\n\n")
                f.write(f"**Base Weight**: {details['base_weight']}\n\n")
                
                if details['positive_traits']:
                    f.write(f"**Positive Traits**: {', '.join(details['positive_traits'])}\n\n")
                if details['negative_traits']:
                    f.write(f"**Negative Traits**: {', '.join(details['negative_traits'])}\n\n")
                if details['opposite_traits']:
                    f.write(f"**Opposite Traits**: {', '.join(details['opposite_traits'])}\n\n")
                
                f.write(f"**Modifiers**: {details['modifier_count']} conditions\n\n")
        
        print(f"Documentation exported to {output_file}")
    
    def create_trait_template(self, trait_name: str, output_file: Optional[str] = None) -> str:
        """
        Create a template for a new trait.
        
        Args:
            trait_name: Name of the new trait
            output_file: Optional file to save the template to
            
        Returns:
            JSON template string
        """
        template = {
            "description": f"Description for {trait_name}",
            "weight": 0,
            "ai_effects": {
                "base_weight": 0,
                "modifiers": [
                    {
                        "condition": "example_condition = yes",
                        "weight_adjustment": 0
                    }
                ]
            },
            "opposite_traits": []
        }
        
        json_template = json.dumps(template, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_template)
            print(f"Trait template saved to {output_file}")
        
        return json_template
    
    def create_character_model_template(self, model_name: str, output_file: Optional[str] = None) -> str:
        """
        Create a template for a new character model.
        
        Args:
            model_name: Name of the new character model
            output_file: Optional file to save the template to
            
        Returns:
            JSON template string
        """
        template = {
            "description": f"Description for {model_name} character model",
            "base_weight": 50,
            "traits": {
                "positive": ["trait1", "trait2"],
                "negative": ["trait3", "trait4"]
            },
            "opposite_traits": ["opposite_trait1", "opposite_trait2"],
            "modifiers": [
                {
                    "condition": "example_condition = yes",
                    "weight_adjustment": 10
                }
            ]
        }
        
        json_template = json.dumps(template, indent=2)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_template)
            print(f"Character model template saved to {output_file}")
        
        return json_template


def main():
    """Main function to demonstrate the model organizer."""
    organizer = ModelOrganizer()
    
    print("=== CK3 AI Model Organizer ===\n")
    
    # Validate trait references
    print("Validating trait references...")
    validation = organizer.validate_trait_references()
    
    if validation['missing_traits']:
        print("❌ Found missing trait references:")
        for issue in validation['missing_traits']:
            print(f"  - {issue['model']}: {', '.join(issue['missing_traits'])}")
    else:
        print("✅ All trait references are valid")
    
    if validation['unused_traits']:
        print(f"⚠️  Unused traits: {', '.join(validation['unused_traits'])}")
    
    print(f"✅ Valid models: {len(validation['valid_models'])}")
    
    # Generate summary
    print("\n=== Model Summary ===")
    summary = organizer.list_model_summary()
    
    print(f"Traits: {summary['traits']['total_count']}")
    print(f"Character Models: {summary['character_models']['total_count']}")
    print(f"Legacy Models: {summary['legacy_models']['total_count']}")
    
    # Export documentation
    print("\nExporting documentation...")
    organizer.export_model_documentation()
    
    print("\n=== Available Commands ===")
    print("organizer.validate_trait_references() - Check for missing traits")
    print("organizer.list_model_summary() - Get summary of all models")
    print("organizer.export_model_documentation() - Export to markdown")
    print("organizer.create_trait_template('new_trait') - Create trait template")
    print("organizer.create_character_model_template('new_model') - Create model template")


if __name__ == "__main__":
    main() 