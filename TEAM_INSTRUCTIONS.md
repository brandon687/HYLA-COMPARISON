# Hyla Stock Comparison Tool - Team Setup Instructions

## For Team Members Receiving This Tool

### What You're Getting
A tool that compares OLD vs NEW stock lists and generates analysis in 5 minutes (vs 2-3 hours manually).

---

## Setup (One Time - 3 Minutes)

### Step 1: Unzip the Package
Double-click `Hyla_Stock_Tool_20251111.zip` to extract it to your Desktop.

### Step 2: Open Terminal
1. Press `Cmd + Space`
2. Type `Terminal`
3. Press Enter

### Step 3: Run Setup
**Copy and paste these commands** into Terminal:

```bash
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
bash SETUP.sh
```

That's it! The setup script will:
- ✅ Check Python installation
- ✅ Install required packages (pandas, openpyxl)
- ✅ Configure the tool

---

## Daily Usage (5 Minutes)

Every day when you receive new stock lists:

### In Terminal, run:
```bash
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
./compare_stocks.sh "YOUR_OLD_FILE.xlsx" "YOUR_NEW_FILE.xlsx"
```

### Replace with actual filenames:
```bash
./compare_stocks.sh "Stock_Nov_10.xlsx" "Stock_Nov_11.xlsx"
```

The tool will:
1. ✅ Process both files
2. ✅ Generate comparison Excel file
3. ✅ Open it automatically (on Mac)

---

## Understanding the Output

Your output Excel file has **7 sheets**:

### 1. Summary
- High-level stats: configurations count, price changes, quantity changes
- **Start here every day** (30 seconds)

### 2. All Comparisons
- Complete dataset with all configurations
- Reference when you need details

### 3. Price Increases
- Items with rising prices (sorted highest first)
- **Action**: Consider buying before further increases

### 4. Price Decreases
- Items with falling prices (sorted lowest first)
- **Caution**: May indicate low demand or quality issues

### 5. Quantity Changes
- Items with changing availability
- **Action**: Large drops = high demand, order quickly

### 6. New Offers
- Brand new items from supplier
- **Action**: Evaluate market fit

### 7. Removed Items
- Items no longer available
- **Action**: Find alternatives

---

## Key Metric to Watch

**"From Offer to List Price Change %"**

This shows your potential profit margin:
- **>40%**: Excellent opportunity
- **30-40%**: Good opportunity
- **20-30%**: Moderate opportunity
- **<20%**: Low margin, pass unless high volume

---

## Example Workflow

**Morning Routine (5 min total):**

1. Download new stock list from supplier
2. Open Terminal
3. Run comparison:
   ```bash
   cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
   ./compare_stocks.sh "yesterday.xlsx" "today.xlsx"
   ```
4. Review Summary sheet (30 sec)
5. Check Price Increases (1 min)
6. Check Quantity Changes (1 min)
7. Make purchasing decisions (2 min)

**Done!**

---

## Troubleshooting

### "Permission denied"
```bash
chmod +x compare_stocks.sh
```

### "pandas not found"
```bash
pip3 install --user pandas openpyxl
```

### "File not found"
Make sure you're in the right directory:
```bash
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
pwd  # Shows current directory
```

### Python not installed
Download from: https://www.python.org/downloads/

---

## Tips for Success

### 1. Consistent File Naming
Use dates in filenames:
- `Stock_List_2025-11-10.xlsx`
- `Stock_List_2025-11-11.xlsx`

### 2. Keep Files Organized
Create a folder structure:
```
~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION/
├── Stock_Files/
│   ├── 2025-11-10_Stock.xlsx
│   └── 2025-11-11_Stock.xlsx
└── Results/
    └── Comparison_20251111.xlsx
```

### 3. Focus on Patterns
Don't analyze every row. Look for:
- Consistently high-demand items
- Good margin opportunities (>30%)
- Popular models/configurations

### 4. Act Fast
When you see:
- Margin >40% ✓
- Quantity drop >50% ✓
- Popular model ✓

**Place order immediately!**

---

## What This Tool Does

### Configuration-Based Analysis
Instead of comparing 6,000+ individual items, it groups by:
- **Model** (e.g., iPhone 14 Pro Max)
- **Capacity** (e.g., 256GB)
- **Lock Status** (e.g., UNLOCKED)
- **Grade** (e.g., DLS B+)

This gives you ~1,000 meaningful configurations to analyze.

### Key Calculations
1. **Quantity Changes**: Shows demand velocity
2. **Price Changes**: Shows supplier pricing trends
3. **Offer→List Changes**: Shows YOUR profit potential
4. **New/Removed**: Shows catalog changes

---

## Need Help?

### Documentation Included
- **START_HERE.txt**: Basic overview
- **QUICK_DEPLOY.md**: 1-page setup guide
- **QUICK_START_GUIDE.md**: Daily workflow details
- **README.md**: Complete reference guide
- **DEPLOYMENT_GUIDE.md**: Detailed setup instructions

### Common Questions

**Q: Is my data secure?**
A: Yes! Everything runs locally on your computer. No data leaves your machine.

**Q: Can I run this on Windows?**
A: The tool is built for Mac but can be adapted. Contact your IT department.

**Q: What if I make a mistake?**
A: The tool only reads files, never modifies them. Your original files are safe.

**Q: How do I update the tool?**
A: Get the latest zip file from your team lead and repeat setup.

---

## Success Metrics

After using this tool regularly:

### Time Savings
- **Before**: 2-3 hours per comparison
- **After**: 5 minutes per comparison
- **Savings**: 95% time reduction

### Better Decisions
- Data-driven purchasing
- Faster response to opportunities
- Reduced stockouts
- Better margin identification

### ROI
**One good purchasing decision can pay for months of analysis time!**

---

## Quick Command Reference

```bash
# Setup (one-time)
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
bash SETUP.sh

# Daily use
./compare_stocks.sh "old.xlsx" "new.xlsx"

# Check if tool is ready
ls -la stock_comparison_tool.py compare_stocks.sh

# Navigate to tool directory
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
```

---

## Getting Started Checklist

- [ ] Unzipped the package to Desktop
- [ ] Opened Terminal
- [ ] Ran `bash SETUP.sh` successfully
- [ ] Tested with sample files
- [ ] Reviewed output Excel file
- [ ] Read QUICK_START_GUIDE.md
- [ ] Understand the 7 output sheets
- [ ] Know what "Offer→List Change %" means
- [ ] Ready to use daily!

---

## Contact

**Questions about**:
- **Setup**: Check DEPLOYMENT_GUIDE.md
- **Daily use**: Check QUICK_START_GUIDE.md
- **Methodology**: Check COMPARISON_METHODOLOGY.md
- **Technical issues**: Contact your team lead

---

**You're ready to transform your stock analysis workflow!**

Start tomorrow with your first daily comparison and see the difference.

---

*Tool Version: 1.0 | Last Updated: November 11, 2025*
