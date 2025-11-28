"""
Bubble Sort implementation.

╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 ALGORITHM: Bubble Sort                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HOW IT WORKS:                                                               ║
║  1. Compare adjacent elements                                                ║
║  2. If they're in wrong order, swap them                                     ║
║  3. Repeat until no more swaps needed                                        ║
║                                                                              ║
║  VISUALIZATION:                                                              ║
║  [5] [3] [8] [1]  ← Compare [5] and [3]                                     ║
║  [3] [5] [8] [1]  ← Swapped! Compare [5] and [8]                            ║
║  [3] [5] [8] [1]  ← OK. Compare [8] and [1]                                 ║
║  [3] [5] [1] [8]  ← Swapped! [8] "bubbled up" to the end ✓                  ║
║                                                                              ║
║  PROPERTIES:                                                                 ║
║  • Time: O(n²) average/worst, O(n) best (already sorted)                    ║
║  • Space: O(1) - in-place                                                   ║
║  • Stable: YES - equal elements keep their relative order                   ║
║  • Early Exit: We stop if a pass makes no swaps (already sorted!)           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from typing import List, Generator

from ..base import SortingAlgorithm
from ...models import GestureImage, Step, StepType


class BubbleSort(SortingAlgorithm):
    """
    Bubble Sort with early exit optimization.
    
    The simplest sorting algorithm - great for learning!
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  💡 WHY BUBBLE SORT?                                                    │
    │                                                                         │
    │  It's not the fastest, but it's:                                       │
    │  ✓ Easy to understand                                                   │
    │  ✓ Easy to implement                                                    │
    │  ✓ Stable (preserves order of equal elements)                          │
    │  ✓ Efficient for nearly-sorted data (with early exit)                  │
    │  ✓ Great for teaching sorting concepts                                 │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    @property
    def name(self) -> str:
        return "Bubble Sort"
    
    @property
    def is_stable(self) -> bool:
        return True  # Bubble sort is stable!
    
    @property
    def is_in_place(self) -> bool:
        return True  # Only uses swaps, no extra arrays
    
    def sort(self, data: List[GestureImage]) -> Generator[Step, None, List[GestureImage]]:
        """
        Sort using bubble sort with early exit.
        
        📚 CONCEPT: Generator Functions (yield)
        
        A generator function uses 'yield' instead of 'return'.
        Each yield PAUSES the function and returns a value.
        The function resumes when next() is called again.
        
        This lets us:
        1. Execute one step of the algorithm
        2. Pause and show that step to the user
        3. Continue to the next step
        
        Without generators, we'd need to pre-compute ALL steps,
        which wastes memory and prevents real-time visualization.
        """
        n = len(data)
        
        # Track statistics for educational display
        comparisons = 0
        swaps = 0
        
        # Outer loop: each pass "bubbles" the largest unsorted element up
        for i in range(n - 1):
            swapped = False  # Track if we made any swaps this pass
            
            # Yield a step showing we're starting a new pass
            yield self._create_step(
                step_type=StepType.COMPARE,
                indices=[],
                description=f"Pass {i + 1}: Scanning from left to right",
                data=data,
                highlight=list(range(n - i, n))  # Highlight already-sorted portion
            )
            
            # Inner loop: compare adjacent elements
            for j in range(n - 1 - i):
                comparisons += 1
                
                # Yield a step showing the comparison
                yield self._create_step(
                    step_type=StepType.COMPARE,
                    indices=[j, j + 1],
                    description=f"Comparing {data[j]} and {data[j + 1]}",
                    data=data,
                    highlight=list(range(n - i, n)),
                    metadata={"comparisons": comparisons, "swaps": swaps}
                )
                
                # If left > right, swap them
                if data[j] > data[j + 1]:
                    # Perform the swap
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                    swaps += 1
                    
                    # Yield a step showing the swap
                    yield self._create_step(
                        step_type=StepType.SWAP,
                        indices=[j, j + 1],
                        description=f"Swapped! {data[j]} ↔ {data[j + 1]}",
                        data=data,
                        highlight=list(range(n - i, n)),
                        metadata={"comparisons": comparisons, "swaps": swaps}
                    )
            
            # Mark the element that bubbled to its final position
            yield self._create_step(
                step_type=StepType.MARK_SORTED,
                indices=[n - 1 - i],
                description=f"{data[n - 1 - i]} is now in its final position",
                data=data,
                highlight=list(range(n - 1 - i, n))
            )
            
            # EARLY EXIT: If no swaps occurred, the array is sorted!
            if not swapped:
                yield self._create_step(
                    step_type=StepType.COMPLETE,
                    indices=[],
                    description=f"No swaps in this pass - array is sorted! (Early exit)",
                    data=data,
                    metadata={"comparisons": comparisons, "swaps": swaps, "early_exit": True}
                )
                return data
        
        # Final step: algorithm complete
        yield self._create_step(
            step_type=StepType.COMPLETE,
            indices=[],
            description=f"Sorting complete! {comparisons} comparisons, {swaps} swaps",
            data=data,
            metadata={"comparisons": comparisons, "swaps": swaps, "early_exit": False}
        )
        
        return data
