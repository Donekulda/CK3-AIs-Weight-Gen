"""
AI Model Manager for CK3 AI Weight Generator

This module contains classes for managing AI models and their parameters
that will be used to generate CK3 triggers using the trait-based system.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class AIModifier:
    """Represents a single AI modifier with condition identifier and weight adjustment."""
    condition_identifier: Optional[str] = None
    condition_values: Optional[Dict[str, str]] = None
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


@dataclass
class TraitInteraction:
    """Represents an interaction between two or more traits."""
    trait_combination: List[str]
    interaction_type: str  # "synergy", "antagonism", "conditional"
    weight_modifier: int
    description: str
    conditions: Optional[List[str]] = None  # Optional CK3 conditions for conditional interactions


@dataclass
class TraitValidationResult:
    """Represents the result of trait validation for a character model."""
    model_name: str
    is_valid: bool
    missing_traits: List[str]
    conflicting_traits: List[Tuple[str, str, str]]  # (trait1, trait2, reason)
    warnings: List[str]
    total_trait_weight: int
    trait_interactions: Optional[List[TraitInteraction]] = None  # Detected interactions


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
        self.trait_interactions: List[TraitInteraction] = []
        self._load_traits()
    
    def _load_traits(self) -> None:
        """Load trait definitions and interactions from all JSON files in the traits directory."""
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
                
                # Load traits
                if 'traits' in data:
                    for trait_name, trait_data in data['traits'].items():
                        if isinstance(trait_data, dict):
                            self.traits[trait_name] = self._create_trait_from_data(trait_name, trait_data)
                
                # Load trait interactions
                if 'interactions' in data:
                    for interaction_data in data['interactions']:
                        if isinstance(interaction_data, dict):
                            interaction = self._create_interaction_from_data(interaction_data)
                            if interaction:
                                self.trait_interactions.append(interaction)
                
                print(f"Loaded traits and interactions from {json_file.name}")
                
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
    
    def _create_interaction_from_data(self, data: Dict[str, Any]) -> Optional[TraitInteraction]:
        """Create a TraitInteraction instance from dictionary data."""
        try:
            return TraitInteraction(
                trait_combination=data.get('trait_combination', []),
                interaction_type=data.get('interaction_type', 'synergy'),
                weight_modifier=data.get('weight_modifier', 0),
                description=data.get('description', ''),
                conditions=data.get('conditions', None)
            )
        except Exception as e:
            print(f"Warning: Error creating interaction from data: {e}")
            return None
    
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
    
    def get_opposite_traits(self, trait_name: str) -> List[str]:
        """Get all traits that are opposite to the given trait."""
        trait = self.get_trait(trait_name)
        if trait:
            return trait.opposite_traits
        return []
    
    def are_traits_compatible(self, trait1: str, trait2: str) -> bool:
        """Check if two traits are compatible (not opposites of each other)."""
        trait1_def = self.get_trait(trait1)
        trait2_def = self.get_trait(trait2)
        
        if not trait1_def or not trait2_def:
            return True  # Unknown traits are assumed compatible
        
        # Check if trait2 is in trait1's opposite traits
        if trait2 in trait1_def.opposite_traits:
            return False
        
        # Check if trait1 is in trait2's opposite traits
        if trait1 in trait2_def.opposite_traits:
            return False
        
        return True
    
    def get_trait_interactions(self) -> List[TraitInteraction]:
        """
        Get all trait interactions loaded from JSON files.
        
        Returns:
            List of all trait interactions
        """
        return self.trait_interactions.copy()
    
    def get_interaction_count(self) -> int:
        """
        Get the total number of trait interactions.
        
        Returns:
            Number of interactions
        """
        return len(self.trait_interactions)
    
    def detect_trait_interactions(self, traits: List[str]) -> List[TraitInteraction]:
        """
        Detect interactions between a list of traits.
        
        Args:
            traits: List of trait names to check for interactions
            
        Returns:
            List of applicable trait interactions
        """
        detected_interactions = []
        trait_set = set(traits)
        
        for interaction in self.trait_interactions:
            interaction_traits = set(interaction.trait_combination)
            
            # Check if all traits in the interaction are present
            if interaction_traits.issubset(trait_set):
                detected_interactions.append(interaction)
        
        return detected_interactions
    
    def calculate_trait_interaction_weight(self, traits: List[str]) -> int:
        """
        Calculate the total weight adjustment from trait interactions.
        
        Args:
            traits: List of trait names
            
        Returns:
            Total weight adjustment from interactions
        """
        interactions = self.detect_trait_interactions(traits)
        total_adjustment = 0
        
        for interaction in interactions:
            total_adjustment += interaction.weight_modifier
        
        return total_adjustment


class AIModelManager:
    """Manages AI models loaded from JSON configuration using the trait-based system."""
    
    def __init__(self, config_manager: Optional[Any] = None, models_file_path: Optional[str] = None):
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
        self._unified_models_cache: Optional[Dict[str, AIModel]] = None
        self._load_models()
        self._build_unified_models()
    
    def detect_trait_interactions(self, traits: List[str]) -> List[TraitInteraction]:
        """
        Detect interactions between a list of traits using the TraitManager.
        
        Args:
            traits: List of trait names to check for interactions
            
        Returns:
            List of applicable trait interactions
        """
        return self.trait_manager.detect_trait_interactions(traits)
    
    def calculate_trait_interaction_weight(self, traits: List[str]) -> int:
        """
        Calculate the total weight adjustment from trait interactions using the TraitManager.
        
        Args:
            traits: List of trait names
            
        Returns:
            Total weight adjustment from interactions
        """
        return self.trait_manager.calculate_trait_interaction_weight(traits)
    
    def add_custom_trait_interaction(self, interaction: TraitInteraction) -> None:
        """
        Add a custom trait interaction to the system.
        
        Args:
            interaction: TraitInteraction to add
        """
        self.trait_manager.trait_interactions.append(interaction)
        # Invalidate cache since interactions have changed
        self._unified_models_cache = None
        print(f"Added custom trait interaction: {interaction.description}")
    
    def get_trait_interactions(self) -> List[TraitInteraction]:
        """
        Get all trait interactions from the TraitManager.
        
        Returns:
            List of all trait interactions
        """
        return self.trait_manager.get_trait_interactions()
    
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
        
        # Clear cache before rebuilding
        self._unified_models_cache = None
        
        for model_name, character_model in self.character_models.items():
            # Calculate total base weight
            total_base_weight = character_model.base_weight
            
            # Collect all modifiers
            all_modifiers = []
            
            # Add character model's own modifiers
            all_modifiers.extend(character_model.modifiers)
            
            # Collect all traits for interaction analysis
            all_model_traits = []
            all_model_traits.extend(character_model.traits.get('positive', []))
            all_model_traits.extend(character_model.traits.get('negative', []))
            all_model_traits.extend(character_model.opposite_traits)
            
            # Add trait interaction modifiers
            interactions = self.detect_trait_interactions(all_model_traits)
            for interaction in interactions:
                if interaction.interaction_type in ["synergy", "antagonism"]:
                    # Simple interaction - just add weight
                    all_modifiers.append(AIModifier(
                        condition=f"# Trait interaction: {interaction.description}",
                        weight_adjustment=interaction.weight_modifier
                    ))
                elif interaction.interaction_type == "conditional" and interaction.conditions:
                    # Conditional interaction - add with conditions
                    condition_str = " ".join(interaction.conditions)
                    all_modifiers.append(AIModifier(
                        condition=condition_str,
                        weight_adjustment=interaction.weight_modifier
                    ))
            
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
        
        # Cache the models
        self._unified_models_cache = self.models.copy()
        print(f"Built {len(self.models)} unified AI models with trait interactions")
    
    def rebuild_models(self, force: bool = False) -> None:
        """
        Rebuild unified models, optionally forcing a full rebuild.
        
        Args:
            force: If True, forces a complete rebuild regardless of cache state
        """
        if force or not self._unified_models_cache:
            print("Forcing model rebuild...")
            self._build_unified_models()
        else:
            print("Using cached models (use force=True to rebuild)")
    
    def invalidate_cache(self) -> None:
        """Invalidate the unified models cache, forcing rebuild on next access."""
        self._unified_models_cache = None
        print("Model cache invalidated")
    
    def is_cache_valid(self) -> bool:
        """
        Check if the unified models cache is valid.
        
        Returns:
            True if cache is valid, False if rebuild is needed
        """
        return self._unified_models_cache is not None
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the current cache state.
        
        Returns:
            Dictionary with cache information
        """
        return {
            'cache_valid': self.is_cache_valid(),
            'cached_models': len(self._unified_models_cache) if self._unified_models_cache else 0,
            'active_models': len(self.models),
            'character_models': len(self.character_models),
            'trait_interactions': len(self.trait_manager.get_trait_interactions())
        }
    
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

    def validate_character_model_traits(self, model: CharacterModel) -> TraitValidationResult:
        """
        Validate all traits referenced in a character model.
        
        Args:
            model: Character model to validate
            
        Returns:
            TraitValidationResult with validation details
        """
        missing_traits = []
        conflicting_traits = []
        warnings = []
        total_weight = model.base_weight
        
        # Collect all traits referenced in the model
        all_traits: Set[str] = set()
        for trait_list in model.traits.values():
            all_traits.update(trait_list)
        all_traits.update(model.opposite_traits)
        
        # Check for missing traits
        for trait_name in all_traits:
            if not self.trait_manager.trait_exists(trait_name):
                missing_traits.append(trait_name)
        
        # Check for trait conflicts
        trait_list = list(all_traits)
        for i, trait1 in enumerate(trait_list):
            for trait2 in trait_list[i+1:]:
                if not self.trait_manager.are_traits_compatible(trait1, trait2):
                    conflicting_traits.append((trait1, trait2, "opposite traits"))
        
        # Check for traits that are both positive and negative
        positive_traits = set(model.traits.get('positive', []))
        negative_traits = set(model.traits.get('negative', []))
        opposite_traits = set(model.opposite_traits)
        
        # Find overlaps
        pos_neg_overlap = positive_traits & negative_traits
        pos_opp_overlap = positive_traits & opposite_traits
        neg_opp_overlap = negative_traits & opposite_traits
        
        for trait in pos_neg_overlap:
            conflicting_traits.append((trait, trait, "both positive and negative"))
        
        for trait in pos_opp_overlap:
            conflicting_traits.append((trait, trait, "both positive and opposite"))
            
        for trait in neg_opp_overlap:
            conflicting_traits.append((trait, trait, "both negative and opposite"))
        
        # Calculate total trait weight contribution
        for trait_name in model.traits.get('positive', []):
            trait_def = self.trait_manager.get_trait(trait_name)
            if trait_def:
                total_weight += trait_def.weight
        
        for trait_name in model.traits.get('negative', []):
            trait_def = self.trait_manager.get_trait(trait_name)
            if trait_def:
                total_weight -= trait_def.weight  # Negative contribution
        
        for trait_name in model.opposite_traits:
            trait_def = self.trait_manager.get_trait(trait_name)
            if trait_def:
                total_weight -= trait_def.weight  # Negative contribution
        
        # Detect trait interactions
        all_model_traits = []
        all_model_traits.extend(model.traits.get('positive', []))
        all_model_traits.extend(model.traits.get('negative', []))
        all_model_traits.extend(model.opposite_traits)
        
        detected_interactions = self.detect_trait_interactions(all_model_traits)
        
        # Add interaction weight to total
        interaction_weight = self.calculate_trait_interaction_weight(all_model_traits)
        total_weight += interaction_weight
        
        # Generate warnings
        if total_weight < 0:
            warnings.append("Total weight is negative - model may not work effectively")
        
        if len(model.traits.get('positive', [])) == 0:
            warnings.append("Model has no positive traits - consider adding some")
        
        # Check for negative interactions
        negative_interactions = [i for i in detected_interactions if i.interaction_type == "antagonism"]
        if negative_interactions:
            warnings.append(f"Found {len(negative_interactions)} antagonistic trait interactions that may cause conflicts")
        
        is_valid = len(missing_traits) == 0 and len(conflicting_traits) == 0
        
        return TraitValidationResult(
            model_name=model.name,
            is_valid=is_valid,
            missing_traits=missing_traits,
            conflicting_traits=conflicting_traits,
            warnings=warnings,
            total_trait_weight=total_weight,
            trait_interactions=detected_interactions
        )
    
    def validate_all_models(self) -> Dict[str, TraitValidationResult]:
        """
        Validate all character models and return results.
        
        Returns:
            Dictionary mapping model names to their validation results
        """
        results = {}
        for model_name, model in self.character_models.items():
            results[model_name] = self.validate_character_model_traits(model)
        return results
    
    def get_trait_usage_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about trait usage across all models.
        
        Returns:
            Dictionary with trait usage statistics
        """
        trait_usage = {}
        total_models = len(self.character_models)
        
        # Initialize trait usage counters
        for trait_name in self.trait_manager.list_traits():
            trait_usage[trait_name] = {
                'positive_usage': 0,
                'negative_usage': 0,
                'opposite_usage': 0,
                'total_usage': 0,
                'usage_percentage': 0.0
            }
        
        # Count trait usage
        for model in self.character_models.values():
            for trait_name in model.traits.get('positive', []):
                if trait_name in trait_usage:
                    trait_usage[trait_name]['positive_usage'] += 1
                    trait_usage[trait_name]['total_usage'] += 1
            
            for trait_name in model.traits.get('negative', []):
                if trait_name in trait_usage:
                    trait_usage[trait_name]['negative_usage'] += 1
                    trait_usage[trait_name]['total_usage'] += 1
            
            for trait_name in model.opposite_traits:
                if trait_name in trait_usage:
                    trait_usage[trait_name]['opposite_usage'] += 1
                    trait_usage[trait_name]['total_usage'] += 1
        
        # Calculate percentages
        for trait_name in trait_usage:
            if total_models > 0:
                trait_usage[trait_name]['usage_percentage'] = (
                    trait_usage[trait_name]['total_usage'] / total_models * 100
                )
        
        # Add summary statistics
        used_traits = [t for t in trait_usage if trait_usage[t]['total_usage'] > 0]
        unused_traits = [t for t in trait_usage if trait_usage[t]['total_usage'] == 0]
        
        return {
            'trait_usage': trait_usage,
            'summary': {
                'total_traits': len(trait_usage),
                'used_traits': len(used_traits),
                'unused_traits': len(unused_traits),
                'usage_rate': len(used_traits) / len(trait_usage) * 100 if trait_usage else 0
            }
        } 