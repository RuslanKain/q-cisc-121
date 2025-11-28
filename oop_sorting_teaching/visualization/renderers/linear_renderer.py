"""
Linear Search renderer.

Linear Search visualization shows:
- Sequential checking of each element
- Current element being compared
- Found/Not Found final state
"""

from typing import List

from .base import StepRenderer
from ...models import GestureImage, Step, StepType


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
        
        if step.type == StepType.SEARCH_RANGE:
            # Show all elements in search range
            for idx in step.indices:
                highlights[idx] = "search_range"
        
        elif step.type == StepType.COMPARE:
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
