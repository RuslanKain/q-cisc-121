"""
Visualization state and configuration.

Contains:
- VisualizationState: Enum for tracking visualization state
- VisualizationConfig: Configuration dataclass for visualization options
"""

from dataclasses import dataclass
from enum import Enum


class VisualizationState(Enum):
    """
    📚 CONCEPT: Finite State Machine
    
    A visualization can only be in ONE of these states at a time.
    This prevents impossible states like "playing AND paused".
    
    BEFORE OOP (with strings):
        state = "idle"
        if state == "plying":  # Typo! Hard to catch bug
            ...
    
    AFTER OOP (with Enum):
        state = VisualizationState.IDLE
        if state == VisualizationState.PLYING:  # Python error! Typo caught
            ...
    """
    IDLE = "idle"              # No steps loaded
    READY = "ready"            # Steps loaded, ready to start
    PLAYING = "playing"        # Auto-playing animation
    PAUSED = "paused"          # Paused mid-animation
    STEPPING = "stepping"      # Manual step-by-step mode
    COMPLETE = "complete"      # Reached the end


@dataclass
class VisualizationConfig:
    """
    Configuration options for the visualizer.
    
    📚 CONCEPT: Configuration Object
    
    Instead of passing many parameters to functions, we bundle
    related settings into a configuration object.
    
    BEFORE:
        def start_visualization(speed, auto_play, loop, show_stats, ...):
    
    AFTER:
        def start_visualization(config: VisualizationConfig):
    
    Benefits:
    - Easy to add new options without changing function signatures
    - Can have sensible defaults
    - Can save/load configurations
    """
    animation_speed_ms: int = 1000      # Milliseconds per step
    auto_play: bool = False              # Start playing immediately
    loop: bool = False                   # Restart when finished
    show_statistics: bool = True         # Show step count, comparisons, etc.
    show_legend: bool = True             # Show color legend
    image_size: int = 60                 # Size of image thumbnails
