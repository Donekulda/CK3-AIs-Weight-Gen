"""
Configuration Manager for CK3 AI Weight Generator

This module contains classes for managing program configuration and settings.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


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
            
            self._parse_program_config()
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {config_to_load}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading configuration from {config_to_load}: {e}")
    
    def _parse_program_config(self) -> None:
        """Parse the program configuration section."""
        prog_config = self.config_data.get('program_config', {})
        
        ai_markers_data = prog_config.get('ai_markers', {})
        ai_markers = AIMarkers(
            library_marker=ai_markers_data.get('library_marker', '# AI-MODEL-LIB'),
            start_marker=ai_markers_data.get('start_marker', '# AI-START'),
            end_marker=ai_markers_data.get('end_marker', '# AI-END'),
            model_pattern=ai_markers_data.get('model_pattern', 'using:\\s*\\{([^}]+)\\}'),
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
    
    def get_final_events_path(self) -> Path:
        """
        Get the final events path based on configuration.
        
        Returns:
            Path to the events directory considering mod folder settings
        """
        config = self.get_program_config()
        
        if config.target.should_use_mod_folder and config.target.mod_folder:
            if config.target.is_parent:
                # Mod folder is in parent directory
                return Path("..") / config.target.mod_folder / config.target.events_directory
            else:
                # Mod folder is in current directory or absolute path
                return Path(config.target.mod_folder) / config.target.events_directory
        else:
            # Use local events directory
            return Path(config.target.events_directory)
    
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