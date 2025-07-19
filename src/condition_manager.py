"""
Condition Manager for CK3 AI Weight Generator

This module contains classes for managing CK3 condition definitions and
generating valid condition syntax based on condition models.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ConditionType(Enum):
    """Enumeration for condition types."""
    BOOLEAN = "boolean"  # yes/no conditions
    COMPARISON = "comparison"  # <, <=, =, !=, >, >= conditions
    TRAIT = "trait"  # has_trait conditions
    CLAIM = "claim"  # claim conditions
    COMPLEX = "complex"  # complex conditions with multiple parameters


@dataclass
class ConditionDefinition:
    """Represents a CK3 condition definition."""
    name: str
    description: str
    syntax: str
    input_values: Dict[str, str]
    custom_triggers: Dict[str, str]
    supported_scopes: List[str]
    ai_relevance: str
    condition_type: str


@dataclass
class ConditionCategory:
    """Represents a category of conditions."""
    name: str
    description: str
    conditions: Dict[str, ConditionDefinition]


class ConditionManager:
    """Manages CK3 condition definitions and generates valid condition syntax."""
    
    def __init__(self, conditions_file_path: str = "models/Conditions/condition_models.json"):
        """
        Initialize the Condition Manager.
        
        Args:
            conditions_file_path: Path to the conditions JSON file
        """
        self.conditions_file_path = Path(conditions_file_path)
        self.categories: Dict[str, ConditionCategory] = {}
        self.all_conditions: Dict[str, ConditionDefinition] = {}
        self._load_conditions()
    
    def _load_conditions(self) -> None:
        """Load condition definitions from the JSON file."""
        if not self.conditions_file_path.exists():
            print(f"Warning: Conditions file not found: {self.conditions_file_path}")
            return
        
        try:
            with open(self.conditions_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'conditions' in data:
                for category_name, category_data in data['conditions'].items():
                    category = self._create_category_from_data(category_name, category_data)
                    self.categories[category_name] = category
                    
                    # Add conditions to the global dictionary
                    for condition_name, condition_def in category.conditions.items():
                        self.all_conditions[condition_name] = condition_def
            
            print(f"Loaded {len(self.all_conditions)} conditions from {self.conditions_file_path.name}")
            
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in conditions file: {e}")
        except Exception as e:
            print(f"Warning: Error loading conditions: {e}")
    
    def _create_category_from_data(self, name: str, data: Dict[str, Any]) -> ConditionCategory:
        """Create a ConditionCategory instance from dictionary data."""
        conditions = {}
        
        if 'conditions' in data:
            for condition_name, condition_data in data['conditions'].items():
                conditions[condition_name] = self._create_condition_from_data(condition_name, condition_data)
        
        return ConditionCategory(
            name=name,
            description=data.get('description', ''),
            conditions=conditions
        )
    
    def _create_condition_from_data(self, name: str, data: Dict[str, Any]) -> ConditionDefinition:
        """Create a ConditionDefinition instance from dictionary data."""
        return ConditionDefinition(
            name=name,
            description=data.get('description', ''),
            syntax=data.get('syntax', ''),
            input_values=data.get('input_values', {}),
            custom_triggers=data.get('custom_triggers', {}),
            supported_scopes=data.get('supported_scopes', []),
            ai_relevance=data.get('ai_relevance', 'medium'),
            condition_type=data.get('condition_type', 'complex')
        )
    
    def _determine_condition_type(self, data: Dict[str, Any]) -> str:
        """Determine the condition type based on the data."""
        return data.get('condition_type', 'complex')
    
    def get_condition(self, condition_name: str) -> Optional[ConditionDefinition]:
        """Get a condition definition by name."""
        return self.all_conditions.get(condition_name)
    
    def list_conditions(self) -> List[str]:
        """Get a list of all available condition names."""
        return list(self.all_conditions.keys())
    
    def list_categories(self) -> List[str]:
        """Get a list of all condition categories."""
        return list(self.categories.keys())
    
    def get_conditions_by_category(self, category_name: str) -> Optional[ConditionCategory]:
        """Get all conditions in a specific category."""
        return self.categories.get(category_name)
    
    def get_high_relevance_conditions(self) -> List[ConditionDefinition]:
        """Get all conditions with high AI relevance."""
        return [cond for cond in self.all_conditions.values() if cond.ai_relevance == 'high']
    
    def validate_condition_syntax(self, condition_name: str, value: str = None) -> Tuple[bool, str]:
        """
        Validate if a condition syntax is correct.
        
        Args:
            condition_name: Name of the condition
            value: Value to validate (optional)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        condition = self.get_condition(condition_name)
        if not condition:
            return False, f"Unknown condition: {condition_name}"
        
        # Basic validation based on condition type
        if condition.condition_type == ConditionType.BOOLEAN:
            if value and value not in ['yes', 'no']:
                return False, f"Boolean condition '{condition_name}' requires 'yes' or 'no', got '{value}'"
        
        elif condition.condition_type == ConditionType.TRAIT:
            # For trait conditions, we could validate against known traits
            if value and not value.strip():
                return False, f"Trait condition '{condition_name}' requires a trait name"
        
        elif condition.condition_type == ConditionType.COMPARISON:
            if value:
                # Validate comparison operators
                operators = ['<', '<=', '=', '!=', '>', '>=']
                if not any(value.startswith(op) for op in operators):
                    return False, f"Comparison condition '{condition_name}' requires an operator (<, <=, =, !=, >, >=)"
        
        return True, ""
    
    def generate_condition_syntax(self, condition_name: str, value: str = None) -> str:
        """
        Generate valid CK3 condition syntax.
        
        Args:
            condition_name: Name of the condition
            value: Value for the condition (optional)
            
        Returns:
            Generated condition syntax string
        """
        condition = self.get_condition(condition_name)
        if not condition:
            return f"# Unknown condition: {condition_name}"
        
        if value:
            return f"{condition_name} = {value}"
        else:
            # Return the basic syntax template
            return condition.syntax
    
    def get_common_conditions_for_ai(self) -> Dict[str, List[str]]:
        """
        Get common conditions organized by relevance for AI decision making.
        
        Returns:
            Dictionary mapping relevance levels to lists of condition names
        """
        result = {
            'high': [],
            'medium': [],
            'low': []
        }
        
        for condition_name, condition in self.all_conditions.items():
            result[condition.ai_relevance].append(condition_name)
        
        return result
    
    def suggest_conditions_for_trait(self, trait_name: str) -> List[str]:
        """
        Suggest relevant conditions for a specific trait.
        
        Args:
            trait_name: Name of the trait
            
        Returns:
            List of suggested condition names
        """
        suggestions = []
        
        # Map traits to relevant conditions
        trait_condition_map = {
            'ambitious': ['is_ruler', 'has_claim_on', 'prestige', 'wealth'],
            'content': ['is_ruler', 'wealth', 'prestige'],
            'brave': ['is_commander', 'is_at_war', 'martial'],
            'craven': ['is_commander', 'is_at_war', 'martial'],
            'greedy': ['wealth', 'prestige', 'is_ruler'],
            'generous': ['wealth', 'prestige'],
            'wrathful': ['has_rival', 'has_enemy', 'martial'],
            'calm': ['has_rival', 'has_enemy', 'diplomacy'],
            'paranoid': ['has_spouse', 'has_children', 'intrigue'],
            'trusting': ['has_spouse', 'has_children', 'diplomacy'],
            'proud': ['is_ruler', 'prestige', 'diplomacy'],
            'humble': ['is_ruler', 'prestige', 'piety'],
            'patient': ['age', 'learning', 'stewardship'],
            'reckless': ['is_commander', 'is_at_war', 'martial'],
            'zealous': ['piety', 'learning', 'has_education_learning_trigger'],
            'cynical': ['piety', 'learning', 'has_education_learning_trigger'],
            'scholar': ['learning', 'has_education_learning_trigger'],
            'diplomat': ['diplomacy', 'has_education_diplomacy_trigger'],
            'merchant': ['stewardship', 'wealth', 'has_education_stewardship_trigger']
        }
        
        if trait_name in trait_condition_map:
            suggestions = trait_condition_map[trait_name]
        
        return suggestions
    
    def get_condition_count(self) -> int:
        """Get the total number of available conditions."""
        return len(self.all_conditions)
    
    def search_conditions(self, query: str) -> List[ConditionDefinition]:
        """
        Search for conditions by name or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching condition definitions
        """
        query_lower = query.lower()
        results = []
        
        for condition in self.all_conditions.values():
            if (query_lower in condition.name.lower() or 
                query_lower in condition.description.lower()):
                results.append(condition)
        
        return results
    
    def get_condition_by_identifier(self, identifier: str) -> Optional[ConditionDefinition]:
        """
        Get a condition by its identifier (e.g., 'IS_RULER', 'HAS_TRAIT').
        
        Args:
            identifier: Condition identifier
            
        Returns:
            ConditionDefinition if found, None otherwise
        """
        return self.all_conditions.get(identifier)
    
    def generate_condition_from_identifier(self, identifier: str, **kwargs) -> str:
        """
        Generate a condition string from an identifier with input values.
        
        Args:
            identifier: Condition identifier (e.g., 'IS_RULER', 'HAS_TRAIT')
            **kwargs: Input values for the condition
            
        Returns:
            Generated condition string
        """
        condition = self.get_condition_by_identifier(identifier)
        if not condition:
            return f"# Unknown condition identifier: {identifier}"
        
        # Check if this is a custom trigger
        if len(kwargs) == 1:
            key, value = list(kwargs.items())[0]
            if key in condition.custom_triggers:
                return condition.custom_triggers[key]
        
        # Generate from syntax template with dollar symbol replacement
        result = condition.syntax
        
        for key, value in kwargs.items():
            placeholder = f"${key}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def get_available_identifiers(self) -> List[str]:
        """
        Get a list of all available condition identifiers.
        
        Returns:
            List of condition identifiers
        """
        return list(self.all_conditions.keys())
    
    def get_custom_triggers_for_condition(self, identifier: str) -> Dict[str, str]:
        """
        Get custom triggers for a specific condition.
        
        Args:
            identifier: Condition identifier
            
        Returns:
            Dictionary of custom trigger names to trigger strings
        """
        condition = self.get_condition_by_identifier(identifier)
        if condition:
            return condition.custom_triggers
        return {}
    
    def validate_condition_identifier(self, identifier: str, **kwargs) -> Tuple[bool, str]:
        """
        Validate if a condition identifier and its input values are correct.
        
        Args:
            identifier: Condition identifier
            **kwargs: Input values to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        condition = self.get_condition_by_identifier(identifier)
        if not condition:
            return False, f"Unknown condition identifier: {identifier}"
        
        # For boolean conditions, we only need one of the input values
        if condition.condition_type == "boolean":
            if not kwargs:
                return False, f"Boolean condition '{identifier}' requires one input value (yes/no)"
            # Check if at least one valid boolean value is provided
            valid_values = ['yes', 'no']
            provided_values = list(kwargs.values())
            if not any(val in valid_values for val in provided_values):
                return False, f"Boolean condition '{identifier}' requires 'yes' or 'no', got {provided_values}"
        else:
            # For other conditions, check if all required input values are provided
            required_inputs = set(condition.input_values.keys())
            provided_inputs = set(kwargs.keys())
            
            missing_inputs = required_inputs - provided_inputs
            if missing_inputs:
                return False, f"Missing required input values: {', '.join(missing_inputs)}"
        
        # Validate input values based on condition type
        if condition.condition_type == "boolean":
            for key, value in kwargs.items():
                if value not in ['yes', 'no']:
                    return False, f"Boolean condition '{identifier}' requires 'yes' or 'no' for '{key}', got '{value}'"
        
        elif condition.condition_type == "comparison":
            for key, value in kwargs.items():
                if key == "operator" and value not in ['<', '<=', '=', '!=', '>', '>=']:
                    return False, f"Comparison condition '{identifier}' requires valid operator (<, <=, =, !=, >, >=), got '{value}'"
                elif key.endswith("_threshold") and not str(value).replace('.', '').replace('-', '').isdigit():
                    return False, f"Comparison condition '{identifier}' requires numeric value for '{key}', got '{value}'"
        
        return True, ""
    
    def list_condition_identifiers_by_type(self, condition_type: str) -> List[str]:
        """
        Get all condition identifiers of a specific type.
        
        Args:
            condition_type: Type of conditions to list
            
        Returns:
            List of condition identifiers
        """
        return [name for name, condition in self.all_conditions.items() 
                if condition.condition_type == condition_type] 