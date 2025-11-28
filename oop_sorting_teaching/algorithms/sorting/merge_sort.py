"""
Merge Sort implementation.

╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 ALGORITHM: Merge Sort                                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HOW IT WORKS (Divide and Conquer):                                          ║
║  1. DIVIDE: Split the array in half                                          ║
║  2. CONQUER: Recursively sort each half                                      ║
║  3. COMBINE: Merge the sorted halves back together                           ║
║                                                                              ║
║  VISUALIZATION:                                                              ║
║                                                                              ║
║  Depth 0:  [5, 3, 8, 1]                                                     ║
║                ↓ split                                                       ║
║  Depth 1:  [5, 3]     [8, 1]                                                ║
║              ↓           ↓                                                   ║
║  Depth 2:  [5] [3]   [8] [1]                                                ║
║              ↓ merge     ↓ merge                                             ║
║  Depth 1:  [3, 5]     [1, 8]                                                ║
║                ↓ merge                                                       ║
║  Depth 0:  [1, 3, 5, 8]  ← SORTED!                                          ║
║                                                                              ║
║  PROPERTIES:                                                                 ║
║  • Time: O(n log n) always (best = average = worst)                         ║
║  • Space: O(n) - needs extra array for merging                              ║
║  • Stable: YES - equal elements keep their relative order                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Generator

from ..base import SortingAlgorithm
from ...models import GestureImage, Step, StepType


class MergeSort(SortingAlgorithm):
    """
    Merge Sort - a stable, efficient divide-and-conquer algorithm.
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  💡 WHY MERGE SORT?                                                     │
    │                                                                         │
    │  ✓ Guaranteed O(n log n) - no worst case!                              │
    │  ✓ Stable - perfect for our stability demonstrations                   │
    │  ✓ Parallelizable - each half can be sorted independently              │
    │  ✓ Great for linked lists (no random access needed)                    │
    │                                                                         │
    │  ✗ Uses O(n) extra space (not in-place)                                │
    │  ✗ Slower than quicksort in practice (more memory operations)          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self):
        """Initialize with tracking variables."""
        self._comparisons = 0
        self._moves = 0
    
    @property
    def name(self) -> str:
        return "Merge Sort"
    
    @property
    def is_stable(self) -> bool:
        return True  # Merge sort is stable!
    
    @property
    def is_in_place(self) -> bool:
        return False  # Needs extra space for merging
    
    def sort(self, data: List[GestureImage]) -> Generator[Step, None, List[GestureImage]]:
        """
        Sort using merge sort.
        
        This is a wrapper that starts the recursive process.
        """
        self._comparisons = 0
        self._moves = 0
        
        if len(data) <= 1:
            return data
        
        # Start the recursive sorting
        yield from self._merge_sort_recursive(data, 0, len(data) - 1, 0)
        
        # Final step
        yield self._create_step(
            step_type=StepType.COMPLETE,
            indices=[],
            description=f"Sorting complete! {self._comparisons} comparisons, {self._moves} moves",
            data=data,
            metadata={"comparisons": self._comparisons, "moves": self._moves}
        )
        
        return data
    
    def _merge_sort_recursive(
        self,
        data: List[GestureImage],
        left: int,
        right: int,
        depth: int
    ) -> Generator[Step, None, None]:
        """
        Recursive merge sort implementation.
        
        📚 CONCEPT: Recursion
        
        Recursion is when a function calls itself.
        Each call works on a smaller piece of the problem.
        
        Base case: When to stop (array of size 1)
        Recursive case: Split, sort halves, merge
        """
        # BASE CASE: Array of 1 element is already sorted
        if left >= right:
            return
        
        # Calculate middle point
        mid = (left + right) // 2
        
        # Yield step showing the split
        yield self._create_step(
            step_type=StepType.SPLIT,
            indices=list(range(left, right + 1)),
            description=f"Depth {depth}: Splitting [{left}:{right}] into [{left}:{mid}] and [{mid+1}:{right}]",
            data=data,
            depth=depth,
            metadata={"left": left, "mid": mid, "right": right}
        )
        
        # RECURSIVE CASE: Sort left half
        yield from self._merge_sort_recursive(data, left, mid, depth + 1)
        
        # Sort right half
        yield from self._merge_sort_recursive(data, mid + 1, right, depth + 1)
        
        # Merge the sorted halves
        yield from self._merge(data, left, mid, right, depth)
    
    def _merge(
        self,
        data: List[GestureImage],
        left: int,
        mid: int,
        right: int,
        depth: int
    ) -> Generator[Step, None, None]:
        """
        Merge two sorted subarrays.
        
        Left subarray: data[left:mid+1]
        Right subarray: data[mid+1:right+1]
        """
        # Create temporary arrays (this is why merge sort needs O(n) space)
        left_arr = data[left:mid + 1]
        right_arr = data[mid + 1:right + 1]
        
        yield self._create_step(
            step_type=StepType.MERGE,
            indices=list(range(left, right + 1)),
            description=f"Depth {depth}: Merging [{left}:{mid}] and [{mid+1}:{right}]",
            data=data,
            depth=depth
        )
        
        i = 0  # Index for left subarray
        j = 0  # Index for right subarray
        k = left  # Index for merged array
        
        # Merge while both subarrays have elements
        while i < len(left_arr) and j < len(right_arr):
            self._comparisons += 1
            
            # Compare elements from both subarrays
            # Using <= (not <) to maintain stability!
            if left_arr[i] <= right_arr[j]:
                data[k] = left_arr[i]
                i += 1
            else:
                data[k] = right_arr[j]
                j += 1
            
            self._moves += 1
            k += 1
            
            yield self._create_step(
                step_type=StepType.MOVE,
                indices=[k - 1],
                description=f"Placed {data[k - 1]} at position {k - 1}",
                data=data,
                depth=depth,
                metadata={"comparisons": self._comparisons, "moves": self._moves}
            )
        
        # Copy remaining elements from left subarray
        while i < len(left_arr):
            data[k] = left_arr[i]
            self._moves += 1
            i += 1
            k += 1
        
        # Copy remaining elements from right subarray
        while j < len(right_arr):
            data[k] = right_arr[j]
            self._moves += 1
            j += 1
            k += 1
        
        yield self._create_step(
            step_type=StepType.MARK_SORTED,
            indices=list(range(left, right + 1)),
            description=f"Merged: positions {left} to {right} are now sorted",
            data=data,
            depth=depth
        )
