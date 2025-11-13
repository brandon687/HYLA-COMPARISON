# Hyla Stock Comparison Tool

A comprehensive tool for comparing supplier stock lists to make data-driven purchasing decisions.

**Now with a modern web interface!** Upload files via drag-and-drop, get instant analysis, and download professional reports.

## Two Ways to Use

### 🌐 Web Interface (Recommended)
- Beautiful drag-and-drop interface
- No command line needed
- Real-time progress indicators
- Multiple export formats
- **Try it now:** `python3 web_app.py` then visit http://localhost:5001

### 💻 Command Line
- Scriptable and automatable
- Perfect for batch processing
- Integration with workflows

## Overview

This tool compares OLD (previous offers) and NEW (current) stock lists from your supplier, providing detailed analysis of:
- Price changes (list prices and offer-to-list margins)
- Quantity availability trends
- New product offerings
- Removed/discontinued items
- Configuration-level aggregations for strategic insights

## Files in This Project

### Core Files
- **`web_app.py`** - Web interface (Flask application)
- **`stock_comparison_tool.py`** - Core comparison engine
- **`templates/index.html`** - Web dashboard UI
- **`COMPARISON_METHODOLOGY.md`** - Detailed documentation of comparison logic and strategy
- **`README.md`** - This file

### Documentation
- **`WEB_UI_GUIDE.md`** - How to use the web interface
- **`RAILWAY_DEPLOYMENT.md`** - Deploy to Railway (cloud hosting)
- **`READY_FOR_DEPLOYMENT.md`** - Deployment checklist and status

### Sample Files (Your Data)
- **`**NEW**Stock_List_Filtered_11112025 (4).xlsx`** - Current stock list (NEW)
- **`**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx`** - Previous offers (OLD)
- **`Stock_Comparison_Analysis_20251111_163429.xlsx`** - Your colleague's comparison output
- **`STOCK_COMPARISON_REPORT.md`** - Your colleague's detailed report
- **`TEST_Comparison_Output.xlsx`** - Test output from our tool

### Claude Code Integration
- **`.claude/hyla-stock-comparison.md`** - Skill definition for Claude Code

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
# or
pip install Flask pandas openpyxl Werkzeug
```

### Web Interface (Easiest!)

1. **Start the server:**
   ```bash
   python3 web_app.py
   ```

2. **Open your browser:**
   ```
   http://localhost:5001
   ```

3. **Upload and compare:**
   - Drag OLD file to left box
   - Drag NEW file to right box
   - Click "Compare Stock Lists"
   - Download your results!

### Command Line Usage

```bash
python stock_comparison_tool.py "<OLD_file.xlsx>" "<NEW_file.xlsx>" "<output_file.xlsx>"
```

**Example:**
```bash
python stock_comparison_tool.py \
  "**OLD**Stock_List_Filtered_11112025 (OFFERS).xlsx" \
  "**NEW**Stock_List_Filtered_11112025 (4).xlsx" \
  "Comparison_$(date +%Y%m%d).xlsx"
```

## What Gets Generated

The tool creates an Excel workbook with 7 sheets:

### 1. Summary
High-level statistics including:
- Total configurations (OLD vs NEW)
- Matching, removed, and new configurations
- Average price changes
- Total quantity metrics
- Net quantity change

### 2. All Comparisons
Complete comparison of all configurations with all metrics:
- Item counts (OLD vs NEW)
- Quantities (OLD vs NEW with changes)
- List prices (OLD vs NEW with changes)
- Offer prices (OLD only)
- **Offer-to-List changes** (strategic margin insights)

### 3. Price Increases
Configurations with rising list prices, sorted by % change.
**Action**: Consider purchasing before further increases.

### 4. Price Decreases
Configurations with falling list prices, sorted by % change.
**Action**: May indicate oversupply or declining demand; evaluate carefully.

### 5. Quantity Changes
All configurations sorted by quantity change.
**Action**: Large decreases suggest high demand; act quickly.

### 6. New Offers
Configurations that appear only in the NEW file.
**Action**: New inventory opportunities; evaluate market demand.

### 7. Removed Items
Configurations that appear only in the OLD file.
**Action**: No longer available; consider alternatives or stock up from other sources.

## Understanding the Comparison Logic

### Configuration Grouping
Items are grouped by:
```
Configuration = Model + Capacity + Lock Status + Grade
```

Example: `iPhone 14 Pro Max / 256GB / UNLOCKED / DLS B+`

This approach provides product-level insights rather than individual stock-keeping unit analysis.

### Key Metrics

#### 1. Quantity Metrics
- **OLD Qty**: Total available quantity in OLD file
- **NEW Qty**: Total available quantity in NEW file
- **Qty Change**: NEW Qty - OLD Qty
- **Qty Change %**: (Qty Change / OLD Qty) × 100

#### 2. Price Metrics
- **OLD List Price**: Average list price (OLD)
- **NEW List Price**: Average list price (NEW)
- **OLD Offer Price**: Average offer price (OLD)
- **List Price Change**: NEW List - OLD List
- **List Price Change %**: Change percentage

#### 3. Strategic Margin Metric
- **From Offer to List Price Change**: NEW List Price - OLD Offer Price
- **From Offer to List Price Change %**: Percentage change

This shows how much the current list price has changed relative to the previous offer price, indicating potential profit margins if you purchased at the old offer price.

## Purchasing Decision Framework

### High-Priority Opportunities
Look for configurations with:
1. **High Offer-to-List Change** (>30%): Substantial price increases suggest buying opportunity if you purchased at old offer prices
2. **Large Quantity Drops** (>50%): Indicates high demand; consider increasing orders
3. **Stable/Increasing Prices + Good Availability**: Safe bets for inventory

### Caution Indicators
1. **Removed Configurations**: Popular items no longer available; find alternatives
2. **Large Price Drops**: May indicate quality issues or declining demand
3. **Quantity Stagnation**: Items not moving might have demand problems

### Strategic Insights
Based on your test data:
- **859 OLD configurations** → **1,089 NEW configurations** (+26.7%)
- **823 matching configurations** (96% retention)
- **Average Offer-to-List change: +40.2%** (significant margin opportunity)
- **Net quantity change: -72,566 units** (-61% decrease, suggesting high sales velocity)

## Daily Workflow

### 1. Receive New Stock List
Save with date-stamped filename:
```
Stock_List_YYYYMMDD.xlsx
```

### 2. Run Comparison
```bash
python stock_comparison_tool.py \
  "Stock_List_20251110.xlsx" \
  "Stock_List_20251111.xlsx" \
  "Comparison_20251111.xlsx"
```

### 3. Review Summary Sheet
Check high-level metrics:
- New configurations available
- Average price changes
- Quantity trends

### 4. Analyze Detailed Sheets
Focus on:
- **Price Increases**: Buy before further increases
- **Quantity Changes**: Identify fast-moving items
- **New Offers**: Evaluate new opportunities

### 5. Make Purchasing Decisions
Prioritize based on:
- Profit margins (Offer-to-List changes)
- Demand signals (quantity drops)
- Market trends (new vs removed items)

## Data Quality Notes

### Duplicate Handling
The tool automatically removes duplicate `Item #` entries (keeping first occurrence):
- Typical: ~255 duplicates per OLD file
- Typical: ~1,751 duplicates per NEW file

### Missing Values
- `New Offer Price` may be missing in NEW files (handled as NaN)
- Calculations exclude missing values appropriately

### File Format Differences
- **OLD files**: Clean format with immediate headers
- **NEW files**: May contain metadata rows (automatically detected and skipped)

## Advanced Features

### Custom Output Filename
```bash
python stock_comparison_tool.py old.xlsx new.xlsx "Custom_Name_$(date +%Y%m%d_%H%M%S).xlsx"
```

### Programmatic Usage
```python
from stock_comparison_tool import StockComparator

comparator = StockComparator("old.xlsx", "new.xlsx", "output.xlsx")
success = comparator.run()

# Access comparison data
if success:
    df_comparison = comparator.df_comparison
    df_summary = comparator.generate_summary()
```

## Troubleshooting

### "Required column not found"
- Verify both files have all required columns:
  - Item #, Model, Capacity, Lock Status, Grade, Available Quantity, List Price

### "File not found"
- Check file paths and filenames (use quotes for names with spaces)
- Ensure files are in the expected directory

### Unexpected Results
- Review the Summary sheet first
- Check if files are truly different (see STOCK_COMPARISON_REPORT.md for example of identical files)
- Verify data quality in source files

## Future Enhancements

Potential additions:
- Historical trend analysis (tracking across multiple days)
- Automated email reports
- Configurable alert thresholds
- Database integration
- Web dashboard
- API endpoint for automated workflows

## Support

For questions or issues:
1. Review `COMPARISON_METHODOLOGY.md` for detailed logic
2. Check sample outputs in test files
3. Examine your colleague's report for reference analysis

## License

Internal tool for Hyla purchasing analysis.

---

**Last Updated**: November 11, 2025
**Version**: 1.0
**Author**: Stock Comparison Analysis System
