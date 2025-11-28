"""
Quick Sort renderer.

Quick Sort visualization shows:
- Pivot selection (special highlight)
- Partition regions (left/right of pivot)
- Element movements during partitioning
- Instability when duplicates are reordered
"""

from typing import List

from .base import StepRenderer
from ...models import GestureImage, Step, StepType


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
        
        elif step.type == StepType.MOVE:
            for idx in step.indices:
                highlights[idx] = "insert"
        
        elif step.type == StepType.MARK_SORTED:
            for idx in step.indices:
                highlights[idx] = "sorted"
        
        elif step.type == StepType.INSTABILITY_WARNING:
            # Red warning for stability violation
            for idx in step.indices:
                highlights[idx] = "swap"
        
        elif step.type == StepType.COMPLETE:
            for i in range(len(images)):
                highlights[i] = "sorted"
        
        # Depth color (Queen's red shades)
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
