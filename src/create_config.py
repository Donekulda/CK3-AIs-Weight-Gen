#!/usr/bin/env python3
"""
Utility script to create a user configuration file from the default configuration.

This script helps users set up their own configuration by copying the default
configuration file to config.json, which they can then modify with their custom settings.
"""

import sys
from pathlib import Path

from .config_manager import ConfigManager


def main():
    """Main function to create user configuration."""
    print("CK3 AI Weight Generator - Configuration Setup")
    print("=" * 50)
    
    try:
        # Create a temporary config manager to access the utility methods
        config_manager = ConfigManager()
        
        # Check if user config already exists
        if config_manager.has_user_config():
            print(f"User configuration file already exists: {config_manager.config_file_path}")
            print("If you want to recreate it, please delete the existing file first.")
            return 1
        
        # Check if default config exists
        if not config_manager.has_default_config():
            print(f"Default configuration file not found: {config_manager.default_config_path}")
            print("Please ensure config.default.json exists in the current directory.")
            return 1
        
        # Create user config from default
        if config_manager.create_user_config_from_default():
            print("\nConfiguration setup completed successfully!")
            print("\nNext steps:")
            print("1. Edit config.json with your custom settings")
            print("2. Run the main program")
            return 0
        else:
            print("Failed to create user configuration file.")
            return 1
            
    except Exception as e:
        print(f"Error during configuration setup: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 