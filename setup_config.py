#!/usr/bin/env python3
"""
CK3 AI Weight Generator - Configuration Setup

This script helps users set up their configuration for the CK3 AI Weight Generator,
including CK3 mod folder detection and project configuration.
"""

import json
import sys
from pathlib import Path
from typing import Dict

from src.config_manager import ConfigManager


def create_user_config() -> bool:
    """
    Create a user configuration file from the default.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        config_manager = ConfigManager()
        
        if config_manager.has_user_config():
            print("User configuration already exists.")
            return True
        
        if config_manager.create_user_config_from_default():
            print("User configuration created successfully!")
            return True
        else:
            print("Failed to create user configuration.")
            return False
            
    except Exception as e:
        print(f"Error creating configuration: {e}")
        return False


def detect_ck3_paths() -> Dict[str, str]:
    """
    Detect common CK3 installation and mod paths.
    
    Returns:
        Dictionary of detected paths
    """
    paths = {}
    
    # Common Steam Workshop paths
    steam_paths = [
        "~/.steam/steam/steamapps/workshop/content/1158310",
        "C:/Program Files (x86)/Steam/steamapps/workshop/content/1158310",
        "C:/Steam/steamapps/workshop/content/1158310"
    ]
    
    for path in steam_paths:
        expanded_path = Path(path).expanduser()
        if expanded_path.exists():
            paths["steam_workshop"] = str(expanded_path)
            break
    
    # Common Paradox mod paths
    paradox_paths = [
        "~/.local/share/Paradox Interactive/Crusader Kings III/mod",
        "~/Documents/Paradox Interactive/Crusader Kings III/mod",
        "C:/Users/*/Documents/Paradox Interactive/Crusader Kings III/mod"
    ]
    
    for path in paradox_paths:
        expanded_path = Path(path).expanduser()
        if expanded_path.exists():
            paths["paradox_mods"] = str(expanded_path)
            break
    
    return paths


def update_config_with_paths(config_file: Path, paths: Dict[str, str]) -> bool:
    """
    Update configuration file with detected paths.
    
    Args:
        config_file: Path to configuration file
        paths: Dictionary of detected paths
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read current config
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        # Update CK3 mod config section
        if "ck3_mod_config" not in config:
            config["ck3_mod_config"] = {}
        
        ck3_config = config["ck3_mod_config"]
        
        if "steam_workshop" in paths:
            ck3_config["steam_workshop_path"] = paths["steam_workshop"]
            ck3_config["use_steam_workshop"] = True
        
        if "paradox_mods" in paths:
            ck3_config["paradox_mod_path"] = paths["paradox_mods"]
            ck3_config["use_paradox_mods"] = True
        
        # Write updated config
        with open(config_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        print(f"Error updating configuration: {e}")
        return False


def interactive_project_setup(config_file: Path) -> bool:
    """
    Interactive project setup.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read current config
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        print("\nMod Configuration:")
        print("=" * 30)
        
        # Get mod info
        mod_name = input("Mod name [CK3 AI Weight Generator]: ").strip()
        if not mod_name:
            mod_name = "CK3 AI Weight Generator"
        
        project_group = input("Project group [default]: ").strip()
        if not project_group:
            project_group = "default"
        
        author = input("Author name [CK3 Modder]: ").strip()
        if not author:
            author = "CK3 Modder"
        
        # Update mod_config section
        if "mod_config" not in config:
            config["mod_config"] = {}
        
        mod_config = config["mod_config"]
        
        mod_config["name"] = mod_name
        mod_config["project_group"] = project_group
        mod_config["author"] = author
        
        # Write updated config
        with open(config_file, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        
        print(f"\nMod configured:")
        print(f"  Name: {mod_name}")
        print(f"  Group: {project_group}")
        print(f"  Author: {author}")
        
        return True
        
    except Exception as e:
        print(f"Error in mod setup: {e}")
        return False


def setup_from_descriptor(mod_path: Path) -> bool:
    """
    Set up configuration from a descriptor.mod file.
    
    Args:
        mod_path: Path to mod directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        config_manager = ConfigManager()
        
        print(f"Setting up configuration from mod: {mod_path}")
        
        # Parse descriptor.mod
        mod_info = config_manager.parse_descriptor_mod(mod_path)
        if not mod_info:
            print("No descriptor.mod found or failed to parse.")
            return False
        
        print("Found mod information:")
        for key, value in mod_info.items():
            print(f"  {key}: {value}")
        
        # Update configuration
        if config_manager.update_config_from_descriptor(mod_path):
            print("Configuration updated successfully!")
            return True
        else:
            print("Failed to update configuration.")
            return False
            
    except Exception as e:
        print(f"Error setting up from descriptor: {e}")
        return False


def main():
    """Main entry point for configuration setup."""
    print("CK3 AI Weight Generator - Configuration Setup")
    print("=" * 50)
    
    try:
        # Check if user wants to set up from a mod directory
        if len(sys.argv) > 1:
            mod_path = Path(sys.argv[1])
            if mod_path.exists() and mod_path.is_dir():
                if setup_from_descriptor(mod_path):
                    print("\nSetup complete!")
                    return
                else:
                    print("Setup from descriptor failed, continuing with manual setup...")
        
        # Create user config if it doesn't exist
        if not create_user_config():
            print("Failed to create configuration. Exiting.")
            sys.exit(1)
        
        config_file = Path("config.json")
        
        # Detect CK3 paths
        print("\nDetecting CK3 installation paths...")
        paths = detect_ck3_paths()
        
        if paths:
            print("Detected paths:")
            for path_type, path in paths.items():
                print(f"  {path_type}: {path}")
            
            # Update config with detected paths
            if update_config_with_paths(config_file, paths):
                print("Configuration updated with detected paths.")
            else:
                print("Failed to update configuration with paths.")
        else:
            print("No CK3 paths detected automatically.")
            print("You may need to manually configure paths in config.json")
        
        # Interactive mod setup
        print("\nSetting up mod information...")
        if interactive_project_setup(config_file):
            print("Mod setup complete!")
        else:
            print("Mod setup failed.")
        
        print("\nConfiguration setup complete!")
        print("\nNext steps:")
        print("1. Review config.json and adjust settings if needed")
        print("2. Run 'python ck3_mod_manager.py' to discover available mods")
        print("3. Run 'python ck3_parser.py' to process your mods")
        print("\nOr run: python setup_config.py <mod_directory> to set up from a mod")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 