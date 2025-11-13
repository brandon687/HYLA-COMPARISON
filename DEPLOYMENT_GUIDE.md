# Hyla Stock Comparison Tool - Deployment Guide

## Quick Deploy (Copy-Paste Ready)

This guide will help you or your team deploy the Hyla Stock Comparison Tool on any Mac with a fresh terminal.

---

## Prerequisites Check

Before starting, ensure you have:
- macOS (any recent version)
- Terminal access
- Admin/sudo privileges (for installing Python packages)

---

## Step 1: Open Terminal

1. Press `Cmd + Space` to open Spotlight
2. Type `Terminal` and press Enter
3. You should see a blank terminal window

---

## Step 2: Check Python Installation

Copy and paste this command into terminal:

```bash
python3 --version
```

**Expected output**: `Python 3.9.x` or higher

If you see "command not found", install Python first:
- Download from https://www.python.org/downloads/
- Or use Homebrew: `brew install python3`

---

## Step 3: Install Required Python Packages

Copy and paste this entire block:

```bash
pip3 install pandas openpyxl
```

**Expected output**: Successfully installed pandas and openpyxl (or "already satisfied")

**Troubleshooting**:
- If you see "permission denied", try: `pip3 install --user pandas openpyxl`
- If `pip3` not found, try: `python3 -m pip install pandas openpyxl`

---

## Step 4: Create Project Directory

Copy and paste these commands:

```bash
# Navigate to Desktop
cd ~/Desktop

# Create project directory
mkdir -p "HYLA_STOCK_TOOL"

# Navigate into it
cd "HYLA_STOCK_TOOL"

# Verify you're in the right place
pwd
```

**Expected output**: `/Users/[your-username]/Desktop/HYLA_STOCK_TOOL`

---

## Step 5: Download/Copy the Tool Files

### Option A: If Receiving via Shared Folder/USB

If someone is sharing the folder with you:

```bash
# Copy from shared location (adjust path as needed)
cp -r "/path/to/shared/HYLA COMPARISON SKILL"/* ~/Desktop/HYLA_STOCK_TOOL/

# Make shell script executable
chmod +x ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh
```

### Option B: If Setting Up from Scratch

If you have access to the original folder:

```bash
# Copy everything from the original location
cp -r "/Users/brandonin/Desktop/HYLA COMPARISON SKILL"/* ~/Desktop/HYLA_STOCK_TOOL/

# Make shell script executable
chmod +x ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh
```

---

## Step 6: Verify Installation

Check that all files are present:

```bash
cd ~/Desktop/HYLA_STOCK_TOOL
ls -la
```

**You should see**:
```
stock_comparison_tool.py
compare_stocks.sh
README.md
QUICK_START_GUIDE.md
COMPARISON_METHODOLOGY.md
DEPLOYMENT_GUIDE.md
VALIDATION_REPORT.md
... (and other files)
```

---

## Step 7: Test the Tool

Run a test to make sure everything works:

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

# Test Python script directly
python3 stock_comparison_tool.py --help 2>&1 | head -5
```

If you see usage information or the tool starts running, it's working!

---

## Step 8: Run Your First Comparison

Place your stock list files in the `HYLA_STOCK_TOOL` directory, then:

```bash
cd ~/Desktop/HYLA_STOCK_TOOL

# Run comparison (adjust filenames as needed)
./compare_stocks.sh "OLD_Stock_List.xlsx" "NEW_Stock_List.xlsx"
```

**OR** using Python directly:

```bash
python3 stock_comparison_tool.py "OLD_Stock_List.xlsx" "NEW_Stock_List.xlsx"
```

---

## Complete First-Time Setup Script

For a completely fresh start, copy and paste this ENTIRE block:

```bash
#!/bin/bash

echo "================================================"
echo "Hyla Stock Comparison Tool - Setup"
echo "================================================"

# Step 1: Check Python
echo ""
echo "Step 1: Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3 from python.org"
    exit 1
fi

# Step 2: Install packages
echo ""
echo "Step 2: Installing required Python packages..."
pip3 install --user pandas openpyxl --quiet
if [ $? -eq 0 ]; then
    echo "✓ Packages installed successfully"
else
    echo "✗ Package installation failed"
    exit 1
fi

# Step 3: Create directory
echo ""
echo "Step 3: Creating project directory..."
mkdir -p ~/Desktop/HYLA_STOCK_TOOL
cd ~/Desktop/HYLA_STOCK_TOOL
echo "✓ Created directory: ~/Desktop/HYLA_STOCK_TOOL"

# Step 4: Copy files (YOU NEED TO ADJUST THIS PATH)
echo ""
echo "Step 4: Copying tool files..."
echo "NOTE: You need to manually copy the tool files to this directory"
echo "      Or run: cp -r /path/to/source/* ~/Desktop/HYLA_STOCK_TOOL/"

# Step 5: Make executable
echo ""
echo "Step 5: Making shell script executable..."
if [ -f ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh ]; then
    chmod +x ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh
    echo "✓ Shell script is executable"
else
    echo "⚠ compare_stocks.sh not found yet"
fi

# Step 6: Verify
echo ""
echo "Step 6: Verifying installation..."
cd ~/Desktop/HYLA_STOCK_TOOL
if [ -f "stock_comparison_tool.py" ]; then
    echo "✓ stock_comparison_tool.py found"
else
    echo "✗ stock_comparison_tool.py not found"
fi

if [ -f "compare_stocks.sh" ]; then
    echo "✓ compare_stocks.sh found"
else
    echo "✗ compare_stocks.sh not found"
fi

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Place your OLD and NEW Excel files in ~/Desktop/HYLA_STOCK_TOOL/"
echo "2. Run: cd ~/Desktop/HYLA_STOCK_TOOL"
echo "3. Run: ./compare_stocks.sh \"OLD_file.xlsx\" \"NEW_file.xlsx\""
echo ""
```

---

## For Sharing with Team Members

### Package the Tool for Distribution

Create a shareable package:

```bash
# Navigate to Desktop
cd ~/Desktop

# Create a clean copy for distribution
mkdir -p HYLA_TOOL_DISTRIBUTION

# Copy only essential files
cp "HYLA COMPARISON SKILL/stock_comparison_tool.py" HYLA_TOOL_DISTRIBUTION/
cp "HYLA COMPARISON SKILL/compare_stocks.sh" HYLA_TOOL_DISTRIBUTION/
cp "HYLA COMPARISON SKILL/README.md" HYLA_TOOL_DISTRIBUTION/
cp "HYLA COMPARISON SKILL/QUICK_START_GUIDE.md" HYLA_TOOL_DISTRIBUTION/
cp "HYLA COMPARISON SKILL/COMPARISON_METHODOLOGY.md" HYLA_TOOL_DISTRIBUTION/
cp "HYLA COMPARISON SKILL/DEPLOYMENT_GUIDE.md" HYLA_TOOL_DISTRIBUTION/

# Create a zip file
cd ~/Desktop
zip -r HYLA_STOCK_TOOL.zip HYLA_TOOL_DISTRIBUTION/

echo "✓ Distribution package created: ~/Desktop/HYLA_STOCK_TOOL.zip"
```

### Instructions for Recipients

Send them this message along with the zip file:

```
Hi Team,

I'm sharing the Hyla Stock Comparison Tool. Here's how to set it up:

1. Download the HYLA_STOCK_TOOL.zip file
2. Unzip it to your Desktop
3. Open Terminal (Cmd+Space, type "Terminal")
4. Run these commands:

   cd ~/Desktop/HYLA_TOOL_DISTRIBUTION
   pip3 install --user pandas openpyxl
   chmod +x compare_stocks.sh

5. To use:
   ./compare_stocks.sh "OLD_file.xlsx" "NEW_file.xlsx"

Full guide: Open DEPLOYMENT_GUIDE.md in the folder
Quick start: Open QUICK_START_GUIDE.md

Questions? Let me know!
```

---

## Claude Code / OpCode Integration

### For Claude Code Users

1. **Copy the skill file**:
```bash
# Create Claude skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skill
cp ~/Desktop/HYLA_STOCK_TOOL/.claude/hyla-stock-comparison.md ~/.claude/skills/
```

2. **Use in Claude Code**:
```
User: "Compare my stock lists using the Hyla skill"
Claude: [Activates skill and runs comparison]
```

### For OpCode Users

1. **Add as a custom command**:
```bash
# Navigate to OpCode commands directory (path may vary)
cd ~/.opcode/commands

# Create a new command
cat > hyla-compare.sh << 'EOF'
#!/bin/bash
cd ~/Desktop/HYLA_STOCK_TOOL
./compare_stocks.sh "$1" "$2"
EOF

chmod +x hyla-compare.sh
```

2. **Use in OpCode**:
```
/hyla-compare "old.xlsx" "new.xlsx"
```

---

## Troubleshooting

### Issue: "Permission denied" when running script

**Solution**:
```bash
chmod +x ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh
```

### Issue: "pandas not found" or "openpyxl not found"

**Solution**:
```bash
pip3 install --user pandas openpyxl
# OR
python3 -m pip install --user pandas openpyxl
```

### Issue: "No such file or directory"

**Solution**: Check your current directory
```bash
pwd  # Shows current directory
cd ~/Desktop/HYLA_STOCK_TOOL  # Navigate to correct directory
ls -la  # List all files
```

### Issue: Excel file not found

**Solution**: Make sure files are in the same directory
```bash
# List files to verify
ls *.xlsx

# Or provide full path
./compare_stocks.sh "/full/path/to/OLD.xlsx" "/full/path/to/NEW.xlsx"
```

### Issue: Python version too old

**Solution**: Upgrade Python
```bash
# Check version
python3 --version

# If less than 3.9, install newer version
brew install python@3.11
# OR download from python.org
```

---

## Advanced: Create System-Wide Command

To run the tool from anywhere:

```bash
# Create a symlink in your PATH
sudo ln -s ~/Desktop/HYLA_STOCK_TOOL/compare_stocks.sh /usr/local/bin/hyla-compare

# Now you can run from anywhere:
hyla-compare "old.xlsx" "new.xlsx"
```

---

## Daily Usage Workflow

Once set up, your daily workflow is:

```bash
# 1. Navigate to tool directory
cd ~/Desktop/HYLA_STOCK_TOOL

# 2. Copy new files from Downloads (or wherever they arrive)
cp ~/Downloads/Stock_List_Today.xlsx .

# 3. Run comparison
./compare_stocks.sh "Stock_List_Yesterday.xlsx" "Stock_List_Today.xlsx"

# 4. Open result
open Comparison_*.xlsx
```

---

## File Organization Best Practice

Keep your files organized:

```
~/Desktop/HYLA_STOCK_TOOL/
├── stock_comparison_tool.py     (tool - don't modify)
├── compare_stocks.sh             (tool - don't modify)
├── Documentation/
│   ├── README.md
│   ├── QUICK_START_GUIDE.md
│   └── DEPLOYMENT_GUIDE.md
├── Stock_Files/
│   ├── 2025-11-10_Stock_List.xlsx
│   ├── 2025-11-11_Stock_List.xlsx
│   └── ... (daily files)
└── Comparison_Results/
    ├── Comparison_20251110.xlsx
    ├── Comparison_20251111.xlsx
    └── ... (output files)
```

**Setup this structure**:
```bash
cd ~/Desktop/HYLA_STOCK_TOOL
mkdir -p Documentation Stock_Files Comparison_Results
mv *.md Documentation/
```

**Run with organized structure**:
```bash
./compare_stocks.sh \
  "Stock_Files/2025-11-10_Stock_List.xlsx" \
  "Stock_Files/2025-11-11_Stock_List.xlsx" \
  "Comparison_Results/Comparison_$(date +%Y%m%d).xlsx"
```

---

## Team Setup Checklist

When deploying to team members:

- [ ] Python 3.9+ installed
- [ ] pandas and openpyxl packages installed
- [ ] Tool files copied to Desktop
- [ ] Shell script made executable
- [ ] Test run completed successfully
- [ ] QUICK_START_GUIDE.md reviewed
- [ ] Sample files tested
- [ ] Output file opened and verified
- [ ] Daily workflow understood

---

## Support & Documentation

**Quick Reference**:
- Daily workflow: `QUICK_START_GUIDE.md`
- Full documentation: `README.md`
- Methodology details: `COMPARISON_METHODOLOGY.md`
- Validation proof: `VALIDATION_REPORT.md`

**Getting Help**:
1. Check the troubleshooting section above
2. Review the README.md file
3. Verify all files are in place: `ls -la`
4. Check Python packages: `pip3 list | grep -E "pandas|openpyxl"`

---

## Security Notes

- The tool runs locally on your machine
- No data is sent to external servers
- Excel files are processed locally
- Your stock data remains private

---

## Version Information

- **Tool Version**: 1.0
- **Python Requirement**: 3.9+
- **Dependencies**: pandas, openpyxl
- **Platform**: macOS (adaptable to Linux/Windows)
- **Last Updated**: November 11, 2025

---

## Quick Command Reference

```bash
# Setup (one-time)
cd ~/Desktop/HYLA_STOCK_TOOL
pip3 install --user pandas openpyxl
chmod +x compare_stocks.sh

# Daily use
./compare_stocks.sh "old.xlsx" "new.xlsx"

# Check installation
python3 --version
pip3 list | grep pandas

# Navigate to tool
cd ~/Desktop/HYLA_STOCK_TOOL

# List files
ls -la

# View help
./compare_stocks.sh
```

---

**You're ready to go! Start comparing stock lists and making better purchasing decisions.**

For questions or issues, refer to the documentation files in the same directory.
