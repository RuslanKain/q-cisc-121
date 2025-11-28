"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CISC 121 - HAND GESTURE RECOGNITION APP                  ║
║                         Queen's University                                   ║
║                                                                              ║
║  PURPOSE: This app uses AI to recognize hand gestures (one, peace, etc.)   ║
║  VERSION: Procedural (step-by-step) - Great for beginners!                  ║
║                                                                              ║
║  HOW TO RUN: python app.py                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ==============================================================================
# SECTION 1: IMPORTS
# ==============================================================================
# What are imports?
#   Imports let us use code that other people wrote.
#   Instead of writing everything from scratch, we can use "libraries".
#
# Think of it like borrowing tools:
#   - gradio = tools for building web pages
#   - transformers = tools for AI/machine learning
#   - time = tools for measuring how long things take
#   - os = tools for working with the operating system (like reading files)
# ==============================================================================

import gradio as gr
# "gr" is a short nickname for "gradio" - it saves us typing!
# Example: instead of gradio.Button(), we can write gr.Button()

from transformers import pipeline
# "pipeline" is a function that makes using AI models easy.
# It handles all the complicated setup for us.

from time import perf_counter
# "perf_counter" is like a stopwatch - it measures time very precisely.

import os
# "os" lets us interact with the operating system
# We use it to read environment variables (like secret tokens)


# ==============================================================================
# SECTION 2: CONFIGURATION (SETTINGS)
# ==============================================================================
# What is configuration?
#   These are settings we can change to customize how the app works.
#   By putting them at the top, they're easy to find and modify.
# ==============================================================================

# The AI model we will use for hand gesture recognition
# 
# MODEL OPTIONS:
#   1. "dima806/hand_gestures_image_detection" (RECOMMENDED)
#      - Recognizes: one, two, three, four, fist, ok, like, peace, etc.
#      - Trained specifically for hand gestures!
#
#   2. "google/vit-base-patch16-224" (General purpose)
#      - Recognizes 1000 everyday objects (cats, cars, etc.)
#      - NOT trained for hand gestures - won't work for finger counting
#
#   3. "microsoft/resnet-50" (General purpose, faster)
#      - Similar to Google's model, but faster
#
MODEL_NAME = "dima806/hand_gestures_image_detection"

# Hugging Face Token (Optional but recommended)
# Some models require authentication to download.
# Get your free token at: https://huggingface.co/settings/tokens
#
# Option 1: Set as environment variable (recommended for security)
#   export HF_TOKEN="your_token_here"
#
# Option 2: Paste directly here (less secure, but okay for learning)
#   HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxx"
#
HF_TOKEN = os.environ.get("HF_TOKEN", None)
# os.environ.get() tries to read the HF_TOKEN from environment variables
# If not found, it returns None (which means "no token")

# App title and description
APP_TITLE = "## 🎓 CISC 121 - Hand Gesture Recognition App"
APP_DESCRIPTION = """
Welcome! This app uses AI to recognize **hand gestures**.

**Supported Gestures:**
✋ one, ✌️ two/peace, 🤟 three, 🖖 four, ✊ fist, 👍 like, 👎 dislike, 👌 ok, 🤚 stop

**How to use:**
1. **Upload an image** OR **use your webcam**
2. Show a hand gesture clearly in frame
3. Click **"🔍 Analyze Image"** to see the AI's prediction

> 💡 **Tip:** Make sure your hand is well-lit and clearly visible!
"""


# ==============================================================================
# SECTION 3: HELPER FUNCTIONS
# ==============================================================================
# What are functions?
#   Functions are reusable blocks of code that do one specific job.
#   We give them a name, and then we can "call" them whenever we need them.
#
# Why use functions?
#   1. Reusability - write once, use many times
#   2. Organization - break big problems into small pieces
#   3. Readability - give meaningful names to actions
# ==============================================================================

def create_greeting(name):
    """
    Creates a personalized greeting message.
    
    What is a docstring? (This text you're reading!)
        A docstring explains what a function does.
        It helps other programmers (and future you!) understand the code.
    
    Parameters:
    -----------
    name : str
        The name of the person to greet.
        "str" means "string" - a piece of text.
    
    Returns:
    --------
    str
        A greeting message as a string.
    
    Example:
    --------
    >>> create_greeting("Alice")
    "Hello Alice! Welcome to CISC 121!"
    """
    # f-strings let us put variables inside text
    # The {name} gets replaced with the actual value of 'name'
    greeting = f"Hello {name}! Welcome to CISC 121!"
    return greeting


def analyze_image(image):
    """
    Sends an image to the AI model and gets back predictions.
    
    How does this work?
        1. We send the image to Hugging Face's servers
        2. The AI model analyzes the image
        3. We get back a list of predictions with confidence scores
    
    Parameters:
    -----------
    image : PIL.Image or numpy.ndarray
        The image to analyze. Gradio handles the format for us.
    
    Returns:
    --------
    tuple
        A tuple containing:
        - results (list): The AI's predictions
        - elapsed_time (float): How long the analysis took in seconds
    
    What is a tuple?
        A tuple is like a container that holds multiple values.
        We use it when a function needs to return more than one thing.
    """
    # Safety check: make sure we actually received an image
    # "None" means "nothing" - the user might not have taken a photo yet
    if image is None:
        print("⚠️ No image provided")
        return None, 0.0
    
    # Debug: Print what type of image we received
    print(f"📷 Received image type: {type(image)}")
    print(f"📷 Image info: {image if not hasattr(image, 'size') else f'Size: {image.size}'}")
    
    # Start the stopwatch
    start_time = perf_counter()
    
    # Create the AI classifier
    # "pipeline" sets up everything we need to use the model
    try:
        print(f"🔄 Loading model: {MODEL_NAME}")
        print(f"🔑 HF Token: {'Set' if HF_TOKEN else 'Not set (may limit some models)'}")
        
        # Create the classifier with optional token
        classifier = pipeline(
            task="image-classification",  # What kind of task?
            model=MODEL_NAME,             # Which AI model to use?
            token=HF_TOKEN                # Authentication token (optional)
        )
        
        print("📷 Analyzing image...")
        
        # Handle different image formats that Gradio might send
        # Gradio can send: PIL Image, numpy array, or file path
        from PIL import Image
        
        if isinstance(image, str):
            # It's a file path - open it
            print("   (Converting from file path)")
            image = Image.open(image)
        elif hasattr(image, 'convert'):
            # It's already a PIL Image - ensure it's in RGB format
            print("   (Image is PIL format)")
            if image.mode != 'RGB':
                image = image.convert('RGB')
        else:
            # It might be a numpy array - convert to PIL
            print("   (Converting from numpy array)")
            import numpy as np
            if isinstance(image, np.ndarray):
                image = Image.fromarray(image)
        
        # Send the image to the model and get predictions
        results = classifier(image)
        
        print(f"✅ Analysis complete! Found {len(results)} predictions.")
        
    except Exception as error:
        # If something goes wrong, we catch the error
        # This prevents the app from crashing
        print(f"❌ Error during image analysis: {error}")
        print(f"   Error type: {type(error).__name__}")
        
        # Print full traceback for debugging
        import traceback
        traceback.print_exc()
        
        # Common error explanations
        if "401" in str(error) or "unauthorized" in str(error).lower():
            print("   💡 This might be an authentication issue. Try setting HF_TOKEN.")
        elif "connection" in str(error).lower() or "network" in str(error).lower():
            print("   💡 Check your internet connection.")
        elif "memory" in str(error).lower():
            print("   💡 The model might be too large. Try a smaller model.")
        
        return None, 0.0
    
    # Stop the stopwatch
    end_time = perf_counter()
    
    # Calculate how long it took
    elapsed_time = end_time - start_time
    
    return results, elapsed_time


def format_results(results, elapsed_time):
    """
    Formats the AI predictions into a readable string.
    
    Why format results?
        The raw data from the AI is hard to read.
        We transform it into a nice, human-friendly format.
    
    Parameters:
    -----------
    results : list or None
        The predictions from the AI model.
        Each prediction has a 'label' and a 'score' (confidence).
    
    elapsed_time : float
        How long the analysis took, in seconds.
    
    Returns:
    --------
    str
        A formatted string showing the predictions.
    """
    # Handle the case where analysis failed
    if results is None:
        return "❌ Could not analyze the image. Please try again."
    
    # Start building our output message
    output_lines = []
    
    # Add a header
    output_lines.append("## 🔍 Analysis Results\n")
    output_lines.append(f"⏱️ *Analysis completed in {elapsed_time:.2f} seconds*\n")
    
    # What does :.2f mean?
    #   It formats a number to show 2 decimal places.
    #   Example: 1.23456 becomes "1.23"
    
    output_lines.append("### Top Predictions:\n")
    
    # Loop through the top 5 predictions
    # enumerate() gives us both the index (i) and the item (prediction)
    for i, prediction in enumerate(results[:5]):
        label = prediction['label']       # What the AI thinks it sees
        score = prediction['score']       # How confident it is (0 to 1)
        percentage = score * 100          # Convert to percentage
        
        # Add a medal emoji for top 3
        if i == 0:
            medal = "🥇"
        elif i == 1:
            medal = "🥈"
        elif i == 2:
            medal = "🥉"
        else:
            medal = "  "
        
        output_lines.append(f"{medal} **{label}**: {percentage:.1f}%\n")
    
    # Join all lines into one string
    # '\n' means "new line" (like pressing Enter)
    return ''.join(output_lines)


# ==============================================================================
# SECTION 4: MAIN APPLICATION
# ==============================================================================
# This section builds the actual web interface.
# We use Gradio's "Blocks" system to create a custom layout.
#
# What is gr.Blocks()?
#   It's like a container for our app.
#   Everything inside the "with" block becomes part of the interface.
#
# What does "with" do?
#   "with" creates a context - it's like saying "everything in here belongs together"
#   When we exit the "with" block, Gradio knows our app is complete.
# ==============================================================================

def create_app():
    """
    Creates and returns the Gradio application.
    
    Why put this in a function?
        1. It keeps the code organized
        2. We can easily test or modify the app
        3. It's a good habit for larger programs
    
    Returns:
    --------
    gr.Blocks
        The complete Gradio application, ready to launch.
    """
    
    # Create the app container
    # Note: We use try/except for theme to support different Gradio versions
    # Older versions don't support the theme parameter the same way
    try:
        # Try modern Gradio syntax (4.x+)
        app = gr.Blocks(
            title="CISC 121 Gesture App",  # Browser tab title
            theme=gr.themes.Soft()          # A nice, modern look
        )
    except TypeError:
        # Fall back for older Gradio versions
        app = gr.Blocks(title="CISC 121 Gesture App")
    
    with app:
        
        # ----------------------------------------------------------------------
        # PART A: HEADER SECTION
        # ----------------------------------------------------------------------
        # gr.Markdown() lets us add formatted text using Markdown syntax
        # Markdown is a simple way to format text (like in README files)
        
        gr.Markdown(APP_TITLE)
        gr.Markdown(APP_DESCRIPTION)
        
        # Add a horizontal line for visual separation
        gr.Markdown("---")
        
        # ----------------------------------------------------------------------
        # PART B: IMAGE INPUT AND RESULTS SECTION
        # ----------------------------------------------------------------------
        # gr.Row() puts components side by side (horizontal layout)
        # gr.Column() stacks components on top of each other (vertical layout)
        
        with gr.Row():
            
            # Left column: Image input
            with gr.Column(scale=1):
                gr.Markdown("### 📸 Image Input")
                
                # Create tabs for different input methods
                # This makes it clearer for users how to provide an image
                with gr.Tabs():
                    
                    # Tab 1: Upload an image file
                    with gr.TabItem("📁 Upload"):
                        upload_input = gr.Image(
                            label="Click to upload or drag an image here",
                            sources=["upload"],
                            type="pil",
                            height=250
                        )
                    
                    # Tab 2: Use webcam (captures on click)
                    with gr.TabItem("📷 Webcam"):
                        webcam_input = gr.Image(
                            label="Click the 📷 button below the preview to capture",
                            sources=["webcam"],
                            type="pil",
                            height=250,
                            mirror_webcam=True
                        )
                
                # Status indicator - shows when image is ready
                status_display = gr.Markdown("👆 *Choose a tab above and provide an image*")
                
                # The submit button
                submit_button = gr.Button(
                    value="🔍 Analyze Image",
                    variant="primary",
                    size="lg"
                )
            
            # Right column: Results
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Results")
                
                # gr.Markdown() can also display dynamic content
                # We'll update this when the user clicks the button
                results_display = gr.Markdown(
                    value="*Upload or capture an image, then click 'Analyze Image' to see results.*"
                )
        
        # ----------------------------------------------------------------------
        # PART C: CONNECTING COMPONENTS (EVENT HANDLING)
        # ----------------------------------------------------------------------
        # Now we connect the inputs to our functions.
        # We have TWO input sources (upload and webcam) that both need to work.
        
        # State variable to store the current image (from either source)
        # gr.State() is a special Gradio component that stores data between interactions
        current_image = gr.State(value=None)
        
        def on_upload(image):
            """Called when user uploads an image."""
            if image is not None:
                return image, "✅ **Image uploaded!** Click 'Analyze Image' to continue."
            return None, "👆 *Choose a tab above and provide an image*"
        
        def on_webcam_capture(image):
            """Called when user captures from webcam."""
            if image is not None:
                return image, "✅ **Photo captured!** Click 'Analyze Image' to continue."
            return None, "👆 *Choose a tab above and provide an image*"
        
        def on_submit(stored_image):
            """
            This function runs when the user clicks the submit button.
            
            It's called an "event handler" because it handles the click event.
            
            Parameters:
            -----------
            stored_image : PIL.Image
                The image stored from upload or webcam capture.
            
            Returns:
            --------
            str
                Formatted results to display.
            """
            # Check if we have an image
            if stored_image is None:
                return "⚠️ **No image detected!**\n\n**To fix this:**\n\n📁 **Upload Tab:** Click the upload area and select an image file\n\n📷 **Webcam Tab:** Click the camera button (📷) to capture a photo\n\nThen click 'Analyze Image' again."
            
            # Step 1: Analyze the image
            results, elapsed_time = analyze_image(stored_image)
            
            # Step 2: Format the results nicely
            formatted = format_results(results, elapsed_time)
            
            # Step 3: Return the formatted text (Gradio displays it)
            return formatted
        
        # Connect upload input - when image changes, store it
        upload_input.change(
            fn=on_upload,
            inputs=[upload_input],
            outputs=[current_image, status_display]
        )
        
        # Connect webcam input - when image is captured, store it
        webcam_input.change(
            fn=on_webcam_capture,
            inputs=[webcam_input],
            outputs=[current_image, status_display]
        )
        
        # Connect the button click to analyze the stored image
        submit_button.click(
            fn=on_submit,
            inputs=[current_image],
            outputs=[results_display]
        )
        
        # ----------------------------------------------------------------------
        # PART D: FOOTER
        # ----------------------------------------------------------------------
        gr.Markdown("---")
        gr.Markdown(
            "*Made for CISC 121 at Queen's University* 🎓"
        )
    
    # Return the completed app
    return app


# ==============================================================================
# SECTION 5: RUNNING THE APP
# ==============================================================================
# This is where we actually start the application.
#
# What does if __name__ == "__main__" mean?
#   This checks if we're running this file directly (not importing it).
#   If we run: python hf_gradio_proj.py → this code runs
#   If we import: from hf_gradio_proj import create_app → this code doesn't run
#
# Why is this useful?
#   It lets us use the same file in two ways:
#   1. As a standalone app (run it directly)
#   2. As a module (import functions into other files)
# ==============================================================================

if __name__ == "__main__":
    # Print a welcome message to the terminal
    print("=" * 60)
    print("🎓 CISC 121 - Gesture Recognition App")
    print("=" * 60)
    print("Starting the application...")
    print("Once ready, open the URL shown below in your browser.")
    print("=" * 60)
    
    # Create the app
    app = create_app()
    
    # Launch the app
    # share=True creates a public URL anyone can access
    # This is useful for sharing with classmates or instructors
    app.launch(share=True)
