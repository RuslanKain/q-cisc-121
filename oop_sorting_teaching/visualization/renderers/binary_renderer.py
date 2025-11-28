"""
Binary Search renderer.

Binary Search visualization shows:
- Current search range (blue brackets)
- Mid point being checked (orange)
- Narrowing of search range
- Found/Not Found final state
"""

from typing import List

from .base import StepRenderer
from ...models import GestureImage, Step, StepType


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
