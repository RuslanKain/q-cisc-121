"""
Sorting algorithms package.

Contains implementations of various sorting algorithms:
- BubbleSort: Simple comparison-based sort (stable, in-place)
- MergeSort: Divide-and-conquer sort (stable, not in-place)
- QuickSort: Fast divide-and-conquer sort (unstable, in-place)

Each algorithm inherits from SortingAlgorithm and implements
the sort() generator method.
"""

from .bubble_sort import BubbleSort
from .merge_sort import MergeSort
from .quick_sort import QuickSort, PivotStrategy, PartitionScheme

__all__ = [
    'BubbleSort',
    'MergeSort',
    'QuickSort',
    'PivotStrategy',
    'PartitionScheme',
]
