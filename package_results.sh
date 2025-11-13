#!/bin/bash
#
# Package comparison results into a distributable zip
#

# Find the most recent comparison files
EXCEL_FILE=$(ls -t Executive_Comparison*.xlsx 2>/dev/null | head -1)
HTML_FILE="${EXCEL_FILE%.xlsx}_Dashboard.html"

if [ -z "$EXCEL_FILE" ]; then
    echo "No comparison files found!"
    exit 1
fi

# Create package directory
PACKAGE_DIR="Comparison_Package_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PACKAGE_DIR"

# Copy files
cp "$EXCEL_FILE" "$PACKAGE_DIR/"
cp "$HTML_FILE" "$PACKAGE_DIR/" 2>/dev/null

# Create README
cat > "$PACKAGE_DIR/README.txt" << 'README'
STOCK COMPARISON RESULTS
========================

FILES INCLUDED:
- Executive_Comparison.xlsx: Full Excel workbook with 7 sheets
- Executive_Comparison_Dashboard.html: Visual dashboard for CEO

HOW TO USE:
1. Open Dashboard HTML in any web browser for quick overview
2. Open Excel file for detailed analysis

EXCEL SHEETS:
1. Summary - KPIs + Top 20 insights
2. All Comparisons - Complete data
3-7. Filtered views (Price changes, Qty changes, New/Removed)

Questions? See main documentation.
README

# Create zip
ZIP_NAME="Comparison_Results_$(date +%Y%m%d_%H%M%S).zip"
zip -r "$ZIP_NAME" "$PACKAGE_DIR" > /dev/null

# Cleanup
rm -rf "$PACKAGE_DIR"

echo "✓ Package created: $ZIP_NAME"
ls -lh "$ZIP_NAME" | awk '{print "Size: " $5}'

