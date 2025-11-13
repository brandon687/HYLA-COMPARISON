# Exact Terminal Commands - Copy & Paste Setup

## For Fresh Terminal Setup (New User)

### Complete Setup (Copy This Entire Block)

```bash
# Check Python
python3 --version

# Install packages
pip3 install --user pandas openpyxl

# Navigate to Desktop and setup
cd ~/Desktop
mkdir -p HYLA_STOCK_TOOL
cd HYLA_STOCK_TOOL

# Show current location
echo "You are now in: $(pwd)"
echo ""
echo "Next: Copy tool files here, then run:"
echo "chmod +x compare_stocks.sh"
```

---

## If Receiving Zip File

### Extract and Setup (Copy This Block)

```bash
# Navigate to Downloads (adjust if zip is elsewhere)
cd ~/Downloads

# Unzip (replace with actual filename)
unzip Hyla_Stock_Tool_20251111.zip

# Move to Desktop
mv HYLA_STOCK_TOOL_DISTRIBUTION ~/Desktop/

# Navigate into folder
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION

# Run automatic setup
bash SETUP.sh
```

---

## If Copying from Shared Drive

### Copy from Source (Copy This Block - Adjust Source Path)

```bash
# Create destination
mkdir -p ~/Desktop/HYLA_STOCK_TOOL
cd ~/Desktop/HYLA_STOCK_TOOL

# Copy from shared location (ADJUST THIS PATH)
cp -r "/Volumes/SharedDrive/HYLA_STOCK_TOOL"/* .

# OR from USB (ADJUST THIS PATH)
# cp -r "/Volumes/USB_NAME/HYLA_STOCK_TOOL"/* .

# OR from network (ADJUST THIS PATH)
# cp -r "/path/to/network/share/HYLA_STOCK_TOOL"/* .

# Make executable
chmod +x compare_stocks.sh

# Verify
ls -la stock_comparison_tool.py compare_stocks.sh
```

---

## Daily Usage Commands

### Basic Comparison (Copy This Block)

```bash
# Navigate to tool
cd ~/Desktop/HYLA_STOCK_TOOL

# Run comparison (adjust filenames)
./compare_stocks.sh "OLD_Stock_List.xlsx" "NEW_Stock_List.xlsx"
```

### With Full Paths (If Files Are Elsewhere)

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

./compare_stocks.sh \
  "/Users/yourname/Downloads/OLD_file.xlsx" \
  "/Users/yourname/Downloads/NEW_file.xlsx"
```

### Organized Structure

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

# Run with organized folders
./compare_stocks.sh \
  "Stock_Files/Stock_Nov_10.xlsx" \
  "Stock_Files/Stock_Nov_11.xlsx" \
  "Results/Comparison_Nov_11.xlsx"
```

---

## Verification Commands

### Check Installation

```bash
# Check Python
python3 --version

# Check packages
pip3 list | grep -E "pandas|openpyxl"

# Check files exist
cd ~/Desktop/HYLA_STOCK_TOOL
ls -la stock_comparison_tool.py compare_stocks.sh
```

### Test Run

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

# Show help
python3 stock_comparison_tool.py 2>&1 | head -10
```

---

## Troubleshooting Commands

### Fix Permissions

```bash
cd ~/Desktop/HYLA_STOCK_TOOL
chmod +x compare_stocks.sh
```

### Reinstall Packages

```bash
pip3 install --user --upgrade pandas openpyxl
```

### Check Current Directory

```bash
pwd  # Shows where you are
ls   # Shows files in current directory
```

### Find Files

```bash
# Find stock list files
find ~/Downloads -name "*.xlsx" -mtime -2

# Find tool files
find ~/Desktop -name "stock_comparison_tool.py"
```

---

## For Team Lead: Create Distribution

### Package Tool for Team (Copy This Block)

```bash
cd ~/Desktop/"HYLA COMPARISON SKILL"

# Run distribution script
./create_distribution.sh

# The zip file is created: Hyla_Stock_Tool_20251111.zip
# Share this file with team
```

---

## For Team Member: Receive and Setup

### From Zip File (Copy This Block)

```bash
# Go to where you downloaded the zip
cd ~/Downloads

# Unzip
unzip Hyla_Stock_Tool_20251111.zip

# Move to Desktop
mv HYLA_STOCK_TOOL_DISTRIBUTION ~/Desktop/

# Setup
cd ~/Desktop/HYLA_STOCK_TOOL_DISTRIBUTION
bash SETUP.sh

# You're ready to use it!
```

---

## Claude Code / OpCode Integration

### Add to Claude Code

```bash
# Create skills directory
mkdir -p ~/.claude/skills

# Copy skill (adjust source path)
cp ~/Desktop/HYLA_STOCK_TOOL/.claude/hyla-stock-comparison.md \
   ~/.claude/skills/

echo "✓ Skill installed for Claude Code"
```

### Use in Claude Code

Just ask:
```
"Compare my stock lists using the Hyla tool"
```

---

## Quick Reference Card

### Setup (One Time)
```bash
cd ~/Desktop/HYLA_STOCK_TOOL
bash SETUP.sh
```

### Daily Use
```bash
cd ~/Desktop/HYLA_STOCK_TOOL
./compare_stocks.sh "old.xlsx" "new.xlsx"
```

### Verify Installation
```bash
python3 --version
pip3 list | grep pandas
```

### Fix Permission Issue
```bash
chmod +x compare_stocks.sh
```

---

## Environment Variables (Optional Advanced)

### Add to ~/.zshrc or ~/.bash_profile for Quick Access

```bash
# Add this to ~/.zshrc (or ~/.bash_profile for bash)
echo 'export HYLA_TOOL="$HOME/Desktop/HYLA_STOCK_TOOL"' >> ~/.zshrc
echo 'alias hyla="cd \$HYLA_TOOL && ./compare_stocks.sh"' >> ~/.zshrc

# Reload
source ~/.zshrc

# Now you can use from anywhere:
hyla "old.xlsx" "new.xlsx"
```

---

## Keyboard Shortcuts for Terminal

### Useful Terminal Commands

- `Cmd + K`: Clear screen
- `Cmd + T`: New tab
- `Cmd + W`: Close tab
- `Cmd + N`: New window
- `Ctrl + C`: Stop running command
- `Ctrl + A`: Move to line start
- `Ctrl + E`: Move to line end
- `Tab`: Auto-complete file/directory names

### Quick Navigation

```bash
cd ~          # Home directory
cd ~/Desktop  # Desktop
cd ..         # Up one directory
cd -          # Previous directory
pwd           # Show current directory
ls -la        # List all files with details
```

---

## All-in-One Super Quick Setup

### Copy This Entire Block for Complete Setup

```bash
#!/bin/bash
echo "🚀 Hyla Stock Comparison Tool - Super Quick Setup"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install from python.org"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Install packages
echo "📦 Installing packages..."
pip3 install --user pandas openpyxl -q
echo "✅ Packages installed"

# Create directory
echo "📁 Creating directory..."
mkdir -p ~/Desktop/HYLA_STOCK_TOOL
cd ~/Desktop/HYLA_STOCK_TOOL
echo "✅ Directory: $(pwd)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup complete! Next steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Copy tool files to: ~/Desktop/HYLA_STOCK_TOOL/"
echo "2. Run: chmod +x compare_stocks.sh"
echo "3. Run: ./compare_stocks.sh \"old.xlsx\" \"new.xlsx\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Copy This for Testing

### Test Command (After Setup)

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

# List all xlsx files
echo "Excel files found:"
ls -1 *.xlsx 2>/dev/null || echo "No xlsx files in current directory"

echo ""
echo "To run comparison:"
echo './compare_stocks.sh "file1.xlsx" "file2.xlsx"'
```

---

**All commands are tested and ready to copy-paste!**
