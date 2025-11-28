"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎓 CISC 121 - OOP Sorting & Searching Visualizer                          ║
║                                                                              ║
║   Queen's University - Introduction to Computing Science I                   ║
║                                                                              ║
║   Package: oop_sorting_teaching                                              ║
║   Purpose: Learn Object-Oriented Programming through visual algorithm demos  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 CONCEPT: Python Packages
═══════════════════════════

A PACKAGE is a way to organize related Python code into a folder structure.

Think of it like a filing cabinet:
• The cabinet (package) holds related folders
• Each folder (subpackage) holds related files
• Each file (module) holds related code

WHY USE PACKAGES?
• Organization: Related code lives together
• Reusability: Import just what you need
• Maintainability: Smaller files are easier to understand
• Collaboration: Different people can work on different modules

PACKAGE STRUCTURE:
├── oop_sorting_teaching/          # Main package
│   ├── __init__.py                # This file - makes it a package
│   ├── models/                    # Data structures
│   │   ├── gesture.py             # GestureRanking, GestureImage
│   │   ├── step.py                # StepType, Step
│   │   └── image_list.py          # ImageList
│   ├── algorithms/                # Sorting & searching
│   │   ├── sorting/               # Sorting algorithms
│   │   └── searching/             # Search algorithms
│   ├── visualization/             # Display logic
│   │   ├── renderers/             # HTML renderers
│   │   └── visualizer.py          # Main visualizer
│   └── tests/                     # Test functions

IMPORTING FROM THIS PACKAGE:
   # Import specific classes
   from oop_sorting_teaching.models import GestureImage, GestureRanking
   
   # Import algorithm
   from oop_sorting_teaching.algorithms.sorting import BubbleSort
   
   # Or use the convenient shortcuts below:
   from oop_sorting_teaching import GestureImage, BubbleSort
"""

# ==============================================================================
# CONVENIENT IMPORTS
# ==============================================================================
# These imports let users do:
#     from oop_sorting_teaching import GestureImage
# instead of:
#     from oop_sorting_teaching.models.gesture import GestureImage
# ==============================================================================

# Core models
from .models import (
    GestureRanking,
    GestureImage,
    StepType,
    Step,
    ImageList,
)

# Sorting algorithms
from .algorithms import (
    SortingAlgorithm,
    SearchAlgorithm,
    BubbleSort,
    MergeSort,
    QuickSort,
    PivotStrategy,
    PartitionScheme,
    LinearSearch,
    BinarySearch,
)

# Visualization
from .visualization import (
    VisualizationState,
    VisualizationConfig,
    Visualizer,
    StepRenderer,
    RendererFactory,
)

# Define what gets exported with "from oop_sorting_teaching import *"
__all__ = [
    # Models
    "GestureRanking",
    "GestureImage", 
    "StepType",
    "Step",
    "ImageList",
    # Sorting
    "SortingAlgorithm",
    "BubbleSort",
    "MergeSort",
    "QuickSort",
    "PivotStrategy",
    "PartitionScheme",
    # Searching
    "SearchAlgorithm",
    "LinearSearch",
    "BinarySearch",
    # Visualization
    "VisualizationState",
    "VisualizationConfig",
    "Visualizer",
    "StepRenderer",
    "RendererFactory",
]

# Package version
__version__ = "1.0.0"
