"""
Event Parser for CK3 AI Weight Generator

This module contains classes for parsing CK3 event files and extracting
AI model references and parameters.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ParseState(Enum):
    """Enumeration for parsing states."""
    SEARCHING = "searching"
    IN_AI_BLOCK = "in_ai_block"
    COLLECTING_PARAMS = "collecting_params"


@dataclass(frozen=True)
class AIBlock:
    """Represents an AI block found in an event file."""
    start_line: int
    end_line: int
    model_name: str
    content: str
    file_path: Path
    preserved_comments: tuple = None
    original_lines: tuple = None
    start_marker_line: str = None
    end_marker_line: str = None
    ai_block_start_line: int = None
    ai_block_end_line: int = None


@dataclass
class ParsedEvent:
    """Represents a parsed event file with AI blocks."""
    file_path: Path
    has_ai_lib: bool
    ai_blocks: List[AIBlock]


class EventParser:
    """Parser for CK3 event files to extract AI model references."""
    
    def __init__(self, config_manager=None):
        """
        Initialize the event parser.
        
        Args:
            config_manager: ConfigManager instance (optional)
        """
        self.config_manager = config_manager
        
        if config_manager:
            markers = config_manager.get_program_config().ai_markers
            self.ai_lib_pattern = re.compile(re.escape(markers.library_marker), re.IGNORECASE)
            self.ai_start_pattern = re.compile(re.escape(markers.start_marker), re.IGNORECASE)
            self.ai_end_pattern = re.compile(re.escape(markers.end_marker), re.IGNORECASE)
            self.model_pattern = re.compile(markers.model_pattern, re.IGNORECASE)
            self.comment_pattern = re.compile(markers.comment_pattern, re.IGNORECASE)
        else:
            self.ai_lib_pattern = re.compile(r'#\s*AI-MODEL-LIB', re.IGNORECASE)
            self.ai_start_pattern = re.compile(r'#\s*AI-START', re.IGNORECASE)
            self.ai_end_pattern = re.compile(r'#\s*AI-END', re.IGNORECASE)
            self.model_pattern = re.compile(r'using:\s*\{([^}]+)\}', re.IGNORECASE)
            self.comment_pattern = re.compile(r'#\s*(.+)', re.IGNORECASE)
    
    def parse_event_file(self, file_path: Path) -> ParsedEvent:
        """
        Parse a single event file to extract AI blocks.
        
        Args:
            file_path: Path to the event file to parse
            
        Returns:
            ParsedEvent containing the parsing results
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Event file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.split('\n')
        
        has_ai_lib = self._check_ai_lib_presence(content)
        ai_blocks = self._extract_ai_blocks(file_path, lines)
        
        return ParsedEvent(
            file_path=file_path,
            has_ai_lib=has_ai_lib,
            ai_blocks=ai_blocks
        )
    
    def _check_ai_lib_presence(self, content: str) -> bool:
        """
        Check if the file contains AI-MODEL-LIB marker.
        
        Args:
            content: File content as string
            
        Returns:
            True if AI-MODEL-LIB is found, False otherwise
        """
        return bool(self.ai_lib_pattern.search(content))
    
    def _extract_ai_blocks(self, file_path: Path, lines: List[str]) -> List[AIBlock]:
        """
        Extract AI blocks from the file lines.
        
        Args:
            file_path: Path to the event file
            lines: List of file lines
            
        Returns:
            List of AIBlock instances
        """
        ai_blocks = []
        state = ParseState.SEARCHING
        current_block_start = -1
        current_model_name = ""
        current_content = []
        preserved_comments = []
        original_lines = []
        ai_chance_start = -1
        start_marker_line = ""
        end_marker_line = ""
        ai_block_start_line = -1
        ai_block_end_line = -1
        
        for line_num, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            if state == ParseState.SEARCHING:
                # Look for ai_chance = { line
                if "ai_chance = {" in line_stripped:
                    ai_chance_start = line_num
                
                if self.ai_start_pattern.search(line):
                    state = ParseState.IN_AI_BLOCK
                    current_block_start = line_num
                    current_content = []
                    preserved_comments = []
                    original_lines = []
                    start_marker_line = line
                    ai_block_start_line = line_num + 1  # Content starts after the start marker
                    
                    # Try to extract model name from the same line or next few lines
                    model_match = self.model_pattern.search(line)
                    if model_match:
                        current_model_name = model_match.group(1).strip()
                    else:
                        # Look ahead for model name
                        current_model_name = self._find_model_name_ahead(lines, line_num)
            
            elif state == ParseState.IN_AI_BLOCK:
                # Check if this is the end marker
                if self.ai_end_pattern.search(line):
                    # End of AI block found
                    end_marker_line = line
                    ai_block_end_line = line_num - 1  # Content ends before the end marker
                    if current_model_name:
                        # Find the closing brace of the ai_chance block
                        ai_chance_end = self._find_ai_chance_end(lines, line_num)
                        
                        ai_block = AIBlock(
                            start_line=ai_chance_start if ai_chance_start > 0 else current_block_start,
                            end_line=ai_chance_end if ai_chance_end > 0 else line_num,
                            model_name=current_model_name,
                            content='\n'.join(current_content),
                            file_path=file_path,
                            preserved_comments=tuple(preserved_comments) if preserved_comments else None,
                            original_lines=tuple(original_lines) if original_lines else None,
                            start_marker_line=start_marker_line,
                            end_marker_line=end_marker_line,
                            ai_block_start_line=ai_block_start_line,
                            ai_block_end_line=ai_block_end_line
                        )
                        ai_blocks.append(ai_block)
                    
                    # Reset for next block
                    state = ParseState.SEARCHING
                    current_block_start = -1
                    current_model_name = ""
                    current_content = []
                    preserved_comments = []
                    original_lines = []
                    ai_chance_start = -1
                    start_marker_line = ""
                    end_marker_line = ""
                    ai_block_start_line = -1
                    ai_block_end_line = -1
                else:
                    # This is content between the markers
                    current_content.append(line)
                    original_lines.append(line_num)
                    
                    # Check if this is a comment line (but not a marker)
                    if (self.comment_pattern.search(line) and 
                        not self.ai_start_pattern.search(line) and 
                        not self.ai_end_pattern.search(line)):
                        preserved_comments.append(line.strip())
        
        return ai_blocks
    
    def _find_model_name_ahead(self, lines: List[str], start_line: int) -> str:
        """
        Look ahead in lines to find model name after AI-START.
        
        Args:
            lines: List of file lines
            start_line: Starting line number to search from
            
        Returns:
            Model name if found, empty string otherwise
        """
        # Look ahead up to 5 lines
        for i in range(start_line, min(start_line + 5, len(lines))):
            line = lines[i - 1]  # Convert to 0-based index
            model_match = self.model_pattern.search(line)
            if model_match:
                return model_match.group(1).strip()
        
        return ""
    
    def _find_ai_chance_end(self, lines: List[str], start_line: int) -> int:
        """
        Find the closing brace of the ai_chance block.
        
        Args:
            lines: List of file lines
            start_line: Starting line number to search from
            
        Returns:
            Line number of the closing brace, or -1 if not found
        """
        brace_count = 0
        found_opening = False
        
        for i in range(start_line, len(lines)):
            line = lines[i - 1]  # Convert to 0-based index
            line_stripped = line.strip()
            
            # Count opening and closing braces
            for char in line_stripped:
                if char == '{':
                    brace_count += 1
                    found_opening = True
                elif char == '}':
                    brace_count -= 1
                    if found_opening and brace_count == 0:
                        return i
        
        return -1
    
    def parse_events_directory(self, events_dir: Path) -> List[ParsedEvent]:
        """
        Parse all event files in a directory.
        
        Args:
            events_dir: Path to the events directory
            
        Returns:
            List of ParsedEvent instances
        """
        if not events_dir.exists() or not events_dir.is_dir():
            raise FileNotFoundError(f"Events directory not found: {events_dir}")
        
        parsed_events = []
        
        # Get file extensions from config if available
        if self.config_manager:
            extensions = self.config_manager.get_file_extensions()
        else:
            extensions = [".txt"]
        
        # Build glob pattern - use simple pattern for .txt files
        for file_path in events_dir.glob("*.txt"):
            try:
                parsed_event = self.parse_event_file(file_path)
                parsed_events.append(parsed_event)
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")
                continue
        
        return parsed_events
    
    def get_ai_blocks_summary(self, parsed_events: List[ParsedEvent]) -> Dict[str, int]:
        """
        Get a summary of AI blocks by model name.
        
        Args:
            parsed_events: List of parsed events
            
        Returns:
            Dictionary mapping model names to their usage count
        """
        summary = {}
        
        for event in parsed_events:
            for block in event.ai_blocks:
                model_name = block.model_name
                summary[model_name] = summary.get(model_name, 0) + 1
        
        return summary 