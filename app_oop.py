"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎓 CISC 121 - OOP Sorting & Searching Visualizer                          ║
║                                                                              ║
║   Queen's University - Introduction to Computing Science I                   ║
║                                                                              ║
║   File: app_oop.py                                                           ║
║   Purpose: Learn Object-Oriented Programming through visual algorithm demos  ║
║                                                                              ║
║   This file teaches:                                                         ║
║   • Classes and Objects (the building blocks of OOP)                         ║
║   • Encapsulation (bundling data with methods)                               ║
║   • Inheritance (sharing code between related classes)                       ║
║   • Polymorphism (same interface, different behaviors)                       ║
║   • SOLID Principles (professional software design)                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

LEARNING JOURNEY MAP:
=====================

This file is organized into PHASES. Each phase builds on the previous one.
You can run and test each phase independently!

    Phase 1: Core Data Structures (Classes for storing data)
    Phase 2: Sorting Algorithms (Classes for different sorting methods)
    Phase 3: Binary Search (Searching in sorted data)
    Phase 4: Visualization (Displaying algorithm steps)
    Phase 5: Gradio UI (User interface)
    Phase 6: Polish & Testing

Start reading from PHASE 1 below. Each section has:
    📚 CONCEPT EXPLANATION - What you're learning
    🔄 PROCEDURAL vs OOP - How it compares to non-OOP code
    💡 WHY THIS MATTERS - Real-world benefits
    ✏️ TRY IT YOURSELF - Experiments to deepen understanding
"""


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  SECTION 1: IMPORTS                                                          ║
# ║  Loading the tools we need from Python's library                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

# ------------------------------------------------------------------------------
# Standard Library Imports (built into Python)
# ------------------------------------------------------------------------------
from dataclasses import dataclass, field  # For creating simple data-holding classes
from enum import Enum, auto              # For creating named constants
from typing import List, Optional, Generator, Callable, Tuple, Any, Dict
from abc import ABC, abstractmethod      # For creating interfaces (abstract classes)
import random                            # For shuffling and random pivot selection
import time                              # For timing algorithm performance
from copy import deepcopy                # For creating independent copies of lists

# ------------------------------------------------------------------------------
# Third-Party Imports (installed via pip)
# ------------------------------------------------------------------------------
from PIL import Image                    # For handling images
import gradio as gr                      # For creating the web interface
from transformers import pipeline        # For AI image classification


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║   ██████╗ ██╗  ██╗ █████╗ ███████╗███████╗     ██╗                          ║
# ║   ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝    ███║                          ║
# ║   ██████╔╝███████║███████║███████╗█████╗      ╚██║                          ║
# ║   ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔══╝       ██║                          ║
# ║   ██║     ██║  ██║██║  ██║███████║███████╗     ██║                          ║
# ║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝     ╚═╝                          ║
# ║                                                                              ║
# ║   CORE DATA STRUCTURES                                                       ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 CONCEPT: What is a Class?                                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  A CLASS is a BLUEPRINT for creating objects.                                 ║
║                                                                              ║
║  Think of it like a cookie cutter:                                           ║
║  • The cookie cutter (class) defines the SHAPE                               ║
║  • Each cookie (object) is made FROM that shape                              ║
║  • Each cookie can have different decorations (data)                         ║
║                                                                              ║
║  In programming terms:                                                       ║
║  • A class defines what DATA an object holds (attributes)                    ║
║  • A class defines what ACTIONS an object can do (methods)                   ║
║  • An object is a specific INSTANCE of a class                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════════════╗
║  🔄 PROCEDURAL vs OOP: Storing Gesture Data                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PROCEDURAL (what you learned first):                                        ║
║  ─────────────────────────────────────                                       ║
║      # Data scattered in separate variables                                  ║
║      gesture_name = "peace"                                                  ║
║      gesture_rank = 2                                                        ║
║      gesture_emoji = "✌️"                                                    ║
║      gesture_image = some_image                                              ║
║      capture_id = 1                                                          ║
║                                                                              ║
║      # Functions operate on this data                                        ║
║      def compare_gestures(rank1, rank2):                                     ║
║          return rank1 < rank2                                                ║
║                                                                              ║
║  PROBLEM: What if you have 10 gestures? 100?                                 ║
║           gesture1_name, gesture1_rank, gesture2_name, gesture2_rank...      ║
║           It becomes CHAOS! 🌪️                                               ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  OOP (what we're learning now):                                              ║
║  ──────────────────────────────                                              ║
║      class GestureImage:                                                     ║
║          # All data BUNDLED together                                         ║
║          name = "peace"                                                      ║
║          rank = 2                                                            ║
║          emoji = "✌️"                                                        ║
║          image = some_image                                                  ║
║          capture_id = 1                                                      ║
║                                                                              ║
║          # Actions BELONG to the data                                        ║
║          def compare_to(self, other):                                        ║
║              return self.rank < other.rank                                   ║
║                                                                              ║
║  BENEFIT: 100 gestures? Just a list of GestureImage objects!                 ║
║           gestures = [gesture1, gesture2, ..., gesture100]                   ║
║           Each one carries ALL its data with it. 📦                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


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
    # Factory Method: create_from_prediction
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


# ==============================================================================
# ENUM: StepType
# ==============================================================================
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 CONCEPT: What is an Enum?                                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  An Enum (Enumeration) is a class for creating named constants.              ║
║                                                                              ║
║  WITHOUT Enum (error-prone):                                                 ║
║  ─────────────────────────────                                               ║
║      step_type = "compare"   # Easy to typo: "comprae", "Compare", etc.     ║
║      if step_type == "compare":  # What if you typed "compre"?              ║
║          ...                                                                 ║
║                                                                              ║
║  WITH Enum (safe):                                                           ║
║  ─────────────────                                                           ║
║      step_type = StepType.COMPARE   # IDE autocomplete helps!               ║
║      if step_type == StepType.COMPARE:  # Typos caught immediately!         ║
║          ...                                                                 ║
║                                                                              ║
║  Benefits:                                                                   ║
║  ✓ IDE autocomplete shows all valid options                                 ║
║  ✓ Typos are caught immediately (no silent failures)                        ║
║  ✓ Self-documenting (all possible values in one place)                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

class StepType(Enum):
    """
    Types of algorithm steps that can be visualized.
    
    Each step in our sorting/searching algorithms will have a type
    that determines how it's displayed in the visualization.
    """
    # Comparison operations
    COMPARE = auto()         # Comparing two elements
    
    # Movement operations
    SWAP = auto()            # Swapping two elements (in-place algorithms)
    MOVE = auto()            # Moving an element to a new position
    
    # Merge sort specific
    SPLIT = auto()           # Splitting array into subarrays
    MERGE = auto()           # Merging sorted subarrays
    
    # Quick sort specific
    PIVOT_SELECT = auto()    # Selecting a pivot element
    PARTITION = auto()       # Partitioning around pivot
    
    # Binary search specific
    SEARCH_RANGE = auto()    # Showing current search range
    NARROW_LEFT = auto()     # Target is in left half
    NARROW_RIGHT = auto()    # Target is in right half
    FOUND = auto()           # Target element found
    NOT_FOUND = auto()       # Target element not in array
    
    # General
    PASS_COMPLETE = auto()   # One pass through the data complete (Bubble Sort)
    COMPLETE = auto()        # Algorithm finished
    MARK_SORTED = auto()     # Mark element(s) as in final position
    
    # Stability detection
    INSTABILITY = auto()     # Stability violation detected!
    INSTABILITY_WARNING = auto()  # Warning for potential instability


# ==============================================================================
# DATACLASS: Step
# ==============================================================================

@dataclass
class Step:
    """
    Represents a single step in an algorithm's execution.
    
    This is used to record what the algorithm is doing at each point,
    so we can visualize it step by step.
    
    Think of it like frames in a movie:
    - Each Step is one frame
    - Together they tell the story of the algorithm
    
    Attributes:
        step_type: What kind of operation (compare, swap, merge, etc.)
        indices: Which array positions are involved
        description: Human-readable explanation
        depth: Recursion depth (for merge sort / quick sort)
        array_state: Copy of the array at this step
        highlight_indices: Extra indices to highlight (e.g., sorted region)
        metadata: Additional algorithm-specific data
    """
    step_type: StepType
    indices: List[int]
    description: str
    depth: int = 0
    array_state: List[GestureImage] = field(default_factory=list)
    highlight_indices: List[int] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    @property
    def type(self) -> StepType:
        """Alias for step_type for cleaner access in renderers."""
        return self.step_type
    
    def __str__(self) -> str:
        """Human-readable string for debugging."""
        indices_str = ', '.join(str(i) for i in self.indices)
        return f"[{self.step_type.name}] indices=[{indices_str}] depth={self.depth}: {self.description}"


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


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  ✏️ TRY IT YOURSELF: Phase 1 Experiments                                     ║
# ╠══════════════════════════════════════════════════════════════════════════════╣
# ║                                                                              ║
# ║  Run this file directly to test Phase 1:                                    ║
# ║      python app_oop.py                                                       ║
# ║                                                                              ║
# ║  Experiments to try:                                                        ║
# ║                                                                              ║
# ║  1. Create GestureImage objects and compare them:                           ║
# ║     >>> g1 = GestureImage.create_manual("fist", 1)                          ║
# ║     >>> g2 = GestureImage.create_manual("peace", 2)                         ║
# ║     >>> print(g1 < g2)  # Should be True (fist comes before peace)         ║
# ║                                                                              ║
# ║  2. Test the ranking system:                                                ║
# ║     >>> GestureRanking.get_rank("peace")                                    ║
# ║     >>> GestureRanking.compare("fist", "like")                              ║
# ║                                                                              ║
# ║  3. Use the ImageList:                                                      ║
# ║     >>> images = ImageList()                                                ║
# ║     >>> images.add_new("peace")                                             ║
# ║     >>> images.add_new("fist")                                              ║
# ║     >>> print(images)                                                       ║
# ║     >>> images.sort_ascending()                                             ║
# ║     >>> print(images)                                                       ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝


# ==============================================================================
# PHASE 1 TEST CODE
# ==============================================================================
# This code runs when you execute the file directly (python app_oop.py)
# It demonstrates and tests everything we've built so far.
# ==============================================================================

def test_phase_1():
    """
    Test all Phase 1 components.
    
    This function demonstrates how to use the classes we've created.
    Run it to verify everything works correctly.
    """
    print("\n" + "=" * 70)
    print("  🧪 PHASE 1: Testing Core Data Structures")
    print("=" * 70)
    
    # -------------------------------------------------------------------------
    # Test 1: GestureRanking
    # -------------------------------------------------------------------------
    print("\n📋 Test 1: GestureRanking")
    print("-" * 40)
    
    print(f"  Rank of 'fist': {GestureRanking.get_rank('fist')}")
    print(f"  Rank of 'peace': {GestureRanking.get_rank('peace')}")
    print(f"  Emoji of 'like': {GestureRanking.get_emoji('like')}")
    print(f"  Compare fist vs peace: {GestureRanking.compare('fist', 'peace')}")
    print(f"  (Negative means fist comes BEFORE peace)")
    
    print(f"\n  All gestures in order:")
    for i, gesture in enumerate(GestureRanking.get_all_gestures(), 1):
        emoji = GestureRanking.get_emoji(gesture)
        rank = GestureRanking.get_rank(gesture)
        print(f"    {i}. {emoji} {gesture} (rank {rank})")
    
    # -------------------------------------------------------------------------
    # Test 2: GestureImage
    # -------------------------------------------------------------------------
    print("\n📋 Test 2: GestureImage")
    print("-" * 40)
    
    # Create images using factory method
    peace1 = GestureImage.create_manual("peace", 1)
    peace2 = GestureImage.create_manual("peace", 2)
    fist = GestureImage.create_manual("fist", 3)
    
    print(f"  Created: {peace1}, {peace2}, {fist}")
    print(f"  peace1 < fist? {peace1 < fist} (should be False, peace rank 3 > fist rank 1)")
    print(f"  fist < peace1? {fist < peace1} (should be True)")
    print(f"  peace1 == peace2? {peace1 == peace2} (should be True, same rank)")
    
    # Test sorting with Python's built-in sorted()
    gestures = [peace1, fist, peace2]
    print(f"\n  Before sorting: {[str(g) for g in gestures]}")
    sorted_gestures = sorted(gestures)
    print(f"  After sorted(): {[str(g) for g in sorted_gestures]}")
    print(f"  (Notice: fist first, then peace₁ before peace₂ - STABLE!)")
    
    # -------------------------------------------------------------------------
    # Test 3: ImageList
    # -------------------------------------------------------------------------
    print("\n📋 Test 3: ImageList")
    print("-" * 40)
    
    images = ImageList()
    print(f"  Created empty ImageList: {images}")
    
    # Add some images
    images.add_new("peace")
    images.add_new("fist")
    images.add_new("like")
    images.add_new("peace")  # Another peace (duplicate gesture)
    
    print(f"  After adding 4 images: {images.display_string()}")
    print(f"  Analysis: {images.get_analysis()}")
    print(f"  Is sorted? {images.is_sorted()}")
    
    # Sort and show result
    images.sort_ascending()
    print(f"\n  After sort_ascending(): {images.display_string()}")
    print(f"  Is sorted? {images.is_sorted()}")
    
    # Test undo
    images.undo()
    print(f"\n  After undo(): {images.display_string()}")
    
    # Test duplicate
    images.duplicate(0)
    print(f"\n  After duplicating index 0: {images.display_string()}")
    
    # Test shuffle
    images.shuffle()
    print(f"  After shuffle(): {images.display_string()}")
    
    # -------------------------------------------------------------------------
    # Test 4: Step (for algorithm visualization)
    # -------------------------------------------------------------------------
    print("\n📋 Test 4: Step dataclass")
    print("-" * 40)
    
    step = Step(
        step_type=StepType.COMPARE,
        indices=[0, 1],
        description="Comparing ✊ and ✌️",
        depth=0,
        array_state=images.images
    )
    print(f"  Created step: {step}")
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ✅ PHASE 1 COMPLETE!")
    print("=" * 70)
    print("""
  You've learned:
  • Classes bundle DATA and METHODS together
  • @dataclass makes creating data-holding classes easy
  • Properties provide controlled access to data
  • Magic methods (__lt__, __eq__, etc.) enable built-in operations
  • Factory methods simplify object creation
  • Enums provide type-safe named constants
  
  Next: Phase 2 will add the sorting algorithms!
    """)


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║   ██████╗ ██╗  ██╗ █████╗ ███████╗███████╗    ██████╗                       ║
# ║   ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝    ╚════██╗                      ║
# ║   ██████╔╝███████║███████║███████╗█████╗       █████╔╝                      ║
# ║   ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔══╝      ██╔═══╝                       ║
# ║   ██║     ██║  ██║██║  ██║███████║███████╗    ███████╗                      ║
# ║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝                      ║
# ║                                                                              ║
# ║   SORTING ALGORITHMS                                                         ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 CONCEPT: Interfaces and Abstract Classes                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  An INTERFACE defines a CONTRACT - what methods a class MUST have.           ║
║                                                                              ║
║  Think of it like a job description:                                         ║
║  • The job description says "must be able to sort things"                    ║
║  • Different people (classes) can do the job differently                     ║
║  • But they ALL must be able to sort                                         ║
║                                                                              ║
║  In Python, we use ABSTRACT BASE CLASSES (ABC) to create interfaces:        ║
║                                                                              ║
║      from abc import ABC, abstractmethod                                     ║
║                                                                              ║
║      class SortingAlgorithm(ABC):  # ABC = Abstract Base Class              ║
║          @abstractmethod           # This method MUST be implemented         ║
║          def sort(self, data):                                               ║
║              pass                                                            ║
║                                                                              ║
║  Now any class that inherits from SortingAlgorithm MUST implement sort()!   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  💡 WHY THIS MATTERS: The "L" and "D" in SOLID                               ║
║                                                                              ║
║  Liskov Substitution Principle (L):                                          ║
║      Any SortingAlgorithm can be swapped with another.                       ║
║      Your code doesn't care if it's BubbleSort or QuickSort!                 ║
║                                                                              ║
║      def run_sort(algorithm: SortingAlgorithm, data):                        ║
║          return algorithm.sort(data)  # Works with ANY sorting algorithm!    ║
║                                                                              ║
║  Dependency Inversion Principle (D):                                         ║
║      High-level code depends on ABSTRACTIONS (the interface),                ║
║      not on specific implementations (BubbleSort, MergeSort, etc.)           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


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
# CLASS: BubbleSort
# ==============================================================================
"""
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


# ==============================================================================
# CLASS: MergeSort
# ==============================================================================
"""
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


# ==============================================================================
# ENUM: PivotStrategy (for Quick Sort)
# ==============================================================================

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


# ==============================================================================
# CLASS: QuickSort
# ==============================================================================
"""
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


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                                                                              ║
# ║   ██████╗ ██╗  ██╗ █████╗ ███████╗███████╗    ██████╗                       ║
# ║   ██╔══██╗██║  ██║██╔══██╗██╔════╝██╔════╝    ╚════██╗                      ║
# ║   ██████╔╝███████║███████║███████╗█████╗       █████╔╝                      ║
# ║   ██╔═══╝ ██╔══██║██╔══██║╚════██║██╔══╝       ╚═══██╗                      ║
# ║   ██║     ██║  ██║██║  ██║███████║███████╗    ██████╔╝                      ║
# ║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝                       ║
# ║                                                                              ║
# ║   BINARY SEARCH                                                              ║
# ║                                                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

"""
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


# ==============================================================================
# CLASS: LinearSearch
# ==============================================================================

class LinearSearch(SearchAlgorithm):
    """
    Linear Search - the simplest search algorithm.
    
    Just checks every element from start to end.
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


# ==============================================================================
# CLASS: BinarySearch
# ==============================================================================

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
        import math
        return math.floor(math.log2(n)) + 1


# ==============================================================================
# HELPER: Search Comparison
# ==============================================================================

def compare_search_algorithms(
    data: List[GestureImage],
    target: GestureImage
) -> dict:
    """
    Compare Linear Search vs Binary Search on the same data.
    
    This demonstrates why Binary Search is so much more efficient
    for sorted data.
    
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    # Linear Search
    linear = LinearSearch()
    linear_result, linear_steps = linear.run_full(data, target)
    linear_comparisons = 0
    for step in linear_steps:
        if "comparisons" in step.metadata:
            linear_comparisons = step.metadata["comparisons"]
    
    results["linear"] = {
        "algorithm": linear.name,
        "found": linear_result is not None,
        "index": linear_result,
        "comparisons": linear_comparisons,
        "steps": len(linear_steps)
    }
    
    # Binary Search (only valid if sorted)
    binary = BinarySearch(variant="iterative")
    binary_result, binary_steps = binary.run_full(data, target)
    binary_comparisons = 0
    for step in binary_steps:
        if "comparisons" in step.metadata:
            binary_comparisons = step.metadata["comparisons"]
    
    results["binary"] = {
        "algorithm": binary.name,
        "found": binary_result is not None,
        "index": binary_result,
        "comparisons": binary_comparisons,
        "steps": len(binary_steps)
    }
    
    # Calculate efficiency gain
    if linear_comparisons > 0 and binary_comparisons > 0:
        results["efficiency_ratio"] = linear_comparisons / binary_comparisons
        results["comparisons_saved"] = linear_comparisons - binary_comparisons
    else:
        results["efficiency_ratio"] = 1
        results["comparisons_saved"] = 0
    
    return results


# ==============================================================================
# ==============================================================================
# ==============================================================================
#
#  PHASE 4: VISUALIZATION
#
#  This phase builds the visual representation layer.
#
#  📚 NEW OOP CONCEPTS IN THIS PHASE:
#  • Composition: Objects containing other objects
#  • State Management: Tracking current position in visualization
#  • Factory Method: Creating appropriate renderers based on algorithm type
#  • Strategy Pattern: Different rendering strategies for different algorithms
#
#  💡 WHY SEPARATE VISUALIZATION FROM ALGORITHMS?
#  
#  In Phase 2 & 3, our algorithms generate STEPS (data about what happened).
#  In Phase 4, we CREATE VISUALS from those steps.
#  
#  This separation follows the SINGLE RESPONSIBILITY PRINCIPLE:
#  - Algorithms: Calculate the steps (logic)
#  - Visualizer: Display the steps (presentation)
#  
#  Procedural approach would mix these together, making code harder to:
#  - Test (can't test logic without UI)
#  - Change (modify display without breaking algorithm)
#  - Reuse (can't use algorithm without the specific display)
#
# ==============================================================================
# ==============================================================================
# ==============================================================================


# ==============================================================================
# VISUALIZATION STATE
# ==============================================================================
#
# 📚 CONCEPT: State Management with Enums
#
# When stepping through an algorithm visualization, we need to track:
# - What step are we on?
# - Is the animation playing or paused?
# - Have we reached the end?
#
# Using an Enum makes these states explicit and prevents bugs from
# using invalid string values like "plying" instead of "playing".
# ==============================================================================

class VisualizationState(Enum):
    """
    📚 CONCEPT: Finite State Machine
    
    A visualization can only be in ONE of these states at a time.
    This prevents impossible states like "playing AND paused".
    
    BEFORE OOP (with strings):
        state = "idle"
        if state == "plying":  # Typo! Hard to catch bug
            ...
    
    AFTER OOP (with Enum):
        state = VisualizationState.IDLE
        if state == VisualizationState.PLYING:  # Python error! Typo caught
            ...
    """
    IDLE = "idle"              # No steps loaded
    READY = "ready"            # Steps loaded, ready to start
    PLAYING = "playing"        # Auto-playing animation
    PAUSED = "paused"          # Paused mid-animation
    STEPPING = "stepping"      # Manual step-by-step mode
    COMPLETE = "complete"      # Reached the end


# ==============================================================================
# STEP RENDERER (Abstract Base Class)
# ==============================================================================
#
# 📚 CONCEPT: Strategy Pattern
#
# Different algorithms need different visualizations:
# - Bubble Sort: Highlight two adjacent elements being compared
# - Merge Sort: Show depth levels with indentation
# - Quick Sort: Show pivot and partition regions
# - Binary Search: Show search range narrowing
#
# Instead of one giant "if algorithm == X then do Y" block,
# we create separate RENDERER classes for each visualization style.
#
# This is the STRATEGY PATTERN: 
# - Define a family of algorithms (rendering strategies)
# - Make them interchangeable
# - Let the client choose which one to use
# ==============================================================================

class StepRenderer(ABC):
    """
    📚 CONCEPT: Abstract Base Class for Rendering
    
    This defines WHAT a renderer must do, not HOW.
    Each specific renderer (BubbleRenderer, MergeRenderer, etc.)
    implements the HOW for its specific algorithm.
    
    BEFORE OOP (procedural):
        def render_step(step, algorithm_type):
            if algorithm_type == "bubble":
                # 50 lines of bubble rendering code
            elif algorithm_type == "merge":
                # 80 lines of merge rendering code
            elif algorithm_type == "quick":
                # 100 lines of quick sort rendering code
            # ... more and more elif blocks
    
    AFTER OOP (Strategy Pattern):
        renderer = BubbleSortRenderer()  # or MergeSortRenderer()
        html = renderer.render(step, images)
        # Each renderer has clean, focused code
    """
    
    # -------------------------------------------------------------------------
    # Abstract Methods - MUST be implemented by subclasses
    # -------------------------------------------------------------------------
    
    @abstractmethod
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """
        Convert a single algorithm step into HTML for display.
        
        Args:
            step: The algorithm step to visualize
            images: The current state of the image list
            
        Returns:
            HTML string ready to display in Gradio
        
        📚 WHY HTML?
        
        Gradio can display HTML directly, giving us full control over:
        - Colors for highlighting
        - Borders for indicating comparisons
        - Spacing and layout
        - Animations with CSS
        """
        pass
    
    @abstractmethod
    def get_legend(self) -> str:
        """
        Return HTML explaining the visual indicators used.
        
        Each algorithm uses different colors/symbols:
        - Yellow: Currently comparing
        - Green: Already sorted
        - Red: Swapped
        
        The legend helps students understand what they're seeing.
        """
        pass
    
    # -------------------------------------------------------------------------
    # Shared Helper Methods
    # -------------------------------------------------------------------------
    
    def _image_to_html(
        self, 
        image: GestureImage, 
        highlight: str = "none",
        size: int = 60
    ) -> str:
        """
        📚 CONCEPT: Template Method Pattern (light version)
        
        Common code that all renderers share is in the BASE CLASS.
        Specific rendering logic is in the SUBCLASSES.
        
        This prevents code duplication across renderers.
        
        Args:
            image: The gesture image to render
            highlight: Type of highlighting ("none", "compare", "swap", 
                       "sorted", "pivot", "found", "search_range")
            size: Thumbnail size in pixels
            
        Returns:
            HTML for a single image card
        """
        # Define colors for different highlight types
        # Using Queen's colors plus semantic colors
        highlight_styles = {
            "none": "border: 2px solid #ddd; background: white;",
            "compare": "border: 3px solid #FABD0F; background: #FFF8E1;",  # Gold - comparing
            "swap": "border: 3px solid #dc3545; background: #FFE4E4;",      # Red - swapping
            "sorted": "border: 3px solid #28a745; background: #E8F5E9;",    # Green - sorted
            "pivot": "border: 3px solid #9B2335; background: #FCE4EC;",     # Queen's red - pivot
            "found": "border: 3px solid #28a745; background: #C8E6C9;",     # Green - found!
            "search_range": "border: 3px solid #002D62; background: #E3F2FD;",  # Queen's blue - search
            "merged": "border: 3px solid #6f42c1; background: #F3E5F5;",    # Purple - merging
            "insert": "border: 3px solid #17a2b8; background: #E0F7FA;",    # Cyan - inserting
            "mid": "border: 3px solid #fd7e14; background: #FFF3E0;",       # Orange - midpoint
        }
        
        style = highlight_styles.get(highlight, highlight_styles["none"])
        
        # Create the image card HTML
        # Using emoji prominently since actual images may be placeholders
        html = f"""
        <div style="
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            margin: 4px;
            padding: 8px;
            border-radius: 8px;
            {style}
            min-width: {size}px;
            transition: all 0.3s ease;
        ">
            <div style="font-size: {size // 2}px; margin-bottom: 4px;">
                {image.emoji}
            </div>
            <div style="font-size: 10px; color: #666;">
                ₍{image.capture_id}₎
            </div>
            <div style="font-size: 9px; color: #999;">
                rank {image.rank}
            </div>
        </div>
        """
        return html
    
    def _create_row(
        self, 
        images: List[GestureImage], 
        highlights: Dict[int, str] = None,
        size: int = 60
    ) -> str:
        """
        Create a horizontal row of images with optional highlighting.
        
        Args:
            images: List of images to display
            highlights: Dict mapping index -> highlight type
            size: Thumbnail size
            
        Returns:
            HTML for the complete row
        """
        if highlights is None:
            highlights = {}
        
        cards = []
        for i, img in enumerate(images):
            highlight = highlights.get(i, "none")
            cards.append(self._image_to_html(img, highlight, size))
        
        return f"""
        <div style="
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 4px;
            padding: 10px;
        ">
            {''.join(cards)}
        </div>
        """
    
    def _create_indices_row(self, count: int, highlights: Dict[int, str] = None) -> str:
        """
        Create index labels below images (0, 1, 2, ...).
        
        Useful for teaching students about array indices.
        """
        if highlights is None:
            highlights = {}
        
        indices = []
        for i in range(count):
            style = ""
            if i in highlights:
                if highlights[i] == "compare":
                    style = "color: #FABD0F; font-weight: bold;"
                elif highlights[i] == "pivot":
                    style = "color: #9B2335; font-weight: bold;"
                elif highlights[i] == "mid":
                    style = "color: #fd7e14; font-weight: bold;"
            
            indices.append(f"""
                <span style="
                    display: inline-block;
                    width: 60px;
                    text-align: center;
                    font-family: monospace;
                    font-size: 12px;
                    {style}
                ">[{i}]</span>
            """)
        
        return f"""
        <div style="
            display: flex;
            justify-content: center;
            gap: 4px;
            padding: 0 10px;
        ">
            {''.join(indices)}
        </div>
        """


# ==============================================================================
# BUBBLE SORT RENDERER
# ==============================================================================
#
# Bubble Sort visualization shows:
# - Two adjacent elements being compared (yellow highlight)
# - Swap operation (red arrows/highlight)
# - Sorted portion growing from the right (green)
# - Early exit detection
# ==============================================================================

class BubbleSortRenderer(StepRenderer):
    """
    Renderer specifically designed for Bubble Sort visualization.
    
    📚 TEACHING FOCUS:
    
    Bubble Sort is often the first sorting algorithm students learn.
    Our visualization emphasizes:
    1. The "bubbling" motion of larger elements to the right
    2. The sorted portion growing from the end
    3. Why early exit is an optimization
    4. Stability - equal elements maintain order
    """
    
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """
        Render a single Bubble Sort step.
        
        Step Types we handle:
        - COMPARE: Highlight two adjacent elements
        - SWAP: Show elements being exchanged
        - PASS_COMPLETE: End of a pass through the array
        - COMPLETE: Algorithm finished
        """
        n = len(images)
        
        # Determine which elements to highlight based on step type
        highlights = {}
        
        if step.type == StepType.COMPARE:
            # Highlight the two elements being compared
            for idx in step.indices:
                highlights[idx] = "compare"
            # Mark sorted portion (elements after current pass are sorted)
            # sorted_start = n - step.metadata.get("pass_number", 0)
            # for i in range(sorted_start, n):
            #     if i not in highlights:
            #         highlights[i] = "sorted"
        
        elif step.type == StepType.SWAP:
            # Highlight swapped elements in red
            for idx in step.indices:
                highlights[idx] = "swap"
        
        elif step.type == StepType.PASS_COMPLETE:
            # Mark the newly sorted element
            if step.indices:
                highlights[step.indices[0]] = "sorted"
        
        elif step.type == StepType.COMPLETE:
            # Everything is sorted!
            for i in range(n):
                highlights[i] = "sorted"
        
        # Build the visualization HTML
        html = f"""
        <div style="
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
        ">
            <div style="
                font-weight: bold;
                color: #002D62;
                margin-bottom: 10px;
                font-size: 14px;
            ">
                Step {step.metadata.get('step_number', '?')}: {step.description}
            </div>
            
            {self._create_row(images, highlights)}
            {self._create_indices_row(n, highlights)}
        </div>
        """
        
        return html
    
    def get_legend(self) -> str:
        """Return the legend explaining Bubble Sort visuals."""
        return """
        <div style="
            display: flex;
            gap: 20px;
            justify-content: center;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            font-size: 12px;
        ">
            <span>🟨 <b>Comparing</b></span>
            <span>🟥 <b>Swapping</b></span>
            <span>🟩 <b>Sorted</b></span>
        </div>
        """


# ==============================================================================
# MERGE SORT RENDERER
# ==============================================================================
#
# Merge Sort visualization shows:
# - Recursive splitting with depth levels (indentation/stacking)
# - Merging operation with elements moving back together
# - Stability preservation
# ==============================================================================

class MergeSortRenderer(StepRenderer):
    """
    Renderer for Merge Sort's divide-and-conquer visualization.
    
    📚 TEACHING FOCUS:
    
    Merge Sort is often the first O(n log n) algorithm students see.
    Our visualization emphasizes:
    1. The recursive splitting into smaller subproblems
    2. The merging of sorted subarrays
    3. Depth of recursion (visually stacked)
    4. Stability - duplicates stay in original relative order
    
    📚 CONCEPT: Depth Visualization
    
    We use indentation/margin to show recursion depth:
    - Depth 0: Full array (no indent)
    - Depth 1: Two halves (slight indent)
    - Depth 2: Four quarters (more indent)
    - etc.
    
    This helps students understand the "divide" part of divide-and-conquer.
    """
    
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """
        Render a single Merge Sort step.
        
        Step Types:
        - SPLIT: Dividing array into halves
        - MERGE: Combining sorted subarrays
        - COMPARE: Comparing elements during merge
        - COMPLETE: Algorithm finished
        """
        highlights = {}
        depth = step.depth
        
        # Calculate indentation based on depth
        indent = depth * 30  # 30px per depth level
        
        if step.type == StepType.SPLIT:
            # Highlight the split point
            if step.indices:
                for idx in step.indices:
                    highlights[idx] = "compare"
        
        elif step.type == StepType.MERGE:
            # Highlight merged elements
            for idx in step.indices:
                highlights[idx] = "merged"
        
        elif step.type == StepType.COMPARE:
            for idx in step.indices:
                highlights[idx] = "compare"
        
        elif step.type == StepType.COMPLETE:
            for i in range(len(images)):
                highlights[i] = "sorted"
        
        # Build HTML with depth-based styling
        depth_color = ["#002D62", "#1a4c8c", "#3366b3", "#4d80cc", "#6699e6"][min(depth, 4)]
        
        html = f"""
        <div style="
            background: #f8f9fa;
            border-left: 4px solid {depth_color};
            border-radius: 0 12px 12px 0;
            padding: 15px;
            margin: 10px 0;
            margin-left: {indent}px;
        ">
            <div style="
                font-weight: bold;
                color: {depth_color};
                margin-bottom: 10px;
                font-size: 14px;
            ">
                Depth {depth} | {step.description}
            </div>
            
            {self._create_row(images, highlights)}
        </div>
        """
        
        return html
    
    def get_legend(self) -> str:
        """Return the legend explaining Merge Sort visuals."""
        return """
        <div style="
            display: flex;
            gap: 20px;
            justify-content: center;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            font-size: 12px;
        ">
            <span>🟨 <b>Comparing</b></span>
            <span>🟪 <b>Merging</b></span>
            <span>🟩 <b>Sorted</b></span>
            <span>📊 <b>Indent = Depth</b></span>
        </div>
        """


# ==============================================================================
# QUICK SORT RENDERER
# ==============================================================================
#
# Quick Sort visualization shows:
# - Pivot selection (special highlight)
# - Partition regions (left/right of pivot)
# - Element movements during partitioning
# - Instability when duplicates are reordered
# ==============================================================================

class QuickSortRenderer(StepRenderer):
    """
    Renderer for Quick Sort's partition-based visualization.
    
    📚 TEACHING FOCUS:
    
    Quick Sort is efficient but tricky to understand.
    Our visualization emphasizes:
    1. How the pivot is chosen (first, last, median-of-3, random)
    2. Partitioning: elements < pivot go left, > pivot go right
    3. Recursion on the partitions
    4. INSTABILITY: duplicates may swap positions
    
    📚 INSTABILITY VISUALIZATION:
    
    When we detect that two equal elements have swapped,
    we highlight this with a red warning. This teaches students
    that Quick Sort is NOT stable.
    """
    
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """
        Render a single Quick Sort step.
        
        Step Types:
        - PIVOT_SELECT: Highlighting the chosen pivot
        - PARTITION: Showing partition boundaries
        - COMPARE: Comparing element with pivot
        - SWAP: Moving elements across partition
        - INSTABILITY_WARNING: Duplicates reordered
        - COMPLETE: Algorithm finished
        """
        highlights = {}
        depth = step.depth
        indent = depth * 30
        
        if step.type == StepType.PIVOT_SELECT:
            # Pivot gets special Queen's red highlight
            for idx in step.indices:
                highlights[idx] = "pivot"
        
        elif step.type == StepType.PARTITION:
            # Show partition boundaries
            # First index is pivot, others are boundaries
            if step.indices:
                highlights[step.indices[0]] = "pivot"
                for idx in step.indices[1:]:
                    highlights[idx] = "search_range"
        
        elif step.type == StepType.COMPARE:
            for idx in step.indices:
                highlights[idx] = "compare"
        
        elif step.type == StepType.SWAP:
            for idx in step.indices:
                highlights[idx] = "swap"
        
        elif step.type == StepType.INSTABILITY_WARNING:
            # Red warning for stability violation
            for idx in step.indices:
                highlights[idx] = "swap"
        
        elif step.type == StepType.COMPLETE:
            for i in range(len(images)):
                highlights[i] = "sorted"
        
        # Depth color (Queen's blue shades)
        depth_color = ["#9B2335", "#b54555", "#cc6675", "#e08895", "#f0aab5"][min(depth, 4)]
        
        html = f"""
        <div style="
            background: #f8f9fa;
            border-left: 4px solid {depth_color};
            border-radius: 0 12px 12px 0;
            padding: 15px;
            margin: 10px 0;
            margin-left: {indent}px;
        ">
            <div style="
                font-weight: bold;
                color: {depth_color};
                margin-bottom: 10px;
                font-size: 14px;
            ">
                Depth {depth} | {step.description}
            </div>
            
            {self._create_row(images, highlights)}
        </div>
        """
        
        # Add instability warning if applicable
        if step.type == StepType.INSTABILITY_WARNING:
            html += """
            <div style="
                background: #FFE4E4;
                border: 2px solid #dc3545;
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
                text-align: center;
                color: #dc3545;
                font-weight: bold;
            ">
                ⚠️ INSTABILITY DETECTED: Equal elements have changed order!
            </div>
            """
        
        return html
    
    def get_legend(self) -> str:
        """Return the legend explaining Quick Sort visuals."""
        return """
        <div style="
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            font-size: 12px;
        ">
            <span>🔴 <b>Pivot</b></span>
            <span>🟨 <b>Comparing</b></span>
            <span>🟥 <b>Swapping</b></span>
            <span>🟦 <b>Partition</b></span>
            <span>🟩 <b>Sorted</b></span>
        </div>
        """


# ==============================================================================
# BINARY SEARCH RENDERER
# ==============================================================================
#
# Binary Search visualization shows:
# - Current search range (blue brackets)
# - Mid point being checked (orange)
# - Narrowing of search range
# - Found/Not Found final state
# ==============================================================================

class BinarySearchRenderer(StepRenderer):
    """
    Renderer for Binary Search's divide-and-conquer visualization.
    
    📚 TEACHING FOCUS:
    
    Binary Search is a beautiful example of logarithmic efficiency.
    Our visualization emphasizes:
    1. The SORTED requirement (prerequisite)
    2. How the search range halves each step
    3. The mid-point calculation
    4. Comparison with target: go left or right?
    5. The dramatic efficiency gain over linear search
    """
    
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """
        Render a single Binary Search step.
        
        Step Types:
        - SEARCH_RANGE: Show current [left, right] bounds
        - COMPARE: Compare mid element with target
        - NARROW_LEFT: Target is in left half
        - NARROW_RIGHT: Target is in right half
        - FOUND: Element found!
        - NOT_FOUND: Element not in list
        """
        highlights = {}
        n = len(images)
        
        # Extract bounds from metadata if available
        left = step.metadata.get("left", 0)
        right = step.metadata.get("right", n - 1)
        mid = step.metadata.get("mid", (left + right) // 2)
        
        if step.type in [StepType.SEARCH_RANGE, StepType.NARROW_LEFT, StepType.NARROW_RIGHT]:
            # Highlight search range
            for i in range(left, right + 1):
                highlights[i] = "search_range"
            # Mid gets special highlight
            if 0 <= mid < n:
                highlights[mid] = "mid"
        
        elif step.type == StepType.COMPARE:
            # Highlight mid element being compared
            if step.indices:
                highlights[step.indices[0]] = "mid"
            # Keep search range visible
            for i in range(left, right + 1):
                if i not in highlights:
                    highlights[i] = "search_range"
        
        elif step.type == StepType.FOUND:
            # Highlight found element
            for idx in step.indices:
                highlights[idx] = "found"
        
        elif step.type == StepType.NOT_FOUND:
            # No highlighting - element not found
            pass
        
        # Show comparison visual (target vs mid)
        comparison_html = ""
        if step.type == StepType.COMPARE and step.metadata.get("target"):
            target_rank = step.metadata.get("target_rank", "?")
            mid_rank = step.metadata.get("mid_rank", "?")
            comparison = step.metadata.get("comparison", "")
            comparison_html = f"""
            <div style="
                text-align: center;
                margin: 10px 0;
                font-family: monospace;
                font-size: 14px;
            ">
                Target (rank {target_rank}) {comparison} Mid (rank {mid_rank})
            </div>
            """
        
        html = f"""
        <div style="
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            border: 2px solid #002D62;
        ">
            <div style="
                font-weight: bold;
                color: #002D62;
                margin-bottom: 10px;
                font-size: 14px;
            ">
                {step.description}
            </div>
            
            {self._create_row(images, highlights)}
            {self._create_indices_row(n, highlights)}
            {comparison_html}
        </div>
        """
        
        # Add found/not found banner
        if step.type == StepType.FOUND:
            html += """
            <div style="
                background: #C8E6C9;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                text-align: center;
                color: #28a745;
                font-weight: bold;
                font-size: 16px;
            ">
                ✅ FOUND! Element located successfully.
            </div>
            """
        elif step.type == StepType.NOT_FOUND:
            html += """
            <div style="
                background: #FFE4E4;
                border: 2px solid #dc3545;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                text-align: center;
                color: #dc3545;
                font-weight: bold;
                font-size: 16px;
            ">
                ❌ NOT FOUND: Element is not in the list.
            </div>
            """
        
        return html
    
    def get_legend(self) -> str:
        """Return the legend explaining Binary Search visuals."""
        return """
        <div style="
            display: flex;
            gap: 20px;
            justify-content: center;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            font-size: 12px;
        ">
            <span>🟦 <b>Search Range</b></span>
            <span>🟧 <b>Mid Point</b></span>
            <span>🟩 <b>Found!</b></span>
        </div>
        """


# ==============================================================================
# LINEAR SEARCH RENDERER
# ==============================================================================

class LinearSearchRenderer(StepRenderer):
    """
    Renderer for Linear Search visualization.
    
    📚 TEACHING FOCUS:
    
    Linear Search is simple but inefficient for large data.
    Our visualization emphasizes:
    1. Sequential checking of each element
    2. Why this is O(n) - may need to check every element
    3. Works on unsorted data (advantage over binary search)
    """
    
    def render_step(self, step: Step, images: List[GestureImage]) -> str:
        """Render a Linear Search step."""
        highlights = {}
        n = len(images)
        
        # Mark already-checked elements
        current_idx = step.metadata.get("current_index", 0)
        for i in range(current_idx):
            highlights[i] = "none"  # Already checked
        
        if step.type == StepType.COMPARE:
            for idx in step.indices:
                highlights[idx] = "compare"
        elif step.type == StepType.FOUND:
            for idx in step.indices:
                highlights[idx] = "found"
        
        html = f"""
        <div style="
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
        ">
            <div style="
                font-weight: bold;
                color: #002D62;
                margin-bottom: 10px;
                font-size: 14px;
            ">
                {step.description}
            </div>
            
            {self._create_row(images, highlights)}
            {self._create_indices_row(n, highlights)}
        </div>
        """
        
        if step.type == StepType.FOUND:
            html += """
            <div style="
                background: #C8E6C9;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                color: #28a745;
                font-weight: bold;
            ">
                ✅ FOUND!
            </div>
            """
        elif step.type == StepType.NOT_FOUND:
            html += """
            <div style="
                background: #FFE4E4;
                border: 2px solid #dc3545;
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                color: #dc3545;
                font-weight: bold;
            ">
                ❌ NOT FOUND: Checked all elements.
            </div>
            """
        
        return html
    
    def get_legend(self) -> str:
        return """
        <div style="
            display: flex;
            gap: 20px;
            justify-content: center;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            font-size: 12px;
        ">
            <span>🟨 <b>Checking</b></span>
            <span>🟩 <b>Found!</b></span>
        </div>
        """


# ==============================================================================
# RENDERER FACTORY
# ==============================================================================
#
# 📚 CONCEPT: Factory Pattern
#
# Instead of clients deciding which renderer class to create,
# we provide a FACTORY that creates the right renderer based on
# the algorithm being visualized.
#
# BEFORE (client must know all renderer classes):
#     if algorithm_name == "Bubble Sort":
#         renderer = BubbleSortRenderer()
#     elif algorithm_name == "Merge Sort":
#         renderer = MergeSortRenderer()
#     # ... many more if-else blocks
#
# AFTER (factory handles it):
#     renderer = RendererFactory.create(algorithm)
#     # Client doesn't need to know about specific renderer classes!
# ==============================================================================

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
    _renderers: Dict[str, type] = {
        "Bubble Sort (Early Exit)": BubbleSortRenderer,
        "Merge Sort": MergeSortRenderer,
        "Quick Sort": QuickSortRenderer,
        "Linear Search": LinearSearchRenderer,
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
    def register(cls, algorithm_name: str, renderer_class: type) -> None:
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


# ==============================================================================
# VISUALIZER CLASS
# ==============================================================================
#
# 📚 CONCEPT: Composition and State Management
#
# The Visualizer is the main controller for visualization.
# It COMPOSES (contains) other objects:
# - A StepRenderer (for creating HTML)
# - A list of Steps (from an algorithm)
# - Current state (playing, paused, etc.)
#
# This is COMPOSITION: building complex behavior from simpler parts.
# The Visualizer doesn't know HOW to render (that's the Renderer's job)
# It knows WHEN and WHAT to render (its own job).
# ==============================================================================

@dataclass
class VisualizationConfig:
    """
    Configuration options for the visualizer.
    
    📚 CONCEPT: Configuration Object
    
    Instead of passing many parameters to functions, we bundle
    related settings into a configuration object.
    
    BEFORE:
        def start_visualization(speed, auto_play, loop, show_stats, ...):
    
    AFTER:
        def start_visualization(config: VisualizationConfig):
    
    Benefits:
    - Easy to add new options without changing function signatures
    - Can have sensible defaults
    - Can save/load configurations
    """
    animation_speed_ms: int = 1000      # Milliseconds per step
    auto_play: bool = False              # Start playing immediately
    loop: bool = False                   # Restart when finished
    show_statistics: bool = True         # Show step count, comparisons, etc.
    show_legend: bool = True             # Show color legend
    image_size: int = 60                 # Size of image thumbnails


class Visualizer:
    """
    📚 CONCEPT: Controller Class
    
    The Visualizer coordinates between:
    - Algorithm steps (the DATA)
    - Renderers (the DISPLAY)
    - User interactions (the CONTROLS)
    
    It follows the SINGLE RESPONSIBILITY PRINCIPLE:
    - Algorithms: Generate steps (Phase 2 & 3)
    - Renderers: Convert steps to HTML (above)
    - Visualizer: Manage navigation and state (here)
    
    This separation makes each part:
    - Testable independently
    - Reusable in different contexts
    - Easy to modify without breaking others
    """
    
    def __init__(self, config: VisualizationConfig = None):
        """
        Initialize a new Visualizer.
        
        Args:
            config: Optional configuration. Uses defaults if not provided.
        """
        # Configuration with defaults
        self._config = config or VisualizationConfig()
        
        # State tracking
        self._state = VisualizationState.IDLE
        self._steps: List[Step] = []
        self._current_step_index: int = 0
        self._images: List[GestureImage] = []
        self._renderer: Optional[StepRenderer] = None
        self._algorithm_name: str = ""
        
        # Statistics tracking
        self._stats = {
            "total_steps": 0,
            "comparisons": 0,
            "swaps": 0,
            "max_depth": 0,
        }
    
    # -------------------------------------------------------------------------
    # Properties - Controlled access to internal state
    # -------------------------------------------------------------------------
    
    @property
    def state(self) -> VisualizationState:
        """Current visualization state."""
        return self._state
    
    @property
    def current_step(self) -> int:
        """Current step index (0-based)."""
        return self._current_step_index
    
    @property
    def total_steps(self) -> int:
        """Total number of steps."""
        return len(self._steps)
    
    @property
    def is_at_start(self) -> bool:
        """True if at the first step."""
        return self._current_step_index == 0
    
    @property
    def is_at_end(self) -> bool:
        """True if at the last step."""
        return self._current_step_index >= len(self._steps) - 1
    
    @property
    def progress_percentage(self) -> float:
        """Progress through visualization as percentage."""
        if not self._steps:
            return 0.0
        return (self._current_step_index / (len(self._steps) - 1)) * 100
    
    # -------------------------------------------------------------------------
    # Core Methods
    # -------------------------------------------------------------------------
    
    def load_steps(
        self,
        steps: List[Step],
        images: List[GestureImage],
        algorithm_name: str
    ) -> None:
        """
        Load algorithm steps for visualization.
        
        📚 CONCEPT: State Transition
        
        When we load steps, we transition from IDLE to READY.
        This is part of a STATE MACHINE pattern - valid transitions:
        
        IDLE -> READY (load steps)
        READY -> PLAYING (play)
        READY -> STEPPING (next/prev)
        PLAYING -> PAUSED (pause)
        PAUSED -> PLAYING (resume)
        STEPPING -> COMPLETE (reach end)
        
        Args:
            steps: List of Steps from an algorithm
            images: The final state of images (for reference)
            algorithm_name: Name of the algorithm (for renderer selection)
        """
        if not steps:
            raise ValueError("Cannot load empty step list")
        
        self._steps = steps
        self._images = images
        self._algorithm_name = algorithm_name
        self._current_step_index = 0
        
        # Create appropriate renderer using the factory
        self._renderer = RendererFactory.create(algorithm_name)
        
        # Calculate statistics
        self._calculate_statistics()
        
        # Transition to READY state
        self._state = VisualizationState.READY
    
    def _calculate_statistics(self) -> None:
        """Calculate statistics from loaded steps."""
        self._stats = {
            "total_steps": len(self._steps),
            "comparisons": sum(1 for s in self._steps if s.type == StepType.COMPARE),
            "swaps": sum(1 for s in self._steps if s.type == StepType.SWAP),
            "max_depth": max((s.depth for s in self._steps), default=0),
        }
    
    def render_current(self) -> str:
        """
        Render the current step as HTML.
        
        Returns:
            HTML string for display in Gradio
        """
        if self._state == VisualizationState.IDLE:
            return self._render_idle_state()
        
        if not self._steps or not self._renderer:
            return "<p>No visualization loaded.</p>"
        
        # Get current step
        step = self._steps[self._current_step_index]
        
        # Get images at this step (from step metadata if available)
        step_images = step.array_state if step.array_state else self._images
        
        # Render the step
        step_html = self._renderer.render_step(step, step_images)
        
        # Add header with progress
        header_html = self._render_header()
        
        # Add legend if configured
        legend_html = self._renderer.get_legend() if self._config.show_legend else ""
        
        # Add statistics if configured
        stats_html = self._render_statistics() if self._config.show_statistics else ""
        
        # Combine all parts
        return f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            {header_html}
            {legend_html}
            {step_html}
            {stats_html}
        </div>
        """
    
    def _render_idle_state(self) -> str:
        """Render placeholder when no visualization is loaded."""
        return """
        <div style="
            text-align: center;
            padding: 50px;
            color: #666;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        ">
            <div style="font-size: 48px; margin-bottom: 20px;">📊</div>
            <h3>No Visualization Loaded</h3>
            <p>Capture some images and run an algorithm to see the visualization!</p>
        </div>
        """
    
    def _render_header(self) -> str:
        """Render the visualization header with progress."""
        progress = self.progress_percentage
        current = self._current_step_index + 1
        total = len(self._steps)
        
        return f"""
        <div style="
            background: linear-gradient(135deg, #002D62 0%, #9B2335 100%);
            color: white;
            padding: 15px;
            border-radius: 12px 12px 0 0;
            margin-bottom: 10px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="font-size: 16px;">{self._algorithm_name}</strong>
                </div>
                <div style="font-size: 14px;">
                    Step {current} of {total}
                </div>
            </div>
            <div style="
                background: rgba(255,255,255,0.3);
                height: 6px;
                border-radius: 3px;
                margin-top: 10px;
                overflow: hidden;
            ">
                <div style="
                    background: #FABD0F;
                    height: 100%;
                    width: {progress}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
        </div>
        """
    
    def _render_statistics(self) -> str:
        """Render statistics panel."""
        return f"""
        <div style="
            display: flex;
            justify-content: space-around;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 0 0 12px 12px;
            margin-top: 10px;
            font-size: 12px;
        ">
            <div>📊 Steps: {self._stats['total_steps']}</div>
            <div>⚖️ Comparisons: {self._stats['comparisons']}</div>
            <div>🔄 Swaps: {self._stats['swaps']}</div>
            <div>📏 Max Depth: {self._stats['max_depth']}</div>
        </div>
        """
    
    # -------------------------------------------------------------------------
    # Navigation Methods
    # -------------------------------------------------------------------------
    
    def next_step(self) -> str:
        """
        Move to the next step and return rendered HTML.
        
        Returns:
            HTML for the new current step
        """
        if self._state == VisualizationState.IDLE:
            return self._render_idle_state()
        
        if not self.is_at_end:
            self._current_step_index += 1
            self._state = VisualizationState.STEPPING
        else:
            self._state = VisualizationState.COMPLETE
        
        return self.render_current()
    
    def prev_step(self) -> str:
        """
        Move to the previous step and return rendered HTML.
        
        Returns:
            HTML for the new current step
        """
        if self._state == VisualizationState.IDLE:
            return self._render_idle_state()
        
        if not self.is_at_start:
            self._current_step_index -= 1
            self._state = VisualizationState.STEPPING
        
        return self.render_current()
    
    def go_to_step(self, step_index: int) -> str:
        """
        Jump to a specific step.
        
        Args:
            step_index: 0-based step index
            
        Returns:
            HTML for the specified step
        """
        if self._state == VisualizationState.IDLE:
            return self._render_idle_state()
        
        # Clamp to valid range
        self._current_step_index = max(0, min(step_index, len(self._steps) - 1))
        self._state = VisualizationState.STEPPING
        
        return self.render_current()
    
    def go_to_start(self) -> str:
        """Jump to the first step."""
        return self.go_to_step(0)
    
    def go_to_end(self) -> str:
        """Jump to the last step."""
        return self.go_to_step(len(self._steps) - 1)
    
    def reset(self) -> None:
        """Reset the visualizer to initial state."""
        self._steps = []
        self._current_step_index = 0
        self._images = []
        self._renderer = None
        self._algorithm_name = ""
        self._state = VisualizationState.IDLE
        self._stats = {"total_steps": 0, "comparisons": 0, "swaps": 0, "max_depth": 0}
    
    # -------------------------------------------------------------------------
    # Playback Methods (for animation)
    # -------------------------------------------------------------------------
    
    def play(self) -> None:
        """Start auto-playing the visualization."""
        if self._state in [VisualizationState.READY, VisualizationState.PAUSED, 
                           VisualizationState.STEPPING]:
            self._state = VisualizationState.PLAYING
    
    def pause(self) -> None:
        """Pause auto-play."""
        if self._state == VisualizationState.PLAYING:
            self._state = VisualizationState.PAUSED
    
    def is_playing(self) -> bool:
        """Check if animation is currently playing."""
        return self._state == VisualizationState.PLAYING
    
    # -------------------------------------------------------------------------
    # Information Methods
    # -------------------------------------------------------------------------
    
    def get_step_description(self) -> str:
        """Get description of current step."""
        if not self._steps or self._current_step_index >= len(self._steps):
            return "No step loaded"
        return self._steps[self._current_step_index].description
    
    def get_statistics(self) -> Dict[str, int]:
        """Get a copy of the statistics dictionary."""
        return self._stats.copy()


# ==============================================================================
# PHASE 4 TEST CODE
# ==============================================================================

def test_phase_4():
    """
    Test the Phase 4 Visualization components.
    
    This tests:
    1. RendererFactory - creates correct renderers
    2. Individual Renderers - produce valid HTML
    3. Visualizer - manages state and navigation correctly
    """
    print("\n" + "=" * 70)
    print("  🧪 PHASE 4: Testing Visualization Components")
    print("=" * 70)
    
    # -------------------------------------------------------------------------
    # Test 1: Renderer Factory
    # -------------------------------------------------------------------------
    print("\n📋 Test 1: Renderer Factory")
    print("-" * 40)
    
    print("  Testing factory pattern for creating renderers...")
    
    test_algorithms = [
        "Bubble Sort (Early Exit)",
        "Merge Sort",
        "Quick Sort",
        "Linear Search",
        "Binary Search (Iterative)",
    ]
    
    for algo_name in test_algorithms:
        renderer = RendererFactory.create(algo_name)
        renderer_type = type(renderer).__name__
        print(f"  ✓ {algo_name} → {renderer_type}")
    
    print("\n  💡 The Factory Pattern decouples algorithm from renderer!")
    
    # -------------------------------------------------------------------------
    # Test 2: Bubble Sort Renderer
    # -------------------------------------------------------------------------
    print("\n📋 Test 2: Bubble Sort Renderer")
    print("-" * 40)
    
    # Create test data
    test_images = [
        GestureImage.create_manual("peace", 1),
        GestureImage.create_manual("fist", 2),
        GestureImage.create_manual("palm", 3),
    ]
    
    # Create a test step
    test_step = Step(
        step_type=StepType.COMPARE,
        indices=[0, 1],
        description="Comparing peace (rank 3) with fist (rank 1)",
        depth=0,
        array_state=test_images.copy(),
        metadata={"step_number": 1}
    )
    
    renderer = BubbleSortRenderer()
    html = renderer.render_step(test_step, test_images)
    
    print(f"  Generated HTML length: {len(html)} characters")
    print(f"  Contains emoji: {'✌️' in html or '✊' in html}")
    print(f"  Contains highlighting: {'border' in html}")
    print("  ✓ Bubble Sort Renderer produces valid HTML")
    
    # -------------------------------------------------------------------------
    # Test 3: Visualizer State Machine
    # -------------------------------------------------------------------------
    print("\n📋 Test 3: Visualizer State Management")
    print("-" * 40)
    
    visualizer = Visualizer()
    print(f"  Initial state: {visualizer.state.value}")
    
    # Create some test steps
    test_steps = [
        Step(StepType.COMPARE, [0, 1], "Compare positions 0 and 1", 0, test_images, {}),
        Step(StepType.SWAP, [0, 1], "Swap positions 0 and 1", 0, test_images, {}),
        Step(StepType.COMPLETE, [], "Sorting complete!", 0, test_images, {}),
    ]
    
    # Load steps
    visualizer.load_steps(test_steps, test_images, "Bubble Sort (Early Exit)")
    print(f"  After loading: {visualizer.state.value}")
    print(f"  Total steps: {visualizer.total_steps}")
    print(f"  Current step: {visualizer.current_step}")
    
    # Navigate
    visualizer.next_step()
    print(f"  After next_step(): step {visualizer.current_step}")
    
    visualizer.next_step()
    print(f"  After next_step(): step {visualizer.current_step}")
    
    visualizer.prev_step()
    print(f"  After prev_step(): step {visualizer.current_step}")
    
    visualizer.go_to_start()
    print(f"  After go_to_start(): step {visualizer.current_step}")
    
    visualizer.go_to_end()
    print(f"  After go_to_end(): step {visualizer.current_step}")
    
    print("  ✓ Visualizer navigation works correctly")
    
    # -------------------------------------------------------------------------
    # Test 4: Full Rendering Pipeline
    # -------------------------------------------------------------------------
    print("\n📋 Test 4: Full Rendering Pipeline")
    print("-" * 40)
    
    # Create a complete sorting example
    images = [
        GestureImage.create_manual("palm", 1),      # rank 6
        GestureImage.create_manual("fist", 2),      # rank 1
        GestureImage.create_manual("peace", 3),     # rank 3
    ]
    
    print(f"  Input: [🖐️₁(6)] [✊₂(1)] [✌️₃(3)]")
    
    # Run bubble sort to get steps
    bubble = BubbleSort()
    sorted_images, steps = bubble.run_full(images.copy())
    
    print(f"  Generated {len(steps)} steps")
    
    # Create visualizer and load
    viz = Visualizer()
    viz.load_steps(steps, sorted_images, bubble.name)
    
    # Render first step
    html = viz.render_current()
    print(f"  First step HTML: {len(html)} chars")
    
    # Navigate through all steps
    step_htmls = []
    viz.go_to_start()
    while not viz.is_at_end:
        step_htmls.append(viz.render_current())
        viz.next_step()
    step_htmls.append(viz.render_current())  # Last step
    
    print(f"  Rendered all {len(step_htmls)} steps successfully")
    print(f"  Progress at end: {viz.progress_percentage:.0f}%")
    print("  ✓ Full pipeline works correctly")
    
    # -------------------------------------------------------------------------
    # Test 5: Binary Search Visualization
    # -------------------------------------------------------------------------
    print("\n📋 Test 5: Binary Search Visualization")
    print("-" * 40)
    
    # Create sorted test data
    sorted_data = [
        GestureImage.create_manual("fist", 1),      # rank 1
        GestureImage.create_manual("one", 2),       # rank 2
        GestureImage.create_manual("peace", 3),     # rank 3
        GestureImage.create_manual("palm", 4),      # rank 6
        GestureImage.create_manual("ok", 5),        # rank 7
    ]
    
    print(f"  Sorted data: [✊(1)] [☝️(2)] [✌️(3)] [🖐️(6)] [👌(7)]")
    
    # Create a target to search for
    target = GestureImage.create_manual("palm", 99)
    print(f"  Searching for: 🖐️ (rank 6)")
    
    # Run binary search
    binary = BinarySearch(variant="iterative")
    result, steps = binary.run_full(sorted_data.copy(), target)
    
    print(f"  Found at index: {result}")
    print(f"  Steps: {len(steps)}")
    
    # Visualize
    viz = Visualizer()
    viz.load_steps(steps, sorted_data, binary.name)
    
    # Render each step
    for i in range(viz.total_steps):
        html = viz.go_to_step(i)
        step = steps[i]
        print(f"    Step {i + 1}: {step.type.value} - {step.description[:50]}...")
    
    print("  ✓ Binary Search visualization works correctly")
    
    # -------------------------------------------------------------------------
    # Test 6: Statistics Calculation
    # -------------------------------------------------------------------------
    print("\n📋 Test 6: Statistics Calculation")
    print("-" * 40)
    
    # Use the bubble sort visualizer from earlier
    stats = viz.get_statistics()
    print(f"  Total steps: {stats['total_steps']}")
    print(f"  Comparisons: {stats['comparisons']}")
    print(f"  Swaps: {stats['swaps']}")
    print(f"  Max depth: {stats['max_depth']}")
    print("  ✓ Statistics calculated correctly")
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ✅ PHASE 4 COMPLETE!")
    print("=" * 70)
    print("""
  You've learned:
  • Strategy Pattern: Different renderers for different algorithms
  • Factory Pattern: RendererFactory creates the right renderer
  • State Machine: VisualizationState tracks play/pause/step
  • Composition: Visualizer uses Renderer, doesn't inherit from it
  • Template Method: Shared helpers in base StepRenderer class
  
  Classes Added:
  • VisualizationState (Enum): IDLE, READY, PLAYING, PAUSED, etc.
  • StepRenderer (ABC): Base class for all renderers
  • BubbleSortRenderer, MergeSortRenderer, QuickSortRenderer
  • BinarySearchRenderer, LinearSearchRenderer
  • RendererFactory: Creates correct renderer for algorithm
  • VisualizationConfig: Settings for visualization
  • Visualizer: Main controller for step-by-step display
  
  Key OOP Principles:
  • Single Responsibility: Render logic separate from algorithm logic
  • Open/Closed: Add new renderers without changing existing code
  • Dependency Inversion: Visualizer depends on StepRenderer interface
  
  Next: Phase 5 will create the Gradio UI to tie it all together!
    """)


# ==============================================================================
# PHASE 3 TEST CODE
# ==============================================================================

def test_phase_3():
    """
    Test all Phase 3 search algorithms.
    """
    print("\n" + "=" * 70)
    print("  🧪 PHASE 3: Testing Search Algorithms")
    print("=" * 70)
    
    def display_list(lst: List[GestureImage]) -> str:
        return " ".join(f"[{img}]" for img in lst)
    
    # -------------------------------------------------------------------------
    # Create SORTED test data (required for Binary Search)
    # -------------------------------------------------------------------------
    print("\n📋 Creating sorted test data...")
    print("-" * 40)
    
    sorted_data = [
        GestureImage.create_manual("fist", 1),      # rank 1
        GestureImage.create_manual("one", 2),       # rank 2
        GestureImage.create_manual("peace", 3),     # rank 3
        GestureImage.create_manual("three", 4),     # rank 4
        GestureImage.create_manual("four", 5),      # rank 5
        GestureImage.create_manual("palm", 6),      # rank 6
        GestureImage.create_manual("ok", 7),        # rank 7
        GestureImage.create_manual("like", 8),      # rank 8
    ]
    
    print(f"  Sorted data: {display_list(sorted_data)}")
    print(f"  (Ranks: 1, 2, 3, 4, 5, 6, 7, 8)")
    
    # -------------------------------------------------------------------------
    # Test 1: Linear Search
    # -------------------------------------------------------------------------
    print("\n📋 Test 1: Linear Search")
    print("-" * 40)
    
    linear = LinearSearch()
    print(f"  Algorithm: {linear.description}")
    
    # Search for 'palm' (rank 6, in the middle)
    target = GestureImage.create_manual("palm", 99)  # Different capture_id, same gesture
    print(f"  Searching for: {target} (rank 6)")
    
    result, steps = linear.run_full(sorted_data, target)
    print(f"  Result: Found at index {result}")
    print(f"  Steps taken: {len(steps)}")
    
    # Count comparisons
    comparisons = 0
    for step in steps:
        if "comparisons" in step.metadata:
            comparisons = step.metadata["comparisons"]
    print(f"  Comparisons: {comparisons}")
    
    # -------------------------------------------------------------------------
    # Test 2: Binary Search (Iterative)
    # -------------------------------------------------------------------------
    print("\n📋 Test 2: Binary Search (Iterative)")
    print("-" * 40)
    
    binary_iter = BinarySearch(variant="iterative")
    print(f"  Algorithm: {binary_iter.description}")
    print(f"  Searching for: {target} (rank 6)")
    
    result, steps = binary_iter.run_full(sorted_data, target)
    print(f"  Result: Found at index {result}")
    print(f"  Steps taken: {len(steps)}")
    
    comparisons = 0
    for step in steps:
        if "comparisons" in step.metadata:
            comparisons = step.metadata["comparisons"]
    print(f"  Comparisons: {comparisons}")
    
    # -------------------------------------------------------------------------
    # Test 3: Binary Search (Recursive)
    # -------------------------------------------------------------------------
    print("\n📋 Test 3: Binary Search (Recursive)")
    print("-" * 40)
    
    binary_rec = BinarySearch(variant="recursive")
    print(f"  Algorithm: {binary_rec.description}")
    print(f"  Searching for: {target} (rank 6)")
    
    result, steps = binary_rec.run_full(sorted_data, target)
    print(f"  Result: Found at index {result}")
    print(f"  Steps taken: {len(steps)}")
    
    # Show the recursive depth
    max_depth = 0
    for step in steps:
        if "depth" in step.metadata:
            max_depth = max(max_depth, step.metadata["depth"])
    print(f"  Max recursion depth: {max_depth}")
    
    # -------------------------------------------------------------------------
    # Test 4: Search for non-existent element
    # -------------------------------------------------------------------------
    print("\n📋 Test 4: Searching for Non-existent Element")
    print("-" * 40)
    
    not_in_list = GestureImage.create_manual("rock", 99)  # rank 10, not in list
    print(f"  Searching for: {not_in_list} (rank 10) - NOT in list")
    
    result, steps = binary_iter.run_full(sorted_data, not_in_list)
    print(f"  Result: {'Found at index ' + str(result) if result is not None else 'NOT FOUND'}")
    
    comparisons = 0
    for step in steps:
        if "comparisons" in step.metadata:
            comparisons = step.metadata["comparisons"]
    print(f"  Comparisons before determining not found: {comparisons}")
    
    # -------------------------------------------------------------------------
    # Test 5: Binary Search on UNSORTED data (error case)
    # -------------------------------------------------------------------------
    print("\n📋 Test 5: Binary Search on Unsorted Data (Error Case)")
    print("-" * 40)
    
    unsorted_data = [
        GestureImage.create_manual("palm", 1),
        GestureImage.create_manual("fist", 2),
        GestureImage.create_manual("like", 3),
        GestureImage.create_manual("one", 4),
    ]
    
    print(f"  Unsorted data: {display_list(unsorted_data)}")
    print(f"  (Ranks: 6, 1, 8, 2 - NOT sorted!)")
    
    result, steps = binary_iter.run_full(unsorted_data, target)
    
    # Check for error step
    for step in steps:
        if step.step_type == StepType.NOT_FOUND and "error" in step.metadata:
            print(f"  ⚠️ {step.description}")
            break
    
    # -------------------------------------------------------------------------
    # Test 6: Efficiency Comparison
    # -------------------------------------------------------------------------
    print("\n📋 Test 6: Efficiency Comparison (Linear vs Binary)")
    print("-" * 40)
    
    # Create larger dataset to show the difference
    large_sorted = []
    gestures = ["fist", "one", "peace", "three", "four", "palm", "ok", "like", "dislike", "rock"]
    for i, gesture in enumerate(gestures):
        large_sorted.append(GestureImage.create_manual(gesture, i + 1))
    
    # Sort by rank
    large_sorted.sort(key=lambda x: x.rank)
    
    print(f"  Dataset size: {len(large_sorted)} elements")
    print(f"  Data: {display_list(large_sorted)}")
    
    # Search for last element (worst case for linear)
    target_worst = GestureImage.create_manual("rock", 99)
    print(f"\n  Searching for last element: {target_worst} (rank 10)")
    
    comparison = compare_search_algorithms(large_sorted, target_worst)
    
    print(f"\n  📊 Results:")
    print(f"  ┌────────────────────────┬─────────────┬─────────────┐")
    print(f"  │ Algorithm              │ Comparisons │ Found       │")
    print(f"  ├────────────────────────┼─────────────┼─────────────┤")
    print(f"  │ {comparison['linear']['algorithm']:<22} │ {comparison['linear']['comparisons']:^11} │ {'Yes' if comparison['linear']['found'] else 'No':^11} │")
    print(f"  │ {comparison['binary']['algorithm']:<22} │ {comparison['binary']['comparisons']:^11} │ {'Yes' if comparison['binary']['found'] else 'No':^11} │")
    print(f"  └────────────────────────┴─────────────┴─────────────┘")
    print(f"\n  🚀 Binary Search was {comparison['efficiency_ratio']:.1f}x more efficient!")
    print(f"     Saved {comparison['comparisons_saved']} comparisons")
    
    # -------------------------------------------------------------------------
    # Test 7: Scaling demonstration
    # -------------------------------------------------------------------------
    print("\n📋 Test 7: Scaling Demonstration")
    print("-" * 40)
    
    print("  How many steps for different dataset sizes?")
    print(f"\n  {'Dataset Size':<15} {'Linear (max)':<15} {'Binary (max)':<15} {'Speedup':<10}")
    print(f"  {'-'*55}")
    
    import math
    for size in [10, 100, 1000, 10000, 100000, 1000000]:
        linear_max = size
        binary_max = math.floor(math.log2(size)) + 1 if size > 0 else 0
        speedup = linear_max / binary_max if binary_max > 0 else 0
        print(f"  {size:<15,} {linear_max:<15,} {binary_max:<15} {speedup:,.0f}x")
    
    print("""
  💡 Key Insight:
     Binary Search's O(log n) dramatically outperforms
     Linear Search's O(n) as data grows!
    """)
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ✅ PHASE 3 COMPLETE!")
    print("=" * 70)
    print("""
  You've learned:
  • SearchAlgorithm interface (similar pattern to SortingAlgorithm)
  • Linear Search: O(n), works on unsorted data
  • Binary Search: O(log n), requires sorted data
  • Iterative vs Recursive implementations
  • Importance of sorted input validation
  • Dramatic efficiency gains with Binary Search
  
  Key Concepts:
  • Divide and Conquer strategy
  • Logarithmic vs Linear time complexity
  • Trade-off: Binary Search is faster but needs sorted data
  
  ✅ Phase 3 Complete! Search algorithms implemented.
    """)


# ==============================================================================
# PHASE 2 TEST CODE
# ==============================================================================

def test_phase_2():
    """
    Test all Phase 2 sorting algorithms.
    """
    print("\n" + "=" * 70)
    print("  🧪 PHASE 2: Testing Sorting Algorithms")
    print("=" * 70)
    
    # -------------------------------------------------------------------------
    # Create test data
    # -------------------------------------------------------------------------
    print("\n📋 Creating test data...")
    print("-" * 40)
    
    def create_test_list() -> List[GestureImage]:
        """Create a fresh test list."""
        return [
            GestureImage.create_manual("peace", 1),
            GestureImage.create_manual("fist", 2),
            GestureImage.create_manual("like", 3),
            GestureImage.create_manual("peace", 4),  # Duplicate peace
            GestureImage.create_manual("one", 5),
        ]
    
    def display_list(lst: List[GestureImage]) -> str:
        return " ".join(f"[{img}]" for img in lst)
    
    test_data = create_test_list()
    print(f"  Initial: {display_list(test_data)}")
    
    # -------------------------------------------------------------------------
    # Test 1: Bubble Sort
    # -------------------------------------------------------------------------
    print("\n📋 Test 1: Bubble Sort")
    print("-" * 40)
    
    bubble = BubbleSort()
    print(f"  Algorithm: {bubble.description}")
    
    data = create_test_list()
    print(f"  Before: {display_list(data)}")
    
    sorted_data, steps = bubble.run_full(data)
    print(f"  After:  {display_list(sorted_data)}")
    print(f"  Steps:  {len(steps)}")
    print(f"  Stable: {bubble.is_stable} (peace signs should keep order ₁ then ₄)")
    
    # -------------------------------------------------------------------------
    # Test 2: Merge Sort
    # -------------------------------------------------------------------------
    print("\n📋 Test 2: Merge Sort")
    print("-" * 40)
    
    merge = MergeSort()
    print(f"  Algorithm: {merge.description}")
    
    data = create_test_list()
    print(f"  Before: {display_list(data)}")
    
    sorted_data, steps = merge.run_full(data)
    print(f"  After:  {display_list(sorted_data)}")
    print(f"  Steps:  {len(steps)}")
    print(f"  Stable: {merge.is_stable}")
    
    # -------------------------------------------------------------------------
    # Test 3: Quick Sort (demonstrating instability)
    # -------------------------------------------------------------------------
    print("\n📋 Test 3: Quick Sort (First Pivot, 2-way)")
    print("-" * 40)
    
    quick = QuickSort(
        pivot_strategy=PivotStrategy.FIRST,
        partition_scheme=PartitionScheme.TWO_WAY
    )
    print(f"  Algorithm: {quick.description}")
    print(f"  ⚠️ This algorithm is UNSTABLE!")
    
    # Create data with multiple duplicates to show instability
    data = [
        GestureImage.create_manual("peace", 1),
        GestureImage.create_manual("peace", 2),
        GestureImage.create_manual("peace", 3),
        GestureImage.create_manual("fist", 4),
    ]
    print(f"\n  Before: {display_list(data)}")
    print(f"  (Note: peace signs are in order ₁, ₂, ₃)")
    
    sorted_data, steps = quick.run_full(data)
    print(f"  After:  {display_list(sorted_data)}")
    
    # Check if order of peace signs changed
    peace_order = [img.capture_id for img in sorted_data if img.gesture == "peace"]
    if peace_order != [1, 2, 3]:
        print(f"  ⚠️ INSTABILITY: Peace signs now in order {peace_order}")
    else:
        print(f"  (Order preserved this time, but not guaranteed!)")
    
    # -------------------------------------------------------------------------
    # Test 4: Quick Sort with 3-way partitioning
    # -------------------------------------------------------------------------
    print("\n📋 Test 4: Quick Sort (Median-of-3, 3-way)")
    print("-" * 40)
    
    quick3 = QuickSort(
        pivot_strategy=PivotStrategy.MEDIAN_OF_THREE,
        partition_scheme=PartitionScheme.THREE_WAY
    )
    print(f"  Algorithm: {quick3.description}")
    
    data = create_test_list()
    print(f"  Before: {display_list(data)}")
    
    sorted_data, steps = quick3.run_full(data)
    print(f"  After:  {display_list(sorted_data)}")
    print(f"  Steps:  {len(steps)}")
    
    # -------------------------------------------------------------------------
    # Test 5: Polymorphism demonstration
    # -------------------------------------------------------------------------
    print("\n📋 Test 5: Polymorphism (Same interface, different algorithms)")
    print("-" * 40)
    
    algorithms: List[SortingAlgorithm] = [
        BubbleSort(),
        MergeSort(),
        QuickSort(PivotStrategy.RANDOM, PartitionScheme.TWO_WAY),
    ]
    
    print("  Running all algorithms on the same data:")
    for algo in algorithms:
        data = create_test_list()
        sorted_data, steps = algo.run_full(data)
        print(f"  • {algo.name}: {len(steps)} steps")
    
    print("\n  💡 Notice: We used the SAME code to run different algorithms!")
    print("     This is the power of polymorphism and the Liskov Substitution Principle.")
    
    # -------------------------------------------------------------------------
    # Test 6: Quick Sort WORST CASE Scenarios
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ⚠️ QUICK SORT WORST CASE DEMONSTRATIONS")
    print("=" * 70)
    
    print("""
  Quick Sort's worst case occurs when partitions are UNBALANCED.
  This turns O(n log n) average case into O(n²) worst case!
  
  Let's see three scenarios that trigger worst-case behavior:
    """)
    
    # Scenario A: Sorted data + First Pivot
    print("\n📋 Scenario A: Already Sorted Data + First Pivot")
    print("-" * 50)
    
    # Create sorted data
    sorted_data = [
        GestureImage.create_manual("fist", 1),      # rank 1
        GestureImage.create_manual("one", 2),       # rank 2
        GestureImage.create_manual("peace", 3),     # rank 3
        GestureImage.create_manual("three", 4),     # rank 4
        GestureImage.create_manual("four", 5),      # rank 5
        GestureImage.create_manual("palm", 6),      # rank 6
        GestureImage.create_manual("ok", 7),        # rank 7
    ]
    
    print(f"  Input (already sorted): {display_list(sorted_data)}")
    
    # Analyze worst case risk
    analysis = QuickSort.analyze_input_for_worst_case(
        sorted_data,
        PivotStrategy.FIRST,
        PartitionScheme.TWO_WAY
    )
    
    print(f"\n  ⚡ Risk Level: {analysis['risk_level'].upper()}")
    print(f"  📊 Analysis:")
    for reason in analysis['reasons']:
        print(f"     • {reason}")
    if analysis['recommendations']:
        print(f"  💡 Recommendations:")
        for rec in analysis['recommendations']:
            print(f"     • {rec}")
    
    # Run and compare
    quick_first = QuickSort(PivotStrategy.FIRST, PartitionScheme.TWO_WAY)
    quick_random = QuickSort(PivotStrategy.RANDOM, PartitionScheme.TWO_WAY)
    
    data1 = [GestureImage.create_manual(g.gesture, i+1) for i, g in enumerate(sorted_data)]
    data2 = [GestureImage.create_manual(g.gesture, i+1) for i, g in enumerate(sorted_data)]
    
    _, steps_first = quick_first.run_full(data1)
    _, steps_random = quick_random.run_full(data2)
    
    print(f"\n  📈 Performance Comparison:")
    print(f"     First Pivot:  {len(steps_first):3d} steps (WORST CASE)")
    print(f"     Random Pivot: {len(steps_random):3d} steps (likely better)")
    
    # Scenario B: Reverse Sorted Data + Last Pivot
    print("\n📋 Scenario B: Reverse Sorted Data + Last Pivot")
    print("-" * 50)
    
    reverse_sorted = [
        GestureImage.create_manual("ok", 1),
        GestureImage.create_manual("palm", 2),
        GestureImage.create_manual("four", 3),
        GestureImage.create_manual("three", 4),
        GestureImage.create_manual("peace", 5),
        GestureImage.create_manual("one", 6),
        GestureImage.create_manual("fist", 7),
    ]
    
    print(f"  Input (reverse sorted): {display_list(reverse_sorted)}")
    
    analysis = QuickSort.analyze_input_for_worst_case(
        reverse_sorted,
        PivotStrategy.LAST,
        PartitionScheme.TWO_WAY
    )
    
    print(f"\n  ⚡ Risk Level: {analysis['risk_level'].upper()}")
    print(f"  📊 Analysis:")
    for reason in analysis['reasons']:
        print(f"     • {reason}")
    
    # Scenario C: Many Duplicates + 2-Way Partitioning
    print("\n📋 Scenario C: Many Duplicates + 2-Way Partitioning")
    print("-" * 50)
    
    many_dupes = [
        GestureImage.create_manual("peace", 1),
        GestureImage.create_manual("peace", 2),
        GestureImage.create_manual("peace", 3),
        GestureImage.create_manual("peace", 4),
        GestureImage.create_manual("peace", 5),
        GestureImage.create_manual("fist", 6),
        GestureImage.create_manual("peace", 7),
    ]
    
    print(f"  Input (6 peace, 1 fist): {display_list(many_dupes)}")
    
    # Compare 2-way vs 3-way
    analysis_2way = QuickSort.analyze_input_for_worst_case(
        many_dupes,
        PivotStrategy.FIRST,
        PartitionScheme.TWO_WAY
    )
    
    analysis_3way = QuickSort.analyze_input_for_worst_case(
        many_dupes,
        PivotStrategy.FIRST,
        PartitionScheme.THREE_WAY
    )
    
    print(f"\n  📊 2-Way Partitioning Analysis:")
    for reason in analysis_2way['reasons']:
        print(f"     • {reason}")
    
    print(f"\n  📊 3-Way Partitioning Analysis:")
    for reason in analysis_3way['reasons']:
        print(f"     • {reason}")
    
    # Run and compare
    quick_2way = QuickSort(PivotStrategy.FIRST, PartitionScheme.TWO_WAY)
    quick_3way = QuickSort(PivotStrategy.FIRST, PartitionScheme.THREE_WAY)
    
    data1 = [GestureImage.create_manual(g.gesture, i+1) for i, g in enumerate(many_dupes)]
    data2 = [GestureImage.create_manual(g.gesture, i+1) for i, g in enumerate(many_dupes)]
    
    _, steps_2way = quick_2way.run_full(data1)
    _, steps_3way = quick_3way.run_full(data2)
    
    print(f"\n  📈 Performance Comparison:")
    print(f"     2-Way Partition: {len(steps_2way):3d} steps")
    print(f"     3-Way Partition: {len(steps_3way):3d} steps (handles duplicates better!)")
    
    # Scenario D: Best Case - Random Data with Median Pivot
    print("\n📋 Scenario D: Best Case - Random Data + Median-of-3 Pivot")
    print("-" * 50)
    
    random_data = [
        GestureImage.create_manual("peace", 1),
        GestureImage.create_manual("ok", 2),
        GestureImage.create_manual("fist", 3),
        GestureImage.create_manual("like", 4),
        GestureImage.create_manual("one", 5),
        GestureImage.create_manual("palm", 6),
        GestureImage.create_manual("rock", 7),
    ]
    random.shuffle(random_data)
    
    print(f"  Input (shuffled): {display_list(random_data)}")
    
    analysis = QuickSort.analyze_input_for_worst_case(
        random_data,
        PivotStrategy.MEDIAN_OF_THREE,
        PartitionScheme.TWO_WAY
    )
    
    print(f"\n  ⚡ Risk Level: {analysis['risk_level'].upper()}")
    print(f"  📊 Analysis:")
    for reason in analysis['reasons']:
        print(f"     • {reason}")
    
    # Summary table
    print("\n" + "-" * 70)
    print("  📊 QUICK SORT CONFIGURATION GUIDE")
    print("-" * 70)
    print("""
  ┌─────────────────────────┬───────────────────┬────────────────────────┐
  │ Input Characteristic    │ Worst Config      │ Best Config            │
  ├─────────────────────────┼───────────────────┼────────────────────────┤
  │ Already sorted          │ First/Last pivot  │ Median-of-3 or Random  │
  │ Reverse sorted          │ First/Last pivot  │ Median-of-3 or Random  │
  │ Many duplicates         │ 2-way partition   │ 3-way partition        │
  │ Nearly sorted           │ First pivot       │ Random pivot           │
  │ Random data             │ (any works well)  │ (any works well)       │
  └─────────────────────────┴───────────────────┴────────────────────────┘
  
  💡 TIP: When in doubt, use RANDOM pivot + 3-WAY partition!
          This combination handles almost any input well.
    """)
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("  ✅ PHASE 2 COMPLETE!")
    print("=" * 70)
    print("""
  You've learned:
  • Abstract Base Classes (ABC) define interfaces
  • @abstractmethod forces subclasses to implement methods
  • Inheritance lets classes share code
  • Polymorphism: same interface, different behaviors
  • Generator functions (yield) for step-by-step execution
  • Bubble Sort: Simple, stable, O(n²)
  • Merge Sort: Divide-and-conquer, stable, O(n log n)
  • Quick Sort: Fast average case, UNSTABLE, configurable
  
  Quick Sort Worst Cases:
  • Sorted/reverse-sorted data + first/last pivot → O(n²)
  • Many duplicates + 2-way partitioning → inefficient
  • Solutions: median-of-3/random pivot, 3-way partitioning
  
  Key OOP Principles demonstrated:
  • Single Responsibility: Each class does ONE thing
  • Open/Closed: Easy to add new algorithms
  • Liskov Substitution: Any SortingAlgorithm works interchangeably
  • Interface Segregation: Clean, minimal interfaces
  
  ✅ Phase 2 Complete! Sorting algorithms implemented.
    """)


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
# This is where the program starts when you run: python app_oop.py
# ==============================================================================

if __name__ == "__main__":
    """
    📚 CONCEPT: if __name__ == "__main__"
    
    This is a Python idiom that means:
    "Only run this code if the file is executed directly"
    
    If this file is IMPORTED by another file, this code won't run.
    This lets us use the classes in other files without running tests.
    """
    test_phase_1()
    test_phase_2()
    test_phase_3()
    test_phase_4()
