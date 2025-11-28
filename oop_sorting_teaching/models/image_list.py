"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Models: image_list.py                                                       ║
║  A managed collection of GestureImage objects                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module contains:
• ImageList - A class that manages a list of GestureImage objects

📚 WHY A SPECIAL LIST CLASS?
   Python already has lists, so why create ImageList?
   
   1. ENCAPSULATION: Bundle the list with its operations
   2. VALIDATION: Enforce rules (max 100 elements)
   3. HISTORY: Built-in undo functionality
   4. CONVENIENCE: Methods like shuffle(), duplicate(), is_sorted()
   
   This is the OOP way: data + behavior together in one package.
"""

from typing import List, Optional
from copy import deepcopy
import random

from PIL import Image

from oop_sorting_teaching.models.gesture import GestureImage


# ==============================================================================
# CLASS: ImageList
# ==============================================================================

class ImageList:
    """
    A managed collection of GestureImage objects.
    
    This class handles:
    - Adding and removing images
    - Duplicating images (for testing)
    - Tracking history (for undo)
    - Enforcing the 100-element limit
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  🔄 PROCEDURAL vs OOP: Managing a list of items                         │
    │                                                                         │
    │  PROCEDURAL:                                                            │
    │      images = []                                                        │
    │      def add_image(images, img):                                        │
    │          if len(images) < 100:                                          │
    │              images.append(img)                                         │
    │      def remove_image(images, index):                                   │
    │          if 0 <= index < len(images):                                   │
    │              images.pop(index)                                          │
    │      # Functions scattered, list is just raw data                       │
    │                                                                         │
    │  OOP:                                                                   │
    │      class ImageList:                                                   │
    │          def add(self, img): ...                                        │
    │          def remove(self, index): ...                                   │
    │      # List AND its operations are bundled together!                    │
    │      # Can't accidentally use wrong function on wrong list.             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # Class constant: maximum number of elements allowed
    MAX_SIZE = 100
    
    def __init__(self):
        """
        Initialize an empty ImageList.
        
        📚 CONCEPT: __init__ is the Constructor
        
        The constructor is called when you create a new object:
            my_list = ImageList()  # This calls __init__
        
        It sets up the initial state of the object.
        """
        self._images: List[GestureImage] = []  # The actual list (private)
        self._history: List[List[GestureImage]] = []  # For undo functionality
        self._next_capture_id: int = 1  # Counter for unique IDs
    
    # -------------------------------------------------------------------------
    # Properties: Controlled access to data
    # -------------------------------------------------------------------------
    """
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║  📚 CONCEPT: Properties (@property)                                     ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║  A property looks like an attribute but is actually a method.           ║
    ║                                                                         ║
    ║  WITHOUT property:                                                      ║
    ║      length = my_list.get_length()  # Method call (ugly)               ║
    ║                                                                         ║
    ║  WITH property:                                                         ║
    ║      length = my_list.length  # Looks like attribute (clean!)          ║
    ║                                                                         ║
    ║  Benefits:                                                              ║
    ║  ✓ Clean syntax (no parentheses needed)                                ║
    ║  ✓ Can add validation/computation without changing interface           ║
    ║  ✓ Can be read-only (no setter = cannot modify)                        ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """
    
    @property
    def length(self) -> int:
        """Number of images in the list."""
        return len(self._images)
    
    @property
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return len(self._images) == 0
    
    @property
    def is_full(self) -> bool:
        """Check if the list has reached maximum capacity."""
        return len(self._images) >= self.MAX_SIZE
    
    @property
    def images(self) -> List[GestureImage]:
        """
        Get a COPY of the images list.
        
        Why a copy? To prevent external code from modifying
        our internal list directly. This is called ENCAPSULATION.
        """
        return self._images.copy()
    
    # -------------------------------------------------------------------------
    # Core Operations
    # -------------------------------------------------------------------------
    
    def add(self, image: GestureImage) -> bool:
        """
        Add an image to the list.
        
        Args:
            image: The GestureImage to add
            
        Returns:
            True if added successfully, False if list is full
        """
        if self.is_full:
            print(f"⚠️ Cannot add: list is at maximum capacity ({self.MAX_SIZE})")
            return False
        
        self._save_state()  # Save for undo
        self._images.append(image)
        return True
    
    def add_new(
        self,
        gesture_name: str,
        image: Optional[Image.Image] = None,
        confidence: float = 0.0
    ) -> Optional[GestureImage]:
        """
        Create and add a new GestureImage.
        
        This is a convenience method that:
        1. Creates a new GestureImage with auto-generated capture_id
        2. Adds it to the list
        
        Args:
            gesture_name: Name of the gesture
            image: The image data
            confidence: AI confidence score
            
        Returns:
            The created GestureImage, or None if list is full
        """
        if self.is_full:
            return None
        
        gesture_image = GestureImage.create_from_prediction(
            gesture_name=gesture_name,
            capture_id=self._next_capture_id,
            image=image,
            confidence=confidence
        )
        
        if self.add(gesture_image):
            self._next_capture_id += 1
            return gesture_image
        return None
    
    def remove(self, index: int) -> Optional[GestureImage]:
        """
        Remove and return the image at the given index.
        
        Args:
            index: Position of the image to remove (0-based)
            
        Returns:
            The removed GestureImage, or None if index invalid
        """
        if not 0 <= index < len(self._images):
            print(f"⚠️ Invalid index: {index}")
            return None
        
        self._save_state()
        return self._images.pop(index)
    
    def duplicate(self, index: int) -> Optional[GestureImage]:
        """
        Create a duplicate of the image at the given index.
        
        The duplicate gets a NEW capture_id (important for stability testing).
        
        Args:
            index: Position of the image to duplicate
            
        Returns:
            The new duplicate GestureImage, or None if failed
        """
        if not 0 <= index < len(self._images):
            print(f"⚠️ Invalid index: {index}")
            return None
        
        if self.is_full:
            print(f"⚠️ Cannot duplicate: list is at maximum capacity")
            return None
        
        original = self._images[index]
        
        # Create duplicate with new capture_id
        duplicate = GestureImage(
            gesture=original.gesture,
            rank=original.rank,
            emoji=original.emoji,
            capture_id=self._next_capture_id,
            image=original.image,
            thumbnail=original.thumbnail,
            confidence=original.confidence
        )
        
        self._save_state()
        # Insert right after the original
        self._images.insert(index + 1, duplicate)
        self._next_capture_id += 1
        
        return duplicate
    
    def clear(self) -> None:
        """Remove all images from the list."""
        self._save_state()
        self._images.clear()
    
    def swap(self, i: int, j: int) -> bool:
        """
        Swap elements at indices i and j.
        
        This is the fundamental operation for in-place sorting algorithms.
        
        Args:
            i: First index
            j: Second index
            
        Returns:
            True if swap successful, False if indices invalid
        """
        if not (0 <= i < len(self._images) and 0 <= j < len(self._images)):
            return False
        
        self._images[i], self._images[j] = self._images[j], self._images[i]
        return True
    
    # -------------------------------------------------------------------------
    # List Manipulation
    # -------------------------------------------------------------------------
    
    def shuffle(self) -> None:
        """Randomly shuffle the images."""
        self._save_state()
        random.shuffle(self._images)
    
    def reverse(self) -> None:
        """Reverse the order of images."""
        self._save_state()
        self._images.reverse()
    
    def sort_ascending(self) -> None:
        """Sort images in ascending order (by rank)."""
        self._save_state()
        self._images.sort()  # Uses __lt__ we defined!
    
    def sort_descending(self) -> None:
        """Sort images in descending order (by rank)."""
        self._save_state()
        self._images.sort(reverse=True)
    
    # -------------------------------------------------------------------------
    # Analysis Methods
    # -------------------------------------------------------------------------
    
    def is_sorted(self, ascending: bool = True) -> bool:
        """
        Check if the list is sorted.
        
        Args:
            ascending: If True, check ascending order; else descending
            
        Returns:
            True if sorted in the specified order
        """
        if len(self._images) <= 1:
            return True
        
        for i in range(len(self._images) - 1):
            if ascending:
                if self._images[i] > self._images[i + 1]:
                    return False
            else:
                if self._images[i] < self._images[i + 1]:
                    return False
        return True
    
    def count_unique_gestures(self) -> int:
        """Count how many unique gestures are in the list."""
        return len(set(img.gesture for img in self._images))
    
    def count_duplicates(self) -> int:
        """Count how many duplicate gestures exist."""
        return len(self._images) - self.count_unique_gestures()
    
    def get_sortedness_percentage(self) -> float:
        """
        Calculate how sorted the list is (0% to 100%).
        
        This counts how many adjacent pairs are in correct order.
        """
        if len(self._images) <= 1:
            return 100.0
        
        correct_pairs = 0
        for i in range(len(self._images) - 1):
            if self._images[i] <= self._images[i + 1]:
                correct_pairs += 1
        
        return (correct_pairs / (len(self._images) - 1)) * 100
    
    def get_analysis(self) -> str:
        """Get a human-readable analysis of the current list state."""
        if self.is_empty:
            return "Empty list"
        
        unique = self.count_unique_gestures()
        dupes = self.count_duplicates()
        sorted_pct = self.get_sortedness_percentage()
        
        analysis = f"{len(self._images)} elements, {unique} unique"
        if dupes > 0:
            analysis += f", {dupes} duplicates"
        analysis += f", {sorted_pct:.0f}% sorted"
        
        return analysis
    
    # -------------------------------------------------------------------------
    # History / Undo
    # -------------------------------------------------------------------------
    
    def _save_state(self) -> None:
        """Save current state for undo. (Internal method)"""
        # Keep only last 10 states to save memory
        if len(self._history) >= 10:
            self._history.pop(0)
        self._history.append(deepcopy(self._images))
    
    def undo(self) -> bool:
        """
        Restore the previous state.
        
        Returns:
            True if undo successful, False if no history available
        """
        if not self._history:
            print("⚠️ Nothing to undo")
            return False
        
        self._images = self._history.pop()
        return True
    
    # -------------------------------------------------------------------------
    # Iteration Support
    # -------------------------------------------------------------------------
    """
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║  📚 CONCEPT: Making Objects Iterable                                    ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║  By implementing __iter__ and __len__, our ImageList can be used        ║
    ║  just like a regular Python list:                                       ║
    ║                                                                         ║
    ║      for image in my_image_list:        # Works!                        ║
    ║          print(image)                                                   ║
    ║                                                                         ║
    ║      length = len(my_image_list)         # Works!                       ║
    ║                                                                         ║
    ║      first = my_image_list[0]            # Works!                       ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """
    
    def __len__(self) -> int:
        """Enable len(image_list)."""
        return len(self._images)
    
    def __iter__(self):
        """Enable for image in image_list."""
        return iter(self._images)
    
    def __getitem__(self, index: int) -> GestureImage:
        """Enable image_list[0], image_list[1], etc."""
        return self._images[index]
    
    def __setitem__(self, index: int, value: GestureImage) -> None:
        """Enable image_list[0] = new_image."""
        self._images[index] = value
    
    # -------------------------------------------------------------------------
    # Display Methods
    # -------------------------------------------------------------------------
    
    def display_string(self) -> str:
        """
        Get a string representation showing all images with their emojis.
        
        Example: "[✊₁] [✌️₂] [✌️₃] [👍₄]"
        """
        if self.is_empty:
            return "(empty)"
        return " ".join(f"[{img}]" for img in self._images)
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return f"ImageList({self.display_string()})"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"ImageList(length={len(self._images)}, max={self.MAX_SIZE})"
