#!/usr/bin/env python3
"""
CK3 AI Weight Generator - Main Program

This program processes CK3 event files to generate AI modifiers based on
predefined AI models. It reads event files, extracts AI model references,
and generates appropriate CK3 triggers using the unified trait-based system.

This version uses the new CK3Parser for enhanced mod folder support.
"""

import sys
from pathlib import Path

# Import our custom modules
from src.ck3_parser import CK3Parser


def setup_environment() -> bool:
    """Set up the Python environment and check dependencies."""
    print("Setting up CK3 AI Weight Generator environment...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Warning: Not running in a virtual environment. Consider using one.")
    
    # Check if config file exists
    config_file = Path("config.json")
    if not config_file.exists():
        default_config = Path("config.default.json")
        if default_config.exists():
            print(f"User config file '{config_file}' not found.")
            print(f"Using default configuration from '{default_config}'")
            print("To create your own config, copy 'config.default.json' to 'config.json' and modify as needed.")
        else:
            print("Error: No configuration file found.")
            return False
    
    print("Environment setup complete.")
    return True


def main() -> None:
    """Main program entry point."""
    print("CK3 AI Weight Generator (Unified Trait-Based System)")
    print("Enhanced with CK3 Mod Folder Support")
    print("=" * 60)
    
    try:
        # Setup environment
        if not setup_environment():
            print("Environment setup failed. Exiting.")
            sys.exit(1)
        
        # Initialize the CK3 parser
        parser = CK3Parser("config.json")
        
        # Setup parser environment
        if not parser.setup_environment():
            print("Parser setup failed. Exiting.")
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
        
        print("\nProcessing complete!")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 