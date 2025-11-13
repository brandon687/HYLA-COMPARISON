# Hyla Stock Comparison - Cheat Sheet

## 3 Steps to Run

### 1. Open Terminal
```
Cmd + Space → type "Terminal" → Enter
```

### 2. Navigate to Folder
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
```

### 3. Run Comparison
```bash
./compare_stocks.sh "OLD_file.xlsx" "NEW_file.xlsx"
```

**Output appears in same folder!**

---

## Where Files Go

| You run from | Output goes to |
|--------------|----------------|
| `~/Desktop/HYLA COMPARISON SKILL/` | Same folder |
| Any directory | That directory |

**Simple rule**: Output = where you run the command

---

## File Locations Quick Reference

```
YOUR SITUATION:
  Tool:       ~/Desktop/HYLA COMPARISON SKILL/compare_stocks.sh
  OLD file:   ~/Desktop/HYLA COMPARISON SKILL/old.xlsx
  NEW file:   ~/Desktop/HYLA COMPARISON SKILL/new.xlsx

RUN THIS:
  cd ~/Desktop/"HYLA COMPARISON SKILL"
  ./compare_stocks.sh "old.xlsx" "new.xlsx"

OUTPUT APPEARS:
  ~/Desktop/HYLA COMPARISON SKILL/Comparison_20251111_185530.xlsx
  (Same folder where you ran it!)
```

---

## Custom Output Location

### Want output elsewhere?
```bash
./compare_stocks.sh "old.xlsx" "new.xlsx" "~/Desktop/Results/output.xlsx"
```

Output goes to: `~/Desktop/Results/output.xlsx`

---

## Files in Different Locations

### Stock files in Downloads?
```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh ~/Downloads/old.xlsx ~/Downloads/new.xlsx
```

Output: `~/Desktop/HYLA COMPARISON SKILL/Comparison_*.xlsx`

---

## Quick Commands

```bash
# Check where you are
pwd

# List files here
ls

# Navigate to tool
cd ~/Desktop/"HYLA COMPARISON SKILL"

# Run comparison
./compare_stocks.sh "old.xlsx" "new.xlsx"

# Find output file
ls -lt Comparison_*.xlsx | head -1
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Permission denied" | `chmod +x compare_stocks.sh` |
| "File not found" | Use `pwd` to check location |
| "pandas not found" | `pip3 install --user pandas openpyxl` |

---

## Daily Workflow

```bash
# Morning routine (5 min)
cd ~/Desktop/"HYLA COMPARISON SKILL"
./compare_stocks.sh "yesterday.xlsx" "today.xlsx"
# Press 'y' to open
# Review Summary sheet
# Check Price Increases
# Make decisions
```

---

## That's It!

**Remember**: Output file appears in the **same directory** where you run the command.

For detailed help: `EXECUTION_GUIDE.md`
