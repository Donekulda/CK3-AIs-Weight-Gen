"""
Configuration Manager for CK3 AI Weight Generator

This module contains classes for managing program configuration and settings.
"""

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ModConfig:
    """Configuration for mod information and CK3 mod folder management."""
    name: str
    version: str
    description: str
    project_group: str
    author: str
    steam_workshop_path: str
    paradox_mod_path: str
    game_install_path: str
    mod_folder_name: str
    use_steam_workshop: bool
    use_paradox_mods: bool
    auto_detect_mods: bool
    backup_mod_files: bool
    mod_backup_suffix: str


@dataclass
class AIMarkers:
    """Configuration for AI markers in event files."""
    library_marker: str
    start_marker: str
    end_marker: str
    model_pattern: str
    comment_pattern: str


@dataclass
class ProcessingConfig:
    """Configuration for file processing behavior."""
    preserve_comments: bool
    delete_markers: bool
    backup_files: bool
    backup_suffix: str


@dataclass
class OutputConfig:
    """Configuration for output and logging."""
    indent_level: int
    validate_triggers: bool
    show_summary: bool
    verbose_logging: bool


@dataclass
class TargetConfig:
    """Configuration for target mod and events folders."""
    events_directory: str
    mod_folder: str
    should_use_mod_folder: bool
    is_parent: bool


@dataclass
class ProgramConfig:
    """Main program configuration."""
    events_directory: str
    models_directory: str
    models_file: str
    file_extensions: List[str]
    ai_markers: AIMarkers
    processing: ProcessingConfig
    output: OutputConfig
    target: TargetConfig


class ConfigManager:
    """Manages program configuration and AI model definitions."""
    
    def __init__(self, config_file_path: str = "config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file_path: Path to the configuration file
        """
        self.config_file_path = Path(config_file_path)
        self.default_config_path = Path("config.default.json")
        self.config_data: Dict[str, Any] = {}
        self.mod_config: Optional[ModConfig] = None
        self.program_config: Optional[ProgramConfig] = None
        self.ai_models: Dict[str, Any] = {}
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from the JSON file."""
        # First try to load user config, then fall back to default
        config_to_load = self.config_file_path
        
        if not self.config_file_path.exists():
            if self.default_config_path.exists():
                print(f"User config file '{self.config_file_path}' not found.")
                print(f"Using default configuration from '{self.default_config_path}'")
                print("To create your own config, copy 'config.default.json' to 'config.json' and modify as needed.")
                config_to_load = self.default_config_path
            else:
                raise FileNotFoundError(
                    f"Configuration file not found: {self.config_file_path}\n"
                    f"Default configuration file not found: {self.default_config_path}"
                )
        
        try:
            with open(config_to_load, 'r', encoding='utf-8') as file:
                self.config_data = json.load(file)
            
            self._parse_mod_config()
            self._parse_program_config()
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {config_to_load}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading configuration from {config_to_load}: {e}")
    
    def _parse_mod_config(self) -> None:
        """Parse the mod configuration section."""
        mod_data = self.config_data.get('mod_config', {})
        
        self.mod_config = ModConfig(
            name=mod_data.get('name', 'CK3 AI Weight Generator'),
            version=mod_data.get('version', '1.0.0'),
            description=mod_data.get(
                'description', 'AI weight generation tool for CK3 modding'
            ),
            project_group=mod_data.get('project_group', 'default'),
            author=mod_data.get('author', 'CK3 Modder'),
            steam_workshop_path=mod_data.get(
                'steam_workshop_path', 
                '~/.steam/steam/steamapps/workshop/content/1158310'
            ),
            paradox_mod_path=mod_data.get(
                'paradox_mod_path', 
                '~/.local/share/Paradox Interactive/Crusader Kings III/mod'
            ),
            game_install_path=mod_data.get('game_install_path', ''),
            mod_folder_name=mod_data.get('mod_folder_name', ''),
            use_steam_workshop=mod_data.get('use_steam_workshop', True),
            use_paradox_mods=mod_data.get('use_paradox_mods', False),
            auto_detect_mods=mod_data.get('auto_detect_mods', True),
            backup_mod_files=mod_data.get('backup_mod_files', True),
            mod_backup_suffix=mod_data.get('mod_backup_suffix', '.ai_backup')
        )
    
    def _parse_program_config(self) -> None:
        """Parse the program configuration section."""
        prog_config = self.config_data.get('program_config', {})
        
        ai_markers_data = prog_config.get('ai_markers', {})
        ai_markers = AIMarkers(
            library_marker=ai_markers_data.get(
                'library_marker', '# AI-MODEL-LIB'
            ),
            start_marker=ai_markers_data.get('start_marker', '# AI-START'),
            end_marker=ai_markers_data.get('end_marker', '# AI-END'),
            model_pattern=ai_markers_data.get(
                'model_pattern', 'using:\\s*\\{([^}]+)\\}'
            ),
            comment_pattern=ai_markers_data.get('comment_pattern', '#\\s*(.+)')
        )
        
        processing_data = prog_config.get('processing', {})
        processing = ProcessingConfig(
            preserve_comments=processing_data.get('preserve_comments', True),
            delete_markers=processing_data.get('delete_markers', False),
            backup_files=processing_data.get('backup_files', True),
            backup_suffix=processing_data.get('backup_suffix', '.backup')
        )
        
        output_data = prog_config.get('output', {})
        output = OutputConfig(
            indent_level=output_data.get('indent_level', 2),
            validate_triggers=output_data.get('validate_triggers', True),
            show_summary=output_data.get('show_summary', True),
            verbose_logging=output_data.get('verbose_logging', False)
        )
        
        target_data = prog_config.get('target', {})
        target = TargetConfig(
            events_directory=target_data.get('events_directory', 'events'),
            mod_folder=target_data.get('mod_folder', ''),
            should_use_mod_folder=target_data.get('should_use_mod_folder', False),
            is_parent=target_data.get('is_parent', False)
        )
        
        self.program_config = ProgramConfig(
            events_directory=prog_config.get('events_directory', 'events'),
            models_directory=prog_config.get('models_directory', 'models'),
            models_file=prog_config.get('models_file', 'models/ai_models.json'),
            file_extensions=prog_config.get('file_extensions', ['.txt']),
            ai_markers=ai_markers,
            processing=processing,
            output=output,
            target=target
        )
    
    def get_mod_config(self) -> ModConfig:
        """
        Get the mod configuration.
        
        Returns:
            ModConfig instance
        """
        if self.mod_config is None:
            raise RuntimeError("Mod configuration not loaded")
        return self.mod_config
    
    def get_program_config(self) -> ProgramConfig:
        """
        Get the program configuration.
        
        Returns:
            ProgramConfig instance
        """
        if self.program_config is None:
            raise RuntimeError("Program configuration not loaded")
        return self.program_config
    
    def get_events_directory(self) -> Path:
        """
        Get the events directory path.
        
        Returns:
            Path to the events directory
        """
        config = self.get_program_config()
        return Path(config.events_directory)
    
    def get_models_directory(self) -> Path:
        """
        Get the models directory path.
        
        Returns:
            Path to the models directory
        """
        config = self.get_program_config()
        return Path(config.models_directory)
    
    def get_models_file(self) -> Path:
        """
        Get the models file path.
        
        Returns:
            Path to the models file
        """
        config = self.get_program_config()
        return Path(config.models_file)
    
    def should_preserve_comments(self) -> bool:
        """
        Check if comments should be preserved.
        
        Returns:
            True if comments should be preserved
        """
        config = self.get_program_config()
        return config.processing.preserve_comments
    
    def should_delete_markers(self) -> bool:
        """
        Check if AI markers should be deleted.
        
        Returns:
            True if markers should be deleted
        """
        config = self.get_program_config()
        return config.processing.delete_markers
    
    def should_backup_files(self) -> bool:
        """
        Check if files should be backed up before modification.
        
        Returns:
            True if files should be backed up
        """
        config = self.get_program_config()
        return config.processing.backup_files
    
    def get_backup_suffix(self) -> str:
        """
        Get the backup file suffix.
        
        Returns:
            Backup file suffix
        """
        config = self.get_program_config()
        return config.processing.backup_suffix
    
    def get_indent_level(self) -> int:
        """
        Get the indentation level for generated code.
        
        Returns:
            Indentation level
        """
        config = self.get_program_config()
        return config.output.indent_level
    
    def should_validate_triggers(self) -> bool:
        """
        Check if triggers should be validated.
        
        Returns:
            True if triggers should be validated
        """
        config = self.get_program_config()
        return config.output.validate_triggers
    
    def should_show_summary(self) -> bool:
        """
        Check if summary should be shown.
        
        Returns:
            True if summary should be shown
        """
        config = self.get_program_config()
        return config.output.show_summary
    
    def is_verbose_logging(self) -> bool:
        """
        Check if verbose logging is enabled.
        
        Returns:
            True if verbose logging is enabled
        """
        config = self.get_program_config()
        return config.output.verbose_logging
    
    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of a file if backup is enabled.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to the backup file if created, None otherwise
        """
        if not self.should_backup_files():
            return None
        
        if not file_path.exists():
            return None
        
        backup_path = file_path.with_suffix(file_path.suffix + self.get_backup_suffix())
        
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Warning: Failed to create backup of {file_path}: {e}")
            return None
    
    def get_file_extensions(self) -> List[str]:
        """
        Get the file extensions to process.
        
        Returns:
            List of file extensions
        """
        config = self.get_program_config()
        return config.file_extensions
    
    def get_target_events_directory(self) -> Path:
        """
        Get the target events directory path.
        
        Returns:
            Path to the target events directory
        """
        config = self.get_program_config()
        return Path(config.target.events_directory)
    
    def get_target_mod_folder(self) -> Path:
        """
        Get the target mod folder path.
        
        Returns:
            Path to the target mod folder
        """
        config = self.get_program_config()
        return Path(config.target.mod_folder)
    
    def should_use_mod_folder(self) -> bool:
        """
        Check if mod folder should be used.
        
        Returns:
            True if mod folder should be used
        """
        config = self.get_program_config()
        return config.target.should_use_mod_folder
    
    def is_parent_mod_folder(self) -> bool:
        """
        Check if mod folder is in parent directory.
        
        Returns:
            True if mod folder is in parent directory
        """
        config = self.get_program_config()
        return config.target.is_parent
    
    def has_user_config(self) -> bool:
        """
        Check if a user configuration file exists.
        
        Returns:
            True if user config exists, False otherwise
        """
        return self.config_file_path.exists()
    
    def has_default_config(self) -> bool:
        """
        Check if the default configuration file exists.
        
        Returns:
            True if default config exists, False otherwise
        """
        return self.default_config_path.exists()
    
    def create_user_config_from_default(self) -> bool:
        """
        Create a user configuration file by copying the default configuration.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.has_default_config():
            print(f"Default configuration file not found: {self.default_config_path}")
            return False
        
        if self.has_user_config():
            print(f"User configuration file already exists: {self.config_file_path}")
            return False
        
        try:
            shutil.copy2(self.default_config_path, self.config_file_path)
            print(f"Created user configuration file: {self.config_file_path}")
            print("You can now modify this file with your custom settings.")
            return True
        except Exception as e:
            print(f"Failed to create user configuration file: {e}")
            return False
    
    def get_current_config_source(self) -> str:
        """
        Get the source of the currently loaded configuration.
        
        Returns:
            String indicating which config file is being used
        """
        if self.has_user_config():
            return f"User config: {self.config_file_path}"
        elif self.has_default_config():
            return f"Default config: {self.default_config_path}"
        else:
            return "No config file found"
    
    def expand_path(self, path_str: str) -> Path:
        """
        Expand a path string, handling home directory and environment variables.
        
        Args:
            path_str: Path string to expand
            
        Returns:
            Expanded Path object
        """
        if not path_str:
            return Path()
        
        # Expand user home directory
        expanded = os.path.expanduser(path_str)
        # Expand environment variables
        expanded = os.path.expandvars(expanded)
        
        return Path(expanded)
    
    def get_steam_workshop_path(self) -> Path:
        """
        Get the Steam Workshop path for CK3 mods.
        
        Returns:
            Path to Steam Workshop CK3 mods directory
        """
        mod_config = self.get_mod_config()
        return self.expand_path(mod_config.steam_workshop_path)
    
    def get_paradox_mod_path(self) -> Path:
        """
        Get the Paradox mods path for CK3.
        
        Returns:
            Path to Paradox CK3 mods directory
        """
        mod_config = self.get_mod_config()
        return self.expand_path(mod_config.paradox_mod_path)
    
    def get_game_install_path(self) -> Path:
        """
        Get the CK3 game installation path.
        
        Returns:
            Path to CK3 game installation
        """
        mod_config = self.get_mod_config()
        return self.expand_path(mod_config.game_install_path)
    
    def get_mod_folder_name(self) -> str:
        """
        Get the configured mod folder name.
        
        Returns:
            Mod folder name
        """
        mod_config = self.get_mod_config()
        return mod_config.mod_folder_name
    
    def should_use_steam_workshop(self) -> bool:
        """
        Check if Steam Workshop should be used.
        
        Returns:
            True if Steam Workshop should be used
        """
        mod_config = self.get_mod_config()
        return mod_config.use_steam_workshop
    
    def should_use_paradox_mods(self) -> bool:
        """
        Check if Paradox mods should be used.
        
        Returns:
            True if Paradox mods should be used
        """
        mod_config = self.get_mod_config()
        return mod_config.use_paradox_mods
    
    def should_auto_detect_mods(self) -> bool:
        """
        Check if mods should be auto-detected.
        
        Returns:
            True if mods should be auto-detected
        """
        mod_config = self.get_mod_config()
        return mod_config.auto_detect_mods
    
    def should_backup_mod_files(self) -> bool:
        """
        Check if mod files should be backed up.
        
        Returns:
            True if mod files should be backed up
        """
        mod_config = self.get_mod_config()
        return mod_config.backup_mod_files
    
    def get_mod_backup_suffix(self) -> str:
        """
        Get the mod backup file suffix.
        
        Returns:
            Mod backup file suffix
        """
        mod_config = self.get_mod_config()
        return mod_config.mod_backup_suffix
    
    def find_ck3_mods(self) -> List[Path]:
        """
        Find all available CK3 mods based on configuration.
        
        Returns:
            List of paths to CK3 mod directories
        """
        mod_paths = []
        
        if self.should_use_steam_workshop():
            steam_path = self.get_steam_workshop_path()
            if steam_path.exists():
                # Steam Workshop mods are in numbered folders
                for mod_folder in steam_path.iterdir():
                    if mod_folder.is_dir() and mod_folder.name.isdigit():
                        # Check if it's a valid CK3 mod
                        if self._is_valid_ck3_mod(mod_folder):
                            mod_paths.append(mod_folder)
        
        if self.should_use_paradox_mods():
            paradox_path = self.get_paradox_mod_path()
            if paradox_path.exists():
                for mod_folder in paradox_path.iterdir():
                    if mod_folder.is_dir():
                        if self._is_valid_ck3_mod(mod_folder):
                            mod_paths.append(mod_folder)
        
        return mod_paths
    
    def _is_valid_ck3_mod(self, mod_path: Path) -> bool:
        """
        Check if a directory is a valid CK3 mod.
        
        Args:
            mod_path: Path to check
            
        Returns:
            True if it's a valid CK3 mod
        """
        # Check for descriptor.mod file
        descriptor_file = mod_path / "descriptor.mod"
        if not descriptor_file.exists():
            return False
        
        # Check for common CK3 mod directories
        common_dirs = ["events", "common", "localization", "gfx", "music"]
        has_mod_content = any((mod_path / dir_name).exists() for dir_name in common_dirs)
        
        return has_mod_content
    
    def get_target_mod_path(self) -> Optional[Path]:
        """
        Get the target mod path based on configuration.
        
        Returns:
            Path to target mod, or None if not configured
        """
        mod_folder_name = self.get_mod_folder_name()
        if not mod_folder_name:
            return None
        
        # First check Steam Workshop
        if self.should_use_steam_workshop():
            steam_path = self.get_steam_workshop_path()
            if steam_path.exists():
                # For Steam Workshop, we need to find the mod by name
                for mod_folder in steam_path.iterdir():
                    if mod_folder.is_dir() and mod_folder.name.isdigit():
                        if self._mod_has_name(mod_folder, mod_folder_name):
                            return mod_folder
        
        # Then check Paradox mods
        if self.should_use_paradox_mods():
            paradox_path = self.get_paradox_mod_path()
            if paradox_path.exists():
                target_path = paradox_path / mod_folder_name
                if target_path.exists() and self._is_valid_ck3_mod(target_path):
                    return target_path
        
        return None
    
    def _mod_has_name(self, mod_path: Path, expected_name: str) -> bool:
        """
        Check if a mod has the expected name by reading its descriptor.
        
        Args:
            mod_path: Path to mod directory
            expected_name: Expected mod name
            
        Returns:
            True if mod has the expected name
        """
        descriptor_file = mod_path / "descriptor.mod"
        if not descriptor_file.exists():
            return False
        
        try:
            with open(descriptor_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Look for name = "mod_name" pattern
                import re
                name_match = re.search(r'name\s*=\s*"([^"]+)"', content)
                if name_match:
                    mod_name = name_match.group(1)
                    return mod_name.lower() == expected_name.lower()
        except Exception:
            pass
        
        return False
    
    def create_mod_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of a mod file if mod backup is enabled.
        
        Args:
            file_path: Path to the file to backup
            
        Returns:
            Path to the backup file if created, None otherwise
        """
        if not self.should_backup_mod_files():
            return None
        
        if not file_path.exists():
            return None
        
        backup_path = file_path.with_suffix(
            file_path.suffix + self.get_mod_backup_suffix()
        )
        
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Warning: Failed to create mod backup of {file_path}: {e}")
            return None
    
    def parse_descriptor_mod(self, mod_path: Path) -> Optional[Dict[str, str]]:
        """
        Parse a descriptor.mod file to extract mod information.
        
        Args:
            mod_path: Path to the mod directory containing descriptor.mod
            
        Returns:
            Dictionary with mod information or None if parsing fails
        """
        descriptor_file = mod_path / "descriptor.mod"
        if not descriptor_file.exists():
            return None
        
        try:
            with open(descriptor_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            mod_info = {}
            
            # Parse key-value pairs from descriptor.mod
            import re

            # Extract common fields
            patterns = {
                'name': r'name\s*=\s*"([^"]+)"',
                'version': r'version\s*=\s*"([^"]+)"',
                'description': r'description\s*=\s*"([^"]+)"',
                'supported_version': r'supported_version\s*=\s*"([^"]+)"',
                'remote_file_id': r'remote_file_id\s*=\s*"([^"]+)"'
            }
            
            for field, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    mod_info[field] = match.group(1)
            
            return mod_info
            
        except Exception as e:
            print(f"Warning: Failed to parse descriptor.mod in {mod_path}: {e}")
            return None
    
    def update_config_from_descriptor(self, mod_path: Path) -> bool:
        """
        Update configuration with information from a descriptor.mod file.
        
        Args:
            mod_path: Path to the mod directory
            
        Returns:
            True if successful, False otherwise
        """
        mod_info = self.parse_descriptor_mod(mod_path)
        if not mod_info:
            return False
        
        try:
            # Read current config
            with open(self.config_file_path, 'r', encoding='utf-8') as file:
                config = json.load(file)
            
            # Update mod_config section
            if 'mod_config' not in config:
                config['mod_config'] = {}
            
            mod_config = config['mod_config']
            
            # Update with descriptor information
            if 'name' in mod_info:
                mod_config['name'] = mod_info['name']
            if 'version' in mod_info:
                mod_config['version'] = mod_info['version']
            if 'description' in mod_info:
                mod_config['description'] = mod_info['description']
            
            # Set mod folder name
            mod_config['mod_folder_name'] = mod_path.name
            
            # Write updated config
            with open(self.config_file_path, 'w', encoding='utf-8') as file:
                json.dump(config, file, indent=2, ensure_ascii=False)
            
            # Reload configuration
            self._load_config()
            
            return True
            
        except Exception as e:
            print(f"Error updating config from descriptor: {e}")
            return False
    
    def get_final_target_path(self) -> Path:
        """
        Get the final target path based on all configuration settings.
        
        Returns:
            Path to the target directory
        """
        target_config = self.get_program_config().target
        
        if target_config.should_use_mod_folder:
            if target_config.mod_folder:
                if target_config.is_parent:
                    # Mod folder is in parent directory
                    return Path("..") / target_config.mod_folder
                else:
                    # Mod folder is in current directory or absolute path
                    return Path(target_config.mod_folder)
            else:
                # Use mod folder name from mod_config
                mod_folder_name = self.get_mod_folder_name()
                if mod_folder_name:
                    # Try to find the mod in Steam Workshop or Paradox mods
                    target_mod_path = self.get_target_mod_path()
                    if target_mod_path:
                        return target_mod_path
                    else:
                        # Fallback to local mod folder
                        return Path(mod_folder_name)
        
        # Default to local events directory
        return Path(target_config.events_directory)
    
    def get_final_events_path(self) -> Path:
        """
        Get the final events path based on configuration.
        
        Returns:
            Path to the events directory considering all settings
        """
        target_path = self.get_final_target_path()
        
        # If target path is a mod directory, append events
        if target_path.exists() and target_path.is_dir():
            # Check if this looks like a mod directory
            if (target_path / "descriptor.mod").exists() or (target_path / "events").exists():
                return target_path / "events"
        
        # Otherwise, use the target path directly
        return target_path 