"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Models: step.py                                                             ║
║  Classes for representing algorithm execution steps                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module contains:
• StepType (Enum) - Types of operations (compare, swap, merge, etc.)
• Step (dataclass) - A single step in algorithm execution

📚 WHY RECORD STEPS?
   To visualize algorithms step-by-step, we need to RECORD what happens.
   Each Step captures:
   - WHAT operation occurred (compare, swap, etc.)
   - WHERE it happened (which indices)
   - WHEN in the process (depth for recursive algorithms)
   - Additional context (metadata)
   
   This is the "data" that visualization will render.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, TYPE_CHECKING

# Avoid circular import - only import for type checking
if TYPE_CHECKING:
    from oop_sorting_teaching.models.gesture import GestureImage


# ==============================================================================
# ENUM: StepType
# ==============================================================================
#
# 📚 CONCEPT: Enums for Type Safety
#
# Instead of using strings like "compare" or "swap", we use an Enum.
# This prevents bugs from typos:
#   - String: if step_type == "comprae"  # Typo! No error, silent bug
#   - Enum: if step_type == StepType.COMPRAE  # Python error! Bug caught
# ==============================================================================

class StepType(Enum):
    """
    Types of algorithm steps that can be visualized.
    
    Each step in our sorting/searching algorithms will have a type
    that determines how it's displayed in the visualization.
    
    📚 CONCEPT: auto()
    
    The auto() function automatically assigns incrementing values.
    We don't care what the actual numbers are - we just need
    unique identifiers for each step type.
    """
    # Comparison operations
    COMPARE = auto()         # Comparing two elements
    
    # Movement operations
    SWAP = auto()            # Swapping two elements (in-place algorithms)
    MOVE = auto()            # Moving an element to a new position
    
    # Merge sort specific
    SPLIT = auto()           # Splitting array into subarrays
    MERGE = auto()           # Merging sorted subarrays
    
    # Quick sort specific
    PIVOT_SELECT = auto()    # Selecting a pivot element
    PARTITION = auto()       # Partitioning around pivot
    
    # Binary search specific
    SEARCH_RANGE = auto()    # Showing current search range
    NARROW_LEFT = auto()     # Target is in left half
    NARROW_RIGHT = auto()    # Target is in right half
    FOUND = auto()           # Target element found
    NOT_FOUND = auto()       # Target element not in array
    
    # General
    PASS_COMPLETE = auto()   # One pass through the data complete (Bubble Sort)
    COMPLETE = auto()        # Algorithm finished
    MARK_SORTED = auto()     # Mark element(s) as in final position
    
    # Stability detection
    INSTABILITY = auto()     # Stability violation detected!
    INSTABILITY_WARNING = auto()  # Warning for potential instability


# ==============================================================================
# DATACLASS: Step
# ==============================================================================
#
# 📚 CONCEPT: Recording Algorithm Execution
#
# When an algorithm runs, we want to show EVERY step:
# 1. What operation happened (StepType)
# 2. Which elements were involved (indices)
# 3. What the array looks like now (array_state)
# 4. Any additional info (metadata)
#
# By recording steps, we can:
# - Play back the algorithm visually
# - Step forward and backward
# - Analyze algorithm behavior
# ==============================================================================

@dataclass
class Step:
    """
    Represents a single step in an algorithm's execution.
    
    This is used to record what the algorithm is doing at each point,
    so we can visualize it step by step.
    
    Think of it like frames in a movie:
    - Each Step is one frame
    - Together they tell the story of the algorithm
    
    Attributes:
        step_type: What kind of operation (compare, swap, merge, etc.)
        indices: Which array positions are involved
        description: Human-readable explanation
        depth: Recursion depth (for merge sort / quick sort)
        array_state: Copy of the array at this step
        highlight_indices: Extra indices to highlight (e.g., sorted region)
        metadata: Additional algorithm-specific data
    
    Example:
        step = Step(
            step_type=StepType.COMPARE,
            indices=[3, 4],
            description="Comparing elements at positions 3 and 4",
            depth=0,
            array_state=[...],
            metadata={"comparison_count": 5}
        )
    """
    step_type: StepType
    indices: List[int]
    description: str
    depth: int = 0
    array_state: List['GestureImage'] = field(default_factory=list)
    highlight_indices: List[int] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    @property
    def type(self) -> StepType:
        """
        Alias for step_type for cleaner access in renderers.
        
        This allows: step.type instead of step.step_type
        Makes the code more readable in visualization code.
        """
        return self.step_type
    
    def __str__(self) -> str:
        """Human-readable string for debugging."""
        indices_str = ', '.join(str(i) for i in self.indices)
        return f"[{self.step_type.name}] indices=[{indices_str}] depth={self.depth}: {self.description}"
