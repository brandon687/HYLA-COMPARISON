# Stock List Comparison Methodology

## Overview
This document outlines the methodology for comparing daily stock lists from your supplier to help make better purchasing decisions.

## Data Sources

### 1. NEW Stock List
- **File Format**: Excel (.xlsx)
- **Header Row**: Row 8 (0-indexed: row 7)
- **Structure**: Contains header rows with metadata (last updated timestamp, filters applied)
- **Typical Size**: ~7,000 rows with ~5,200 unique items

### 2. OLD Stock List (Previous Offers)
- **File Format**: Excel (.xlsx)
- **Header Row**: Row 1 (0-indexed: row 0)
- **Structure**: Clean format with immediate headers
- **Typical Size**: ~4,000 rows with ~4,100 unique items

## Key Columns

Both files contain these critical columns:
- `Item #`: Unique identifier for each stock item
- `Model`: Phone model (e.g., "iPhone 14 Pro Max")
- `Capacity`: Storage capacity (e.g., "128GB", "256GB")
- `Grade`: Condition grade (e.g., "DLS A+", "DLS B+", "TPS A+")
- `Lock Status`: Carrier lock status (e.g., "UNLOCKED", "LOCKED")
- `Available Quantity`: Number of units available
- `List Price`: Current list price
- `New Offer Price`: Supplier's offer price (may be NaN in NEW file)
- `Warehouse`: Stock location
- `Category`: Product category (e.g., "Phones")
- `Make`: Manufacturer (e.g., "Apple")

## Comparison Strategy

### Level 1: Configuration-Based Grouping
Instead of comparing individual `Item #` entries, items are grouped by **configuration**:

```
Configuration = Model + Capacity + Lock Status + Grade
```

**Rationale**: Multiple individual items can represent the same product configuration. This approach provides insights at the product level rather than the stock-keeping unit level.

### Level 2: Aggregated Metrics
For each configuration, calculate:

1. **Item Count**
   - OLD Item Count: Number of unique Item #s in OLD file
   - NEW Item Count: Number of unique Item #s in NEW file

2. **Quantity Metrics**
   - OLD Qty: Sum of Available Quantity across all items in configuration (OLD)
   - NEW Qty: Sum of Available Quantity across all items in configuration (NEW)
   - Qty Change: NEW Qty - OLD Qty
   - Qty Change %: (Qty Change / OLD Qty) × 100

3. **Pricing Metrics**
   - OLD List Price: Average List Price across items in configuration (OLD)
   - NEW List Price: Average List Price across items in configuration (NEW)
   - OLD Offer Price: Average New Offer Price (from OLD file)
   - List Price Change $: NEW List Price - OLD List Price
   - List Price Change %: (List Price Change $ / OLD List Price) × 100

4. **Strategic Pricing Insight**
   - From Offer to List Price Change $: NEW List Price - OLD Offer Price
   - From Offer to List Price Change %: ((NEW List Price - OLD Offer Price) / OLD Offer Price) × 100

   **Key Insight**: This metric shows how much the NEW list price has changed relative to the previous OFFER price, indicating potential profit margins or pricing strategy changes.

## Output Structure

The comparison produces multiple sheets/views:

### 1. Summary Sheet
High-level statistics:
- Total configurations (OLD vs NEW)
- Matching configurations
- Removed configurations (in OLD but not NEW)
- New configurations (in NEW but not OLD)
- Total items count
- Average price changes
- Total quantity metrics
- Net quantity change

### 2. All Comparisons Sheet
Complete comparison of all configurations with all calculated metrics.

### 3. Price Increases Sheet
Configurations where `List Price Change %` > 0, sorted by change amount.
**Purchase Decision**: Consider buying before prices increase further.

### 4. Price Decreases Sheet
Configurations where `List Price Change %` < 0, sorted by change amount.
**Purchase Decision**: May indicate declining demand or oversupply.

### 5. Quantity Changes Sheet
Configurations with significant quantity changes.
**Purchase Decision**: Large decreases may indicate high demand; act quickly.

### 6. New Offers Sheet
Configurations that appear only in the NEW file.
**Purchase Decision**: New inventory opportunities; evaluate demand.

### 7. Removed Items Sheet
Configurations that appear only in the OLD file.
**Purchase Decision**: No longer available; consider alternatives.

## Data Quality Considerations

### Duplicate Handling
- Multiple rows with the same `Item #` are consolidated
- Strategy: Keep first occurrence or aggregate (depending on analysis needs)
- Typical duplicates: ~255 per file

### Missing Values
- `New Offer Price` may be NaN (null) in NEW file
- `Transaction Price` often has missing values (~12%)
- Handle appropriately in calculations (use pandas `.dropna()` or `.fillna()`)

### Data Type Conversions
- `Item #`: Convert to string for consistent comparison
- Numeric columns: Ensure proper float/int types
- Text columns: Strip whitespace

## Strategic Insights for Purchasing

### 1. Profit Margin Analysis
Focus on configurations where:
```
From Offer to List Price Change % > 30%
```
This indicates substantial price increases from the offer price you might have purchased at previously.

### 2. Inventory Velocity
Monitor configurations with:
```
Qty Change % < -50%
```
Large quantity drops suggest high demand; consider increasing orders.

### 3. New Opportunities
Evaluate new configurations with:
- High quantity (indicating supplier confidence)
- Competitive pricing vs market
- Popular models/grades

### 4. Risk Indicators
- Removed configurations: May indicate supplier challenges or discontinued items
- Price volatility: Large swings may indicate market uncertainty
- Quantity stagnation: Items not moving might have demand issues

## Automation Considerations

For daily processing:
1. **File Naming Convention**: Use consistent date-stamped names
2. **Header Detection**: Automatically detect header row in NEW file (look for "Item #")
3. **Exception Handling**: Log missing columns, data quality issues
4. **Historical Tracking**: Store results for trend analysis
5. **Alert System**: Flag significant changes (e.g., >50% price change)

## Next Steps

To create a reusable skill:
1. Python script with command-line arguments for file paths
2. Configurable thresholds for alerts
3. HTML/Excel report generation
4. Email notification capability
5. Database integration for historical analysis
