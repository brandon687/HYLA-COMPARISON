# Hyla Stock Comparison Skill

## Description
Analyzes and compares OLD and NEW stock lists from your supplier to provide actionable purchasing insights. This skill groups items by configuration (Model + Capacity + Lock Status + Grade) and calculates quantity changes, price movements, and strategic metrics to help optimize purchasing decisions.

## When to Use
- Daily comparison of new stock lists vs previous offers
- Evaluating supplier pricing changes
- Identifying inventory opportunities
- Tracking quantity availability trends
- Making data-driven purchasing decisions

## What It Does
1. Loads and validates OLD and NEW stock list Excel files
2. Cleans data (removes duplicates, handles missing values)
3. Groups items by configuration (Model + Capacity + Lock Status + Grade)
4. Calculates comprehensive comparison metrics:
   - Quantity changes (absolute and percentage)
   - List price changes (absolute and percentage)
   - Offer-to-List price changes (strategic profit margin insights)
5. Generates detailed Excel report with multiple analysis sheets:
   - Summary statistics
   - All comparisons
   - Price increases
   - Price decreases
   - Quantity changes
   - New offers
   - Removed items

## Key Insights Generated
- **Price Increases**: Configurations with rising prices (consider buying before further increases)
- **Price Decreases**: Configurations with falling prices (may indicate oversupply or declining demand)
- **Quantity Drops**: Large decreases suggest high demand (act quickly)
- **New Opportunities**: New configurations available from supplier
- **Removed Items**: Configurations no longer available (consider alternatives)
- **Profit Margins**: Offer-to-List price changes show potential margins

## Instructions

When the user asks to compare stock lists:

1. **Identify the files**:
   - Ask user to confirm which is the OLD file (previous offers)
   - Ask user to confirm which is the NEW file (current stock list)
   - Suggest output filename with timestamp

2. **Run the comparison**:
   ```bash
   python stock_comparison_tool.py "<OLD_file>" "<NEW_file>" "<output_file>"
   ```

3. **Validate the output**:
   - Check that the output file was created
   - Open the Summary sheet to review high-level statistics
   - Highlight key findings

4. **Present insights**:
   - Summarize total configurations (OLD vs NEW)
   - Highlight matching, new, and removed configurations
   - Point out significant price changes
   - Note quantity trends
   - Identify top opportunities for purchasing

5. **Provide strategic recommendations**:
   - Focus on configurations with high offer-to-list price changes (>30%)
   - Flag quantity drops >50% (high demand indicators)
   - Evaluate new configurations for market fit
   - Warn about removed items if they were popular

## Example Usage

```
User: "I have new stock lists to compare"