#!/usr/bin/env python3
"""
CK3 Mod Manager - Utility Script

This script helps users discover and manage CK3 mods for use with the
AI Weight Generator. It can list available mods, show mod details,
and help configure the tool to work with specific mods.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ck3_parser import CK3Parser
from .config_manager import ConfigManager


def print_mod_list(mods: List[Dict[str, Any]]) -> None:
    """
    Print a formatted list of available mods.
    
    Args:
        mods: List of mod information dictionaries
    """
    if not mods:
        print("No CK3 mods found.")
        return
    
    print(f"\nFound {len(mods)} CK3 mods:")
    print("=" * 80)
    
    for i, mod in enumerate(mods, 1):
        print(f"{i:2d}. {mod['display_name']}")
        print(f"     Path: {mod['path']}")
        print(f"     Version: {mod['version']}")
        print(f"     Source: {mod['source']}")
        if mod['description']:
            print(f"     Description: {mod['description']}")
        print()


def print_mod_details(mod: Dict[str, Any]) -> None:
    """
    Print detailed information about a specific mod.
    
    Args:
        mod: Mod information dictionary
    """
    print(f"\nMod Details: {mod['display_name']}")
    print("=" * 50)
    print(f"Name: {mod['display_name']}")
    print(f"Path: {mod['path']}")
    print(f"Version: {mod['version']}")
    print(f"Source: {mod['source']}")
    if mod['description']:
        print(f"Description: {mod['description']}")
    
    # Check for common CK3 directories
    mod_path = Path(mod['path'])
    common_dirs = ["events", "common", "localization", "gfx", "music"]
    
    print("\nMod Structure:")
    for dir_name in common_dirs:
        dir_path = mod_path / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (not found)")
    
    # Check for events files specifically
    events_dir = mod_path / "events"
    if events_dir.exists():
        event_files = list(events_dir.glob("*.txt"))
        print(f"\nEvent Files: {len(event_files)}")
        for event_file in event_files[:5]:  # Show first 5
            print(f"  - {event_file.name}")
        if len(event_files) > 5:
            print(f"  ... and {len(event_files) - 5} more")


def generate_config_snippet(mod: Dict[str, Any]) -> str:
    """
    Generate a configuration snippet for a specific mod.
    
    Args:
        mod: Mod information dictionary
        
    Returns:
        Configuration snippet as string
    """
    mod_name = mod['display_name']
    mod_path = mod['path']
    
    # Determine if it's Steam Workshop or Paradox mods
    if "steam" in str(mod_path).lower():
        source_type = "Steam Workshop"
        config_type = "steam_workshop"
    else:
        source_type = "Paradox Mods"
        config_type = "paradox_mods"
    
    snippet = f"""# Configuration for {mod_name}
# Add this to your config.json in the ck3_mod_config section:

"ck3_mod_config": {{
    "mod_folder_name": "{mod_name}",
    "use_{config_type}": true,
    "use_paradox_mods": {"true" if config_type == "paradox_mods" else "false"},
    "use_steam_workshop": {"true" if config_type == "steam_workshop" else "false"},
    "auto_detect_mods": true,
    "backup_mod_files": true
}}"""
    
    return snippet


def interactive_mod_selection(mods: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Interactive mod selection menu.
    
    Args:
        mods: List of available mods
        
    Returns:
        Selected mod or None if cancelled
    """
    if not mods:
        print("No mods available for selection.")
        return None
    
    while True:
        print_mod_list(mods)
        print("Enter mod number to view details, 'q' to quit:")
        
        try:
            choice = input("> ").strip()
            
            if choice.lower() == 'q':
                return None
            
            mod_index = int(choice) - 1
            if 0 <= mod_index < len(mods):
                selected_mod = mods[mod_index]
                print_mod_details(selected_mod)
                
                print("\nOptions:")
                print("1. Use this mod")
                print("2. Generate config snippet")
                print("3. Back to mod list")
                
                sub_choice = input("> ").strip()
                
                if sub_choice == "1":
                    return selected_mod
                elif sub_choice == "2":
                    snippet = generate_config_snippet(selected_mod)
                    print("\nConfiguration snippet:")
                    print(snippet)
                    input("\nPress Enter to continue...")
                elif sub_choice == "3":
                    continue
            else:
                print("Invalid selection. Please try again.")
                
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nSelection cancelled.")
            return None


def main():
    """Main entry point for the CK3 mod manager."""
    print("CK3 Mod Manager")
    print("=" * 50)
    
    try:
        # Initialize parser to get mod discovery functionality
        parser = CK3Parser()
        
        # Discover available mods
        print("Discovering CK3 mods...")
        mods = parser.list_available_mods()
        
        if not mods:
            print("No CK3 mods found.")
            print("\nTroubleshooting:")
            print("1. Make sure CK3 is installed")
            print("2. Check if you have any mods installed")
            print("3. Verify the paths in your config.json:")
            
            config = parser.config_manager
            print(f"   Steam Workshop: {config.get_steam_workshop_path()}")
            print(f"   Paradox Mods: {config.get_paradox_mod_path()}")
            
            return
        
        # Interactive menu
        selected_mod = interactive_mod_selection(mods)
        
        if selected_mod:
            print(f"\nSelected mod: {selected_mod['display_name']}")
            print("\nTo use this mod with the AI Weight Generator:")
            print("1. Copy the configuration snippet above")
            print("2. Add it to your config.json file")
            print("3. Run the parser with: python ck3_parser.py")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 