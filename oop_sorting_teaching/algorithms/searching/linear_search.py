"""
Linear Search implementation.

The simplest search algorithm - just checks every element from start to end.
Works on both sorted and unsorted data.

┌─────────────────────────────────────────────────────────────────────────┐
│  💡 WHEN TO USE LINEAR SEARCH?                                          │
│                                                                         │
│  ✓ Data is unsorted (or sorting is too expensive)                      │
│  ✓ Data is very small (< 10 elements)                                  │
│  ✓ You only need to search once                                        │
│  ✓ You need to find ALL occurrences                                    │
│                                                                         │
│  ✗ Large datasets with many searches → use Binary Search               │
└─────────────────────────────────────────────────────────────────────────┘
"""

from typing import List, Generator, Optional

from ..base import SearchAlgorithm
from ...models import GestureImage, Step, StepType


class LinearSearch(SearchAlgorithm):
    """
    Linear Search - the simplest search algorithm.
    
    Just checks every element from start to end.
    Works on both sorted and unsorted data.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    
    @property
    def name(self) -> str:
        return "Linear Search"
    
    @property
    def requires_sorted(self) -> bool:
        return False  # Works on unsorted data!
    
    def search(
        self,
        data: List[GestureImage],
        target: GestureImage
    ) -> Generator[Step, None, Optional[int]]:
        """
        Search by checking each element from left to right.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        comparisons = 0
        
        yield self._create_step(
            step_type=StepType.SEARCH_RANGE,
            indices=list(range(len(data))),
            description=f"Searching for {target} (rank {target.rank}) using Linear Search",
            data=data,
            metadata={"target_rank": target.rank}
        )
        
        for i in range(len(data)):
            comparisons += 1
            
            # Show which element we're checking
            yield self._create_step(
                step_type=StepType.COMPARE,
                indices=[i],
                description=f"Checking index {i}: {data[i]} (rank {data[i].rank}) vs target {target} (rank {target.rank})",
                data=data,
                highlight=[i],
                metadata={"comparisons": comparisons}
            )
            
            if data[i].rank == target.rank:
                # Found it!
                yield self._create_step(
                    step_type=StepType.FOUND,
                    indices=[i],
                    description=f"FOUND at index {i} after {comparisons} comparisons!",
                    data=data,
                    highlight=[i],
                    metadata={"comparisons": comparisons, "found": True}
                )
                return i
        
        # Not found
        yield self._create_step(
            step_type=StepType.NOT_FOUND,
            indices=[],
            description=f"NOT FOUND after checking all {comparisons} elements",
            data=data,
            metadata={"comparisons": comparisons, "found": False}
        )
        return None
