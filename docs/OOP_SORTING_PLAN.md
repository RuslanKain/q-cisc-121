# 🏗️ OOP Version: Sorting & Searching Algorithm Visualizer

## 📋 Overview

This document outlines the plan for `app_oop.py` - an interactive educational tool that lets students:

1. **Capture multiple hand gesture images**
2. **Build custom input arrays** (control duplicates, ordering)
3. **Visualize sorting/searching algorithms step-by-step**
4. **Compare algorithm behaviors** (stability, complexity cases)

---

## 🎯 Educational Goals

Students will learn:

- **Sorting Algorithms**: Bubble Sort, Merge Sort, Quick Sort
- **Searching Algorithms**: Binary Search
- **Complexity Cases**: Best, Average, Worst case inputs
- **Algorithm Properties**: In-place vs Out-of-place, Stable vs Unstable
- **Recursion Visualization**: Depth, partitioning, merging

---

## 🖐️ Gesture Ranking System

To enable sorting, gestures need a defined **ordering**. We'll use this ranking:

| Rank | Gesture            | Emoji | Description              |
| ---- | ------------------ | ----- | ------------------------ |
| 1    | `fist`             | ✊    | Closed fist (0 fingers)  |
| 2    | `one`              | ☝️    | One finger up            |
| 3    | `two_up` / `peace` | ✌️    | Two fingers (peace sign) |
| 4    | `three`            | 🤟    | Three fingers            |
| 5    | `four`             | 🖖    | Four fingers             |
| 6    | `palm` / `stop`    | 🖐️    | Open palm (5 fingers)    |
| 7    | `ok`               | 👌    | OK sign                  |
| 8    | `like`             | 👍    | Thumbs up                |
| 9    | `dislike`          | 👎    | Thumbs down              |
| 10   | `rock`             | 🤘    | Rock sign                |

> **Stability Test**: Duplicates of the same gesture can be distinguished by their **capture order** (e.g., "peace_1", "peace_2"). Stable algorithms preserve this order; unstable ones may swap them.

---

## 🖼️ UI Layout Plan

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  🎓 CISC 121 - Sorting & Searching Visualizer (OOP Version)                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────┐  ┌─────────────────────────────────────────┐│
│  │  📸 CAPTURE IMAGES          │  │  ⚙️ ALGORITHM SETTINGS                  ││
│  │  [Webcam] [Upload]          │  │                                         ││
│  │                             │  │  Algorithm: [Dropdown]                  ││
│  │  [Capture & Add to List]    │  │  • Bubble Sort (Early Exit)             ││
│  │                             │  │  • Merge Sort                           ││
│  │  Captured: 5 images         │  │  • Quick Sort                           ││
│  └─────────────────────────────┘  │                                         ││
│                                   │  Quick Sort Options:                    ││
│                                   │  Pivot: [First|Median-of-3|Random]      ││
│                                   │  Partition: [2-way|3-way]               ││
│                                   │                                         ││
│                                   │  [▶️ Run Step-by-Step]                   ││
│                                   │  [⏩ Run Full Animation]                 ││
│                                   └─────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────────────────────┤
│  📊 IMAGE LIST (Drag to reorder, click + to duplicate)                      │
│                                                                              │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐              │
│  │ IMG │  │ IMG │  │ IMG │  │ IMG │  │ IMG │  │ IMG │  │ IMG │              │
│  │  1  │  │  2  │  │  3  │  │  4  │  │  5  │  │  6  │  │  7  │              │
│  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘  └─────┘              │
│    ✌️       ☝️       🖐️       ✌️       ✊       👍       ✌️                   │
│   [2]      [1]      [5]      [2]      [0]      [8]      [2]                 │
│    ×        ×        ×        ×        ×        ×        ×   [Clear All]    │
│                                                                              │
│  Input Controls:                                                             │
│  [Sort Ascending] [Sort Descending] [Reverse] [Shuffle] [Add Duplicates]    │
├──────────────────────────────────────────────────────────────────────────────┤
│  🔄 ALGORITHM VISUALIZATION                                                  │
│                                                                              │
│  Step 3/15: Comparing indices [2] and [3]                                   │
│  ───────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  (Visual representation changes based on algorithm - see below)             │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  📈 STATISTICS                                                               │
│  Comparisons: 12  |  Swaps: 4  |  Recursive Depth: 2  |  Time: 0.003s       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Algorithm Visualizations

### 1️⃣ Bubble Sort (In-Place, Stable)

**Visual Approach:**

- Highlight the **two elements being compared** (yellow border)
- Show **swap animation** when elements exchange
- Mark **sorted portion** (right side) with green background
- Show **early exit** when no swaps occur in a pass

```
Pass 1:  [✌️] [☝️] [🖐️] [✌️] [✊]
          ↑    ↑
        comparing...

Pass 1:  [☝️] [✌️] [🖐️] [✌️] [✊]
               ↑    ↑
             swapped! comparing next...

Pass 1:  [☝️] [✌️] [✌️] [🖐️] [✊]  ← 🖐️ bubbled right
                         ════════
                         (sorted)
```

**Best/Worst Case Setup:**

- **Best Case**: Pre-sorted array → 1 pass, no swaps, early exit
- **Worst Case**: Reverse sorted → n-1 passes, maximum swaps

---

### 2️⃣ Merge Sort (Out-of-Place, Stable)

**Visual Approach:**

- Show **recursive splitting** with vertical depth
- Each recursion level shifts images **down**
- **Merge operation** shows elements moving back **up** in sorted order
- Use **indentation** to show recursive depth

```
Depth 0:  [✌️] [☝️] [🖐️] [✌️] [✊] [👍]
              ↓ split ↓

Depth 1:  [✌️] [☝️] [🖐️]          [✌️] [✊] [👍]
              ↓ split ↓               ↓ split ↓

Depth 2:  [✌️]  [☝️] [🖐️]        [✌️]  [✊] [👍]
           ↓      ↓    ↓           ↓     ↓    ↓

Depth 3:  [✌️]  [☝️]  [🖐️]       [✌️]  [✊]  [👍]
           ↑ merge ↑                ↑ merge ↑

Depth 2:  [☝️] [✌️]  [🖐️]        [✊] [✌️]  [👍]
               ↑ merge ↑               ↑ merge ↑

Depth 1:  [☝️] [✌️] [🖐️]          [✊] [✌️] [👍]
                    ↑ merge ↑

Depth 0:  [☝️] [✊] [✌️] [✌️] [🖐️] [👍]  ← SORTED!
```

**Key Teaching Points:**

- Divide phase: O(log n) depth
- Merge phase: O(n) work per level
- Total: O(n log n) always
- **Stable**: Notice duplicate ✌️ maintain their relative order

---

### 3️⃣ Quick Sort (In-Place, Unstable)

**Visual Approach:**

- Highlight **pivot** with special border/color
- Show **partitioning** with left/right pointers
- Display **pivot strategies** visually
- Demonstrate **stability issue** with duplicates

#### Pivot Selection Strategies:

```
First Element:        [✌️] [☝️] [🖐️] [✊] [👍]
                       ↑
                     pivot

Median of Three:      [✌️] [☝️] [🖐️] [✊] [👍]
                       ↑         ↑         ↑
                     first    middle     last
                     Median = ✌️ (comparing ranks 2, 5, 8)

Random:               [✌️] [☝️] [🖐️] [✊] [👍]
                                 ↑
                            random pick
```

#### 2-Way vs 3-Way Partitioning:

**2-Way Partitioning:**

```
Pivot = ✌️ (rank 2)

[✌️] [☝️] [🖐️] [✊] [👍]
  P   ←L            R→

Result: [✊] [☝️] | [✌️] | [🖐️] [👍]
         < pivot    P     > pivot
```

**3-Way Partitioning (Dutch National Flag):**

```
Pivot = ✌️ (rank 2)

[✌️] [☝️] [✌️] [✊] [✌️] [👍]
  P

Result: [✊] [☝️] | [✌️] [✌️] [✌️] | [🖐️] [👍]
         < pivot      = pivot        > pivot

(All duplicates grouped together - more efficient!)
```

**Instability Demonstration:**

```
Before: [✌️₁] [✌️₂] [☝️] [✌️₃]  (subscripts show capture order)
After:  [☝️] [✌️₃] [✌️₁] [✌️₂]  (order changed! UNSTABLE)
```

---

### 4️⃣ Binary Search

**Visual Approach:**

- Require **sorted input** (prompt to sort first if not)
- Highlight **search range** with bracket
- Show **mid calculation** and comparison
- Narrow range with animation

```
Target: 🖐️ (rank 5)

Step 1:  [✊] [☝️] [✌️] [✌️] [🖐️] [👍] [👎]
         [===========↑============]
                    mid=3 (✌️)
                    ✌️ < 🖐️ → search right

Step 2:  [✊] [☝️] [✌️] [✌️] [🖐️] [👍] [👎]
                              [====↑====]
                              mid=5 (👍)
                              👍 > 🖐️ → search left

Step 3:  [✊] [☝️] [✌️] [✌️] [🖐️] [👍] [👎]
                              [↑]
                              mid=4 (🖐️)
                              FOUND! ✅
```

---

## 🎮 Input Case Setup Guide

### Creating Best/Average/Worst Cases:

| Algorithm                     | Best Case                     | Average Case    | Worst Case                       |
| ----------------------------- | ----------------------------- | --------------- | -------------------------------- |
| **Bubble Sort**               | Already sorted                | Random order    | Reverse sorted                   |
| **Merge Sort**                | Any order (always O(n log n)) | Any order       | Any order                        |
| **Quick Sort (First Pivot)**  | Random/balanced splits        | Random order    | Already sorted or reverse sorted |
| **Quick Sort (Median-of-3)**  | Random order                  | Random order    | Harder to create                 |
| **Quick Sort (Random Pivot)** | N/A (probabilistic)           | Random order    | Extremely unlikely               |
| **Binary Search**             | Target in middle              | Random position | Target at ends or missing        |

### UI Controls for Case Creation:

```
┌─────────────────────────────────────────────────────────────┐
│  📊 INPUT CASE BUILDER                                      │
│                                                             │
│  Presets:                                                   │
│  [Already Sorted ↑] [Reverse Sorted ↓] [Random] [Many Dupes]│
│                                                             │
│  Manual Controls:                                           │
│  • Drag images to reorder                                   │
│  • Click [+] under image to add duplicate                   │
│  • Click [×] to remove image                                │
│                                                             │
│  Current Input Analysis:                                    │
│  "7 elements, 3 unique, partially sorted (40%)"            │
│  "For Quick Sort (first pivot): This is WORST CASE"        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ OOP Class Structure (SOLID Principles)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLASS DIAGRAM                                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│   GestureImage      │     │   GestureRanking    │
├─────────────────────┤     ├─────────────────────┤
│ - image: PIL.Image  │     │ - RANKINGS: dict    │
│ - gesture: str      │     ├─────────────────────┤
│ - rank: int         │     │ + get_rank(gesture) │
│ - capture_id: int   │     │ + compare(a, b)     │
│ - emoji: str        │     │ + get_emoji(gesture)│
├─────────────────────┤     └─────────────────────┘
│ + __lt__, __eq__    │              ▲
│ + display()         │              │ uses
└─────────────────────┘              │
         │                           │
         │ contains                  │
         ▼                           │
┌─────────────────────┐              │
│   ImageList         │──────────────┘
├─────────────────────┤
│ - images: list      │
│ - history: list     │
├─────────────────────┤
│ + add(image)        │
│ + remove(index)     │
│ + duplicate(index)  │
│ + shuffle()         │
│ + is_sorted()       │
│ + save_state()      │
│ + get_display()     │
└─────────────────────┘
         │
         │ operated on by
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    <<interface>>                                    │
│                    SortingAlgorithm                                 │
├─────────────────────────────────────────────────────────────────────┤
│ + sort(image_list) → Generator[Step]                               │
│ + name: str                                                         │
│ + is_stable: bool                                                   │
│ + is_in_place: bool                                                │
└─────────────────────────────────────────────────────────────────────┘
         ▲
         │ implements
         │
    ┌────┴────┬────────────┬────────────────┐
    │         │            │                │
┌───┴───┐ ┌───┴───┐ ┌──────┴──────┐ ┌───────┴───────┐
│Bubble │ │Merge  │ │ QuickSort   │ │ BinarySearch  │
│Sort   │ │Sort   │ ├─────────────┤ └───────────────┘
└───────┘ └───────┘ │pivot_strategy│
                    │partition_type│
                    └─────────────┘

┌─────────────────────┐
│   Step (dataclass)  │
├─────────────────────┤
│ - type: StepType    │  (COMPARE, SWAP, SPLIT, MERGE, FOUND, etc.)
│ - indices: list     │
│ - description: str  │
│ - depth: int        │
│ - substep: int      │
│ - array_state: list │
└─────────────────────┘

┌─────────────────────┐
│   Visualizer        │
├─────────────────────┤
│ - current_step: int │
│ - steps: list[Step] │
├─────────────────────┤
│ + render_step()     │  → Returns Gradio-compatible display
│ + next_step()       │
│ + prev_step()       │
│ + play_animation()  │
└─────────────────────┘

┌─────────────────────┐
│   GradioApp         │  (Composes all above)
├─────────────────────┤
│ - image_list        │
│ - visualizer        │
│ - classifier        │
├─────────────────────┤
│ + create_ui()       │
│ + handle_capture()  │
│ + handle_sort()     │
│ + handle_search()   │
└─────────────────────┘
```

### SOLID Principles Applied:

| Principle                     | Application                                                                                        |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| **S** - Single Responsibility | Each class has ONE job: `GestureImage` holds data, `BubbleSort` sorts, `Visualizer` displays       |
| **O** - Open/Closed           | New sorting algorithms can be added without modifying existing code (just implement the interface) |
| **L** - Liskov Substitution   | Any `SortingAlgorithm` can be swapped (BubbleSort, MergeSort, QuickSort all work the same way)     |
| **I** - Interface Segregation | `SortingAlgorithm` interface is minimal; search uses a separate interface                          |
| **D** - Dependency Inversion  | `GradioApp` depends on abstractions (`SortingAlgorithm`), not concrete implementations             |

---

## 📝 Implementation Phases

### Phase 1: Core Data Structures

- [ ] `GestureImage` class with ranking/comparison
- [ ] `GestureRanking` with emoji mappings
- [ ] `ImageList` with basic operations
- [ ] `Step` dataclass for algorithm steps

### Phase 2: Sorting Algorithms

- [ ] `SortingAlgorithm` interface
- [ ] `BubbleSort` with early exit
- [ ] `MergeSort` with depth tracking
- [ ] `QuickSort` with configurable pivot/partition

### Phase 3: Binary Search

- [ ] `BinarySearch` with step generation
- [ ] Sorted-input validation

### Phase 4: Visualization

- [ ] `Visualizer` class with step rendering
- [ ] HTML/CSS for highlighting, depth indication
- [ ] Animation controls (play, pause, step)

### Phase 5: Gradio UI

- [ ] Image capture/upload section
- [ ] Image list with manipulation controls
- [ ] Algorithm selection and configuration
- [ ] Statistics display

### Phase 6: Polish & Testing

- [ ] Best/worst case detection
- [ ] Stability demonstration mode
- [ ] Performance comparison view
- [ ] Educational tooltips and explanations

---

## ✅ Design Decisions (Confirmed)

| Question                     | Decision                                      | Details                                                         |
| ---------------------------- | --------------------------------------------- | --------------------------------------------------------------- |
| **Merge Sort Visualization** | **Static stacked depth levels**               | Each recursion depth shown as a separate row, visually stacked  |
| **Image Display**            | **Scrollable horizontal list**                | Capped at **100 elements max**, optimized sizing to prevent lag |
| **Stability Labels**         | **Always visible + highlight on instability** | Show "✌️₁", "✌️₂" always; **red highlight when order violated** |
| **Performance**              | **Cache + Manual assignment**                 | Cache ML predictions AND allow manual gesture override          |

---

## ⚠️ Instability Detection & Demonstration

### How Quick Sort Breaks Stability

**Stability** means: if two elements are equal, their relative order is preserved after sorting.

**Quick Sort is UNSTABLE** because during partitioning, equal elements can swap positions.

### Guaranteed Instability Scenario:

**Setup Instructions for Students:**

1. Capture **3+ images of the SAME gesture** (e.g., three peace signs ✌️)
2. Add them to the list - they'll be labeled: `✌️₁`, `✌️₂`, `✌️₃`
3. Add **one different gesture** with a **lower rank** (e.g., fist ✊)
4. Arrange: `[✌️₁] [✌️₂] [✌️₃] [✊]`
5. Run **Quick Sort with First Pivot**

**What Happens:**

```
Initial:    [✌️₁] [✌️₂] [✌️₃] [✊]
             ↑ pivot (rank 2)

Partition:  Elements < pivot go left, ≥ pivot go right
            [✊] swaps with [✌️₁]

After:      [✊] [✌️₂] [✌️₃] [✌️₁]  ← ✌️₁ moved to end!
                              ⚠️ INSTABILITY DETECTED
                              (Original order was ₁,₂,₃ → now ₂,₃,₁)
```

### Visual Indicator:

```
┌──────────────────────────────────────────────────────────────┐
│  ⚠️ INSTABILITY DETECTED!                                    │
│                                                              │
│  Before: [✌️₁] [✌️₂] [✌️₃]  (capture order: 1, 2, 3)        │
│  After:  [✌️₂] [✌️₃] [✌️₁]  (capture order: 2, 3, 1) ← WRONG │
│                       ═══                                    │
│                   (highlighted in red)                       │
│                                                              │
│  Quick Sort does NOT preserve the original order of equal    │
│  elements. For stable sorting, use Merge Sort or Bubble Sort.│
└──────────────────────────────────────────────────────────────┘
```

### Comparison Table for Students:

| Algorithm   | Stable? | Test Result with [✌️₁][✌️₂][✌️₃][✊]   |
| ----------- | ------- | -------------------------------------- |
| Bubble Sort | ✅ Yes  | [✊][✌️₁][✌️₂][✌️₃] - order preserved  |
| Merge Sort  | ✅ Yes  | [✊][✌️₁][✌️₂][✌️₃] - order preserved  |
| Quick Sort  | ❌ No   | [✊][✌️?][✌️?][✌️?] - order may change |

---

## 📏 Size & Performance Constraints

### Element Limits:

- **Maximum elements**: 100 (prevents UI lag from image copies)
- **Minimum for algorithms**: 3 (meaningful sorting demonstration)
- **Recommended range**: 5-15 elements for clear visualization

### Image Sizing Strategy:

```
Elements    Thumbnail Size    Display
─────────────────────────────────────
1-5         80×80 px         Large, comfortable
6-10        60×60 px         Medium, still clear
11-20       45×45 px         Smaller, emoji more prominent
21-50       30×30 px         Compact, rely on emoji
51-100      20×20 px         Minimal, emoji-focused
```

### Memory Optimization:

- Store images as **compressed thumbnails** (not full resolution)
- Original high-res images stored separately for detail view
- Lazy loading for elements outside visible scroll area

---

## 🚀 Ready to Implement!

Plan approved with all clarifications. Implementation order:

### Phase 1: Core Data Structures ✅ COMPLETE

- [x] `GestureImage` class with ranking/comparison + capture_id
- [x] `GestureRanking` with emoji mappings
- [x] `ImageList` with 100-element cap
- [x] `Step` dataclass for algorithm steps

### Phase 2: Sorting Algorithms ✅ COMPLETE

- [x] `SortingAlgorithm` interface (ABC with abstract methods)
- [x] `BubbleSort` with early exit
- [x] `MergeSort` with depth tracking (static stacked view)
- [x] `QuickSort` with configurable pivot/partition + instability detection
- [x] **NEW:** Worst-case analysis and detection
- [x] **NEW:** Partition balance analysis

#### Quick Sort Worst Case Scenarios (Implemented):

| Scenario                    | Problem                    | Solution                  |
| --------------------------- | -------------------------- | ------------------------- |
| Sorted data + First pivot   | 0/n-1 splits → O(n²)       | Use Median-of-3 or Random |
| Reverse sorted + Last pivot | Same problem               | Use Median-of-3 or Random |
| Many duplicates + 2-way     | Duplicates all on one side | Use 3-way partitioning    |
| Nearly sorted + First pivot | Mostly unbalanced splits   | Use Random pivot          |

### Phase 3: Binary Search ✅ COMPLETE

- [x] `SearchAlgorithm` interface (ABC with abstract methods)
- [x] `LinearSearch` - O(n), works on unsorted data
- [x] `BinarySearchIterative` - O(log n), requires sorted input
- [x] `BinarySearchRecursive` - O(log n), with depth tracking
- [x] Sorted-input validation with helpful error messages
- [x] Efficiency comparison demonstrations (Linear vs Binary scaling)

### Phase 4: Visualization ✅ COMPLETE

- [x] `VisualizationState` Enum (IDLE, READY, PLAYING, PAUSED, etc.)
- [x] `StepRenderer` ABC - Base class for all renderers
- [x] `BubbleSortRenderer` - Highlights comparisons, swaps, sorted region
- [x] `MergeSortRenderer` - Shows depth levels with indentation
- [x] `QuickSortRenderer` - Shows pivot, partition, instability warnings
- [x] `BinarySearchRenderer` - Shows search range narrowing
- [x] `LinearSearchRenderer` - Shows sequential checking
- [x] `RendererFactory` - Factory Pattern for creating renderers
- [x] `VisualizationConfig` - Configuration dataclass
- [x] `Visualizer` - Main controller with state machine

### Phase 5: Gradio UI

- [ ] Image capture/upload with caching
- [ ] Manual gesture assignment option
- [ ] Algorithm selection and configuration
- [ ] Statistics display

### Phase 6: Polish & Testing

- [x] Best/worst case detection (added to Phase 2)
- [ ] Instability demo scenario preset
- [ ] Performance optimization for 100 elements
- [ ] Educational tooltips

---

**Phases 1, 2, 3 & 4 Complete! Ready for Phase 5 (Gradio UI)** 🎓
