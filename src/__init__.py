"""
CK3 AI Weight Generator - Source Package

This package contains all the core modules for the CK3 AI Weight Generator.
"""

__version__ = "1.0.0"
__author__ = "Donekulda"

from .ai_model_manager import AIModelManager

# Import main classes for easier access
from .ck3_parser import CK3Parser, ProcessingSummary
from .ck3_trigger_generator import CK3TriggerGenerator
from .condition_manager import ConditionManager
from .config_manager import ConfigManager
from .event_parser import EventParser
from .model_organizer import ModelOrganizer
from .weight_calculator import WeightCalculator

__all__ = [
    "CK3Parser",
    "ProcessingSummary", 
    "ConfigManager",
    "AIModelManager",
    "CK3TriggerGenerator",
    "EventParser",
    "ConditionManager",
    "WeightCalculator",

    "ModelOrganizer"
] 