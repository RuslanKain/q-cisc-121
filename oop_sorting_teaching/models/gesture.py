"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  Models: gesture.py                                                          ║
║  Core classes for representing hand gestures                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

This module contains:
• GestureRanking - The ranking system for gestures
• GestureImage - Represents a captured gesture with its data

📚 WHY SEPARATE FILES?
   In the procedural style, you might put everything in one big file.
   In OOP, we organize related classes into modules (files).
   
   Benefits:
   • Easier to find code (gesture stuff is in gesture.py)
   • Easier to test (can test gesture.py independently)
   • Easier to reuse (import just what you need)
   • Easier to collaborate (different people work on different files)
"""

from dataclasses import dataclass
from typing import List, Optional
from PIL import Image


# ==============================================================================
# CLASS: GestureRanking
# ==============================================================================
# This class holds the RANKING SYSTEM for gestures.
# It's like a rulebook that says "fist comes before one, one comes before peace..."
#
# 💡 WHY A CLASS? 
#    In procedural code, this would be a dictionary floating around globally.
#    As a class, we can:
#    1. Add METHODS to work with the data (get_rank, get_emoji, compare)
#    2. PROTECT the data from accidental changes
#    3. Keep related functions TOGETHER with the data they use
# ==============================================================================

class GestureRanking:
    """
    Defines the ordering of hand gestures for sorting purposes.
    
    This class encapsulates (bundles together):
    - The ranking of each gesture (which comes first in sorted order)
    - The emoji representation of each gesture
    - Methods to compare gestures
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  📚 CONCEPT: Class Attributes vs Instance Attributes                    │
    │                                                                         │
    │  CLASS ATTRIBUTES: Shared by ALL instances (objects) of the class      │
    │      - Defined directly in the class body                               │
    │      - Like a shared resource everyone can read                         │
    │      - Here: RANKINGS and EMOJIS are class attributes                   │
    │                                                                         │
    │  INSTANCE ATTRIBUTES: Unique to EACH instance                           │
    │      - Defined in __init__ using self.attribute_name                    │
    │      - Like personal belongings each person carries                     │
    │      - Here: GestureRanking doesn't have instance attributes            │
    │              (it's a utility class with shared data)                    │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # -------------------------------------------------------------------------
    # Class Attribute: RANKINGS
    # -------------------------------------------------------------------------
    # This dictionary maps gesture names to their rank (sorting order).
    # Lower rank = comes first when sorted in ascending order.
    #
    # 💭 Design Decision: We ordered gestures roughly by "finger count"
    #    fist (0 fingers) → one → peace (2) → three → four → palm (5) → special signs
    # -------------------------------------------------------------------------
    RANKINGS = {
        "fist":     1,   # ✊ Closed fist (0 fingers showing)
        "one":      2,   # ☝️ One finger up
        "two_up":   3,   # ✌️ Two fingers (peace sign)
        "peace":    3,   # ✌️ Alias for two_up (same gesture, different name)
        "three":    4,   # 🤟 Three fingers
        "four":     5,   # 🖖 Four fingers
        "palm":     6,   # 🖐️ Open palm (5 fingers)
        "stop":     6,   # 🖐️ Alias for palm
        "ok":       7,   # 👌 OK sign
        "like":     8,   # 👍 Thumbs up
        "dislike":  9,   # 👎 Thumbs down
        "rock":    10,   # 🤘 Rock sign
        "call":    11,   # 🤙 Call me sign
        "mute":    12,   # 🤫 Shush/mute gesture
        "no_gesture": 99, # Unknown or no gesture detected
    }
    
    # -------------------------------------------------------------------------
    # Class Attribute: EMOJIS
    # -------------------------------------------------------------------------
    # Visual representation of each gesture.
    # Makes the UI more engaging and helps identify gestures quickly.
    # -------------------------------------------------------------------------
    EMOJIS = {
        "fist":     "✊",
        "one":      "☝️",
        "two_up":   "✌️",
        "peace":    "✌️",
        "three":    "🤟",
        "four":     "🖖",
        "palm":     "🖐️",
        "stop":     "🖐️",
        "ok":       "👌",
        "like":     "👍",
        "dislike":  "👎",
        "rock":     "🤘",
        "call":     "🤙",
        "mute":     "🤫",
        "no_gesture": "❓",
    }
    
    # -------------------------------------------------------------------------
    # Class Method: get_rank
    # -------------------------------------------------------------------------
    # 📚 CONCEPT: @classmethod
    # 
    # A classmethod belongs to the CLASS, not to an instance.
    # - Regular method: needs an object to be called (object.method())
    # - Class method: can be called on the class itself (ClassName.method())
    #
    # Use @classmethod when the method needs CLASS data but not INSTANCE data.
    # -------------------------------------------------------------------------
    @classmethod
    def get_rank(cls, gesture_name: str) -> int:
        """
        Get the sorting rank of a gesture.
        
        Args:
            gesture_name: The name of the gesture (e.g., "peace", "fist")
            
        Returns:
            The rank (1-99) of the gesture. Lower = earlier in sorted order.
            Returns 99 if gesture is unknown.
            
        Example:
            >>> GestureRanking.get_rank("peace")
            3
            >>> GestureRanking.get_rank("fist")
            1
        """
        # .get() returns the value if key exists, otherwise the default (99)
        # This prevents crashes if someone passes an unknown gesture name
        return cls.RANKINGS.get(gesture_name.lower(), 99)
    
    @classmethod
    def get_emoji(cls, gesture_name: str) -> str:
        """
        Get the emoji representation of a gesture.
        
        Args:
            gesture_name: The name of the gesture
            
        Returns:
            The emoji string for this gesture, or ❓ if unknown.
        """
        return cls.EMOJIS.get(gesture_name.lower(), "❓")
    
    @classmethod
    def compare(cls, gesture_a: str, gesture_b: str) -> int:
        """
        Compare two gestures for sorting order.
        
        This follows the standard comparison convention:
        - Returns NEGATIVE if a < b (a comes before b)
        - Returns ZERO if a == b (same rank)
        - Returns POSITIVE if a > b (a comes after b)
        
        Args:
            gesture_a: First gesture name
            gesture_b: Second gesture name
            
        Returns:
            Negative, zero, or positive integer.
            
        Example:
            >>> GestureRanking.compare("fist", "peace")
            -2  # Negative: fist comes before peace
            >>> GestureRanking.compare("peace", "fist")
            2   # Positive: peace comes after fist
        """
        return cls.get_rank(gesture_a) - cls.get_rank(gesture_b)
    
    @classmethod
    def get_all_gestures(cls) -> List[str]:
        """
        Get a list of all known gestures, sorted by rank.
        
        Returns:
            List of gesture names in sorted order.
        """
        # Sort the gesture names by their rank value
        # This uses a lambda function as the sorting key
        sorted_gestures = sorted(
            cls.RANKINGS.keys(),
            key=lambda name: cls.RANKINGS[name]
        )
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for gesture in sorted_gestures:
            if gesture not in seen:
                seen.add(gesture)
                unique.append(gesture)
        return unique


# ==============================================================================
# CLASS: GestureImage (using @dataclass)
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 CONCEPT: What is a @dataclass?                                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  A @dataclass is a shortcut for creating classes that mainly hold DATA.      ║
║                                                                              ║
║  WITHOUT @dataclass (the long way):                                          ║
║  ─────────────────────────────────                                           ║
║      class GestureImage:                                                     ║
║          def __init__(self, gesture, rank, emoji, image, capture_id):        ║
║              self.gesture = gesture                                          ║
║              self.rank = rank                                                ║
║              self.emoji = emoji                                              ║
║              self.image = image                                              ║
║              self.capture_id = capture_id                                    ║
║                                                                              ║
║          def __repr__(self):                                                 ║
║              return f"GestureImage(gesture={self.gesture}, ...)"             ║
║                                                                              ║
║          def __eq__(self, other):                                            ║
║              return self.gesture == other.gesture and ...                    ║
║                                                                              ║
║  WITH @dataclass (the shortcut):                                             ║
║  ───────────────────────────────                                             ║
║      @dataclass                                                              ║
║      class GestureImage:                                                     ║
║          gesture: str                                                        ║
║          rank: int                                                           ║
║          emoji: str                                                          ║
║          image: Image                                                        ║
║          capture_id: int                                                     ║
║                                                                              ║
║  The @dataclass automatically generates __init__, __repr__, __eq__, etc!     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

@dataclass
class GestureImage:
    """
    Represents a captured hand gesture image with its classification.
    
    This is the CORE DATA STRUCTURE of our application.
    Each GestureImage bundles together:
    - The actual image (pixels)
    - The AI's prediction of what gesture it shows
    - A unique ID for tracking (important for stability testing)
    - Visual representations (emoji, rank)
    
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  💡 WHY THIS MATTERS: Encapsulation                                     │
    │                                                                         │
    │  In procedural code, you'd pass around separate variables:              │
    │      process_gesture(image, name, rank, emoji, id)  # 5 parameters!     │
    │                                                                         │
    │  With OOP, you pass ONE object that contains everything:                │
    │      process_gesture(gesture_image)  # 1 parameter!                     │
    │                                                                         │
    │  Benefits:                                                              │
    │  ✓ Less room for errors (can't mix up parameter order)                 │
    │  ✓ Easier to add new attributes later                                  │
    │  ✓ Methods travel WITH the data they operate on                        │
    └─────────────────────────────────────────────────────────────────────────┘
    
    Attributes:
        gesture: The name of the detected gesture (e.g., "peace", "fist")
        rank: Numeric rank for sorting (lower = comes first)
        emoji: Visual emoji representation
        image: The actual PIL Image (can be None if not needed)
        capture_id: Unique ID from capture order (for stability testing)
        thumbnail: Smaller version for display (generated automatically)
    """
    
    # -------------------------------------------------------------------------
    # Dataclass Fields (Attributes)
    # -------------------------------------------------------------------------
    # These define what data each GestureImage object will hold.
    # The type hints (: str, : int, etc.) help document and catch errors.
    # -------------------------------------------------------------------------
    
    gesture: str                           # Name of the gesture
    rank: int                              # Sorting rank (from GestureRanking)
    emoji: str                             # Emoji representation
    capture_id: int                        # Unique ID (for stability tracking)
    image: Optional[Image.Image] = None    # The actual image (optional)
    thumbnail: Optional[Image.Image] = None  # Small version for display
    confidence: float = 0.0                # AI's confidence in the prediction
    
    # -------------------------------------------------------------------------
    # Special Method: __post_init__
    # -------------------------------------------------------------------------
    # This runs AFTER the automatic __init__ created by @dataclass.
    # We use it to create the thumbnail from the full image.
    # -------------------------------------------------------------------------
    def __post_init__(self):
        """
        Called automatically after the object is created.
        Generates a thumbnail if an image is provided.
        """
        if self.image is not None and self.thumbnail is None:
            self._create_thumbnail()
    
    def _create_thumbnail(self, max_size: int = 80):
        """
        Create a smaller version of the image for display.
        
        The underscore prefix (_create_thumbnail) is a Python convention
        meaning "this is an internal method, not meant to be called from outside".
        
        Args:
            max_size: Maximum width/height of the thumbnail
        """
        if self.image is not None:
            # Create a copy so we don't modify the original
            thumb = self.image.copy()
            # Resize while maintaining aspect ratio
            thumb.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            self.thumbnail = thumb
    
    # -------------------------------------------------------------------------
    # Comparison Methods: Making objects sortable
    # -------------------------------------------------------------------------
    """
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║  📚 CONCEPT: Magic Methods (Dunder Methods)                             ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║  Python has special method names surrounded by double underscores.      ║
    ║  These are called "magic methods" or "dunder methods" (double under).   ║
    ║                                                                         ║
    ║  They let your objects work with Python's built-in operations:          ║
    ║                                                                         ║
    ║  __lt__(self, other)  →  enables: object1 < object2                    ║
    ║  __le__(self, other)  →  enables: object1 <= object2                   ║
    ║  __eq__(self, other)  →  enables: object1 == object2                   ║
    ║  __gt__(self, other)  →  enables: object1 > object2                    ║
    ║  __ge__(self, other)  →  enables: object1 >= object2                   ║
    ║  __str__(self)        →  enables: str(object) or print(object)         ║
    ║  __repr__(self)       →  enables: repr(object) (for debugging)         ║
    ║                                                                         ║
    ║  💡 WHY THIS MATTERS:                                                   ║
    ║  With these methods, Python's built-in sorted() function                ║
    ║  automatically works with our GestureImage objects!                     ║
    ║                                                                         ║
    ║      gestures = [gesture1, gesture2, gesture3]                         ║
    ║      sorted_gestures = sorted(gestures)  # Just works! ✨              ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """
    
    def __lt__(self, other: 'GestureImage') -> bool:
        """
        Less than comparison. Enables: gesture1 < gesture2
        
        Compares by rank. If ranks are equal, maintains stability
        by comparing capture_id (earlier captured = smaller).
        """
        if self.rank != other.rank:
            return self.rank < other.rank
        # If same rank, compare by capture_id for stable sorting
        return self.capture_id < other.capture_id
    
    def __le__(self, other: 'GestureImage') -> bool:
        """Less than or equal. Enables: gesture1 <= gesture2"""
        return self.rank <= other.rank
    
    def __gt__(self, other: 'GestureImage') -> bool:
        """Greater than. Enables: gesture1 > gesture2"""
        if self.rank != other.rank:
            return self.rank > other.rank
        return self.capture_id > other.capture_id
    
    def __ge__(self, other: 'GestureImage') -> bool:
        """Greater than or equal. Enables: gesture1 >= gesture2"""
        return self.rank >= other.rank
    
    def __eq__(self, other: object) -> bool:
        """
        Equality comparison. Enables: gesture1 == gesture2
        
        Two gestures are equal if they have the same rank.
        Note: We compare RANKS, not capture_ids, for sorting purposes.
        """
        if not isinstance(other, GestureImage):
            return False
        return self.rank == other.rank
    
    def __hash__(self) -> int:
        """
        Hash function. Required for using objects in sets or as dict keys.
        We hash by capture_id since it's unique.
        """
        return hash(self.capture_id)
    
    # -------------------------------------------------------------------------
    # Display Methods
    # -------------------------------------------------------------------------
    
    def __str__(self) -> str:
        """
        Human-readable string representation.
        Called by print() and str().
        
        Example: "✌️₁" (peace sign, capture #1)
        """
        # Subscript numbers for capture_id
        subscripts = "₀₁₂₃₄₅₆₇₈₉"
        sub_id = ''.join(subscripts[int(d)] for d in str(self.capture_id))
        return f"{self.emoji}{sub_id}"
    
    def __repr__(self) -> str:
        """
        Developer-friendly representation (for debugging).
        Called by repr() and shown in interactive Python.
        """
        return f"GestureImage(gesture='{self.gesture}', rank={self.rank}, id={self.capture_id})"
    
    def display_label(self) -> str:
        """
        Get a label for UI display.
        Shows emoji, gesture name, and capture ID.
        """
        return f"{self.emoji} {self.gesture} (#{self.capture_id})"
    
    # -------------------------------------------------------------------------
    # Factory Methods
    # -------------------------------------------------------------------------
    """
    ╔═════════════════════════════════════════════════════════════════════════╗
    ║  📚 CONCEPT: Factory Methods                                            ║
    ╠═════════════════════════════════════════════════════════════════════════╣
    ║                                                                         ║
    ║  A Factory Method is a class method that CREATES instances.             ║
    ║                                                                         ║
    ║  Instead of:                                                            ║
    ║      gesture = GestureImage(                                            ║
    ║          gesture="peace",                                               ║
    ║          rank=GestureRanking.get_rank("peace"),                         ║
    ║          emoji=GestureRanking.get_emoji("peace"),                       ║
    ║          capture_id=1,                                                  ║
    ║          image=my_image,                                                ║
    ║          confidence=0.95                                                ║
    ║      )                                                                  ║
    ║                                                                         ║
    ║  You can use:                                                           ║
    ║      gesture = GestureImage.create_from_prediction(                     ║
    ║          gesture_name="peace",                                          ║
    ║          capture_id=1,                                                  ║
    ║          image=my_image,                                                ║
    ║          confidence=0.95                                                ║
    ║      )                                                                  ║
    ║                                                                         ║
    ║  The factory method handles the details of looking up rank/emoji!       ║
    ║                                                                         ║
    ╚═════════════════════════════════════════════════════════════════════════╝
    """
    
    @classmethod
    def create_from_prediction(
        cls,
        gesture_name: str,
        capture_id: int,
        image: Optional[Image.Image] = None,
        confidence: float = 0.0
    ) -> 'GestureImage':
        """
        Factory method to create a GestureImage from an AI prediction.
        
        This is a convenient way to create GestureImage objects without
        needing to manually look up ranks and emojis.
        
        Args:
            gesture_name: The predicted gesture name
            capture_id: Unique identifier for this capture
            image: The original image (optional)
            confidence: AI confidence score (0.0 to 1.0)
            
        Returns:
            A new GestureImage instance
        """
        return cls(
            gesture=gesture_name.lower(),
            rank=GestureRanking.get_rank(gesture_name),
            emoji=GestureRanking.get_emoji(gesture_name),
            capture_id=capture_id,
            image=image,
            confidence=confidence
        )
    
    @classmethod
    def create_manual(
        cls,
        gesture_name: str,
        capture_id: int,
        image: Optional[Image.Image] = None
    ) -> 'GestureImage':
        """
        Create a GestureImage with manual gesture assignment (no AI).
        Same as create_from_prediction but with 100% confidence.
        """
        return cls.create_from_prediction(
            gesture_name=gesture_name,
            capture_id=capture_id,
            image=image,
            confidence=1.0  # Manual assignment = 100% confident
        )
