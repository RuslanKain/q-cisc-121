"""
Algorithms subpackage - Sorting and searching algorithms.

This package contains:
• SortingAlgorithm - Abstract base class for sorting
• SearchAlgorithm - Abstract base class for searching
• BubbleSort, MergeSort, QuickSort - Sorting implementations
• LinearSearch, BinarySearch - Search implementations

📚 PACKAGE ORGANIZATION:
   algorithms/
   ├── __init__.py        (this file)
   ├── base.py            (abstract base classes)
   ├── sorting/           (sorting algorithms)
   │   ├── bubble_sort.py
   │   ├── merge_sort.py
   │   └── quick_sort.py
   └── searching/         (search algorithms)
       ├── linear_search.py
       └── binary_search.py
"""

# Import base classes
from .base import SortingAlgorithm, SearchAlgorithm

# Import sorting algorithms
from .sorting import (
    BubbleSort,
    MergeSort,
    QuickSort,
    PivotStrategy,
    PartitionScheme,
)

# Import search algorithms
from .searching import (
    LinearSearch,
    BinarySearch,
)

__all__ = [
    # Base classes
    "SortingAlgorithm",
    "SearchAlgorithm",
    # Sorting
    "BubbleSort",
    "MergeSort",
    "QuickSort",
    "PivotStrategy",
    "PartitionScheme",
    # Searching
    "LinearSearch",
    "BinarySearch",
]
