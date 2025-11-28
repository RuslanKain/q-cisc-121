"""
Base classes for sorting and searching algorithms.

This module defines the abstract base classes (interfaces) that all
sorting and searching algorithms must implement.

OOP Concepts Demonstrated:
- Abstract Base Classes (ABC)
- Abstract methods (@abstractmethod)
- Properties (@property)
- Generator functions (yield)
- Type hints with Generator
"""

from abc import ABC, abstractmethod
from typing import List, Generator, Tuple, Optional

from ..models import GestureImage, Step, StepType


# ==============================================================================
# ABSTRACT CLASS: SortingAlgorithm (The Interface)
# ==============================================================================

class SortingAlgorithm(ABC):
    """
    Abstract base class (interface) for all sorting algorithms.
    
    This defines the CONTRACT that all sorting algorithms must follow:
    - They must have a name
    - They must indicate if they're stable
    - They must indicate if they sort in-place
    - They must implement a sort() method that yields steps
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  🔄 PROCEDURAL vs OOP: Algorithm Organization                           │
    │                                                                         │
    │  PROCEDURAL (scattered functions):                                      │
    │      def bubble_sort(arr): ...                                          │
    │      def merge_sort(arr): ...                                           │
    │      def quick_sort(arr): ...                                           │
    │      # No clear structure, hard to add new algorithms                   │
    │                                                                         │
    │  OOP (organized hierarchy):                                             │
    │      class SortingAlgorithm(ABC):  # The contract                       │
    │          def sort(self): ...                                            │
    │                                                                         │
    │      class BubbleSort(SortingAlgorithm):  # Implements contract         │
    │      class MergeSort(SortingAlgorithm):   # Implements contract         │
    │      class QuickSort(SortingAlgorithm):   # Implements contract         │
    │                                                                         │
    │      # Easy to add new algorithms, all follow same pattern!             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # -------------------------------------------------------------------------
    # Abstract Properties (MUST be implemented by subclasses)
    # -------------------------------------------------------------------------
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The display name of the algorithm (e.g., 'Bubble Sort')."""
        pass
    
    @property
    @abstractmethod
    def is_stable(self) -> bool:
        """
        Whether the algorithm is stable.
        
        A STABLE algorithm preserves the relative order of equal elements.
        
        Example with [✌️₁, ✌️₂, ✊]:
        - Stable: Always produces [✊, ✌️₁, ✌️₂] (original order of peace signs kept)
        - Unstable: Might produce [✊, ✌️₂, ✌️₁] (order can change)
        """
        pass
    
    @property
    @abstractmethod
    def is_in_place(self) -> bool:
        """
        Whether the algorithm sorts in-place (modifies the original array).
        
        In-place: Uses O(1) extra memory (just swaps elements)
        Not in-place: Creates new arrays (uses O(n) extra memory)
        """
        pass
    
    @property
    def description(self) -> str:
        """Human-readable description of the algorithm."""
        stability = "Stable" if self.is_stable else "Unstable"
        memory = "In-place" if self.is_in_place else "Out-of-place"
        return f"{self.name} ({stability}, {memory})"
    
    # -------------------------------------------------------------------------
    # Abstract Method: sort (MUST be implemented by subclasses)
    # -------------------------------------------------------------------------
    
    @abstractmethod
    def sort(self, data: List[GestureImage]) -> Generator[Step, None, List[GestureImage]]:
        """
        Sort the data and yield steps for visualization.
        
        This is a GENERATOR function (uses yield instead of return).
        It allows us to pause the algorithm after each step for visualization.
        
        Args:
            data: List of GestureImage objects to sort
            
        Yields:
            Step objects describing each operation
            
        Returns:
            The sorted list
        """
        pass
    
    # -------------------------------------------------------------------------
    # Concrete Methods (shared by all subclasses)
    # -------------------------------------------------------------------------
    
    def run_full(self, data: List[GestureImage]) -> Tuple[List[GestureImage], List[Step]]:
        """
        Run the sort and collect all steps (non-generator version).
        
        Use this when you want all steps at once, not one at a time.
        
        Args:
            data: List to sort
            
        Returns:
            Tuple of (sorted_list, list_of_all_steps)
        """
        steps = []
        result = None
        
        # Consume the generator and collect steps
        generator = self.sort(data.copy())
        try:
            while True:
                step = next(generator)
                steps.append(step)
        except StopIteration as e:
            result = e.value  # The return value of the generator
        
        return result if result else data, steps
    
    def _create_step(
        self,
        step_type: StepType,
        indices: List[int],
        description: str,
        data: List[GestureImage],
        depth: int = 0,
        highlight: List[int] = None,
        metadata: dict = None
    ) -> Step:
        """
        Helper method to create a Step object.
        
        The underscore prefix indicates this is for internal use.
        """
        return Step(
            step_type=step_type,
            indices=indices,
            description=description,
            depth=depth,
            array_state=[img for img in data],  # Copy the current state
            highlight_indices=highlight or [],
            metadata=metadata or {}
        )


# ==============================================================================
# ABSTRACT CLASS: SearchAlgorithm (The Interface for Search Algorithms)
# ==============================================================================

class SearchAlgorithm(ABC):
    """
    Abstract base class (interface) for all search algorithms.
    
    This is similar to SortingAlgorithm but for searching.
    By having a common interface, we can swap between different
    search algorithms easily (Linear Search, Binary Search, etc.)
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  🔄 PROCEDURAL vs OOP: Search Functions                                 │
    │                                                                         │
    │  PROCEDURAL:                                                            │
    │      def linear_search(arr, target): ...                                │
    │      def binary_search(arr, target): ...                                │
    │      # No clear structure, different return types, etc.                 │
    │                                                                         │
    │  OOP:                                                                   │
    │      class SearchAlgorithm(ABC):                                        │
    │          def search(self, data, target) -> Generator[Step]: ...         │
    │                                                                         │
    │      class LinearSearch(SearchAlgorithm): ...                           │
    │      class BinarySearch(SearchAlgorithm): ...                           │
    │                                                                         │
    │      # All search algorithms follow the same pattern!                   │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The display name of the algorithm."""
        pass
    
    @property
    @abstractmethod
    def requires_sorted(self) -> bool:
        """Whether the algorithm requires sorted input."""
        pass
    
    @property
    def description(self) -> str:
        """Human-readable description."""
        sorted_req = "requires sorted input" if self.requires_sorted else "works on unsorted"
        return f"{self.name} ({sorted_req})"
    
    @abstractmethod
    def search(
        self,
        data: List[GestureImage],
        target: GestureImage
    ) -> Generator[Step, None, Optional[int]]:
        """
        Search for target in data and yield steps for visualization.
        
        Args:
            data: List to search in
            target: Element to find
            
        Yields:
            Step objects describing each operation
            
        Returns:
            Index of target if found, None otherwise
        """
        pass
    
    def run_full(
        self,
        data: List[GestureImage],
        target: GestureImage
    ) -> Tuple[Optional[int], List[Step]]:
        """
        Run the search and collect all steps.
        
        Returns:
            Tuple of (result_index, list_of_all_steps)
        """
        steps = []
        result = None
        
        generator = self.search(data, target)
        try:
            while True:
                step = next(generator)
                steps.append(step)
        except StopIteration as e:
            result = e.value
        
        return result, steps
    
    def _create_step(
        self,
        step_type: StepType,
        indices: List[int],
        description: str,
        data: List[GestureImage],
        highlight: List[int] = None,
        metadata: dict = None
    ) -> Step:
        """Helper to create Step objects."""
        return Step(
            step_type=step_type,
            indices=indices,
            description=description,
            depth=0,
            array_state=[img for img in data],
            highlight_indices=highlight or [],
            metadata=metadata or {}
        )
