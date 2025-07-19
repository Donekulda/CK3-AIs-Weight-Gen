"""
CK3 AI Weight Generator - Source Package

This package contains all the core modules for the CK3 AI Weight Generator.
"""

__version__ = "1.0.0"
__author__ = "Donekulda"

# Import main classes for easier access
from .ai_model_manager import AIModelManager
from .ck3_parser import CK3Parser, ProcessingSummary
from .ck3_trigger_generator import CK3TriggerGenerator, GeneratedTrigger
from .condition_manager import ConditionManager
from .config_manager import ConfigManager
from .event_parser import AIBlock, EventParser, ParsedEvent
from .model_organizer import ModelOrganizer
from .weight_calculator import WeightCalculator

__all__ = [
    # Main classes
    "AIModelManager",
    "CK3Parser",
    "CK3TriggerGenerator",
    "ConditionManager",
    "ConfigManager",
    "EventParser",
    "ModelOrganizer",
    "WeightCalculator",
    
    # Data classes and types
    "ProcessingSummary",
    "ParsedEvent",
    "AIBlock",
    "GeneratedTrigger"
] 