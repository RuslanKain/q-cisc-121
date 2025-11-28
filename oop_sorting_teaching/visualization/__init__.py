"""
Visualization package for algorithm step rendering.

This package provides visualization tools for sorting and searching algorithms:
- VisualizationState: Enum for visualization states
- StepRenderer: Abstract base class for renderers
- Individual renderers for each algorithm
- RendererFactory: Factory for creating renderers
- Visualizer: Main controller for visualization

📚 CONCEPT: Strategy Pattern

Different algorithms need different visualizations:
- Bubble Sort: Highlight two adjacent elements being compared
- Merge Sort: Show depth levels with indentation
- Quick Sort: Show pivot and partition regions
- Binary Search: Show search range narrowing

Instead of one giant "if algorithm == X then do Y" block,
we create separate RENDERER classes for each visualization style.
"""

from .state import VisualizationState, VisualizationConfig
from .renderers import (
    StepRenderer,
    BubbleSortRenderer,
    MergeSortRenderer,
    QuickSortRenderer,
    LinearSearchRenderer,
    BinarySearchRenderer,
)
from .factory import RendererFactory
from .visualizer import Visualizer

__all__ = [
    'VisualizationState',
    'VisualizationConfig',
    'StepRenderer',
    'BubbleSortRenderer',
    'MergeSortRenderer',
    'QuickSortRenderer',
    'LinearSearchRenderer',
    'BinarySearchRenderer',
    'RendererFactory',
    'Visualizer',
]
