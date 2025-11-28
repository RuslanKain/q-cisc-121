"""
Quick Sort implementation.

╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 ALGORITHM: Quick Sort                                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HOW IT WORKS:                                                               ║
║  1. Pick a PIVOT element                                                     ║
║  2. PARTITION: Move smaller elements left, larger elements right             ║
║  3. RECURSE: Sort the left and right partitions                              ║
║                                                                              ║
║  VISUALIZATION (2-way partitioning):                                         ║
║                                                                              ║
║  [3, 8, 1, 5, 2, 9, 4]  pivot = 5                                           ║
║   ↑                 ↑                                                        ║
║   L                 R                                                        ║
║                                                                              ║
║  After partition:                                                            ║
║  [3, 4, 1, 2] [5] [8, 9]                                                    ║
║   < pivot     =   > pivot                                                    ║
║                                                                              ║
║  PROPERTIES:                                                                 ║
║  • Time: O(n log n) average, O(n²) worst case                               ║
║  • Space: O(log n) for recursion stack                                      ║
║  • ⚠️ UNSTABLE: Equal elements may be reordered!                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
from enum import Enum
from typing import List, Generator, Tuple

from ..base import SortingAlgorithm
from ...models import GestureImage, Step, StepType


class PivotStrategy(Enum):
    """
    Strategies for selecting the pivot in Quick Sort.
    
    The pivot choice significantly affects performance:
    - Bad pivot: O(n²) worst case
    - Good pivot: O(n log n) average case
    """
    FIRST = "first"           # Always pick first element (simple but risky)
    LAST = "last"             # Always pick last element
    MEDIAN_OF_THREE = "median" # Pick median of first, middle, last (balanced)
    RANDOM = "random"          # Pick randomly (good average case)


class PartitionScheme(Enum):
    """
    Partitioning schemes for Quick Sort.
    """
    TWO_WAY = "2-way"   # Classic: elements < pivot, elements >= pivot
    THREE_WAY = "3-way"  # Dutch National Flag: <, ==, > (better for duplicates)


class QuickSort(SortingAlgorithm):
    """
    Quick Sort with configurable pivot selection and partitioning.
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  ⚠️ IMPORTANT: Quick Sort is UNSTABLE!                                  │
    │                                                                         │
    │  This is the KEY algorithm for demonstrating instability.               │
    │                                                                         │
    │  Example:                                                               │
    │  Before: [✌️₁, ✌️₂, ✌️₃, ✊]  (three peace signs in order 1,2,3)        │
    │  After:  [✊, ✌️₂, ✌️₁, ✌️₃]  (order changed to 2,1,3!)                 │
    │                                                                         │
    │  The capture_id subscripts let us SEE this instability!                 │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    def __init__(
        self,
        pivot_strategy: PivotStrategy = PivotStrategy.FIRST,
        partition_scheme: PartitionScheme = PartitionScheme.TWO_WAY
    ):
        """
        Initialize Quick Sort with configuration.
        
        Args:
            pivot_strategy: How to choose the pivot element
            partition_scheme: How to partition around the pivot
        """
        self.pivot_strategy = pivot_strategy
        self.partition_scheme = partition_scheme
        self._comparisons = 0
        self._swaps = 0
        self._instability_detected = False
        self._original_order: dict = {}  # Track original positions for stability check
    
    @property
    def name(self) -> str:
        pivot_name = self.pivot_strategy.value.title()
        partition_name = self.partition_scheme.value
        return f"Quick Sort ({pivot_name} Pivot, {partition_name})"
    
    @property
    def is_stable(self) -> bool:
        return False  # Quick sort is NOT stable!
    
    @property
    def is_in_place(self) -> bool:
        return True  # Only uses swaps
    
    def sort(self, data: List[GestureImage]) -> Generator[Step, None, List[GestureImage]]:
        """Sort using quick sort."""
        self._comparisons = 0
        self._swaps = 0
        self._instability_detected = False
        
        # Record original positions for stability checking
        self._original_order = {img.capture_id: i for i, img in enumerate(data)}
        
        if len(data) <= 1:
            return data
        
        yield from self._quick_sort_recursive(data, 0, len(data) - 1, 0)
        
        # Check for instability in final result
        instability_msg = ""
        if self._instability_detected:
            instability_msg = " ⚠️ INSTABILITY DETECTED: Equal elements changed order!"
        
        yield self._create_step(
            step_type=StepType.COMPLETE,
            indices=[],
            description=f"Sorting complete! {self._comparisons} comparisons, {self._swaps} swaps{instability_msg}",
            data=data,
            metadata={
                "comparisons": self._comparisons,
                "swaps": self._swaps,
                "instability_detected": self._instability_detected
            }
        )
        
        return data
    
    def _select_pivot_index(self, data: List[GestureImage], left: int, right: int) -> int:
        """
        Select pivot based on the configured strategy.
        
        Different strategies have different trade-offs:
        - FIRST: Simple but O(n²) on sorted data
        - MEDIAN_OF_THREE: Good balance, avoids worst case
        - RANDOM: Probabilistically good
        """
        if self.pivot_strategy == PivotStrategy.FIRST:
            return left
        
        elif self.pivot_strategy == PivotStrategy.LAST:
            return right
        
        elif self.pivot_strategy == PivotStrategy.RANDOM:
            return random.randint(left, right)
        
        elif self.pivot_strategy == PivotStrategy.MEDIAN_OF_THREE:
            mid = (left + right) // 2
            
            # Find median of first, middle, last
            a, b, c = data[left], data[mid], data[right]
            
            if a <= b <= c or c <= b <= a:
                return mid
            elif b <= a <= c or c <= a <= b:
                return left
            else:
                return right
        
        return left  # Default
    
    def _quick_sort_recursive(
        self,
        data: List[GestureImage],
        left: int,
        right: int,
        depth: int
    ) -> Generator[Step, None, None]:
        """Recursive quick sort implementation."""
        
        if left >= right:
            return
        
        # Select and show pivot
        pivot_idx = self._select_pivot_index(data, left, right)
        
        yield self._create_step(
            step_type=StepType.PIVOT_SELECT,
            indices=[pivot_idx],
            description=f"Depth {depth}: Selected pivot {data[pivot_idx]} at index {pivot_idx}",
            data=data,
            depth=depth,
            metadata={"pivot_strategy": self.pivot_strategy.value}
        )
        
        # Partition based on scheme
        if self.partition_scheme == PartitionScheme.TWO_WAY:
            pivot_final = yield from self._partition_two_way(data, left, right, pivot_idx, depth)
            
            # Recurse on partitions
            yield from self._quick_sort_recursive(data, left, pivot_final - 1, depth + 1)
            yield from self._quick_sort_recursive(data, pivot_final + 1, right, depth + 1)
        
        else:  # THREE_WAY
            lt, gt = yield from self._partition_three_way(data, left, right, pivot_idx, depth)
            
            # Recurse on partitions (skip the equal section)
            yield from self._quick_sort_recursive(data, left, lt - 1, depth + 1)
            yield from self._quick_sort_recursive(data, gt + 1, right, depth + 1)
    
    def _partition_two_way(
        self,
        data: List[GestureImage],
        left: int,
        right: int,
        pivot_idx: int,
        depth: int
    ) -> Generator[Step, None, int]:
        """
        Standard two-way partitioning (Lomuto scheme).
        
        Returns the final position of the pivot.
        """
        # Move pivot to the end
        data[pivot_idx], data[right] = data[right], data[pivot_idx]
        pivot = data[right]
        
        i = left  # Boundary for elements < pivot
        
        yield self._create_step(
            step_type=StepType.PARTITION,
            indices=list(range(left, right + 1)),
            description=f"Partitioning around pivot {pivot}",
            data=data,
            depth=depth
        )
        
        for j in range(left, right):
            self._comparisons += 1
            
            if data[j] < pivot:
                # Check for instability before swap
                if i != j and data[i].rank == data[j].rank:
                    self._check_stability(data[i], data[j])
                
                data[i], data[j] = data[j], data[i]
                self._swaps += 1
                
                yield self._create_step(
                    step_type=StepType.SWAP,
                    indices=[i, j],
                    description=f"Moving {data[i]} to left partition",
                    data=data,
                    depth=depth
                )
                
                i += 1
        
        # Move pivot to final position
        data[i], data[right] = data[right], data[i]
        self._swaps += 1
        
        yield self._create_step(
            step_type=StepType.MARK_SORTED,
            indices=[i],
            description=f"Pivot {data[i]} is now in final position {i}",
            data=data,
            depth=depth
        )
        
        return i
    
    def _partition_three_way(
        self,
        data: List[GestureImage],
        left: int,
        right: int,
        pivot_idx: int,
        depth: int
    ) -> Generator[Step, None, Tuple[int, int]]:
        """
        Three-way partitioning (Dutch National Flag).
        
        Creates three regions: < pivot, == pivot, > pivot
        Better for arrays with many duplicates!
        
        Returns (lt, gt) where:
        - data[left:lt] < pivot
        - data[lt:gt+1] == pivot
        - data[gt+1:right+1] > pivot
        """
        pivot = data[pivot_idx]
        
        lt = left   # data[left:lt] < pivot
        gt = right  # data[gt+1:right+1] > pivot
        i = left    # Current element
        
        yield self._create_step(
            step_type=StepType.PARTITION,
            indices=list(range(left, right + 1)),
            description=f"3-way partitioning around pivot {pivot} (Dutch National Flag)",
            data=data,
            depth=depth
        )
        
        while i <= gt:
            self._comparisons += 1
            
            if data[i] < pivot:
                data[lt], data[i] = data[i], data[lt]
                lt += 1
                i += 1
                self._swaps += 1
                
            elif data[i] > pivot:
                # Check stability before swap
                if data[gt].rank == data[i].rank:
                    self._check_stability(data[i], data[gt])
                
                data[gt], data[i] = data[i], data[gt]
                gt -= 1
                self._swaps += 1
                
            else:
                i += 1
            
            yield self._create_step(
                step_type=StepType.MOVE,
                indices=[lt - 1, i - 1, gt + 1] if lt > left else [i - 1],
                description=f"< pivot: [{left}:{lt}], == pivot: [{lt}:{i}], > pivot: [{gt + 1}:{right + 1}]",
                data=data,
                depth=depth
            )
        
        yield self._create_step(
            step_type=StepType.MARK_SORTED,
            indices=list(range(lt, gt + 1)),
            description=f"All elements equal to pivot are in final positions [{lt}:{gt + 1}]",
            data=data,
            depth=depth
        )
        
        return lt, gt
    
    def _check_stability(self, img1: GestureImage, img2: GestureImage) -> None:
        """
        Check if swapping these elements violates stability.
        
        Stability is violated if:
        - Two elements have the same rank (are "equal")
        - But their relative order changes from the original
        """
        if img1.rank == img2.rank:  # Equal elements
            orig_pos1 = self._original_order.get(img1.capture_id, 0)
            orig_pos2 = self._original_order.get(img2.capture_id, 0)
            
            # If originally img1 came before img2, but now img2 will come first
            if orig_pos1 < orig_pos2:
                self._instability_detected = True
    
    # -------------------------------------------------------------------------
    # Worst Case Analysis Methods
    # -------------------------------------------------------------------------
    
    @staticmethod
    def analyze_input_for_worst_case(
        data: List[GestureImage],
        pivot_strategy: PivotStrategy,
        partition_scheme: PartitionScheme
    ) -> dict:
        """
        Analyze input data to predict if it will cause worst-case behavior.
        
        ╔═════════════════════════════════════════════════════════════════════╗
        ║  📚 WORST CASE SCENARIOS FOR QUICK SORT                             ║
        ╠═════════════════════════════════════════════════════════════════════╣
        ║                                                                     ║
        ║  Quick Sort degrades to O(n²) when partitions are UNBALANCED.       ║
        ║                                                                     ║
        ║  SCENARIO 1: Already Sorted + First/Last Pivot                      ║
        ║  ─────────────────────────────────────────────────────────────      ║
        ║  Input: [1, 2, 3, 4, 5]  Pivot = 1 (first)                         ║
        ║  After partition: [] [1] [2, 3, 4, 5]                              ║
        ║  → Left partition is EMPTY, right has n-1 elements                 ║
        ║  → Recursion depth = n (not log n)                                 ║
        ║  → Time = n + (n-1) + (n-2) + ... = O(n²)                         ║
        ║                                                                     ║
        ║  SCENARIO 2: Reverse Sorted + First/Last Pivot                      ║
        ║  ─────────────────────────────────────────────────────────────      ║
        ║  Same problem, just on the other side.                             ║
        ║                                                                     ║
        ║  SCENARIO 3: Many Duplicates + 2-Way Partitioning                   ║
        ║  ─────────────────────────────────────────────────────────────      ║
        ║  Input: [3, 3, 3, 3, 3]  All elements equal                        ║
        ║  2-way puts duplicates on ONE side → unbalanced!                   ║
        ║  3-way groups duplicates in MIDDLE → balanced!                     ║
        ║                                                                     ║
        ╚═════════════════════════════════════════════════════════════════════╝
        
        Returns:
            Dictionary with analysis results including:
            - is_worst_case: bool
            - risk_level: "low", "medium", "high"
            - reasons: list of strings explaining the risks
            - recommendations: list of strings with suggestions
        """
        n = len(data)
        if n <= 2:
            return {
                "is_worst_case": False,
                "risk_level": "low",
                "reasons": ["Array too small for worst case to matter"],
                "recommendations": []
            }
        
        reasons = []
        recommendations = []
        risk_score = 0
        
        # Check 1: Is the data already sorted or reverse sorted?
        is_sorted_asc = all(data[i] <= data[i+1] for i in range(n-1))
        is_sorted_desc = all(data[i] >= data[i+1] for i in range(n-1))
        is_nearly_sorted = sum(1 for i in range(n-1) if data[i] <= data[i+1]) / (n-1) > 0.8
        
        if is_sorted_asc or is_sorted_desc:
            if pivot_strategy in [PivotStrategy.FIRST, PivotStrategy.LAST]:
                reasons.append(
                    f"Data is {'sorted' if is_sorted_asc else 'reverse sorted'} + "
                    f"{pivot_strategy.value} pivot = WORST CASE! "
                    f"Every partition will be maximally unbalanced (0 vs n-1 split)."
                )
                risk_score += 3
                recommendations.append("Use MEDIAN_OF_THREE or RANDOM pivot strategy")
        elif is_nearly_sorted:
            if pivot_strategy in [PivotStrategy.FIRST, PivotStrategy.LAST]:
                reasons.append(
                    f"Data is nearly sorted ({sum(1 for i in range(n-1) if data[i] <= data[i+1])*100//(n-1)}% in order) + "
                    f"{pivot_strategy.value} pivot = HIGH RISK of unbalanced partitions."
                )
                risk_score += 2
                recommendations.append("Consider MEDIAN_OF_THREE pivot for nearly-sorted data")
        
        # Check 2: How many duplicates?
        unique_values = len(set(img.rank for img in data))
        duplicate_ratio = 1 - (unique_values / n)
        
        if duplicate_ratio > 0.5:  # More than 50% duplicates
            if partition_scheme == PartitionScheme.TWO_WAY:
                reasons.append(
                    f"High duplicate ratio ({duplicate_ratio*100:.0f}%) + 2-way partitioning = "
                    f"INEFFICIENT! All duplicates go to one side."
                )
                risk_score += 2
                recommendations.append("Use 3-WAY partitioning for data with many duplicates")
            else:
                reasons.append(
                    f"High duplicate ratio ({duplicate_ratio*100:.0f}%) but using 3-way partitioning - GOOD! "
                    f"Duplicates will be grouped efficiently."
                )
        
        # Check 3: Pivot strategy effectiveness
        if pivot_strategy == PivotStrategy.RANDOM:
            reasons.append("RANDOM pivot provides probabilistic O(n log n) - safe choice!")
        elif pivot_strategy == PivotStrategy.MEDIAN_OF_THREE:
            reasons.append("MEDIAN_OF_THREE pivot avoids worst case for sorted/reverse-sorted data")
        
        # Determine overall risk level
        if risk_score >= 3:
            risk_level = "high"
            is_worst_case = True
        elif risk_score >= 2:
            risk_level = "medium"
            is_worst_case = False
        else:
            risk_level = "low"
            is_worst_case = False
        
        return {
            "is_worst_case": is_worst_case,
            "risk_level": risk_level,
            "reasons": reasons,
            "recommendations": recommendations,
            "details": {
                "is_sorted_asc": is_sorted_asc,
                "is_sorted_desc": is_sorted_desc,
                "is_nearly_sorted": is_nearly_sorted,
                "duplicate_ratio": duplicate_ratio,
                "unique_values": unique_values,
                "total_elements": n
            }
        }
    
    def analyze_partition_balance(self, left_size: int, right_size: int, total: int) -> str:
        """
        Analyze how balanced a partition is.
        
        Perfect balance: 50/50 split
        Worst case: 0/n or n/0 split
        
        Returns a description of the partition quality.
        """
        if total <= 1:
            return "trivial"
        
        # Calculate balance ratio (0 = worst, 1 = perfect)
        smaller = min(left_size, right_size)
        balance_ratio = smaller / (total - 1) if total > 1 else 1
        
        if balance_ratio >= 0.4:
            return f"GOOD ({left_size}/{right_size} split, {balance_ratio*100:.0f}% balanced)"
        elif balance_ratio >= 0.2:
            return f"MODERATE ({left_size}/{right_size} split, {balance_ratio*100:.0f}% balanced)"
        elif balance_ratio >= 0.1:
            return f"POOR ({left_size}/{right_size} split, {balance_ratio*100:.0f}% balanced)"
        else:
            return f"WORST CASE ({left_size}/{right_size} split - maximally unbalanced!)"
