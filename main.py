#!/usr/bin/env python3
"""
CK3 AI Weight Generator - Main Program

This program processes CK3 event files to generate AI modifiers based on
predefined AI models. It reads event files, extracts AI model references,
and generates appropriate CK3 triggers using the unified trait-based system.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Optional

# Import our custom modules
from config_manager import ConfigManager
from ai_model_manager import AIModelManager, TraitManager, CharacterModel, TraitDefinition, AIModel
from event_parser import EventParser, ParsedEvent, AIBlock
from ck3_trigger_generator import CK3TriggerGenerator, GeneratedTrigger


def setup_environment(config_manager: ConfigManager) -> None:
    """Set up the Python environment and check dependencies."""
    print("Setting up CK3 AI Weight Generator environment...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Not running in a virtual environment. Consider using one.")
    
    # Check required directories from config
    events_dir = config_manager.get_events_directory()
    models_dir = config_manager.get_models_directory()
    
    if not events_dir.exists():
        print(f"Error: Events directory not found at {events_dir}")
        sys.exit(1)
    
    if not models_dir.exists():
        print(f"Error: Models directory not found at {models_dir}")
        sys.exit(1)
    
    print("Environment setup complete.")


def load_ai_models(config_manager: ConfigManager) -> AIModelManager:
    """
    Load AI models from the configuration.
    
    Args:
        config_manager: ConfigManager instance
        
    Returns:
        AIModelManager instance with loaded models
    """
    print("Loading AI models and traits...")
    
    try:
        model_manager = AIModelManager(config_manager)
        trait_manager = model_manager.get_trait_manager()
        
        # Display loaded traits
        print(f"Loaded {trait_manager.get_trait_count()} traits:")
        for trait_name in trait_manager.list_traits():
            trait = trait_manager.get_trait(trait_name)
            print(f"  - {trait_name}: {trait.description} (Weight: {trait.weight})")
        
        # Display loaded character models
        print(f"\nLoaded {len(model_manager.character_models)} character models:")
        for model_name in model_manager.list_character_models():
            model = model_manager.get_character_model(model_name)
            print(f"  - {model_name}: {model.description}")
        
        # Display unified models
        print(f"\nBuilt {model_manager.get_model_count()} unified AI models:")
        for model_name in model_manager.list_models():
            model = model_manager.get_model(model_name)
            print(f"  - {model_name}: {model.description} (Base weight: {model.parameters.base_weight}, Modifiers: {len(model.parameters.modifiers)})")
        
        return model_manager
    
    except Exception as e:
        print(f"Error loading AI models: {e}")
        sys.exit(1)


def parse_event_files(events_dir: Path, config_manager: ConfigManager) -> List[ParsedEvent]:
    """
    Parse all event files in the events directory.
    
    Args:
        events_dir: Path to the events directory
        config_manager: ConfigManager instance
        
    Returns:
        List of parsed event files
    """
    print(f"Parsing event files in {events_dir}...")
    
    try:
        parser = EventParser(config_manager)
        parsed_events = parser.parse_events_directory(events_dir)
        
        print(f"Parsed {len(parsed_events)} event files:")
        
        total_ai_blocks = 0
        files_with_ai_lib = 0
        
        for event in parsed_events:
            if event.has_ai_lib:
                files_with_ai_lib += 1
                print(f"  - {event.file_path.name}: {len(event.ai_blocks)} AI blocks")
                total_ai_blocks += len(event.ai_blocks)
            else:
                print(f"  - {event.file_path.name}: No AI-MODEL-LIB marker")
        
        print(f"Found {files_with_ai_lib} files with AI-MODEL-LIB and {total_ai_blocks} total AI blocks")
        
        return parsed_events
    
    except Exception as e:
        print(f"Error parsing event files: {e}")
        sys.exit(1)


def validate_model_references(model_manager: AIModelManager) -> bool:
    """
    Validate that all trait references in character models exist.
    
    Args:
        model_manager: AIModelManager instance
        
    Returns:
        True if all references are valid, False otherwise
    """
    print("Validating model references...")
    
    trait_manager = model_manager.get_trait_manager()
    available_traits = set(trait_manager.list_traits())
    all_valid = True
    
    for model_name, model in model_manager.character_models.items():
        model_traits = set()
        
        # Collect all traits referenced in this model
        for trait_list in model.traits.values():
            model_traits.update(trait_list)
        model_traits.update(model.opposite_traits)
        
        # Check for missing traits
        missing = model_traits - available_traits
        if missing:
            print(f"  ❌ {model_name}: Missing traits {', '.join(missing)}")
            all_valid = False
        else:
            print(f"  ✅ {model_name}: All trait references valid")
    
    if all_valid:
        print("All model references are valid!")
    else:
        print("Some model references are invalid. Please fix before proceeding.")
    
    return all_valid


def generate_triggers_for_blocks(ai_blocks: List[AIBlock], model_manager: AIModelManager, config_manager: ConfigManager) -> Dict[AIBlock, GeneratedTrigger]:
    """
    Generate CK3 triggers for all AI blocks using the unified trait-based system.
    
    Args:
        ai_blocks: List of AI blocks to process
        model_manager: AIModelManager instance
        config_manager: ConfigManager instance
        
    Returns:
        Dictionary mapping AI blocks to their generated triggers
    """
    print("Generating CK3 triggers for AI blocks...")
    
    generator = CK3TriggerGenerator(config_manager)
    triggers = {}
    
    for block in ai_blocks:
        # Check if this is a unified model reference
        if model_manager.model_exists(block.model_name):
            model = model_manager.get_model(block.model_name)
            trigger = generator.generate_trigger_from_model(model)
            triggers[block] = trigger
            print(f"  - Generated trigger for '{block.model_name}' (weight: {trigger.weight}, conditions: {len(trigger.conditions)})")
        else:
            print(f"  - Warning: Unknown model '{block.model_name}' in {block.file_path.name}")
    
    print(f"Generated {len(triggers)} triggers")
    return triggers


def apply_triggers_to_files(parsed_events: List[ParsedEvent], triggers: Dict[AIBlock, GeneratedTrigger], config_manager: ConfigManager) -> None:
    """
    Apply generated triggers back to the event files.
    
    Args:
        parsed_events: List of parsed event files
        triggers: Dictionary mapping AI blocks to their triggers
        config_manager: ConfigManager instance
    """
    print("Applying triggers to event files...")
    
    generator = CK3TriggerGenerator(config_manager)
    
    for event in parsed_events:
        if not event.ai_blocks:
            continue
        
        # Create backup if enabled
        backup_path = config_manager.create_backup(event.file_path)
        if backup_path:
            print(f"  - Created backup: {backup_path.name}")
        
        # Read the original file
        with open(event.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Apply triggers in reverse order to maintain line numbers
        modified_lines = lines.copy()
        applied_count = 0
        
        for block in sorted(event.ai_blocks, key=lambda b: b.start_line, reverse=True):
            if block in triggers:
                trigger = triggers[block]
                
                # Generate the replacement code
                replacement_code = generator.format_trigger_for_replacement(trigger)
                
                # Build the complete replacement content
                replacement_content = []
                
                # Add start marker if NOT deleting markers
                if not config_manager.should_delete_markers() and block.start_marker_line:
                    replacement_content.append(block.start_marker_line)
                
                # Add preserved comments if enabled
                if config_manager.should_preserve_comments() and block.preserved_comments:
                    for comment in block.preserved_comments:
                        replacement_content.append(f"\t\t{comment}\n")
                
                # Add the generated trigger code
                replacement_lines = replacement_code.split('\n')
                for line in replacement_lines:
                    if line.strip():
                        replacement_content.append(f"\t\t{line.strip()}\n")
                
                # Add end marker if NOT deleting markers
                if not config_manager.should_delete_markers() and block.end_marker_line:
                    replacement_content.append(block.end_marker_line)
                
                # Replace the AI block content
                if not config_manager.should_delete_markers():
                    # Keep markers: replace only the content between markers
                    if block.ai_block_start_line and block.ai_block_end_line:
                        start_idx = block.ai_block_start_line - 1  # Convert to 0-based index
                        end_idx = block.ai_block_end_line
                    else:
                        # Fallback to the entire block if AI block boundaries are not available
                        start_idx = block.start_line - 1  # Convert to 0-based index
                        end_idx = block.end_line
                else:
                    # Delete markers: replace the entire AI block (including markers)
                    start_idx = block.start_line - 1  # Convert to 0-based index
                    end_idx = block.end_line
                
                # Remove the old AI block lines
                del modified_lines[start_idx:end_idx]
                
                # Insert the new content
                for i, line in enumerate(replacement_content):
                    modified_lines.insert(start_idx + i, line)
                
                applied_count += 1
        
        # Write the modified file
        if applied_count > 0:
            with open(event.file_path, 'w', encoding='utf-8') as file:
                file.writelines(modified_lines)
            print(f"  - Applied {applied_count} triggers to {event.file_path.name}")
        else:
            print(f"  - No triggers applied to {event.file_path.name}")


def validate_generated_triggers(triggers: Dict[AIBlock, GeneratedTrigger], config_manager: ConfigManager) -> None:
    """
    Validate all generated triggers for potential issues.
    
    Args:
        triggers: Dictionary mapping AI blocks to their triggers
        config_manager: ConfigManager instance
    """
    if not config_manager.should_validate_triggers():
        print("Validation skipped (disabled in config)")
        return
    
    print("Validating generated triggers...")
    
    generator = CK3TriggerGenerator(config_manager)
    total_errors = 0
    
    for block, trigger in triggers.items():
        errors = generator.validate_trigger_code(trigger)
        if errors:
            print(f"  - Validation errors for '{block.model_name}' in {block.file_path.name}:")
            for error in errors:
                print(f"    * {error}")
            total_errors += len(errors)
    
    if total_errors == 0:
        print("  - All triggers passed validation")
    else:
        print(f"  - Found {total_errors} validation errors")


def print_summary(parsed_events: List[ParsedEvent], triggers: Dict[AIBlock, GeneratedTrigger], config_manager: ConfigManager) -> None:
    """
    Print a summary of the processing results.
    
    Args:
        parsed_events: List of parsed event files
        triggers: Dictionary mapping AI blocks to their triggers
        config_manager: ConfigManager instance
    """
    if not config_manager.should_show_summary():
        return
    
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    
    total_files = len(parsed_events)
    files_with_ai_lib = sum(1 for event in parsed_events if event.has_ai_lib)
    total_ai_blocks = sum(len(event.ai_blocks) for event in parsed_events)
    successful_triggers = len(triggers)
    
    print(f"Event files processed: {total_files}")
    print(f"Files with AI-MODEL-LIB: {files_with_ai_lib}")
    print(f"AI blocks found: {total_ai_blocks}")
    print(f"Triggers generated: {successful_triggers}")
    
    if total_ai_blocks > 0:
        success_rate = (successful_triggers / total_ai_blocks) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    # Show model usage statistics
    model_usage = {}
    for block, trigger in triggers.items():
        model_name = trigger.model_name
        model_usage[model_name] = model_usage.get(model_name, 0) + 1
    
    if model_usage:
        print(f"\nModel usage:")
        for model_name, count in sorted(model_usage.items()):
            print(f"  - {model_name}: {count} triggers")
    
    print("="*50)


def main() -> None:
    """Main program entry point."""
    print("CK3 AI Weight Generator (Unified Trait-Based System)")
    print("=" * 50)
    
    try:
        # Load configuration
        config_manager = ConfigManager("config.json")
        
        # Setup environment
        setup_environment(config_manager)
        
        # Load AI models and traits
        model_manager = load_ai_models(config_manager)
        
        # Validate model references
        if not validate_model_references(model_manager):
            print("Model validation failed. Please fix the issues before proceeding.")
            sys.exit(1)
        
        # Parse event files
        events_dir = config_manager.get_events_directory()
        parsed_events = parse_event_files(events_dir, config_manager)
        
        # Collect all AI blocks
        all_ai_blocks = []
        for event in parsed_events:
            all_ai_blocks.extend(event.ai_blocks)
        
        if not all_ai_blocks:
            print("No AI blocks found. Exiting.")
            return
        
        # Generate triggers using the unified trait-based system
        triggers = generate_triggers_for_blocks(all_ai_blocks, model_manager, config_manager)
        
        if not triggers:
            print("No triggers generated. Exiting.")
            return
        
        # Validate triggers
        validate_generated_triggers(triggers, config_manager)
        
        # Apply triggers to files
        apply_triggers_to_files(parsed_events, triggers, config_manager)
        
        # Print summary
        print_summary(parsed_events, triggers, config_manager)
        
        print("\nProcessing complete!")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 