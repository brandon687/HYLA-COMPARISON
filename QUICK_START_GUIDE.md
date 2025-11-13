# Quick Start Guide - Stock Comparison Tool

## For Daily Use

### Option 1: Simple Shell Script (Recommended)
```bash
./compare_stocks.sh "OLD_Stock.xlsx" "NEW_Stock.xlsx"
```
- Automatically names output with timestamp
- Validates files exist
- Checks dependencies
- Offers to open result when done

### Option 2: Python Script Directly
```bash
python3 stock_comparison_tool.py "OLD_Stock.xlsx" "NEW_Stock.xlsx"
```

### Option 3: Custom Output Name
```bash
./compare_stocks.sh "OLD_Stock.xlsx" "NEW_Stock.xlsx" "Daily_Comparison_Nov11.xlsx"
```

## Understanding Your Results

### Step 1: Open the Output Excel File
You'll see 7 sheets. Start with **Summary**.

### Step 2: Check Summary Stats
Look for:
- **Total Configurations**: How many product configs OLD vs NEW
- **Matching Configurations**: How many stayed the same
- **Avg to Offer Price Change (%)**: Your potential margin indicator

### Step 3: Review Key Sheets

#### Price Increases
Products getting more expensive.
**What to do**: Consider buying now before prices go up more.

#### Quantity Changes
Sort by largest decreases (negative numbers at top).
**What to do**: Big drops = high demand = order more.

#### New Offers
Brand new products available.
**What to do**: Evaluate if they fit your market.

#### Removed Items
Products no longer available.
**What to do**: Find alternatives or stock up elsewhere.

## Key Metric: "From Offer to List Price Change %"

**This is your most important number!**

Example:
- OLD Offer Price: $200
- NEW List Price: $280
- Change: $80 (40%)

**What it means**: If you bought at the old offer price ($200), you could potentially sell at the new list price ($280) for a $80 margin.

**Target**: Look for changes >30% for good opportunities.

## Real Example from Your Data

```
iPhone 14 / 256GB / UNLOCKED / DLS A+
- OLD: 680 units @ $234 offer
- NEW: 174 units @ $355 list
- Offer→List: +52% ($121 increase)
- Quantity: -74% (high demand!)
```

**Decision**: High demand (qty dropped 74%), good margin (52%), but limited stock now (174 units). Act fast if this model fits your market.

## Daily Workflow (5 Minutes)

1. **Download** new stock list from supplier
2. **Run** comparison:
   ```bash
   ./compare_stocks.sh yesterday.xlsx today.xlsx
   ```
3. **Open** Summary sheet - scan the stats
4. **Check** Price Increases - note any critical items
5. **Review** Quantity Changes - find high-demand items
6. **Make** purchasing decisions based on margin + demand

## When to Buy

### High Priority ✓
- Offer→List change >40%
- Quantity drop >50%
- Popular models

### Medium Priority ~
- Offer→List change 20-40%
- Stable quantity
- Good availability

### Low Priority ✗
- Offer→List change <20%
- Quantity increasing (low demand)
- Removed items (risky)

## Troubleshooting

### "Required column not found"
File format issue. Check that file has: Item #, Model, Capacity, Grade, Lock Status, Available Quantity, List Price

### "File not found"
Use quotes around filenames with spaces:
```bash
./compare_stocks.sh "OLD File.xlsx" "NEW File.xlsx"
```

### Numbers Look Wrong
1. Check you didn't swap OLD and NEW files
2. Verify files are actually different (not duplicates)
3. Look at the Summary sheet dates/timestamps

## Tips for Success

### 1. Consistent Naming
Use dates in filenames:
- `Stock_List_20251111_OLD.xlsx`
- `Stock_List_20251111_NEW.xlsx`

### 2. Keep History
Save comparison outputs:
- `Comparison_20251111.xlsx`
- `Comparison_20251112.xlsx`
- Track trends over time

### 3. Focus on Patterns
Don't analyze every single item. Look for:
- Consistently high-demand configs
- Stable margin opportunities
- New trending models

### 4. Act Fast on High-Demand Items
When you see:
- Quantity drops >60%
- Good margins (>30%)
- Popular models

Place orders immediately before stock runs out.

## Example Decision Tree

```
Configuration found in comparison:
│
├─ Is Offer→List change >30%?
│  ├─ YES: Good margin opportunity ✓
│  └─ NO: Low margin, skip unless high volume
│
├─ Did Quantity drop >50%?
│  ├─ YES: High demand, act fast! ✓✓
│  └─ NO: Normal/low demand
│
├─ Is it a popular model?
│  ├─ YES: Safe bet ✓
│  └─ NO: Evaluate market fit first
│
└─ Final decision: Combine above factors
   - All ✓✓: IMMEDIATE BUY
   - Two ✓: STRONG BUY
   - One ✓: CONSIDER
   - None: SKIP
```

## Contact & Support

Questions? Check:
1. **README.md** - Full documentation
2. **COMPARISON_METHODOLOGY.md** - Detailed logic explanation
3. **Test files** - See examples of what output should look like

---

**Remember**: This tool provides insights. You make the final purchasing decisions based on your market knowledge, cash flow, and business strategy.

**Daily habit**: Run comparison every morning when supplier updates stock list. Takes 5 minutes, could save thousands in better purchasing decisions.
