"""
Abstract base class for step renderers.

📚 CONCEPT: Strategy Pattern

Different algorithms need different visualizations:
- Bubble Sort: Highlight two adjacent elements being compared
- Merge Sort: Show depth levels with indentation
- Quick Sort: Show pivot and partition regions
- Binary Search: Show search range narrowing

The StepRenderer ABC defines the interface that all renderers must follow.
"""

from abc import ABC, abstractmethod
from typing import List, Dict

from ...models import GestureImage, Step


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
