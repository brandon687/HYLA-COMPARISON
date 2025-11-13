# Execution Guide - What Happens When You Run the Tool

## Quick Answer

**Where files are created**: In the **same directory** where you run the command (your current working directory).

**What you need**: Just the OLD and NEW Excel files in the right place.

---

## Complete Step-by-Step Walkthrough

### Scenario 1: Files Are in the Same Folder as the Tool

#### Your Setup:
```
~/Desktop/HYLA COMPARISON SKILL/
├── compare_stocks.sh
├── stock_comparison_tool.py
├── OLD_Stock_File.xlsx          ← Your old file
└── NEW_Stock_File.xlsx          ← Your new file
```

#### Commands:
```bash
# 1. Open Terminal (Cmd+Space → "Terminal")

# 2. Navigate to the folder
cd ~/Desktop/"HYLA COMPARISON SKILL"

# 3. Run the comparison
./compare_stocks.sh "OLD_Stock_File.xlsx" "NEW_Stock_File.xlsx"
```

#### What Happens:
1. Tool reads both Excel files
2. Processes the data (5-30 seconds)
3. Creates output file: `Comparison_20251111_184530.xlsx` (with timestamp)
4. **File appears in the SAME folder**: `~/Desktop/HYLA COMPARISON SKILL/`
5. On Mac, it asks: "Open the output file now? (y/n)"
   - Press `y` → Opens in Excel automatically
   - Press `n` → You can open it manually later

#### Result:
```
~/Desktop/HYLA COMPARISON SKILL/
├── compare_stocks.sh
├── stock_comparison_tool.py
├── OLD_Stock_File.xlsx
├── NEW_Stock_File.xlsx
└── Comparison_20251111_184530.xlsx  ← NEW! Created here
```

---

### Scenario 2: Files Are in Your Downloads Folder

#### Your Setup:
```
~/Downloads/
├── Stock_List_Nov_10.xlsx       ← Your old file
└── Stock_List_Nov_11.xlsx       ← Your new file

~/Desktop/HYLA COMPARISON SKILL/
├── compare_stocks.sh
└── stock_comparison_tool.py
```

#### Option A: Copy Files to Tool Directory
```bash
# 1. Open Terminal

# 2. Copy files from Downloads to tool directory
cp ~/Downloads/Stock_List_Nov_10.xlsx ~/Desktop/"HYLA COMPARISON SKILL"/
cp ~/Downloads/Stock_List_Nov_11.xlsx ~/Desktop/"HYLA COMPARISON SKILL"/

# 3. Navigate to tool directory
cd ~/Desktop/"HYLA COMPARISON SKILL"

# 4. Run comparison
./compare_stocks.sh "Stock_List_Nov_10.xlsx" "Stock_List_Nov_11.xlsx"
```

**Output created in**: `~/Desktop/HYLA COMPARISON SKILL/`

#### Option B: Use Full Paths (Files Stay in Downloads)
```bash
# 1. Open Terminal

# 2. Navigate to tool directory
cd ~/Desktop/"HYLA COMPARISON SKILL"

# 3. Run with full paths
./compare_stocks.sh \
  ~/Downloads/Stock_List_Nov_10.xlsx \
  ~/Downloads/Stock_List_Nov_11.xlsx
```

**Output created in**: `~/Desktop/HYLA COMPARISON SKILL/` (where you ran the command)

#### Option C: Specify Output Location
```bash
# 1. Open Terminal

# 2. Navigate to tool directory
cd ~/Desktop/"HYLA COMPARISON SKILL"

# 3. Run with custom output location
./compare_stocks.sh \
  ~/Downloads/Stock_List_Nov_10.xlsx \
  ~/Downloads/Stock_List_Nov_11.xlsx \
  ~/Desktop/Results/Comparison_Nov_11.xlsx
```

**Output created in**: `~/Desktop/Results/` (exactly where you specified)

---

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ YOU: Open Terminal                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ YOU: cd ~/Desktop/"HYLA COMPARISON SKILL"                   │
│                                                             │
│ Now you're here: /Users/brandonin/Desktop/HYLA COMPAR...   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ YOU: ./compare_stocks.sh "old.xlsx" "new.xlsx"             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TOOL: Checking dependencies... ✓                           │
│ TOOL: Loading data... ✓                                    │
│ TOOL: OLD file: 4358 rows                                  │
│ TOOL: NEW file: 6971 rows                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TOOL: Cleaning data... ✓                                   │
│ TOOL: Grouping by configuration... ✓                       │
│ TOOL: OLD configurations: 861                              │
│ TOOL: NEW configurations: 1093                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TOOL: Comparing configurations... ✓                        │
│ TOOL: Matching: 829                                        │
│ TOOL: Removed: 32                                          │
│ TOOL: New: 264                                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TOOL: Generating summary... ✓                              │
│ TOOL: Exporting results... ✓                               │
│                                                             │
│ TOOL: Results exported to:                                 │
│       Comparison_20251111_184530.xlsx                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ TOOL: ✓ Success!                                           │
│ TOOL: Output file: Comparison_20251111_184530.xlsx        │
│                                                             │
│ TOOL: Open the output file now? (y/n)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ YOU: Press 'y' and Enter                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 🎉 Excel opens with your comparison report!                │
└─────────────────────────────────────────────────────────────┘
```

---

## Exact File Locations

### Rule 1: Output Goes to Current Directory
The output file is ALWAYS created in **your current working directory** (where you are when you run the command).

Check where you are:
```bash
pwd
# Shows: /Users/brandonin/Desktop/HYLA COMPARISON SKILL
```

Output will be created HERE.

### Rule 2: Unless You Specify Otherwise
If you provide a third argument (output filename), it goes there:

```bash
./compare_stocks.sh "old.xlsx" "new.xlsx" "~/Desktop/Results/my_comparison.xlsx"
```

Output goes to: `~/Desktop/Results/my_comparison.xlsx`

### Rule 3: Automatic Naming
If you don't specify an output name, it auto-names with timestamp:
- Format: `Comparison_YYYYMMDD_HHMMSS.xlsx`
- Example: `Comparison_20251111_184530.xlsx`

---

## Real Example - Let's Walk Through It

### Starting Point
You just downloaded two files from your supplier:
- `~/Downloads/**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx`
- `~/Downloads/**NEW**Stock_List_Filtered_11112025 (4).xlsx`

### Step 1: Open Terminal
```
Cmd + Space
Type: Terminal
Press: Enter
```

You see:
```
Last login: Tue Nov 11 18:48:46 on ttys000
brandonin@Mac ~ %
```

### Step 2: Navigate to Tool Directory
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
```

Terminal now shows:
```
brandonin@Mac HYLA COMPARISON SKILL %
```

You are now in: `/Users/brandonin/Desktop/HYLA COMPARISON SKILL`

### Step 3: Run the Comparison
```bash
./compare_stocks.sh \
  ~/Downloads/"**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" \
  ~/Downloads/"**NEW**Stock_List_Filtered_11112025 (4).xlsx"
```

### What You See:
```
Checking dependencies...
✓ Found: Python 3.9.13

Starting comparison...

================================================================================
STOCK LIST COMPARISON TOOL
================================================================================
OLD file: /Users/brandonin/Downloads/**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx
NEW file: /Users/brandonin/Downloads/**NEW**Stock_List_Filtered_11112025 (4).xlsx
Output:   Comparison_20251111_184530.xlsx
================================================================================
Loading data...
✓ Loaded OLD file: 4358 rows
✓ Loaded NEW file: 6971 rows

Cleaning data...
  OLD file: 4358 rows, 4103 unique items, 255 duplicates
  NEW file: 6971 rows, 5220 unique items, 1751 duplicates
✓ Data cleaned and ready for grouping

Grouping by configuration...
✓ OLD configurations: 861
✓ NEW configurations: 1093

Comparing configurations...
✓ Matching configurations: 829
✓ Removed configurations: 32
✓ New configurations: 264

Exporting results to Comparison_20251111_184530.xlsx...

Generating summary...
✓ Results exported successfully!

Generated sheets:
  1. Summary - High-level statistics
  2. All Comparisons - Complete comparison
  3. Price Increases - 829 configs
  4. Price Decreases - 829 configs
  5. Quantity Changes - All quantity movements
  6. New Offers - 264 new configurations
  7. Removed Items - 32 removed configurations

================================================================================
COMPARISON COMPLETE!
================================================================================

✓ Success!
Output file: Comparison_20251111_184530.xlsx

Open the output file now? (y/n)
```

### Step 4: Open the File
Press `y` and Enter.

Excel opens with the file: `Comparison_20251111_184530.xlsx`

### Where Is The File?
```bash
# Check:
ls -l Comparison_*.xlsx
```

Shows:
```
-rw-r--r--  1 brandonin  staff  45678  Nov 11 18:45 Comparison_20251111_184530.xlsx
```

Full path: `/Users/brandonin/Desktop/HYLA COMPARISON SKILL/Comparison_20251111_184530.xlsx`

---

## Common Questions

### Q: Can I run it from anywhere?
**A:** Yes, but the output will be created in your current directory.

```bash
# You're in Documents
cd ~/Documents

# Run the tool (with full path to tool)
~/Desktop/"HYLA COMPARISON SKILL"/compare_stocks.sh "old.xlsx" "new.xlsx"

# Output created in: ~/Documents/Comparison_*.xlsx
```

### Q: Can I organize files better?
**A:** Yes! Create a structure:

```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"

# Create folders
mkdir -p Stock_Files Results

# Move stock files
mv *.xlsx Stock_Files/ 2>/dev/null || true

# Run with organized structure
./compare_stocks.sh \
  "Stock_Files/old.xlsx" \
  "Stock_Files/new.xlsx" \
  "Results/Comparison_$(date +%Y%m%d).xlsx"
```

Result:
```
~/Desktop/HYLA COMPARISON SKILL/
├── compare_stocks.sh
├── stock_comparison_tool.py
├── Stock_Files/
│   ├── old.xlsx
│   └── new.xlsx
└── Results/
    └── Comparison_20251111.xlsx  ← Output here!
```

### Q: What if I'm in the wrong directory?
**A:** You'll see "File not found" error:

```
✗ Error: OLD file not found: old.xlsx
```

**Fix**: Navigate to the right place or use full paths.

### Q: Can I rename the output file?
**A:** Yes! Provide third argument:

```bash
./compare_stocks.sh "old.xlsx" "new.xlsx" "My_Daily_Comparison.xlsx"
```

Output: `My_Daily_Comparison.xlsx` (in current directory)

---

## Best Practice: Daily Workflow

### Recommended Setup
```
~/Desktop/HYLA COMPARISON SKILL/
├── compare_stocks.sh
├── stock_comparison_tool.py
├── Stock_Lists/          ← Put daily stock files here
│   ├── 2025-11-10.xlsx
│   ├── 2025-11-11.xlsx
│   └── 2025-11-12.xlsx
└── Comparisons/          ← Outputs go here
    ├── Comparison_20251110.xlsx
    ├── Comparison_20251111.xlsx
    └── Comparison_20251112.xlsx
```

### Daily Commands
```bash
# 1. Navigate
cd ~/Desktop/"HYLA COMPARISON SKILL"

# 2. Copy today's file from Downloads
cp ~/Downloads/Stock_List_Today.xlsx Stock_Lists/$(date +%Y-%m-%d).xlsx

# 3. Run comparison
./compare_stocks.sh \
  "Stock_Lists/2025-11-11.xlsx" \
  "Stock_Lists/2025-11-12.xlsx" \
  "Comparisons/Comparison_$(date +%Y%m%d).xlsx"

# 4. Open result
open "Comparisons/Comparison_$(date +%Y%m%d).xlsx"
```

---

## Summary: The Simple Answer

### Where you run it = Where output is created

```bash
cd /path/to/where/you/want/output
./path/to/tool/compare_stocks.sh "old.xlsx" "new.xlsx"
# Output appears HERE ↑
```

### Most Common Usage
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh "old_file.xlsx" "new_file.xlsx"
# Output: ~/Desktop/HYLA COMPARISON SKILL/Comparison_*.xlsx
```

**That's it!** The tool is smart enough to handle the rest.

---

## Quick Reference Card

| Scenario | Command | Output Location |
|----------|---------|----------------|
| Files in same folder | `./compare_stocks.sh "old.xlsx" "new.xlsx"` | Current directory |
| Files elsewhere | `./compare_stocks.sh ~/Downloads/old.xlsx ~/Downloads/new.xlsx` | Current directory |
| Custom output name | `./compare_stocks.sh "old.xlsx" "new.xlsx" "MyOutput.xlsx"` | Current directory |
| Custom output path | `./compare_stocks.sh "old.xlsx" "new.xlsx" ~/Desktop/MyOutput.xlsx` | ~/Desktop/ |

**Current directory** = Where you are when you run `pwd`
