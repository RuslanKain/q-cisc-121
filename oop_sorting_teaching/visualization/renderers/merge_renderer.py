"""
Merge Sort renderer.

Merge Sort visualization shows:
- Recursive splitting with depth levels (indentation/stacking)
- Merging operation with elements moving back together
- Stability preservation
"""

from typing import List

from .base import StepRenderer
from ...models import GestureImage, Step, StepType


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
        
        elif step.type == StepType.MOVE:
            # Element being placed
            for idx in step.indices:
                highlights[idx] = "insert"
        
        elif step.type == StepType.COMPARE:
            for idx in step.indices:
                highlights[idx] = "compare"
        
        elif step.type == StepType.MARK_SORTED:
            for idx in step.indices:
                highlights[idx] = "sorted"
        
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
