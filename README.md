# 🎓 Queen's University CISC 121 - Gesture Recognition App

<!-- Queen's University Banner -->
<p align="center">
  <img src="https://www.queensu.ca/sites/default/files/assets/pages/queens-logo-red.png" alt="Queen's University Logo" width="300"/>
</p>

<p align="center">
  <strong>School of Computing | CISC 121 - Introduction to Computing Science</strong>
</p>

<!-- Badges with Queen's Colors -->
<p align="center">
  <img src="https://img.shields.io/badge/Queen's-CISC%20121-002452?style=for-the-badge&labelColor=B90E31" alt="CISC 121"/>
  <img src="https://img.shields.io/badge/Python-3.8+-FFD700?style=for-the-badge&logo=python&logoColor=white&labelColor=002452" alt="Python 3.8+"/>
  <img src="https://img.shields.io/badge/Gradio-4.0+-B90E31?style=for-the-badge&logo=gradio&logoColor=white" alt="Gradio"/>
  <img src="https://img.shields.io/badge/Hugging%20Face-API-002452?style=for-the-badge&logo=huggingface&logoColor=white" alt="Hugging Face"/>
</p>

---

## 📖 Project Overview

**Welcome to the CISC 121 Gesture Recognition Project!**

This project teaches you how to build a **web application** that uses **machine learning** to recognize **hand gestures** like thumbs up, peace sign, and counting fingers.

### 🎯 Learning Objectives

By completing this project, you will learn:

1. **Python Basics** - Functions, variables, strings, and more
2. **Web Interfaces** - Building user interfaces with Gradio
3. **APIs** - How to connect to external services (Hugging Face)
4. **Documentation** - Writing clear, helpful code comments
5. **Two Coding Styles** - Procedural vs Object-Oriented Programming

---

## 📁 Project Structure

```
q-cisc-121/
│
├── README.md                    # 📄 This file - Project guide
├── requirements.txt             # 📦 List of required packages
├── app.py                       # 🔧 Main application (Procedural style)
│
├── (Coming Soon)
├── app_oop.py                   # 🏗️ OOP version (classes & SOLID principles)
│
├── docs/                        # 📚 Documentation folder
│   ├── PROCEDURAL_GUIDE.md     # Guide for procedural version
│   └── OOP_GUIDE.md            # Guide for OOP version
│
└── assets/                      # 🖼️ Images and resources
    └── test_images/            # Sample images for testing
```

---

## 🚀 Quick Start Guide

### Step 1: Install Python

Make sure you have Python version **3.8 to 3.12** installed.

> ⚠️ **Note:** Gradio may not work with Python 3.13+ yet. We recommend Python 3.10 or 3.11.

```bash
# Check your Python version
python --version
```

---

### Step 2: Install Required Packages

#### What is `requirements.txt`?

A `requirements.txt` file is a standard way to list all the packages (libraries) a Python project needs. Instead of installing each package one by one, you can install everything at once!

#### Option A: Install All at Once (Recommended)

```bash
# Navigate to the project folder
cd q-cisc-121

# Install all required packages from requirements.txt
pip install -r requirements.txt
```

#### Option B: Install Packages Individually

If you prefer to understand what each package does:

```bash
# Gradio - Creates the web interface (camera, buttons, etc.)
pip install gradio

# Transformers - Hugging Face's AI library for image classification
pip install transformers

# PyTorch - The AI engine that powers the models
pip install torch

# Pillow - For image processing
pip install Pillow
```

#### What Do These Packages Do?

| Package        | Purpose                                    | Size    |
| -------------- | ------------------------------------------ | ------- |
| `gradio`       | Builds the web interface with camera input | ~50 MB  |
| `transformers` | Provides access to AI models               | ~100 MB |
| `torch`        | Runs the AI computations                   | ~2 GB   |
| `Pillow`       | Handles image loading/saving               | ~10 MB  |

> 💡 **Tip:** The first installation may take 5-10 minutes due to the size of PyTorch.

---

### Step 3: Run the App

```bash
# Make sure you're in the project folder
cd q-cisc-121

# Run the app
python app.py
```

---

### Step 4: Open in Browser

After running, you will see output like this:

```
============================================================
🎓 CISC 121 - Gesture Recognition App
============================================================
Starting the application...
Once ready, open the URL shown below in your browser.
============================================================
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxx.gradio.live
```

**Two URLs are provided:**

- **Local URL** - Only works on your computer
- **Public URL** - Share with classmates! (Active for 72 hours)

Click either link or copy-paste it into your web browser!

---

## 🔑 Hugging Face Token Setup (Important!)

To use AI models from Hugging Face, you need a **free access token**. This is like a library card that lets you borrow AI models.

### Why Do I Need a Token?

- Some AI models require authentication
- Tokens help prevent abuse of the free service
- You get higher rate limits with a token

### Step-by-Step: Getting Your Token

#### Step 1: Create a Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Click **"Sign Up"** (top right)
3. Use your Queen's email (`netid@queensu.ca`) or personal email
4. Verify your email

#### Step 2: Generate an Access Token

1. Log in to Hugging Face
2. Click your profile picture → **"Settings"**
3. Click **"Access Tokens"** in the left sidebar
4. Click **"New token"**
5. Give it a name (e.g., "CISC121-Project")
6. Select **"Read"** permission (that's all we need)
7. Click **"Generate"**
8. **Copy the token** (starts with `hf_...`)

> ⚠️ **Important:** Save your token somewhere safe! You can only see it once.

#### Step 3: Use Your Token

**Option A: Environment Variable (Recommended - More Secure)**

```bash
# On Linux/Mac, add to your ~/.bashrc or run before starting:
export HF_TOKEN="hf_your_token_here"

# On Windows PowerShell:
$env:HF_TOKEN="hf_your_token_here"

# On Windows Command Prompt:
set HF_TOKEN=hf_your_token_here
```

**Option B: Directly in Code (Quick but Less Secure)**

Open `app.py` and find this line:

```python
HF_TOKEN = os.environ.get("HF_TOKEN", None)
```

Replace it with:

```python
HF_TOKEN = "hf_your_token_here"
```

> ⚠️ **Security Note:** If you use Option B, don't share your code publicly with the token in it!

---

## 📚 Two Learning Paths

This project offers **two versions** of the same application:

### 🔧 Path 1: Procedural Programming (`app.py`)

**Best for:** Complete beginners, first-time programmers

**What you'll learn:**

- Step-by-step coding (do this, then that)
- Functions as building blocks
- Simple, linear thinking

**Example:**

```python
# Step 1: Define what happens when we greet someone
def greet(name):
    return f"Hello {name}!"

# Step 2: Create the interface
# Step 3: Connect the pieces
# Step 4: Launch!
```

---

### 🏗️ Path 2: Object-Oriented Programming (`app_oop.py` - Coming Soon)

**Best for:** Students ready to level up, future software engineers

**What you'll learn:**

- Classes and Objects (blueprints and instances)
- SOLID Principles (professional coding standards)
- Code organization and reusability

**SOLID Principles Explained Simply:**

| Letter | Principle             | Simple Explanation                                 |
| ------ | --------------------- | -------------------------------------------------- |
| **S**  | Single Responsibility | Each class does ONE job only                       |
| **O**  | Open/Closed           | Add features WITHOUT changing old code             |
| **L**  | Liskov Substitution   | Child classes can replace parent classes           |
| **I**  | Interface Segregation | Don't force classes to use methods they don't need |
| **D**  | Dependency Inversion  | Depend on abstractions, not concrete details       |

---

## 🗺️ Development Plan

This project will be developed in **small, incremental steps**. Each step builds on the previous one.

### Phase 1: Foundation ✅

- [x] Create basic project structure
- [x] Create README with development plan
- [x] Clean up procedural code with better comments

### Phase 2: Procedural Version ✅

- [x] Add clear section headers
- [x] Improve function documentation
- [x] Fix the camera input bug
- [x] Add error handling with explanations
- [x] Test with sample images

### Phase 3: OOP Version 🏗️

- [ ] Create class diagram
- [ ] Implement `ImageProcessor` class (S in SOLID)
- [ ] Implement `GradioInterface` class
- [ ] Implement `ModelConnector` class
- [ ] Connect all classes together
- [ ] Add OOP-specific comments and explanations

### Phase 4: Documentation 📚

- [ ] Create step-by-step guides
- [ ] Add visual diagrams
- [ ] Create glossary of terms
- [ ] Add exercises for students

---

## 📝 Glossary (Key Terms)

| Term             | Definition                                   | Example                                                    |
| ---------------- | -------------------------------------------- | ---------------------------------------------------------- |
| **API**          | A way for programs to talk to each other     | Sending an image to Hugging Face and getting back a result |
| **Function**     | A reusable block of code                     | `def greet(name):`                                         |
| **Gradio**       | A Python library for building web interfaces | `gr.Button("Click")`                                       |
| **Hugging Face** | A platform that hosts AI models              | We use their image classification model                    |
| **Model**        | An AI that has learned from data             | A model trained to recognize hand gestures                 |
| **Parameter**    | Input to a function                          | `name` in `greet(name)`                                    |
| **Return**       | Output from a function                       | `return "Hello!"`                                          |

---

## 🐛 Common Issues & Solutions

### Issue: "Could not analyze the image"

This is the most common issue! Here's how to fix it:

```
1. Check the terminal/console for error messages
2. Make sure you have an internet connection
3. Try setting up your Hugging Face token (see section above)
4. The model might be loading - wait 30-60 seconds on first run
```

### Issue: Camera not working

```
Solution: Grant browser permission to access your camera.
Look for a camera icon in your browser's address bar.
```

### Issue: `ModuleNotFoundError: No module named 'gradio'`

```bash
# Make sure you installed all requirements
pip install -r requirements.txt

# Or install individually
pip install gradio transformers torch Pillow
```

### Issue: `pip` command not found

```bash
# Try using pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt
```

### Issue: Model is slow (30-60 seconds)

```
This is normal! Here's what's happening:
1. First run downloads the AI model (~350 MB)
2. The model loads into memory
3. Subsequent runs will be faster (5-10 seconds)

Tip: Keep the app running instead of restarting it.
```

### Issue: `CUDA out of memory` or GPU errors

```bash
# The model can run on CPU instead of GPU
# This is handled automatically, but may be slower
```

### Issue: Installation takes forever

```
PyTorch is a large package (~2 GB). This is normal.
- On fast internet: 5-10 minutes
- On slow internet: 20-30 minutes

Tip: Use a campus network for faster downloads.
```

---

## ⚠️ Package Installation Tips & Avoiding Breakage

### Why Do Packages Break?

Software libraries (packages) are constantly being updated. Sometimes:

- A new version removes a feature you were using
- Two packages require different versions of the same dependency
- The package author makes breaking changes

### Best Practices to Avoid Problems

#### 1. Use Virtual Environments

Virtual environments keep your project's packages separate from other projects.

```bash
# Create a virtual environment
python -m venv cisc121_env

# Activate it (Linux/Mac)
source cisc121_env/bin/activate

# Activate it (Windows)
cisc121_env\Scripts\activate

# Now install packages - they stay in this environment only
pip install -r requirements.txt
```

#### 2. Pin Package Versions

Our `requirements.txt` uses minimum versions (`>=4.0.0`). For more stability, you can pin exact versions:

```
# Instead of:
gradio>=4.0.0

# Use exact versions:
gradio==4.44.0
```

#### 3. Update Packages Carefully

```bash
# See what's outdated
pip list --outdated

# Update one package at a time and test
pip install --upgrade gradio

# If something breaks, go back to the old version
pip install gradio==4.44.0
```

#### 4. Document What Works

If everything is working, save the exact versions:

```bash
# Save all current package versions
pip freeze > requirements-lock.txt

# Later, recreate the same environment
pip install -r requirements-lock.txt
```

### Common Dependency Conflicts

| Symptom                                   | Likely Cause                         | Solution                                       |
| ----------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| `ImportError` after update                | Package API changed                  | Install the previous version                   |
| `ModuleNotFoundError`                     | Missing dependency                   | Run `pip install -r requirements.txt`          |
| Version conflict warnings                 | Two packages need different versions | Use a virtual environment                      |
| `AttributeError: module has no attribute` | Gradio/transformers API changed      | Check the package documentation for new syntax |

### When Things Break (And They Will!)

1. **Don't panic** - this happens to everyone
2. **Read the error message** - it usually tells you what's wrong
3. **Search the error** - Copy the error message into Google
4. **Check the package's GitHub Issues** - Others may have the same problem
5. **Ask for help** - Piazza, office hours, or classmates

---

## 🤝 Contributing

This is a learning project! If you find bugs or have suggestions:

1. Create an Issue on GitHub
2. Describe the problem clearly
3. If you can fix it, submit a Pull Request!

---

## 📜 License

This project is for educational purposes at Queen's University.

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20-B90E31?style=flat-square" alt="Made with love"/>
  <img src="https://img.shields.io/badge/For-CISC%20121-002452?style=flat-square" alt="For CISC 121"/>
</p>

---

_Last Updated: November 2025_
