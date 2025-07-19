"""
CK3 Trigger Generator for AI Weight Generator

This module contains classes for generating CK3 trigger code based on
unified AI models that combine character models and traits.
"""

from dataclasses import dataclass
from typing import List, Optional

from .ai_model_manager import AIModel, TraitInteraction
from .condition_manager import ConditionManager


@dataclass
class GeneratedTrigger:
    """Represents a generated CK3 trigger block."""
    model_name: str
    weight: int
    conditions: List[str]
    description: str
    trait_conditions: Optional[List[str]] = None  # Specific trait-based conditions
    interaction_conditions: Optional[List[str]] = None  # Trait interaction conditions


class CK3TriggerGenerator:
    """Generates CK3 trigger code based on unified AI models."""
    
    def __init__(self, config_manager=None):
        """
        Initialize the CK3 trigger generator.
        
        Args:
            config_manager: ConfigManager instance (optional)
        """
        self.config_manager = config_manager
        self.condition_manager = ConditionManager()
    
    def _generate_trait_condition(self, trait_name: str, is_negative: bool = False) -> str:
        """
        Generate CK3 condition for a specific trait.
        
        Args:
            trait_name: Name of the trait
            is_negative: Whether this is a negative condition (NOT has_trait)
            
        Returns:
            CK3 condition string
        """
        if is_negative:
            return f"NOT = {{ has_trait = {trait_name} }}"
        else:
            return f"has_trait = {trait_name}"
    
    def _generate_trait_group_condition(self, traits: List[str], group_type: str = "AND") -> str:
        """
        Generate CK3 condition for multiple traits.
        
        Args:
            traits: List of trait names
            group_type: "AND", "OR", or "NOR" for logical grouping
            
        Returns:
            CK3 condition string for multiple traits
        """
        if not traits:
            return ""
        
        if len(traits) == 1:
            return self._generate_trait_condition(traits[0])
        
        if group_type == "AND":
            conditions = [self._generate_trait_condition(trait) for trait in traits]
            return "\n".join(conditions)
        elif group_type == "OR":
            conditions = [f"    {self._generate_trait_condition(trait)}" for trait in traits]
            return "OR = {\n" + "\n".join(conditions) + "\n}"
        elif group_type == "NOR":
            conditions = [f"    {self._generate_trait_condition(trait, is_negative=True)}" for trait in traits]
            return "NOR = {\n" + "\n".join(conditions) + "\n}"
        
        return ""
    
    def _generate_interaction_condition(self, interaction: TraitInteraction) -> str:
        """
        Generate CK3 condition for a trait interaction.
        
        Args:
            interaction: TraitInteraction to generate condition for
            
        Returns:
            CK3 condition string
        """
        trait_conditions = [self._generate_trait_condition(trait) for trait in interaction.trait_combination]
        
        base_condition = "\n".join(trait_conditions)
        
        if interaction.conditions:
            # Add additional conditions for conditional interactions
            additional_conditions = "\n".join(interaction.conditions)
            return f"{base_condition}\n{additional_conditions}"
        
        return base_condition
    
    def _fix_condition_syntax(self, condition: str) -> str:
        """
        Fix common CK3 condition syntax issues using the ConditionManager.
        
        Args:
            condition: Raw condition string
            
        Returns:
            Fixed condition string
        """
        # Skip comment lines
        if condition.strip().startswith("#"):
            return condition
        
        # Handle NOT conditions
        if condition.startswith("NOT = {"):
            inner_condition = condition[8:-1].strip()  # Remove "NOT = { ... }"
            fixed_inner = self._fix_condition_syntax(inner_condition)
            return f"NOT = {{ {fixed_inner} }}"
        
        # Handle OR/AND/NOR blocks
        for block_type in ["OR", "AND", "NOR"]:
            if condition.startswith(f"{block_type} = {{"):
                return condition  # Already properly formatted
        
        # Try to parse the condition using ConditionManager
        parts = condition.split(' = ', 1)
        if len(parts) == 2:
            condition_name, value = parts
            
            # Check if this is a known condition
            condition_def = self.condition_manager.get_condition(condition_name)
            if condition_def:
                # Use the condition manager to generate proper syntax
                return self.condition_manager.generate_condition_syntax(condition_name, value)
        
        return condition
    
    def generate_comprehensive_trigger(self, model: AIModel, ai_manager=None) -> GeneratedTrigger:
        """
        Generate comprehensive CK3 trigger code with enhanced trait integration.
        
        Args:
            model: AI model to generate triggers for
            ai_manager: Optional AIModelManager for accessing trait interactions
            
        Returns:
            GeneratedTrigger containing the comprehensive trigger information
        """
        # Calculate total weight
        total_weight = model.parameters.base_weight
        
        # Separate different types of conditions
        trait_conditions = []
        interaction_conditions = []
        general_conditions = []
        
        for modifier in model.parameters.modifiers:
            if modifier.condition_identifier:
                # Use condition identifier with values
                if modifier.condition_identifier == "HAS_TRAIT" and modifier.condition_values:
                    trait_name = modifier.condition_values.get("trait_name", "")
                    trait_conditions.append(self._generate_trait_condition(trait_name))
                else:
                    condition_string = self.condition_manager.generate_condition_from_identifier(
                        modifier.condition_identifier, 
                        **(modifier.condition_values or {})
                    )
                    general_conditions.append(condition_string)
            else:
                # Handle trait-based conditions and interactions
                if modifier.condition.strip().startswith("# Trait interaction:"):
                    interaction_conditions.append(modifier.condition)
                elif "has_trait" in modifier.condition:
                    fixed_condition = self._fix_condition_syntax(modifier.condition)
                    trait_conditions.append(fixed_condition)
                else:
                    fixed_condition = self._fix_condition_syntax(modifier.condition)
                    general_conditions.append(fixed_condition)
            
            total_weight += modifier.weight_adjustment
        
        # Combine all conditions
        all_conditions = []
        all_conditions.extend(trait_conditions)
        all_conditions.extend(interaction_conditions) 
        all_conditions.extend(general_conditions)
        
        return GeneratedTrigger(
            model_name=model.name,
            weight=total_weight,
            conditions=all_conditions,
            description=f"Generated from unified model '{model.name}' with enhanced trait integration",
            trait_conditions=trait_conditions,
            interaction_conditions=interaction_conditions
        )
    
    def generate_trigger_from_model(self, model: AIModel) -> GeneratedTrigger:
        """
        Generate CK3 trigger code from a unified AI model.
        
        Args:
            model: AI model to generate triggers for
            
        Returns:
            GeneratedTrigger containing the trigger information
        """
        return self.generate_comprehensive_trigger(model)
    
    def format_trigger_block(self, trigger: GeneratedTrigger, event_name: str = "example_event") -> str:
        """
        Format a trigger into a complete CK3 trigger block.
        
        Args:
            trigger: GeneratedTrigger to format
            event_name: Name of the event this trigger belongs to
            
        Returns:
            Formatted CK3 trigger block as string
        """
        lines = []
        lines.append(f"# AI Weight for {trigger.model_name}")
        lines.append(f"# {trigger.description}")
        lines.append("ai_value = {")
        lines.append(f"    base = {trigger.weight}")
        lines.append("")
        
        if trigger.conditions:
            lines.append("    # Conditions")
            for condition in trigger.conditions:
                if condition.strip():
                    # Indent condition properly
                    if condition.startswith("#"):
                        lines.append(f"    {condition}")
                    elif "=" in condition and not condition.strip().startswith(("OR", "AND", "NOR", "NOT")):
                        lines.append("    modifier = {")
                        lines.append("        add = 10  # Weight adjustment")
                        lines.append(f"        {condition}")
                        lines.append("    }")
                    else:
                        # Multi-line conditions
                        condition_lines = condition.split('\n')
                        for cond_line in condition_lines:
                            if cond_line.strip():
                                lines.append(f"    {cond_line}")
                    lines.append("")
        
        lines.append("}")
        return "\n".join(lines)
    
    def generate_trigger_for_model_name(self, model_name: str, model_manager) -> Optional[GeneratedTrigger]:
        """
        Generate trigger for a unified model by name.
        
        Args:
            model_name: Name of the model to generate trigger for
            model_manager: AIModelManager instance
            
        Returns:
            GeneratedTrigger if model exists, None otherwise
        """
        model = model_manager.get_model(model_name)
        if model is None:
            return None
        
        return self.generate_comprehensive_trigger(model)
    
    def format_trigger_for_replacement(self, trigger: GeneratedTrigger, indent_level: Optional[int] = None) -> str:
        """
        Format trigger code for replacement in event files.
        
        Args:
            trigger: Generated trigger to format
            indent_level: Number of indentation levels (uses config if None)
            
        Returns:
            Formatted trigger code string
        """
        if indent_level is None:
            if self.config_manager:
                indent_level = self.config_manager.get_indent_level()
            else:
                indent_level = 2

        # At this point indent_level is guaranteed to be an int
        indent = "\t" * (indent_level if isinstance(indent_level, int) else 2)
        
        # Generate the complete trigger code
        code_lines = []
        code_lines.append("ai_chance = {")
        code_lines.append(f"{indent}base = {trigger.weight}")
        
        # Add conditions as modifiers
        for condition in trigger.conditions:
            if condition.startswith("NOT = {"):
                # Handle NOT conditions
                code_lines.append(f"{indent}modifier = {{")
                code_lines.append(f"{indent}\tadd = -10")
                code_lines.append(f"{indent}\ttrigger = {{")
                code_lines.append(f"{indent}\t\t{condition}")
                code_lines.append(f"{indent}\t}}")
                code_lines.append(f"{indent}}}")
            else:
                # Handle positive conditions
                code_lines.append(f"{indent}modifier = {{")
                code_lines.append(f"{indent}\tadd = 10")
                code_lines.append(f"{indent}\ttrigger = {{")
                code_lines.append(f"{indent}\t\t{condition}")
                code_lines.append(f"{indent}\t}}")
                code_lines.append(f"{indent}}}")
        
        code_lines.append("}")
        
        return "\n".join(code_lines)
    
    def validate_trigger_code(self, trigger: GeneratedTrigger) -> List[str]:
        """
        Validate generated trigger code for common issues using ConditionManager.
        
        Args:
            trigger: Generated trigger to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check weight
        if trigger.weight < 0:
            errors.append("Weight cannot be negative")
        
        # Check conditions using ConditionManager
        for i, condition in enumerate(trigger.conditions):
            if not condition.strip():
                errors.append(f"Condition {i+1} is empty")
                continue
            
            # Try to parse and validate the condition
            if condition.startswith("NOT = {"):
                # Handle NOT conditions - extract the inner condition
                inner_condition = condition[8:-1].strip()  # Remove "NOT = { ... }"
                inner_parts = inner_condition.split(' = ', 1)
                if len(inner_parts) == 2:
                    inner_condition_name, inner_value = inner_parts
                    # Check if this is a known condition
                    is_valid = (
                        self.condition_manager.get_condition(inner_condition_name) is not None
                        or any(
                            inner_condition_name in cond.name.lower()
                            for cond in self.condition_manager.all_conditions.values()
                        )
                    )
                    if not is_valid:
                        errors.append(f"Condition {i+1} (NOT): Unknown condition: {inner_condition_name}")
                else:
                    # NOT condition with complex inner condition
                    if not any(pattern in inner_condition for pattern in ["has_trait", "has_claim_on", "wealth", "prestige"]):
                        errors.append(f"Condition {i+1} (NOT): Invalid inner condition format: {inner_condition}")
            else:
                parts = condition.split(' = ', 1)
                if len(parts) == 2:
                    condition_name, value = parts
                    # Check if this is a known condition
                    is_valid = (
                        self.condition_manager.get_condition(condition_name) is not None
                        or any(
                            condition_name in cond.name.lower()
                            for cond in self.condition_manager.all_conditions.values()
                        )
                    )
                    if not is_valid:
                        errors.append(f"Condition {i+1}: Unknown condition: {condition_name}")
                else:
                    # Check for complex conditions
                    if not any(pattern in condition for pattern in ["has_trait", "has_claim_on", "wealth", "prestige"]):
                        errors.append(f"Condition {i+1} may have invalid format: {condition}")
        
        return errors
    
    def generate_simple_trigger(self, model_name: str, weight: int, conditions: List[str]) -> GeneratedTrigger:
        """
        Generate a simple trigger with basic parameters.
        
        Args:
            model_name: Name of the model
            weight: Base weight for the trigger
            conditions: List of conditions
            
        Returns:
            GeneratedTrigger instance
        """
        return GeneratedTrigger(
            model_name=model_name,
            weight=weight,
            conditions=conditions,
            description=f"Simple trigger for {model_name}"
        )
    
    def generate_optimized_trigger_for_trait(self, trait_name: str, base_weight: int = 50) -> GeneratedTrigger:
        """
        Generate an optimized trigger for a specific trait using ConditionManager suggestions.
        
        Args:
            trait_name: Name of the trait
            base_weight: Base weight for the trigger
            
        Returns:
            GeneratedTrigger instance
        """
        # Get suggested conditions for this trait
        suggested_conditions = self.condition_manager.suggest_conditions_for_trait(trait_name)
        
        # Generate conditions with appropriate values
        conditions = []
        for condition_name in suggested_conditions[:5]:  # Limit to 5 most relevant
            condition_def = self.condition_manager.get_condition(condition_name)
            if condition_def:
                if condition_def.condition_type == "boolean":
                    conditions.append(f"{condition_name} = yes")
                elif condition_def.condition_type == "comparison":
                    # Use a reasonable default value
                    if "wealth" in condition_name:
                        conditions.append(f"{condition_name} < 500")
                    elif "prestige" in condition_name:
                        conditions.append(f"{condition_name} > 1000")
                    elif "martial" in condition_name or "diplomacy" in condition_name:
                        conditions.append(f"{condition_name} > 10")
        
        return GeneratedTrigger(
            model_name=f"optimized_{trait_name}",
            weight=base_weight,
            conditions=conditions,
            description=f"Optimized trigger for {trait_name} trait"
        )
    
    def get_available_conditions(self) -> List[str]:
        """
        Get a list of all available conditions from the ConditionManager.
        
        Returns:
            List of condition names
        """
        return self.condition_manager.list_conditions()
    
    def get_conditions_by_relevance(self, relevance: str = "high") -> List[str]:
        """
        Get conditions filtered by AI relevance.
        
        Args:
            relevance: Relevance level ('high', 'medium', 'low')
            
        Returns:
            List of condition names
        """
        common_conditions = self.condition_manager.get_common_conditions_for_ai()
        return common_conditions.get(relevance, []) 