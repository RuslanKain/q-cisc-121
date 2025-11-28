"""
Bubble Sort renderer.

Bubble Sort visualization shows:
- Two adjacent elements being compared (yellow highlight)
- Swap operation (red arrows/highlight)
- Sorted portion growing from the right (green)
- Early exit detection
"""

from typing import List

from .base import StepRenderer
from ...models import GestureImage, Step, StepType


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
        
        elif step.type == StepType.SWAP:
            # Highlight swapped elements in red
            for idx in step.indices:
                highlights[idx] = "swap"
        
        elif step.type == StepType.PASS_COMPLETE:
            # Mark the newly sorted element
            if step.indices:
                highlights[step.indices[0]] = "sorted"
        
        elif step.type == StepType.MARK_SORTED:
            # Mark element in final position
            for idx in step.indices:
                highlights[idx] = "sorted"
        
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
                {step.description}
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
