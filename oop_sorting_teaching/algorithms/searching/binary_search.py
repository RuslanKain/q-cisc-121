"""
Binary Search implementation.

╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 ALGORITHM: Binary Search                                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WHAT IS BINARY SEARCH?                                                      ║
║  Binary search is an efficient algorithm for finding an item in a SORTED     ║
║  list. Instead of checking every element (linear search), it repeatedly      ║
║  divides the search space in half.                                           ║
║                                                                              ║
║  HOW IT WORKS:                                                               ║
║  1. Look at the MIDDLE element                                               ║
║  2. If it's the target, we're done!                                          ║
║  3. If target is SMALLER, search the LEFT half                               ║
║  4. If target is LARGER, search the RIGHT half                               ║
║  5. Repeat until found or search space is empty                              ║
║                                                                              ║
║  VISUALIZATION:                                                              ║
║                                                                              ║
║  Target: 🖐️ (rank 6)                                                         ║
║                                                                              ║
║  Step 1:  [✊] [☝️] [✌️] [🤟] [🖖] [🖐️] [👌] [👍]                             ║
║           [=================↑==================]                             ║
║                           mid=3 (🤟, rank 4)                                 ║
║                           🤟 < 🖐️ → search RIGHT                             ║
║                                                                              ║
║  Step 2:  [✊] [☝️] [✌️] [🤟] [🖖] [🖐️] [👌] [👍]                             ║
║                               [=====↑=====]                                  ║
║                               mid=5 (🖐️, rank 6)                             ║
║                               FOUND! ✅                                       ║
║                                                                              ║
║  PROPERTIES:                                                                 ║
║  • Time: O(log n) - halves search space each step                           ║
║  • Space: O(1) iterative, O(log n) recursive                                ║
║  • Requirement: Data MUST be sorted!                                        ║
║                                                                              ║
║  COMPARISON WITH LINEAR SEARCH:                                              ║
║  ─────────────────────────────                                               ║
║  For 1000 elements:                                                          ║
║  • Linear Search: up to 1000 comparisons (O(n))                             ║
║  • Binary Search: at most 10 comparisons (O(log n))                         ║
║                                                                              ║
║  For 1,000,000 elements:                                                     ║
║  • Linear Search: up to 1,000,000 comparisons                               ║
║  • Binary Search: at most 20 comparisons!                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import math
from typing import List, Generator, Optional

from ..base import SearchAlgorithm
from ...models import GestureImage, Step, StepType


class BinarySearch(SearchAlgorithm):
    """
    Binary Search - efficient search for sorted data.
    
    Repeatedly divides the search space in half.
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  📚 CONCEPT: Divide and Conquer                                         │
    │                                                                         │
    │  Binary Search uses the same strategy as Merge Sort:                    │
    │  1. DIVIDE the problem in half                                          │
    │  2. CONQUER by recursively solving smaller problem                      │
    │  3. COMBINE (trivial for search - just return the result)              │
    │                                                                         │
    │  Why is this efficient?                                                 │
    │  • Each step eliminates HALF of the remaining elements                 │
    │  • After k steps, only n/2^k elements remain                           │
    │  • When n/2^k = 1, we've found our answer: k = log₂(n)                 │
    │                                                                         │
    │  Example:                                                               │
    │  • 1,000 elements → log₂(1000) ≈ 10 steps                              │
    │  • 1,000,000 elements → log₂(1000000) ≈ 20 steps                       │
    │  • 1,000,000,000 elements → log₂(10⁹) ≈ 30 steps!                       │
    └─────────────────────────────────────────────────────────────────────────┘
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  ⚠️ IMPORTANT: Binary Search REQUIRES SORTED DATA!                      │
    │                                                                         │
    │  If the data is not sorted, Binary Search will give WRONG results!     │
    │                                                                         │
    │  Our implementation checks for this and warns the user.                │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self, variant: str = "iterative"):
        """
        Initialize Binary Search.
        
        Args:
            variant: "iterative" or "recursive"
                     Both do the same thing, just different implementations.
                     Iterative uses a loop, Recursive uses function calls.
        """
        self.variant = variant
        self._comparisons = 0
    
    @property
    def name(self) -> str:
        return f"Binary Search ({self.variant.title()})"
    
    @property
    def requires_sorted(self) -> bool:
        return True  # MUST be sorted!
    
    def search(
        self,
        data: List[GestureImage],
        target: GestureImage
    ) -> Generator[Step, None, Optional[int]]:
        """
        Search using binary search.
        
        Time Complexity: O(log n)
        Space Complexity: O(1) iterative, O(log n) recursive
        """
        self._comparisons = 0
        
        # First, validate that data is sorted
        if not self._is_sorted(data):
            yield self._create_step(
                step_type=StepType.NOT_FOUND,
                indices=[],
                description="⚠️ ERROR: Data is NOT sorted! Binary Search requires sorted input.",
                data=data,
                metadata={"error": "unsorted_input"}
            )
            return None
        
        yield self._create_step(
            step_type=StepType.SEARCH_RANGE,
            indices=list(range(len(data))),
            description=f"Binary Search for {target} (rank {target.rank}) in sorted list of {len(data)} elements",
            data=data,
            metadata={"target_rank": target.rank, "max_steps": self._calculate_max_steps(len(data))}
        )
        
        if self.variant == "iterative":
            result = yield from self._search_iterative(data, target)
        else:
            result = yield from self._search_recursive(data, target, 0, len(data) - 1)
        
        return result
    
    def _search_iterative(
        self,
        data: List[GestureImage],
        target: GestureImage
    ) -> Generator[Step, None, Optional[int]]:
        """
        Iterative implementation of binary search.
        
        Uses a while loop instead of recursion.
        More memory efficient (O(1) space).
        """
        left = 0
        right = len(data) - 1
        step_num = 0
        max_steps = self._calculate_max_steps(len(data))
        
        while left <= right:
            step_num += 1
            mid = (left + right) // 2
            self._comparisons += 1
            
            # Show the current search range
            yield self._create_step(
                step_type=StepType.SEARCH_RANGE,
                indices=list(range(left, right + 1)),
                description=f"Step {step_num}/{max_steps}: Searching range [{left}:{right}], mid={mid}",
                data=data,
                highlight=[mid],
                metadata={
                    "left": left,
                    "right": right,
                    "mid": mid,
                    "comparisons": self._comparisons,
                    "step": step_num
                }
            )
            
            # Compare middle element with target
            mid_value = data[mid]
            
            yield self._create_step(
                step_type=StepType.COMPARE,
                indices=[mid],
                description=f"Comparing: {mid_value} (rank {mid_value.rank}) vs target {target} (rank {target.rank})",
                data=data,
                highlight=[mid],
                metadata={"comparisons": self._comparisons}
            )
            
            if mid_value.rank == target.rank:
                # Found it!
                yield self._create_step(
                    step_type=StepType.FOUND,
                    indices=[mid],
                    description=f"✅ FOUND at index {mid} in only {self._comparisons} comparisons!",
                    data=data,
                    highlight=[mid],
                    metadata={
                        "comparisons": self._comparisons,
                        "found": True,
                        "efficiency": f"Found in {step_num} steps (max possible: {max_steps})"
                    }
                )
                return mid
            
            elif mid_value.rank < target.rank:
                # Target is in the right half
                yield self._create_step(
                    step_type=StepType.SEARCH_RANGE,
                    indices=list(range(mid + 1, right + 1)),
                    description=f"{mid_value} < {target} → Eliminating left half, searching [{mid + 1}:{right}]",
                    data=data,
                    highlight=list(range(mid + 1, right + 1)),
                    metadata={"eliminated": list(range(left, mid + 1))}
                )
                left = mid + 1
            
            else:
                # Target is in the left half
                yield self._create_step(
                    step_type=StepType.SEARCH_RANGE,
                    indices=list(range(left, mid)),
                    description=f"{mid_value} > {target} → Eliminating right half, searching [{left}:{mid - 1}]",
                    data=data,
                    highlight=list(range(left, mid)),
                    metadata={"eliminated": list(range(mid, right + 1))}
                )
                right = mid - 1
        
        # Not found
        yield self._create_step(
            step_type=StepType.NOT_FOUND,
            indices=[],
            description=f"❌ NOT FOUND after {self._comparisons} comparisons. Target {target} is not in the list.",
            data=data,
            metadata={"comparisons": self._comparisons, "found": False}
        )
        return None
    
    def _search_recursive(
        self,
        data: List[GestureImage],
        target: GestureImage,
        left: int,
        right: int,
        depth: int = 0
    ) -> Generator[Step, None, Optional[int]]:
        """
        Recursive implementation of binary search.
        
        Uses function call stack instead of explicit loop.
        Shows the recursive nature more clearly (good for teaching).
        """
        # Base case: empty range
        if left > right:
            yield self._create_step(
                step_type=StepType.NOT_FOUND,
                indices=[],
                description=f"❌ NOT FOUND: Search range is empty (left={left} > right={right})",
                data=data,
                metadata={"comparisons": self._comparisons, "found": False, "depth": depth}
            )
            return None
        
        mid = (left + right) // 2
        self._comparisons += 1
        
        # Show current recursive call
        yield self._create_step(
            step_type=StepType.SEARCH_RANGE,
            indices=list(range(left, right + 1)),
            description=f"Depth {depth}: binary_search(data, target, left={left}, right={right}), mid={mid}",
            data=data,
            highlight=[mid],
            metadata={"depth": depth, "left": left, "right": right, "mid": mid}
        )
        
        mid_value = data[mid]
        
        yield self._create_step(
            step_type=StepType.COMPARE,
            indices=[mid],
            description=f"Depth {depth}: Comparing {mid_value} (rank {mid_value.rank}) vs {target} (rank {target.rank})",
            data=data,
            highlight=[mid],
            metadata={"comparisons": self._comparisons, "depth": depth}
        )
        
        if mid_value.rank == target.rank:
            yield self._create_step(
                step_type=StepType.FOUND,
                indices=[mid],
                description=f"✅ FOUND at index {mid} (recursion depth {depth}, {self._comparisons} comparisons)",
                data=data,
                highlight=[mid],
                metadata={"comparisons": self._comparisons, "found": True, "depth": depth}
            )
            return mid
        
        elif mid_value.rank < target.rank:
            yield self._create_step(
                step_type=StepType.SEARCH_RANGE,
                indices=list(range(mid + 1, right + 1)),
                description=f"Depth {depth}: Recursing into RIGHT half [{mid + 1}:{right}]",
                data=data,
                highlight=list(range(mid + 1, right + 1)),
                metadata={"depth": depth}
            )
            # Recursive call to right half
            result = yield from self._search_recursive(data, target, mid + 1, right, depth + 1)
            return result
        
        else:
            yield self._create_step(
                step_type=StepType.SEARCH_RANGE,
                indices=list(range(left, mid)),
                description=f"Depth {depth}: Recursing into LEFT half [{left}:{mid - 1}]",
                data=data,
                highlight=list(range(left, mid)),
                metadata={"depth": depth}
            )
            # Recursive call to left half
            result = yield from self._search_recursive(data, target, left, mid - 1, depth + 1)
            return result
    
    def _is_sorted(self, data: List[GestureImage]) -> bool:
        """Check if data is sorted in ascending order."""
        for i in range(len(data) - 1):
            if data[i].rank > data[i + 1].rank:
                return False
        return True
    
    @staticmethod
    def _calculate_max_steps(n: int) -> int:
        """Calculate maximum number of steps needed for binary search."""
        if n <= 0:
            return 0
        return math.floor(math.log2(n)) + 1
