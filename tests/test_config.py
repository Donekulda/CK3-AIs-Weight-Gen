#!/usr/bin/env python3
"""
Test script for the new CK3 configuration system.
"""

import sys
from pathlib import Path

from src.config_manager import ConfigManager


def test_config_loading():
    """Test basic configuration loading."""
    print("Testing configuration loading...")
    
    try:
        config_manager = ConfigManager()
        mod_config = config_manager.get_mod_config()
        program_config = config_manager.get_program_config()
        
        print("✅ Configuration loaded successfully")
        print(f"  Mod name: {mod_config.name}")
        print(f"  Project group: {mod_config.project_group}")
        print(f"  Events directory: {program_config.events_directory}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False


def test_descriptor_parsing():
    """Test descriptor.mod parsing."""
    print("\nTesting descriptor.mod parsing...")
    
    try:
        config_manager = ConfigManager()
        
        # Test with the provided descriptor.mod
        test_mod_path = Path("data")
        if test_mod_path.exists():
            mod_info = config_manager.parse_descriptor_mod(test_mod_path)
            if mod_info:
                print("✅ Descriptor.mod parsed successfully")
                for key, value in mod_info.items():
                    print(f"  {key}: {value}")
                return True
            else:
                print("❌ Failed to parse descriptor.mod")
                return False
        else:
            print("⚠️  No test mod directory found at 'data'")
            return True
            
    except Exception as e:
        print(f"❌ Descriptor parsing failed: {e}")
        return False


def test_path_resolution():
    """Test path resolution logic."""
    print("\nTesting path resolution...")
    
    try:
        config_manager = ConfigManager()
        
        # Test final target path
        target_path = config_manager.get_final_target_path()
        print(f"  Final target path: {target_path}")
        
        # Test final events path
        events_path = config_manager.get_final_events_path()
        print(f"  Final events path: {events_path}")
        
        print("✅ Path resolution completed")
        return True
        
    except Exception as e:
        print(f"❌ Path resolution failed: {e}")
        return False


def test_mod_discovery():
    """Test mod discovery functionality."""
    print("\nTesting mod discovery...")
    
    try:
        config_manager = ConfigManager()
        
        # Test Steam Workshop path
        steam_path = config_manager.get_steam_workshop_path()
        print(f"  Steam Workshop path: {steam_path}")
        print(f"  Steam Workshop exists: {steam_path.exists()}")
        
        # Test Paradox mods path
        paradox_path = config_manager.get_paradox_mod_path()
        print(f"  Paradox mods path: {paradox_path}")
        print(f"  Paradox mods exists: {paradox_path.exists()}")
        
        # Test mod finding
        mods = config_manager.find_ck3_mods()
        print(f"  Found {len(mods)} CK3 mods")
        
        print("✅ Mod discovery completed")
        return True
        
    except Exception as e:
        print(f"❌ Mod discovery failed: {e}")
        return False


def main():
    """Main test function."""
    print("CK3 Configuration System Test")
    print("=" * 40)
    
    tests = [
        test_config_loading,
        test_descriptor_parsing,
        test_path_resolution,
        test_mod_discovery
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 