"""
Main Visualizer class for controlling algorithm visualization.

📚 CONCEPT: Composition and State Management

The Visualizer is the main controller for visualization.
It COMPOSES (contains) other objects:
- A StepRenderer (for creating HTML)
- A list of Steps (from an algorithm)
- Current state (playing, paused, etc.)

This is COMPOSITION: building complex behavior from simpler parts.
The Visualizer doesn't know HOW to render (that's the Renderer's job)
It knows WHEN and WHAT to render (its own job).
"""

from typing import List, Optional

from .state import VisualizationState, VisualizationConfig
from .factory import RendererFactory
from .renderers import StepRenderer
from ..models import GestureImage, Step, StepType


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
        """Pause the visualization."""
        if self._state == VisualizationState.PLAYING:
            self._state = VisualizationState.PAUSED
    
    def is_playing(self) -> bool:
        """Check if visualization is currently playing."""
        return self._state == VisualizationState.PLAYING
