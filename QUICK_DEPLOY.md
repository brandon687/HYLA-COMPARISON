# Hyla Stock Comparison - Quick Deploy (1 Page)

## Copy-Paste Setup (Fresh Terminal)

### Step 1: Check Python (30 seconds)
```bash
python3 --version
```
✓ Should show Python 3.9 or higher

### Step 2: Install Packages (1 minute)
```bash
pip3 install --user pandas openpyxl
```
✓ Wait for "Successfully installed" message

### Step 3: Create & Navigate to Directory (10 seconds)
```bash
cd ~/Desktop && mkdir -p HYLA_STOCK_TOOL && cd HYLA_STOCK_TOOL
```
✓ You're now in: `/Users/[you]/Desktop/HYLA_STOCK_TOOL`

### Step 4: Copy Tool Files (Adjust source path)
```bash
# Option A: If files are on USB/shared drive (adjust path)
cp -r /Volumes/USB_DRIVE/HYLA_STOCK_TOOL/* .

# Option B: If files are in another location
cp -r "/path/to/source/HYLA COMPARISON SKILL"/* .
```

### Step 5: Make Executable (5 seconds)
```bash
chmod +x compare_stocks.sh
```

### Step 6: Test (10 seconds)
```bash
ls -la stock_comparison_tool.py compare_stocks.sh
```
✓ Both files should be listed

---

## First Run

```bash
cd ~/Desktop/HYLA_STOCK_TOOL
./compare_stocks.sh "YOUR_OLD_FILE.xlsx" "YOUR_NEW_FILE.xlsx"
```

---

## Complete Auto-Setup Script

**Copy & paste this entire block** into terminal:

```bash
#!/bin/bash
echo "🚀 Hyla Stock Comparison Tool - Quick Setup"
echo ""

# Install packages
echo "📦 Installing Python packages..."
pip3 install --user pandas openpyxl -q

# Create directory
echo "📁 Creating directory..."
mkdir -p ~/Desktop/HYLA_STOCK_TOOL
cd ~/Desktop/HYLA_STOCK_TOOL

echo ""
echo "✓ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Copy tool files to: ~/Desktop/HYLA_STOCK_TOOL/"
echo "  2. Run: chmod +x compare_stocks.sh"
echo "  3. Run: ./compare_stocks.sh \"old.xlsx\" \"new.xlsx\""
echo ""
echo "Current directory: $(pwd)"
```

---

## Daily Usage (After Setup)

```bash
cd ~/Desktop/HYLA_STOCK_TOOL
./compare_stocks.sh "OLD_Stock_List.xlsx" "NEW_Stock_List.xlsx"
```

**That's it!** Output opens automatically.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Permission denied" | `chmod +x compare_stocks.sh` |
| "pandas not found" | `pip3 install --user pandas openpyxl` |
| "File not found" | Check you're in right directory: `pwd` |
| "Python not found" | Install from python.org |

---

## Share with Team

**Create distribution package:**
```bash
cd ~/Desktop
zip -r HYLA_TOOL.zip "HYLA COMPARISON SKILL"/{stock_comparison_tool.py,compare_stocks.sh,*.md}
```

**Send teammates**: HYLA_TOOL.zip + this QUICK_DEPLOY.md file

**They run**:
```bash
# Unzip to Desktop
cd ~/Desktop
unzip HYLA_TOOL.zip

# Install & setup
pip3 install --user pandas openpyxl
cd HYLA_STOCK_TOOL
chmod +x compare_stocks.sh

# Use it
./compare_stocks.sh "old.xlsx" "new.xlsx"
```

---

## File Structure Check

Run this to verify everything is in place:
```bash
cd ~/Desktop/HYLA_STOCK_TOOL && ls -1
```

**You should see:**
```
compare_stocks.sh
stock_comparison_tool.py
README.md
QUICK_START_GUIDE.md
DEPLOYMENT_GUIDE.md
```

---

**Questions?** → Open `README.md` for full docs
**Daily workflow?** → Open `QUICK_START_GUIDE.md`

**Ready to use!** 🎉
