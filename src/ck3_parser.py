#!/usr/bin/env python3
"""
CK3 Parser - Main Control Script

This is the primary control script for parsing Crusader Kings 3 files.
It can handle multiple file types including events, and is designed to be
extensible for future CK3 file types.

The parser supports both local development and CK3 mod folder integration.
"""

import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ai_model_manager import AIModelManager
from .ck3_trigger_generator import CK3TriggerGenerator, GeneratedTrigger

# Import our custom modules
from .config_manager import ConfigManager
from .event_parser import AIBlock, EventParser, ParsedEvent


class FileType(Enum):
    """Enumeration for supported CK3 file types."""
    EVENTS = "events"
    COMMON = "common"
    LOCALIZATION = "localization"
    GFX = "gfx"
    MUSIC = "music"
    INTERFACE = "interface"


@dataclass
class ParseResult:
    """Result of parsing a specific file type."""
    file_type: FileType
    files_processed: int
    files_with_ai_blocks: int
    total_ai_blocks: int
    successful_triggers: int
    errors: List[str]
    parsed_data: Any


@dataclass
class ProcessingSummary:
    """Summary of all processing results."""
    project_name: str
    project_group: str
    target_mod: Optional[str]
    file_types_processed: List[FileType]
    total_files: int
    total_ai_blocks: int
    total_triggers: int
    total_errors: int
    results_by_type: Dict[FileType, ParseResult]


class CK3Parser:
    """Main parser class for CK3 files with mod folder support."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the CK3 parser.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_manager = ConfigManager(config_file)
        self.mod_config = self.config_manager.get_mod_config()
        
        # Initialize parsers
        self.event_parser = EventParser(self.config_manager)
        self.ai_model_manager = None
        self.trigger_generator = None
        
        # Processing state
        self.target_mod_path = None
        self.processing_results = []
        
    def setup_environment(self) -> bool:
        """
        Set up the parsing environment.
        
        Returns:
            True if setup successful, False otherwise
        """
        print(f"Setting up {self.mod_config.name} v{self.mod_config.version}")
        print(f"Project Group: {self.mod_config.project_group}")
        print(f"Author: {self.mod_config.author}")
        print("=" * 50)
        
        # Load AI models
        try:
            print("Loading AI models and traits...")
            self.ai_model_manager = AIModelManager(self.config_manager)
            self.trigger_generator = CK3TriggerGenerator(self.config_manager)
            print("AI models loaded successfully.")
        except Exception as e:
            print(f"Error loading AI models: {e}")
            return False
        
        # Determine target path
        self.target_mod_path = self._determine_target_path()
        if self.target_mod_path:
            print(f"Target mod: {self.target_mod_path}")
        else:
            print("Using local development mode")
        
        return True
    
    def _determine_target_path(self) -> Optional[Path]:
        """
        Determine the target path for processing.
        
        Returns:
            Path to target mod or None for local development
        """
        # Use the new final target path logic
        target_path = self.config_manager.get_final_target_path()
        
        # Check if this is a valid mod path
        if target_path.exists() and target_path.is_dir():
            # Check if it's a mod directory
            if (target_path / "descriptor.mod").exists() or (target_path / "events").exists():
                return target_path
        
        # Check if we should use a specific mod by name
        if self.mod_config.mod_folder_name:
            return self.config_manager.get_target_mod_path()
        
        return None
    
    def list_available_mods(self) -> List[Dict[str, Any]]:
        """
        List all available CK3 mods.
        
        Returns:
            List of mod information dictionaries
        """
        mods = []
        
        if self.config_manager.should_use_steam_workshop():
            steam_path = self.config_manager.get_steam_workshop_path()
            if steam_path.exists():
                print(f"Scanning Steam Workshop: {steam_path}")
                for mod_folder in steam_path.iterdir():
                    if mod_folder.is_dir() and mod_folder.name.isdigit():
                        mod_info = self._get_mod_info(mod_folder)
                        if mod_info:
                            mods.append(mod_info)
        
        if self.config_manager.should_use_paradox_mods():
            paradox_path = self.config_manager.get_paradox_mod_path()
            if paradox_path.exists():
                print(f"Scanning Paradox mods: {paradox_path}")
                for mod_folder in paradox_path.iterdir():
                    if mod_folder.is_dir():
                        mod_info = self._get_mod_info(mod_folder)
                        if mod_info:
                            mods.append(mod_info)
        
        return mods
    
    def _get_mod_info(self, mod_path: Path) -> Optional[Dict[str, Any]]:
        """
        Get information about a mod.
        
        Args:
            mod_path: Path to mod directory
            
        Returns:
            Mod information dictionary or None if invalid
        """
        if not self.config_manager._is_valid_ck3_mod(mod_path):
            return None
        
        descriptor_file = mod_path / "descriptor.mod"
        mod_info = {
            "path": mod_path,
            "name": mod_path.name,
            "display_name": mod_path.name,
            "version": "Unknown",
            "description": "",
            "source": "Unknown"
        }
        
        if descriptor_file.exists():
            try:
                with open(descriptor_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Extract mod information
                    import re
                    
                    name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
                    if name_match:
                        mod_info["display_name"] = name_match.group(1)
                    
                    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
                    if version_match:
                        mod_info["version"] = version_match.group(1)
                    
                    desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
                    if desc_match:
                        mod_info["description"] = desc_match.group(1)
                    
                    # Determine source
                    if "steam" in str(mod_path).lower():
                        mod_info["source"] = "Steam Workshop"
                    else:
                        mod_info["source"] = "Paradox Mods"
                        
            except Exception:
                pass
        
        return mod_info
    
    def parse_events(self) -> ParseResult:
        """
        Parse event files.
        
        Returns:
            ParseResult for events
        """
        print("\nParsing event files...")
        
        # Determine events directory
        if self.target_mod_path:
            events_dir = self.target_mod_path / "events"
        else:
            events_dir = self.config_manager.get_events_directory()
        
        if not events_dir.exists():
            return ParseResult(
                file_type=FileType.EVENTS,
                files_processed=0,
                files_with_ai_blocks=0,
                total_ai_blocks=0,
                successful_triggers=0,
                errors=[f"Events directory not found: {events_dir}"],
                parsed_data=[]
            )
        
        try:
            parsed_events = self.event_parser.parse_events_directory(events_dir)
            
            # Generate triggers
            all_ai_blocks = []
            for event in parsed_events:
                all_ai_blocks.extend(event.ai_blocks)
            
            triggers = {}
            for block in all_ai_blocks:
                if self.ai_model_manager.model_exists(block.model_name):
                    model = self.ai_model_manager.get_model(block.model_name)
                    trigger = self.trigger_generator.generate_trigger_from_model(model)
                    triggers[block] = trigger
            
            return ParseResult(
                file_type=FileType.EVENTS,
                files_processed=len(parsed_events),
                files_with_ai_blocks=sum(1 for e in parsed_events if e.has_ai_lib),
                total_ai_blocks=len(all_ai_blocks),
                successful_triggers=len(triggers),
                errors=[],
                parsed_data={"events": parsed_events, "triggers": triggers}
            )
            
        except Exception as e:
            return ParseResult(
                file_type=FileType.EVENTS,
                files_processed=0,
                files_with_ai_blocks=0,
                total_ai_blocks=0,
                successful_triggers=0,
                errors=[f"Error parsing events: {e}"],
                parsed_data=[]
            )
    
    def parse_all(self, file_types: Optional[List[FileType]] = None) -> ProcessingSummary:
        """
        Parse all specified file types.
        
        Args:
            file_types: List of file types to parse, or None for all
            
        Returns:
            ProcessingSummary with all results
        """
        if file_types is None:
            file_types = [FileType.EVENTS]  # Currently only events supported
        
        print(f"\nStarting parsing of {len(file_types)} file types...")
        
        results_by_type = {}
        total_files = 0
        total_ai_blocks = 0
        total_triggers = 0
        total_errors = 0
        
        for file_type in file_types:
            if file_type == FileType.EVENTS:
                result = self.parse_events()
            else:
                # Placeholder for future file types
                result = ParseResult(
                    file_type=file_type,
                    files_processed=0,
                    files_with_ai_blocks=0,
                    total_ai_blocks=0,
                    successful_triggers=0,
                    errors=[f"File type {file_type.value} not yet implemented"],
                    parsed_data=[]
                )
            
            results_by_type[file_type] = result
            total_files += result.files_processed
            total_ai_blocks += result.total_ai_blocks
            total_triggers += result.successful_triggers
            total_errors += len(result.errors)
            
            # Print result summary
            print(f"\n{file_type.value.upper()} Results:")
            print(f"  Files processed: {result.files_processed}")
            print(f"  Files with AI blocks: {result.files_with_ai_blocks}")
            print(f"  Total AI blocks: {result.total_ai_blocks}")
            print(f"  Successful triggers: {result.successful_triggers}")
            if result.errors:
                print(f"  Errors: {len(result.errors)}")
                for error in result.errors:
                    print(f"    - {error}")
        
        return ProcessingSummary(
            project_name=self.mod_config.name,
            project_group=self.mod_config.project_group,
            target_mod=self.mod_config.mod_folder_name or None,
            file_types_processed=file_types,
            total_files=total_files,
            total_ai_blocks=total_ai_blocks,
            total_triggers=total_triggers,
            total_errors=total_errors,
            results_by_type=results_by_type
        )
    
    def apply_changes(self, summary: ProcessingSummary) -> bool:
        """
        Apply generated changes to files.
        
        Args:
            summary: Processing summary with results
            
        Returns:
            True if successful, False otherwise
        """
        print("\nApplying changes to files...")
        
        success = True
        
        for file_type, result in summary.results_by_type.items():
            if file_type == FileType.EVENTS and result.parsed_data:
                try:
                    self._apply_event_changes(result.parsed_data)
                    print(f"  ✅ Applied changes to {file_type.value}")
                except Exception as e:
                    print(f"  ❌ Error applying changes to {file_type.value}: {e}")
                    success = False
            elif result.errors:
                print(f"  ⚠️  Skipping {file_type.value} due to errors")
        
        return success
    
    def _apply_event_changes(self, parsed_data: Dict[str, Any]) -> None:
        """
        Apply changes to event files.
        
        Args:
            parsed_data: Parsed event data with triggers
        """
        events = parsed_data.get("events", [])
        triggers = parsed_data.get("triggers", {})
        
        for event in events:
            if not event.ai_blocks:
                continue
            
            # Create backup if enabled
            if self.target_mod_path:
                backup_path = self.config_manager.create_mod_backup(event.file_path)
            else:
                backup_path = self.config_manager.create_backup(event.file_path)
            
            if backup_path:
                print(f"    Created backup: {backup_path.name}")
            
            # Apply triggers
            self._apply_triggers_to_event_file(event, triggers)
    
    def _apply_triggers_to_event_file(self, event: ParsedEvent, triggers: Dict[AIBlock, GeneratedTrigger]) -> None:
        """
        Apply triggers to a single event file.
        
        Args:
            event: Parsed event file
            triggers: Dictionary mapping AI blocks to triggers
        """
        # Read the original file
        with open(event.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Apply triggers in reverse order to maintain line numbers
        modified_lines = lines.copy()
        applied_count = 0
        
        for block in sorted(event.ai_blocks, key=lambda b: b.start_line, reverse=True):
            if block in triggers:
                trigger = triggers[block]
                
                # Generate replacement code
                replacement_code = self.trigger_generator.format_trigger_for_replacement(trigger)
                
                # Build replacement content
                replacement_content = []
                
                # Add start marker if NOT deleting markers
                if not self.config_manager.should_delete_markers() and block.start_marker_line:
                    replacement_content.append(block.start_marker_line)
                
                # Add preserved comments if enabled
                if self.config_manager.should_preserve_comments() and block.preserved_comments:
                    for comment in block.preserved_comments:
                        replacement_content.append(f"\t\t{comment}\n")
                
                # Add generated trigger code
                replacement_lines = replacement_code.split('\n')
                for line in replacement_lines:
                    if line.strip():
                        replacement_content.append(f"\t\t{line.strip()}\n")
                
                # Add end marker if NOT deleting markers
                if not self.config_manager.should_delete_markers() and block.end_marker_line:
                    replacement_content.append(block.end_marker_line)
                
                # Replace the AI block content
                if not self.config_manager.should_delete_markers():
                    if block.ai_block_start_line and block.ai_block_end_line:
                        start_idx = block.ai_block_start_line - 1
                        end_idx = block.ai_block_end_line
                    else:
                        start_idx = block.start_line - 1
                        end_idx = block.end_line
                else:
                    start_idx = block.start_line - 1
                    end_idx = block.end_line
                
                # Remove old lines and insert new content
                del modified_lines[start_idx:end_idx]
                for i, line in enumerate(replacement_content):
                    modified_lines.insert(start_idx + i, line)
                
                applied_count += 1
        
        # Write modified file
        if applied_count > 0:
            with open(event.file_path, 'w', encoding='utf-8') as file:
                file.writelines(modified_lines)
            print(f"    Applied {applied_count} triggers to {event.file_path.name}")
    
    def print_summary(self, summary: ProcessingSummary) -> None:
        """
        Print a comprehensive summary of processing results.
        
        Args:
            summary: Processing summary to display
        """
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        print(f"Project: {summary.project_name}")
        print(f"Group: {summary.project_group}")
        if summary.target_mod:
            print(f"Target Mod: {summary.target_mod}")
        print(f"File Types Processed: {len(summary.file_types_processed)}")
        print(f"Total Files: {summary.total_files}")
        print(f"Total AI Blocks: {summary.total_ai_blocks}")
        print(f"Total Triggers Generated: {summary.total_triggers}")
        print(f"Total Errors: {summary.total_errors}")
        
        if summary.total_ai_blocks > 0:
            success_rate = (summary.total_triggers / summary.total_ai_blocks) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print("\nResults by File Type:")
        for file_type, result in summary.results_by_type.items():
            print(f"  {file_type.value.upper()}:")
            print(f"    Files: {result.files_processed}")
            print(f"    AI Blocks: {result.total_ai_blocks}")
            print(f"    Triggers: {result.successful_triggers}")
            if result.errors:
                print(f"    Errors: {len(result.errors)}")
        
        print("="*60)


def main():
    """Main entry point for the CK3 parser."""
    parser = CK3Parser()
    
    try:
        # Setup environment
        if not parser.setup_environment():
            print("Environment setup failed. Exiting.")
            sys.exit(1)
        
        # Parse all supported file types
        summary = parser.parse_all()
        
        # Apply changes if any triggers were generated
        if summary.total_triggers > 0:
            if parser.apply_changes(summary):
                print("\n✅ All changes applied successfully!")
            else:
                print("\n⚠️  Some changes failed to apply.")
        else:
            print("\nℹ️  No triggers generated. No changes to apply.")
        
        # Print final summary
        parser.print_summary(summary)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 