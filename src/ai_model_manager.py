"""
AI Model Manager for CK3 AI Weight Generator

This module contains classes for managing AI models and their parameters
that will be used to generate CK3 triggers using the trait-based system.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class AIModifier:
    """Represents a single AI modifier with condition identifier and weight adjustment."""
    condition_identifier: str = None
    condition_values: Dict[str, str] = None
    condition: str = ""  # For trait-based conditions only
    weight_adjustment: int = 0


@dataclass
class TraitDefinition:
    """Represents a trait definition with its effects and opposite traits."""
    name: str
    description: str
    weight: int
    ai_effects: Dict[str, Any]
    opposite_traits: List[str]


@dataclass
class AIModelParameters:
    """Represents the parameters for an AI model."""
    base_weight: int
    modifiers: List[AIModifier]


@dataclass
class AIModel:
    """Represents a complete AI model with description and parameters."""
    name: str
    description: str
    parameters: AIModelParameters


@dataclass
class CharacterModel:
    """Represents a character model that references traits."""
    name: str
    description: str
    base_weight: int
    traits: Dict[str, List[str]]  # positive and negative traits
    opposite_traits: List[str]
    modifiers: List[AIModifier]


class TraitManager:
    """Manages trait definitions loaded from JSON files."""
    
    def __init__(self, traits_dir: str = "models/Traits"):
        """
        Initialize the Trait Manager.
        
        Args:
            traits_dir: Path to the directory containing trait JSON files
        """
        self.traits_dir = Path(traits_dir)
        self.traits: Dict[str, TraitDefinition] = {}
        self._load_traits()
    
    def _load_traits(self) -> None:
        """Load trait definitions from all JSON files in the traits directory."""
        if not self.traits_dir.exists():
            print(f"Warning: Traits directory not found: {self.traits_dir}")
            return
        
        json_files = list(self.traits_dir.glob("*.json"))
        
        if not json_files:
            print(f"Warning: No JSON files found in traits directory: {self.traits_dir}")
            return
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                if 'traits' in data:
                    for trait_name, trait_data in data['traits'].items():
                        if isinstance(trait_data, dict):
                            self.traits[trait_name] = self._create_trait_from_data(trait_name, trait_data)
                
                print(f"Loaded traits from {json_file.name}")
                
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in {json_file.name}: {e}")
                continue
            except Exception as e:
                print(f"Warning: Error loading traits from {json_file.name}: {e}")
                continue
    
    def _create_trait_from_data(self, name: str, data: Dict[str, Any]) -> TraitDefinition:
        """Create a TraitDefinition instance from dictionary data."""
        return TraitDefinition(
            name=name,
            description=data.get('description', ''),
            weight=data.get('weight', 0),
            ai_effects=data.get('ai_effects', {}),
            opposite_traits=data.get('opposite_traits', [])
        )
    
    def get_trait(self, trait_name: str) -> Optional[TraitDefinition]:
        """Get a trait definition by name."""
        return self.traits.get(trait_name)
    
    def list_traits(self) -> List[str]:
        """Get a list of all available trait names."""
        return list(self.traits.keys())
    
    def trait_exists(self, trait_name: str) -> bool:
        """Check if a trait exists."""
        return trait_name in self.traits
    
    def get_trait_count(self) -> int:
        """Get the total number of available traits."""
        return len(self.traits)


class AIModelManager:
    """Manages AI models loaded from JSON configuration using the trait-based system."""
    
    def __init__(self, config_manager=None, models_file_path: str = None):
        """
        Initialize the AI Model Manager.
        
        Args:
            config_manager: ConfigManager instance
            models_file_path: Path to the JSON file containing character model definitions
        """
        self.config_manager = config_manager
        self.trait_manager = TraitManager()
        
        if models_file_path:
            self.models_file_path = Path(models_file_path)
        else:
            self.models_file_path = Path("models/Characters/character_models.json")
        
        self.character_models: Dict[str, CharacterModel] = {}
        self.models: Dict[str, AIModel] = {}  # Final unified models
        self._load_models()
        self._build_unified_models()
    
    def _load_models(self) -> None:
        """Load character models from all JSON files in the models directory."""
        models_dir = self.models_file_path.parent
        
        if not models_dir.exists():
            raise FileNotFoundError(f"Models directory not found: {models_dir}")
        
        # Load all JSON files in the models directory
        json_files = list(models_dir.glob("*.json"))
        
        if not json_files:
            raise FileNotFoundError(f"No JSON files found in models directory: {models_dir}")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # Handle different JSON structures
                if isinstance(data, dict):
                    # If the file contains a 'models' key, use that
                    if 'models' in data:
                        models_data = data['models']
                    else:
                        # If the file is a direct model definition, use the whole file
                        models_data = data
                    
                    # Process each model in the file
                    for model_name, model_data in models_data.items():
                        if isinstance(model_data, dict):
                            # Check if this is a character model format
                            if 'traits' in model_data:
                                self.character_models[model_name] = self._create_character_model_from_data(model_name, model_data)
                            else:
                                print(f"Warning: Invalid model format for '{model_name}' in {json_file.name} - missing 'traits' field")
                        else:
                            print(f"Warning: Invalid model data for '{model_name}' in {json_file.name}")
                
                elif isinstance(data, list):
                    # If the file contains a list of models
                    for model_data in data:
                        if isinstance(model_data, dict) and 'name' in model_data:
                            model_name = model_data['name']
                            if 'traits' in model_data:
                                self.character_models[model_name] = self._create_character_model_from_data(model_name, model_data)
                            else:
                                print(f"Warning: Invalid model format in {json_file.name} - missing 'traits' field")
                        else:
                            print(f"Warning: Invalid model data in {json_file.name}")
                
                print(f"Loaded character models from {json_file.name}")
                
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in {json_file.name}: {e}")
                continue
            except Exception as e:
                print(f"Warning: Error loading models from {json_file.name}: {e}")
                continue
    
    def _create_character_model_from_data(self, name: str, data: Dict[str, Any]) -> CharacterModel:
        """Create a CharacterModel instance from dictionary data."""
        modifiers = []
        for mod_data in data.get('modifiers', []):
            modifier = AIModifier(
                condition_identifier=mod_data.get('condition_identifier', None),
                condition_values=mod_data.get('condition_values', {}),
                condition=mod_data.get('condition', ''),
                weight_adjustment=mod_data.get('weight_adjustment', 0)
            )
            modifiers.append(modifier)
        
        return CharacterModel(
            name=name,
            description=data.get('description', ''),
            base_weight=data.get('base_weight', 0),
            traits=data.get('traits', {}),
            opposite_traits=data.get('opposite_traits', []),
            modifiers=modifiers
        )
    
    def _build_unified_models(self) -> None:
        """Build unified AIModel instances from character models and traits."""
        print("Building unified AI models from character models and traits...")
        
        for model_name, character_model in self.character_models.items():
            # Calculate total base weight
            total_base_weight = character_model.base_weight
            
            # Collect all modifiers
            all_modifiers = []
            
            # Add character model's own modifiers
            all_modifiers.extend(character_model.modifiers)
            
            # Add trait-based modifiers
            for trait_name in character_model.traits.get('positive', []):
                trait = self.trait_manager.get_trait(trait_name)
                if trait:
                    # Add positive trait modifier using condition identifier
                    all_modifiers.append(AIModifier(
                        condition_identifier="HAS_TRAIT",
                        condition_values={"trait_name": trait_name},
                        weight_adjustment=trait.weight
                    ))
                    
                    # Add trait's AI effects modifiers
                    for mod_data in trait.ai_effects.get('modifiers', []):
                        all_modifiers.append(AIModifier(
                            condition=mod_data.get('condition', ''),
                            weight_adjustment=mod_data.get('weight_adjustment', 0)
                        ))
            
            # Add negative trait modifiers (NOT conditions)
            for trait_name in character_model.traits.get('negative', []):
                trait = self.trait_manager.get_trait(trait_name)
                if trait:
                    # Add negative trait modifier (reduces weight)
                    all_modifiers.append(AIModifier(
                        condition=f"NOT = {{ has_trait = {trait_name} }}",
                        weight_adjustment=-trait.weight
                    ))
            
            # Add opposite trait modifiers (strong negative)
            for trait_name in character_model.opposite_traits:
                trait = self.trait_manager.get_trait(trait_name)
                if trait:
                    # Add opposite trait modifier (strongly reduces weight)
                    all_modifiers.append(AIModifier(
                        condition=f"NOT = {{ has_trait = {trait_name} }}",
                        weight_adjustment=-trait.weight
                    ))
            
            # Create unified model parameters
            parameters = AIModelParameters(
                base_weight=total_base_weight,
                modifiers=all_modifiers
            )
            
            # Create unified AI model
            unified_model = AIModel(
                name=model_name,
                description=character_model.description,
                parameters=parameters
            )
            
            self.models[model_name] = unified_model
        
        print(f"Built {len(self.models)} unified AI models")
    
    def get_model(self, model_name: str) -> Optional[AIModel]:
        """
        Get a unified AI model by name.
        
        Args:
            model_name: Name of the model to retrieve
            
        Returns:
            AIModel instance if found, None otherwise
        """
        return self.models.get(model_name)
    
    def get_character_model(self, model_name: str) -> Optional[CharacterModel]:
        """
        Get a character model by name.
        
        Args:
            model_name: Name of the character model to retrieve
            
        Returns:
            CharacterModel instance if found, None otherwise
        """
        return self.character_models.get(model_name)
    
    def list_models(self) -> List[str]:
        """
        Get a list of all available unified model names.
        
        Returns:
            List of model names
        """
        return list(self.models.keys())
    
    def list_character_models(self) -> List[str]:
        """
        Get a list of all available character model names.
        
        Returns:
            List of character model names
        """
        return list(self.character_models.keys())
    
    def model_exists(self, model_name: str) -> bool:
        """
        Check if a unified model exists.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            True if model exists, False otherwise
        """
        return model_name in self.models
    
    def get_model_count(self) -> int:
        """
        Get the total number of available unified models.
        
        Returns:
            Number of models
        """
        return len(self.models)
    
    def get_trait_manager(self) -> TraitManager:
        """
        Get the trait manager instance.
        
        Returns:
            TraitManager instance
        """
        return self.trait_manager 