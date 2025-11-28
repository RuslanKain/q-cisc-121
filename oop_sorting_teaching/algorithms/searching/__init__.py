"""
Searching algorithms package.

Contains implementations of various search algorithms:
- LinearSearch: Simple sequential search (works on unsorted data)
- BinarySearch: Efficient divide-and-conquer search (requires sorted data)

Each algorithm inherits from SearchAlgorithm and implements
the search() generator method.
"""

from .linear_search import LinearSearch
from .binary_search import BinarySearch

__all__ = [
    'LinearSearch',
    'BinarySearch',
]
