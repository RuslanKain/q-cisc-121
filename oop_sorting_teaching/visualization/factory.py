"""
Renderer Factory for creating algorithm-specific renderers.

📚 CONCEPT: Factory Pattern

A Factory is a class that creates objects for you.

Benefits:
1. ENCAPSULATION: Client doesn't need to know about specific classes
2. EXTENSIBILITY: Adding a new algorithm just needs a new entry here
3. CONSISTENCY: All renderers are created the same way
"""

from typing import Dict, Type

from .renderers import (
    StepRenderer,
    BubbleSortRenderer,
    MergeSortRenderer,
    QuickSortRenderer,
    LinearSearchRenderer,
    BinarySearchRenderer,
)


class RendererFactory:
    """
    📚 CONCEPT: Factory Pattern
    
    A Factory is a class that creates objects for you.
    
    Benefits:
    1. ENCAPSULATION: Client doesn't need to know about specific classes
    2. EXTENSIBILITY: Adding a new algorithm just needs a new entry here
    3. CONSISTENCY: All renderers are created the same way
    
    PROCEDURAL APPROACH:
        # Scattered if-else throughout the code
        # Hard to maintain, easy to miss cases
    
    OOP FACTORY APPROACH:
        # Single place to manage all renderer creation
        # Easy to extend with new algorithms
    """
    
    # Class-level mapping of algorithm names to renderer classes
    # 📚 CONCEPT: Class Variables
    # These belong to the CLASS, not to instances
    _renderers: Dict[str, Type[StepRenderer]] = {
        "Bubble Sort": BubbleSortRenderer,
        "Bubble Sort (Early Exit)": BubbleSortRenderer,
        "Merge Sort": MergeSortRenderer,
        "Quick Sort": QuickSortRenderer,
        "Linear Search": LinearSearchRenderer,
        "Binary Search": BinarySearchRenderer,
        "Binary Search (Iterative)": BinarySearchRenderer,
        "Binary Search (Recursive)": BinarySearchRenderer,
    }
    
    @classmethod
    def create(cls, algorithm_name: str) -> StepRenderer:
        """
        Create the appropriate renderer for an algorithm.
        
        📚 CONCEPT: @classmethod
        
        A class method receives the CLASS (cls) instead of an instance (self).
        This is perfect for factories because:
        - We don't need an instance of RendererFactory
        - We're creating OTHER objects, not modifying ourselves
        
        Args:
            algorithm_name: Name of the algorithm (from algorithm.name)
            
        Returns:
            The appropriate StepRenderer subclass instance
            
        Raises:
            ValueError: If no renderer exists for the algorithm
        """
        # Check if we have a renderer for this algorithm
        renderer_class = cls._renderers.get(algorithm_name)
        
        if renderer_class is None:
            # Try partial matching (in case of configuration details in name)
            for key, value in cls._renderers.items():
                if key in algorithm_name or algorithm_name in key:
                    renderer_class = value
                    break
        
        if renderer_class is None:
            raise ValueError(
                f"No renderer found for algorithm: {algorithm_name}\n"
                f"Available renderers: {list(cls._renderers.keys())}"
            )
        
        # Create and return an instance of the renderer
        return renderer_class()
    
    @classmethod
    def register(cls, algorithm_name: str, renderer_class: Type[StepRenderer]) -> None:
        """
        Register a new renderer for an algorithm.
        
        📚 CONCEPT: Open/Closed Principle
        
        This method lets us ADD new renderers without MODIFYING
        the factory class itself. The factory is:
        - OPEN for extension (add new renderers)
        - CLOSED for modification (don't change existing code)
        
        Example:
            class MyCustomRenderer(StepRenderer):
                ...
            
            RendererFactory.register("My Algorithm", MyCustomRenderer)
        """
        cls._renderers[algorithm_name] = renderer_class
    
    @classmethod
    def available_renderers(cls) -> list:
        """Return list of available renderer names."""
        return list(cls._renderers.keys())
