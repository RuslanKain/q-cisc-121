"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🎓 CISC 121 - OOP Sorting & Searching Visualizer                          ║
║                                                                              ║
║   Queen's University - Introduction to Computing Science I                   ║
║                                                                              ║
║   This application demonstrates Object-Oriented Programming concepts        ║
║   through interactive visualization of sorting and searching algorithms.     ║
║                                                                              ║
║   HOW TO RUN: python app_oop_gradio.py                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

📚 PHASE 5: Gradio UI

This is the final phase - creating a user-friendly web interface that:
1. Allows capturing/uploading gesture images
2. Displays the image list with gesture recognition
3. Lets users run sorting/searching algorithms
4. Visualizes each step of the algorithm

The UI demonstrates COMPOSITION - the GradioApp class composes:
- ImageList (data management)
- SortingAlgorithm / SearchAlgorithm (algorithm execution)
- Visualizer (step-by-step display)
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import gradio as gr
from PIL import Image
import os
from typing import List, Tuple, Optional

# Import our OOP package
from oop_sorting_teaching import (
    # Models
    GestureRanking,
    GestureImage,
    ImageList,
    StepType,
    Step,
    # Sorting
    BubbleSort,
    MergeSort,
    QuickSort,
    PivotStrategy,
    PartitionScheme,
    # Searching
    LinearSearch,
    BinarySearch,
    # Visualization
    Visualizer,
    VisualizationConfig,
    RendererFactory,
)

# Try to import transformers for gesture recognition
try:
    from transformers import pipeline
    CLASSIFIER_AVAILABLE = True
except ImportError:
    CLASSIFIER_AVAILABLE = False
    print("⚠️ transformers not installed. Using manual gesture selection.")


# ==============================================================================
# CONFIGURATION
# ==============================================================================

MODEL_NAME = "dima806/hand_gestures_image_detection"
HF_TOKEN = os.environ.get("HF_TOKEN", None)

APP_TITLE = "## 🎓 CISC 121 - OOP Sorting & Searching Visualizer"
APP_DESCRIPTION = """
**Learn Object-Oriented Programming through Algorithm Visualization!**

This app demonstrates key OOP concepts:
- 📦 **Classes & Objects**: GestureImage, ImageList, Algorithms
- 🎭 **Inheritance**: All sorting algorithms inherit from SortingAlgorithm
- 🔄 **Polymorphism**: Swap between algorithms seamlessly
- 🏭 **Factory Pattern**: RendererFactory creates the right visualizer

**How to use:**
1. **Add images** using the buttons below (capture or manual)
2. **View your list** of gesture images
3. **Run an algorithm** to see step-by-step visualization
4. **Navigate steps** to understand how the algorithm works
"""


# ==============================================================================
# GRADIO APP CLASS
# ==============================================================================

class GradioApp:
    """
    📚 CONCEPT: Composition
    
    The GradioApp class COMPOSES (contains) other objects:
    - ImageList for managing captured images
    - Visualizer for displaying algorithm steps
    - Classifier for gesture recognition (if available)
    
    This is the Controller in MVC pattern - it coordinates
    between user interface (View) and data/logic (Model).
    """
    
    def __init__(self):
        """Initialize the application state."""
        self.image_list = ImageList()
        self.visualizer = Visualizer(VisualizationConfig(
            show_statistics=True,
            show_legend=True,
            image_size=60
        ))
        self._capture_count = 0
        
        # Initialize classifier if available
        self.classifier = None
        if CLASSIFIER_AVAILABLE:
            try:
                self.classifier = pipeline(
                    "image-classification",
                    model=MODEL_NAME,
                    token=HF_TOKEN
                )
                print(f"✅ Loaded model: {MODEL_NAME}")
            except Exception as e:
                print(f"⚠️ Could not load model: {e}")
    
    # -------------------------------------------------------------------------
    # Image Management Methods
    # -------------------------------------------------------------------------
    
    def add_manual_gesture(self, gesture_name: str) -> Tuple[str, str]:
        """
        Add a gesture image manually (without camera).
        
        Returns:
            Tuple of (image_list_html, status_message)
        """
        if not gesture_name:
            return self._render_image_list(), "⚠️ Please select a gesture"
        
        self._capture_count += 1
        self.image_list.add_new(gesture_name)
        
        return (
            self._render_image_list(),
            f"✅ Added {GestureRanking.get_emoji(gesture_name)} {gesture_name} (#{self._capture_count})"
        )
    
    def add_from_image(self, image: Image.Image) -> Tuple[str, str]:
        """
        Add a gesture from an uploaded/captured image.
        Uses AI classification if available, otherwise prompts for manual selection.
        """
        if image is None:
            return self._render_image_list(), "⚠️ No image provided"
        
        if self.classifier:
            try:
                # Classify the image
                results = self.classifier(image)
                if results:
                    top_result = results[0]
                    gesture_name = top_result['label'].lower()
                    confidence = top_result['score']
                    
                    self._capture_count += 1
                    img = GestureImage.create_from_prediction(
                        gesture_name=gesture_name,
                        capture_id=self._capture_count,
                        image=image,
                        confidence=confidence
                    )
                    self.image_list._save_state()  # Save before modifying
                    self.image_list._images.append(img)
                    
                    return (
                        self._render_image_list(),
                        f"✅ Detected: {img.emoji} {gesture_name} ({confidence:.1%} confidence)"
                    )
            except Exception as e:
                return self._render_image_list(), f"⚠️ Classification error: {e}"
        
        return self._render_image_list(), "⚠️ No classifier available. Use manual gesture selection."
    
    def remove_image(self, index: int) -> Tuple[str, str]:
        """Remove an image at the given index."""
        if 0 <= index < len(self.image_list):
            removed = self.image_list[index]
            self.image_list.remove(index)
            return self._render_image_list(), f"✅ Removed {removed}"
        return self._render_image_list(), "⚠️ Invalid index"
    
    def shuffle_images(self) -> Tuple[str, str]:
        """Shuffle the image list."""
        self.image_list.shuffle()
        return self._render_image_list(), "🔀 Shuffled!"
    
    def clear_images(self) -> Tuple[str, str]:
        """Clear all images."""
        count = len(self.image_list)
        self.image_list.clear()
        self._capture_count = 0
        self.visualizer.reset()
        return self._render_image_list(), f"🗑️ Cleared {count} images"
    
    def undo_action(self) -> Tuple[str, str]:
        """Undo the last action."""
        if self.image_list.undo():
            return self._render_image_list(), "↩️ Undone!"
        return self._render_image_list(), "⚠️ Nothing to undo"
    
    def add_sample_data(self) -> Tuple[str, str]:
        """Add sample data for testing."""
        gestures = ['fist', 'peace', 'like', 'peace', 'ok', 'fist']
        for g in gestures:
            self._capture_count += 1
            self.image_list.add_new(g)
        return self._render_image_list(), f"✅ Added {len(gestures)} sample gestures"
    
    def add_instability_demo(self) -> Tuple[str, str]:
        """
        Add data specifically designed to demonstrate Quick Sort instability.
        
        📚 EDUCATIONAL PURPOSE:
        This creates a scenario where Quick Sort will reorder equal elements,
        demonstrating that it's an UNSTABLE sorting algorithm.
        
        Setup: [✌️₁] [✌️₂] [✌️₃] [✊₄]
        After Quick Sort: The peace signs may be reordered (e.g., ₂,₃,₁)
        After Bubble/Merge Sort: Order preserved (₁,₂,₃)
        """
        self.clear_images()
        # Three peace signs followed by a lower-ranked fist
        demo_gestures = ['peace', 'peace', 'peace', 'fist']
        for g in demo_gestures:
            self._capture_count += 1
            self.image_list.add_new(g)
        
        return (
            self._render_image_list(),
            "🎓 Instability Demo: [✌️₁][✌️₂][✌️₃][✊₄]\n"
            "Try Quick Sort vs Bubble Sort - watch the subscript order!"
        )
    
    def add_worst_case_demo(self) -> Tuple[str, str]:
        """
        Add already-sorted data to demonstrate worst-case for Quick Sort.
        
        📚 EDUCATIONAL PURPOSE:
        When data is already sorted and we use First Pivot strategy,
        Quick Sort degrades to O(n²) - its worst case!
        """
        self.clear_images()
        # Sorted order: fist(1) < peace(2) < like(3) < ok(4) < call(5)
        sorted_gestures = ['fist', 'peace', 'like', 'ok', 'call']
        for g in sorted_gestures:
            self._capture_count += 1
            self.image_list.add_new(g)
        
        return (
            self._render_image_list(),
            "🎓 Worst-Case Demo: Already sorted data!\n"
            "Quick Sort with First Pivot → O(n²)\n"
            "Try Median-of-3 or Random pivot to see the difference."
        )
    
    def add_binary_search_demo(self) -> Tuple[str, str]:
        """
        Add sorted data for binary search demonstration.
        
        📚 EDUCATIONAL PURPOSE:
        Binary search requires sorted data. This preset shows
        how O(log n) is much faster than O(n) linear search.
        """
        self.clear_images()
        # Create larger sorted dataset for more dramatic comparison
        gestures = ['fist', 'fist', 'peace', 'peace', 'like', 'like', 
                    'ok', 'ok', 'call', 'call', 'palm', 'palm']
        for g in gestures:
            self._capture_count += 1
            self.image_list.add_new(g)
        
        return (
            self._render_image_list(),
            "🎓 Search Demo: 12 sorted elements\n"
            "Linear Search: up to 12 comparisons\n"
            "Binary Search: at most 4 comparisons (log₂12 ≈ 3.6)"
        )
    
    # -------------------------------------------------------------------------
    # Algorithm Execution Methods
    # -------------------------------------------------------------------------
    
    def run_sort(self, algorithm_name: str, pivot_strategy: str = "first", 
                 partition_scheme: str = "2-way") -> Tuple[str, str, str]:
        """
        Run a sorting algorithm on the image list.
        
        Returns:
            Tuple of (visualization_html, image_list_html, status_message)
        """
        if len(self.image_list) < 2:
            return (
                self.visualizer.render_current(),
                self._render_image_list(),
                "⚠️ Need at least 2 images to sort"
            )
        
        # Create the algorithm instance
        if algorithm_name == "Bubble Sort":
            algo = BubbleSort()
        elif algorithm_name == "Merge Sort":
            algo = MergeSort()
        elif algorithm_name == "Quick Sort":
            # Map string to enum
            pivot_map = {
                "first": PivotStrategy.FIRST,
                "last": PivotStrategy.LAST,
                "median": PivotStrategy.MEDIAN_OF_THREE,
                "random": PivotStrategy.RANDOM,
            }
            partition_map = {
                "2-way": PartitionScheme.TWO_WAY,
                "3-way": PartitionScheme.THREE_WAY,
            }
            algo = QuickSort(
                pivot_strategy=pivot_map.get(pivot_strategy, PivotStrategy.FIRST),
                partition_scheme=partition_map.get(partition_scheme, PartitionScheme.TWO_WAY)
            )
        else:
            return (
                self.visualizer.render_current(),
                self._render_image_list(),
                f"⚠️ Unknown algorithm: {algorithm_name}"
            )
        
        # Get data copy and run algorithm
        data = list(self.image_list)
        sorted_data, steps = algo.run_full(data)
        
        # Load into visualizer
        self.visualizer.load_steps(steps, sorted_data, algo.name)
        
        # Update the image list to sorted order
        self.image_list._save_state()  # Save before modifying
        self.image_list._images = list(sorted_data)
        
        return (
            self.visualizer.render_current(),
            self._render_image_list(),
            f"✅ {algo.name}: {len(steps)} steps"
        )
    
    def run_search(self, algorithm_name: str, target_index: int) -> Tuple[str, str]:
        """
        Run a search algorithm.
        
        Args:
            algorithm_name: "Linear Search" or "Binary Search"
            target_index: Index of the target element to search for
            
        Returns:
            Tuple of (visualization_html, status_message)
        """
        if len(self.image_list) < 1:
            return self.visualizer.render_current(), "⚠️ Need at least 1 image to search"
        
        if not (0 <= target_index < len(self.image_list)):
            return self.visualizer.render_current(), "⚠️ Invalid target index"
        
        data = list(self.image_list)
        target = data[target_index]
        
        # For binary search, we need sorted data
        if algorithm_name == "Binary Search":
            if not self.image_list.is_sorted():
                return (
                    self.visualizer.render_current(),
                    "⚠️ Binary Search requires sorted data! Run a sort first."
                )
            algo = BinarySearch(variant="iterative")
        else:
            algo = LinearSearch()
        
        # Run the search
        result_index, steps = algo.run_full(data, target)
        
        # Load into visualizer
        self.visualizer.load_steps(steps, data, algo.name)
        
        if result_index is not None:
            status = f"✅ {algo.name}: Found {target} at index {result_index}"
        else:
            status = f"❌ {algo.name}: {target} not found"
        
        return self.visualizer.render_current(), status
    
    # -------------------------------------------------------------------------
    # Visualization Navigation Methods
    # -------------------------------------------------------------------------
    
    def viz_next(self) -> str:
        """Go to next visualization step."""
        return self.visualizer.next_step()
    
    def viz_prev(self) -> str:
        """Go to previous visualization step."""
        return self.visualizer.prev_step()
    
    def viz_start(self) -> str:
        """Go to first step."""
        return self.visualizer.go_to_start()
    
    def viz_end(self) -> str:
        """Go to last step."""
        return self.visualizer.go_to_end()
    
    def viz_goto(self, step: int) -> str:
        """Go to a specific step."""
        return self.visualizer.go_to_step(int(step) - 1)  # Convert to 0-based
    
    # -------------------------------------------------------------------------
    # Rendering Methods
    # -------------------------------------------------------------------------
    
    def _render_image_list(self) -> str:
        """Render the current image list as HTML."""
        if len(self.image_list) == 0:
            return """
            <div style="
                text-align: center;
                padding: 40px;
                color: #666;
                background: #f8f9fa;
                border-radius: 12px;
                border: 2px dashed #ddd;
            ">
                <div style="font-size: 48px; margin-bottom: 15px;">📷</div>
                <h3 style="margin: 0 0 10px 0;">No Images Yet</h3>
                <p style="margin: 0;">Add gestures using the buttons above!</p>
            </div>
            """
        
        # Build image cards
        cards = []
        for i, img in enumerate(self.image_list):
            card = f"""
            <div style="
                display: inline-flex;
                flex-direction: column;
                align-items: center;
                margin: 6px;
                padding: 12px;
                border-radius: 10px;
                background: white;
                border: 2px solid #ddd;
                min-width: 70px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="font-size: 32px; margin-bottom: 4px;">{img.emoji}</div>
                <div style="font-size: 11px; color: #666;">₍{img.capture_id}₎</div>
                <div style="font-size: 10px; color: #999;">rank {img.rank}</div>
                <div style="font-size: 9px; color: #aaa; margin-top: 4px;">[{i}]</div>
            </div>
            """
            cards.append(card)
        
        # Analysis
        analysis = self.image_list.get_analysis()
        is_sorted = "✅ Sorted" if self.image_list.is_sorted() else "❌ Not Sorted"
        
        return f"""
        <div style="
            background: linear-gradient(135deg, #002D62 0%, #9B2335 100%);
            color: white;
            padding: 15px;
            border-radius: 12px 12px 0 0;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>Image List ({len(self.image_list)} items)</strong>
                <span>{is_sorted}</span>
            </div>
        </div>
        <div style="
            background: #f8f9fa;
            padding: 15px;
            border-radius: 0 0 12px 12px;
            border: 1px solid #ddd;
            border-top: none;
        ">
            <div style="
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 4px;
            ">
                {''.join(cards)}
            </div>
            <div style="
                margin-top: 15px;
                padding-top: 10px;
                border-top: 1px solid #ddd;
                font-size: 12px;
                color: #666;
                text-align: center;
            ">
                {analysis}
            </div>
        </div>
        """
    
    # -------------------------------------------------------------------------
    # Create Gradio UI
    # -------------------------------------------------------------------------
    
    def create_ui(self) -> gr.Blocks:
        """
        Create the Gradio interface.
        
        📚 CONCEPT: Builder Pattern (light version)
        
        We build up the UI component by component, each with its
        own responsibility. The final result is a complete interface.
        """
        
        with gr.Blocks(
            title="CISC 121 - OOP Sorting Visualizer",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="red",
            )
        ) as demo:
            
            # Header
            gr.Markdown(APP_TITLE)
            gr.Markdown(APP_DESCRIPTION)
            
            with gr.Tabs():
                # ============================================================
                # TAB 1: Image Management
                # ============================================================
                with gr.TabItem("📷 Capture & Manage"):
                    with gr.Row():
                        # Left column: Add images
                        with gr.Column(scale=1):
                            gr.Markdown("### Add Gestures")
                            
                            # Manual gesture selection
                            gesture_dropdown = gr.Dropdown(
                                choices=GestureRanking.get_all_gestures(),
                                label="Select Gesture",
                                info="Choose a gesture to add"
                            )
                            add_btn = gr.Button("➕ Add Gesture", variant="primary")
                            
                            gr.Markdown("---")
                            
                            # Image upload
                            image_input = gr.Image(
                                label="Upload Image",
                                type="pil",
                                sources=["upload", "webcam"]
                            )
                            classify_btn = gr.Button("🔍 Classify & Add")
                            
                            gr.Markdown("---")
                            
                            # Quick actions
                            with gr.Row():
                                sample_btn = gr.Button("📝 Add Samples")
                                shuffle_btn = gr.Button("🔀 Shuffle")
                            with gr.Row():
                                undo_btn = gr.Button("↩️ Undo")
                                clear_btn = gr.Button("🗑️ Clear", variant="stop")
                            
                            gr.Markdown("---")
                            
                            # Educational demos
                            gr.Markdown("### 🎓 Educational Demos")
                            instability_btn = gr.Button(
                                "⚠️ Instability Demo",
                                variant="secondary"
                            )
                            worst_case_btn = gr.Button(
                                "📉 Worst-Case Demo",
                                variant="secondary"
                            )
                            search_demo_btn = gr.Button(
                                "🔍 Search Demo",
                                variant="secondary"
                            )
                        
                        # Right column: Image list display
                        with gr.Column(scale=2):
                            gr.Markdown("### Current Image List")
                            image_list_display = gr.HTML(
                                value=self._render_image_list()
                            )
                            status_msg = gr.Textbox(
                                label="Status",
                                interactive=False
                            )
                    
                    # Wire up events for Tab 1
                    add_btn.click(
                        fn=self.add_manual_gesture,
                        inputs=[gesture_dropdown],
                        outputs=[image_list_display, status_msg]
                    )
                    classify_btn.click(
                        fn=self.add_from_image,
                        inputs=[image_input],
                        outputs=[image_list_display, status_msg]
                    )
                    sample_btn.click(
                        fn=self.add_sample_data,
                        outputs=[image_list_display, status_msg]
                    )
                    shuffle_btn.click(
                        fn=self.shuffle_images,
                        outputs=[image_list_display, status_msg]
                    )
                    undo_btn.click(
                        fn=self.undo_action,
                        outputs=[image_list_display, status_msg]
                    )
                    clear_btn.click(
                        fn=self.clear_images,
                        outputs=[image_list_display, status_msg]
                    )
                    instability_btn.click(
                        fn=self.add_instability_demo,
                        outputs=[image_list_display, status_msg]
                    )
                    worst_case_btn.click(
                        fn=self.add_worst_case_demo,
                        outputs=[image_list_display, status_msg]
                    )
                    search_demo_btn.click(
                        fn=self.add_binary_search_demo,
                        outputs=[image_list_display, status_msg]
                    )
                
                # ============================================================
                # TAB 2: Sorting Algorithms
                # ============================================================
                with gr.TabItem("📊 Sorting"):
                    with gr.Row():
                        # Left: Algorithm selection
                        with gr.Column(scale=1):
                            gr.Markdown("### Select Algorithm")
                            
                            sort_algo = gr.Radio(
                                choices=["Bubble Sort", "Merge Sort", "Quick Sort"],
                                value="Bubble Sort",
                                label="Algorithm",
                                info="Each has different time complexity and stability"
                            )
                            
                            # Educational info accordion
                            with gr.Accordion("📚 Algorithm Info", open=False):
                                gr.Markdown("""
**Bubble Sort** - O(n²) average, O(n) best
- ✅ Stable (preserves order of equal elements)
- Simple but slow for large lists
- Best when: Nearly sorted data

**Merge Sort** - O(n log n) always  
- ✅ Stable
- Consistent performance
- Uses extra memory for merging

**Quick Sort** - O(n log n) average, O(n²) worst
- ❌ Unstable (may reorder equal elements)
- Fast in practice, in-place
- Best when: Random data, good pivot
                                """)
                            
                            # Quick Sort options (only shown when Quick Sort selected)
                            with gr.Group() as quicksort_options:
                                gr.Markdown("**Quick Sort Options**")
                                pivot_strategy = gr.Radio(
                                    choices=["first", "last", "median", "random"],
                                    value="first",
                                    label="Pivot Strategy",
                                    info="Median/Random avoid worst-case O(n²)"
                                )
                                partition_scheme = gr.Radio(
                                    choices=["2-way", "3-way"],
                                    value="2-way",
                                    label="Partition Scheme",
                                    info="3-way handles duplicates better"
                                )
                            
                            run_sort_btn = gr.Button("▶️ Run Sort", variant="primary", size="lg")
                            
                            gr.Markdown("---")
                            gr.Markdown("### Current List")
                            sort_list_display = gr.HTML(value=self._render_image_list())
                        
                        # Right: Visualization
                        with gr.Column(scale=2):
                            gr.Markdown("### Visualization")
                            sort_viz_display = gr.HTML(
                                value=self.visualizer.render_current()
                            )
                            
                            # Navigation controls
                            with gr.Row():
                                viz_start_btn = gr.Button("⏮️ Start")
                                viz_prev_btn = gr.Button("◀️ Prev")
                                step_slider = gr.Slider(
                                    minimum=1,
                                    maximum=100,
                                    step=1,
                                    value=1,
                                    label="Step"
                                )
                                viz_next_btn = gr.Button("Next ▶️")
                                viz_end_btn = gr.Button("End ⏭️")
                            
                            sort_status = gr.Textbox(label="Status", interactive=False)
                    
                    # Wire up sorting events
                    run_sort_btn.click(
                        fn=self.run_sort,
                        inputs=[sort_algo, pivot_strategy, partition_scheme],
                        outputs=[sort_viz_display, sort_list_display, sort_status]
                    )
                    viz_next_btn.click(fn=self.viz_next, outputs=[sort_viz_display])
                    viz_prev_btn.click(fn=self.viz_prev, outputs=[sort_viz_display])
                    viz_start_btn.click(fn=self.viz_start, outputs=[sort_viz_display])
                    viz_end_btn.click(fn=self.viz_end, outputs=[sort_viz_display])
                    step_slider.change(fn=self.viz_goto, inputs=[step_slider], outputs=[sort_viz_display])
                
                # ============================================================
                # TAB 3: Searching Algorithms
                # ============================================================
                with gr.TabItem("🔍 Searching"):
                    with gr.Row():
                        # Left: Search controls
                        with gr.Column(scale=1):
                            gr.Markdown("### Search Settings")
                            
                            search_algo = gr.Radio(
                                choices=["Linear Search", "Binary Search"],
                                value="Linear Search",
                                label="Algorithm",
                                info="Binary Search is O(log n) but requires sorted data"
                            )
                            
                            # Educational info accordion
                            with gr.Accordion("📚 Algorithm Info", open=False):
                                gr.Markdown("""
**Linear Search** - O(n)
- Works on ANY list (sorted or unsorted)
- Checks each element one by one
- Simple but slow for large lists

**Binary Search** - O(log n)
- ⚠️ REQUIRES SORTED DATA!
- Halves the search space each step
- Much faster: 1000 elements → only 10 comparisons!

**Example (searching 1000 elements):**
- Linear: up to 1000 checks
- Binary: at most 10 checks (log₂1000 ≈ 10)
                                """)
                            
                            target_index = gr.Number(
                                label="Target Index",
                                value=0,
                                precision=0,
                                info="Which element to search for (by index)"
                            )
                            
                            run_search_btn = gr.Button("🔍 Run Search", variant="primary", size="lg")
                            
                            gr.Markdown("---")
                            gr.Markdown("### Current List")
                            search_list_display = gr.HTML(value=self._render_image_list())
                        
                        # Right: Visualization
                        with gr.Column(scale=2):
                            gr.Markdown("### Visualization")
                            search_viz_display = gr.HTML(
                                value=self.visualizer.render_current()
                            )
                            
                            # Navigation controls
                            with gr.Row():
                                search_start_btn = gr.Button("⏮️ Start")
                                search_prev_btn = gr.Button("◀️ Prev")
                                search_next_btn = gr.Button("Next ▶️")
                                search_end_btn = gr.Button("End ⏭️")
                            
                            search_status = gr.Textbox(label="Status", interactive=False)
                    
                    # Wire up search events
                    run_search_btn.click(
                        fn=self.run_search,
                        inputs=[search_algo, target_index],
                        outputs=[search_viz_display, search_status]
                    )
                    search_next_btn.click(fn=self.viz_next, outputs=[search_viz_display])
                    search_prev_btn.click(fn=self.viz_prev, outputs=[search_viz_display])
                    search_start_btn.click(fn=self.viz_start, outputs=[search_viz_display])
                    search_end_btn.click(fn=self.viz_end, outputs=[search_viz_display])
                
                # ============================================================
                # TAB 4: Learn OOP
                # ============================================================
                with gr.TabItem("📚 Learn OOP"):
                    gr.Markdown("""
                    # Object-Oriented Programming Concepts
                    
                    This application demonstrates several key OOP concepts:
                    
                    ## 📦 Classes & Objects
                    
                    **Classes** are blueprints for creating objects. In this app:
                    - `GestureImage` - represents a single captured gesture
                    - `ImageList` - manages a collection of gestures
                    - `BubbleSort`, `MergeSort`, `QuickSort` - sorting algorithms
                    - `Visualizer` - handles step-by-step display
                    
                    ## 🎭 Inheritance
                    
                    **Inheritance** lets classes share code. All sorting algorithms inherit from `SortingAlgorithm`:
                    
                    ```python
                    class SortingAlgorithm(ABC):  # Abstract Base Class
                        @abstractmethod
                        def sort(self, data): ...
                    
                    class BubbleSort(SortingAlgorithm):  # Inherits from SortingAlgorithm
                        def sort(self, data):
                            # Bubble sort implementation
                    ```
                    
                    ## 🔄 Polymorphism
                    
                    **Polymorphism** means "same interface, different behavior":
                    
                    ```python
                    # All these work the same way!
                    algo = BubbleSort()
                    algo = MergeSort()
                    algo = QuickSort()
                    
                    # Same method call, different algorithms
                    result, steps = algo.run_full(data)
                    ```
                    
                    ## 🏭 Factory Pattern
                    
                    **Factory Pattern** creates objects without exposing creation logic:
                    
                    ```python
                    # Factory creates the right renderer automatically
                    renderer = RendererFactory.create("Bubble Sort")
                    ```
                    
                    ## 📊 Algorithm Comparison
                    
                    | Algorithm | Time (Best) | Time (Worst) | Stable? | In-Place? |
                    |-----------|-------------|--------------|---------|-----------|
                    | Bubble Sort | O(n) | O(n²) | ✅ Yes | ✅ Yes |
                    | Merge Sort | O(n log n) | O(n log n) | ✅ Yes | ❌ No |
                    | Quick Sort | O(n log n) | O(n²) | ❌ No | ✅ Yes |
                    | Linear Search | O(1) | O(n) | - | - |
                    | Binary Search | O(1) | O(log n) | - | - |
                    
                    ## 🔍 Stability
                    
                    A **stable** sort preserves the relative order of equal elements.
                    
                    Example with two peace signs ✌️₁ and ✌️₂:
                    - **Stable**: Always produces [✌️₁, ✌️₂] (original order kept)
                    - **Unstable**: Might produce [✌️₂, ✌️₁] (order can change)
                    
                    Try Quick Sort with duplicate gestures to see instability!
                    """)
            
            # Footer
            gr.Markdown("""
            ---
            *Built for CISC 121 - Queen's University*
            """)
        
        return demo


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def main():
    """Create and launch the Gradio app."""
    app = GradioApp()
    demo = app.create_ui()
    demo.launch(share=False)


if __name__ == "__main__":
    main()
