#!/bin/bash
#
# compare_stocks.sh - Easy wrapper for daily stock comparison
#
# Usage:
#   ./compare_stocks.sh <old_file> <new_file>
#
# Example:
#   ./compare_stocks.sh "OLD_Stock.xlsx" "NEW_Stock.xlsx"
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -lt 2 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo ""
    echo "Usage: $0 <old_file> <new_file> [output_file]"
    echo ""
    echo "Example:"
    echo '  ./compare_stocks.sh "OLD_Stock.xlsx" "NEW_Stock.xlsx"'
    exit 1
fi

OLD_FILE="$1"
NEW_FILE="$2"
OUTPUT_FILE="${3:-Comparison_$(date +%Y%m%d_%H%M%S).xlsx}"

# Check if files exist
if [ ! -f "$OLD_FILE" ]; then
    echo -e "${RED}Error: OLD file not found: $OLD_FILE${NC}"
    exit 1
fi

if [ ! -f "$NEW_FILE" ]; then
    echo -e "${RED}Error: NEW file not found: $NEW_FILE${NC}"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 not found${NC}"
    exit 1
fi

# Check if required packages are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Required Python packages not installed${NC}"
    echo "Please run: pip install pandas openpyxl"
    exit 1
fi

# Run the comparison
echo -e "${GREEN}Starting comparison...${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/stock_comparison_tool.py" "$OLD_FILE" "$NEW_FILE" "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Success!${NC}"
    echo -e "Output file: ${GREEN}$OUTPUT_FILE${NC}"
    echo ""
    echo -e "${YELLOW}📦 Files created:${NC}"
    echo -e "  ✓ Excel report: ${GREEN}$OUTPUT_FILE${NC}"
    echo -e "  ✓ HTML dashboard: ${GREEN}${OUTPUT_FILE%.xlsx}_Dashboard.html${NC}"
    echo -e "  ✓ Download package: ${GREEN}${OUTPUT_FILE%.xlsx}_Package.zip${NC}"
    echo ""
    echo -e "${YELLOW}💡 Tip: Excel and HTML opened automatically!${NC}"
    echo -e "   Share the ZIP file with your team via email/Slack"
else
    echo -e "${RED}✗ Comparison failed${NC}"
    exit 1
fi
