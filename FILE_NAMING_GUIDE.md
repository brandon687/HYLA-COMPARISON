# File Naming Guide - How to Reference Your Files

## The Confusion Explained

You saw this command:
```bash
./compare_stocks.sh "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" "**NEW**Stock_List_Filtered_11112025 (4).xlsx"
```

**Question**: Do I need to rename my files to have "OLD" and "NEW" in the name?

**Answer**: NO! These are just YOUR ACTUAL FILE NAMES. Use whatever names your files have.

---

## How It Actually Works

### The Tool Doesn't Care About File Names

The tool just needs TWO Excel files:
- **First argument** = The older/previous file (can be named ANYTHING)
- **Second argument** = The newer/current file (can be named ANYTHING)

You're just telling the tool:
- "Compare THIS file (first one)"
- "Against THIS file (second one)"

---

## Real Examples

### Example 1: Your Current Files

**Your actual files are named**:
```
**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx
**NEW**Stock_List_Filtered_11112025 (4).xlsx
```

**Command**:
```bash
./compare_stocks.sh \
  "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" \
  "**NEW**Stock_List_Filtered_11112025 (4).xlsx"
```

You're literally typing the EXACT file names that exist in your folder.

---

### Example 2: Files Named With Dates

**Your files are named**:
```
Stock_List_2025-11-10.xlsx
Stock_List_2025-11-11.xlsx
```

**Command**:
```bash
./compare_stocks.sh \
  "Stock_List_2025-11-10.xlsx" \
  "Stock_List_2025-11-11.xlsx"
```

---

### Example 3: Files Named by Supplier

**Your files are named**:
```
Supplier_Morning_Report.xlsx
Supplier_Evening_Report.xlsx
```

**Command**:
```bash
./compare_stocks.sh \
  "Supplier_Morning_Report.xlsx" \
  "Supplier_Evening_Report.xlsx"
```

---

### Example 4: Files With Weird Names

**Your files are named**:
```
download (1).xlsx
download (2).xlsx
```

**Command**:
```bash
./compare_stocks.sh \
  "download (1).xlsx" \
  "download (2).xlsx"
```

---

## How to Find Your Actual File Names

### In Terminal:
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
ls *.xlsx
```

This shows ALL Excel files with their EXACT names.

Example output:
```
**NEW**Stock_List_Filtered_11112025 (4).xlsx
**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx
Stock_Comparison_Analysis_20251111_163429.xlsx
```

Then copy-paste the exact names into your command.

---

## The Easy Way: Tab Completion

### Use Tab to Auto-Complete File Names

1. Start typing:
   ```bash
   ./compare_stocks.sh "**O
   ```

2. Press `Tab` key

3. Terminal auto-completes:
   ```bash
   ./compare_stocks.sh "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx"
   ```

4. Add space, start typing second file:
   ```bash
   ./compare_stocks.sh "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" "**N
   ```

5. Press `Tab` again

6. Terminal auto-completes:
   ```bash
   ./compare_stocks.sh "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" "**NEW**Stock_List_Filtered_11112025 (4).xlsx"
   ```

**This prevents typos!**

---

## Why Quotes Matter

### Files with spaces NEED quotes:

❌ **WRONG** (without quotes):
```bash
./compare_stocks.sh **OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx **NEW**Stock_List_Filtered_11112025 (4).xlsx
```
Error: Too many arguments

✅ **RIGHT** (with quotes):
```bash
./compare_stocks.sh "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" "**NEW**Stock_List_Filtered_11112025 (4).xlsx"
```

### Files without spaces DON'T need quotes (but quotes are safe):

✅ **Both work**:
```bash
./compare_stocks.sh old.xlsx new.xlsx
./compare_stocks.sh "old.xlsx" "new.xlsx"
```

**Best practice**: Always use quotes to be safe.

---

## Common Mistakes

### Mistake 1: Not Using Actual File Names
❌ **WRONG**:
```bash
./compare_stocks.sh "old.xlsx" "new.xlsx"
```
When your files are actually named:
```
Stock_List_Nov_10.xlsx
Stock_List_Nov_11.xlsx
```

**Error**: File not found

✅ **RIGHT**:
```bash
./compare_stocks.sh "Stock_List_Nov_10.xlsx" "Stock_List_Nov_11.xlsx"
```

### Mistake 2: Wrong Order
The tool compares: `OLD` (first) vs `NEW` (second)

❌ **WRONG** (backwards):
```bash
./compare_stocks.sh "Stock_Nov_11.xlsx" "Stock_Nov_10.xlsx"
```
This compares Nov 11 as OLD and Nov 10 as NEW (backwards!)

✅ **RIGHT**:
```bash
./compare_stocks.sh "Stock_Nov_10.xlsx" "Stock_Nov_11.xlsx"
```

### Mistake 3: Files Not in Same Directory
❌ **WRONG**:
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh "old.xlsx" "new.xlsx"
```
When files are actually in `~/Downloads/`

**Error**: File not found

✅ **RIGHT** (Option 1 - Copy files):
```bash
cp ~/Downloads/*.xlsx ~/Desktop/"HYLA COMPARISON SKILL"/
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh "old.xlsx" "new.xlsx"
```

✅ **RIGHT** (Option 2 - Use full paths):
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh ~/Downloads/old.xlsx ~/Downloads/new.xlsx
```

---

## Pro Tips

### Tip 1: Rename Files for Easier Use

If your supplier sends files with complex names, rename them:

```bash
# Before
cp ~/Downloads/"Supplier_Stock_List_Filtered_11112025_Morning_Report_v2_FINAL.xlsx" \
   ~/Desktop/"HYLA COMPARISON SKILL"/Stock_Nov_11.xlsx

# Now use simple name
./compare_stocks.sh "Stock_Nov_10.xlsx" "Stock_Nov_11.xlsx"
```

### Tip 2: Use Consistent Naming Convention

Pick a format and stick to it:

**Option A - Dates**:
```
Stock_2025-11-10.xlsx
Stock_2025-11-11.xlsx
Stock_2025-11-12.xlsx
```

**Option B - Days**:
```
Stock_Monday.xlsx
Stock_Tuesday.xlsx
Stock_Wednesday.xlsx
```

**Option C - Descriptive**:
```
Stock_Yesterday.xlsx
Stock_Today.xlsx
```

### Tip 3: Keep Old Files Organized

Create a folder structure:
```bash
mkdir -p ~/Desktop/"HYLA COMPARISON SKILL"/Archives
mv Stock_2025-11-*.xlsx Archives/  # Move old files
```

---

## Your Specific Situation

### What You Have:
```
~/Desktop/HYLA COMPARISON SKILL/
├── **OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx
└── **NEW**Stock_List_Filtered_11112025 (4).xlsx
```

### Exact Command to Use:
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"

./compare_stocks.sh \
  "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" \
  "**NEW**Stock_List_Filtered_11112025 (4).xlsx"
```

### Why This Works:
- `"**OLD**..."` is the ACTUAL file name (with the asterisks and everything)
- `"**NEW**..."` is the ACTUAL file name
- You're not renaming anything
- You're just typing what the files are actually called

---

## Tomorrow's Workflow

### When You Get New Files Tomorrow:

**Step 1**: Download new file from supplier

**Step 2**: Put it in your folder with a clear name:
```bash
cp ~/Downloads/new_supplier_file.xlsx \
   ~/Desktop/"HYLA COMPARISON SKILL"/Stock_Nov_12.xlsx
```

**Step 3**: Compare with yesterday's file:
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh \
  "**NEW**Stock_List_Filtered_11112025 (4).xlsx" \
  "Stock_Nov_12.xlsx"
```

**Note**: Yesterday's NEW file becomes today's OLD file!

---

## Quick Reference

```bash
# List files to see exact names
ls *.xlsx

# Use Tab completion to avoid typos
./compare_stocks.sh "[start typing and press Tab]"

# Always use quotes for safety
./compare_stocks.sh "file1.xlsx" "file2.xlsx"

# Order matters: OLD first, NEW second
./compare_stocks.sh "older_file.xlsx" "newer_file.xlsx"
```

---

## Summary

**You DON'T need to rename files to "old" and "new"**

**You DO need to**:
1. Use the EXACT file names as they exist
2. Put quotes around names with spaces
3. Put the older file FIRST, newer file SECOND
4. Make sure files are in the same directory (or use full paths)

**Just type whatever your files are actually named!**

---

## Test It Now

```bash
# 1. See your actual file names
cd ~/Desktop/"HYLA COMPARISON SKILL"
ls *.xlsx

# 2. Copy the exact names you see
# 3. Paste them in the command:
./compare_stocks.sh "[exact name 1]" "[exact name 2]"
```

That's it! 🎉
