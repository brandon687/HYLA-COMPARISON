# Hyla Stock Comparison Dashboard - Deployment Guide

## Overview

The Hyla Stock Comparison Dashboard is a web-based tool that allows anyone to compare stock lists through a simple drag-and-drop interface. No technical knowledge required!

## What You Get

- **Modern Web Interface**: Beautiful, intuitive dashboard accessible through any web browser
- **Drag-and-Drop Upload**: Simply drag your Excel files or click to browse
- **Instant Analysis**: Get comprehensive comparison reports in seconds
- **Multiple Output Formats**: Download Excel workbooks, HTML dashboards, text reports, or complete packages
- **Visual Statistics**: See key metrics and changes at a glance

## Quick Start (3 Steps)

### Step 1: Install Python (If Not Already Installed)

**macOS:**
```bash
# Check if Python is installed
python3 --version

# If not installed, download from:
# https://www.python.org/downloads/
```

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer and check "Add Python to PATH"
3. Verify installation: Open Command Prompt and type `python --version`

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### Step 2: Start the Dashboard

**macOS/Linux:**
```bash
cd "HYLA COMPARISON SKILL"
./start_dashboard.sh
```

**Windows:**
```cmd
cd "HYLA COMPARISON SKILL"
python web_app.py
```

### Step 3: Open Your Browser

Navigate to: **http://localhost:5000**

That's it! The dashboard is now running.

## How to Use the Dashboard

### 1. Upload Files

1. **OLD File (Left)**: Drag and drop your previous stock list or click to browse
2. **NEW File (Right)**: Drag and drop your current stock list or click to browse

Supported formats: `.xlsx`, `.xls`

### 2. Compare

Click the blue **"Compare Stock Lists"** button. The analysis will begin immediately.

### 3. View Results

After a few moments, you'll see:

**Summary Statistics:**
- Total configurations (OLD → NEW)
- Matching items
- Significant changes (quantity change ≥ 100)
- Net quantity change
- New configurations added
- Removed configurations
- Average price change

### 4. Download Reports

Choose from four download options:

1. **Excel Workbook** - Complete analysis with multiple sheets
   - Summary statistics
   - Significant changes
   - All matching items
   - Top price increases/decreases
   - Top quantity increases/decreases

2. **Dashboard (HTML)** - Interactive visual report
   - Charts and graphs
   - Top 10 insights
   - Print-friendly format

3. **Complete Package (ZIP)** - All files bundled together
   - Excel workbook
   - HTML dashboard
   - Text report

4. **Text Report** - Plain text summary
   - Easy to email or copy
   - All key metrics included

## Features Explained

### Real-Time Statistics

The dashboard displays live statistics as soon as comparison completes:

- **Total Configs**: Shows configuration count change (OLD → NEW)
- **Matching Items**: Configurations present in both lists
- **Significant Changes**: Items with quantity change ≥ 100 units
- **Net Qty Change**: Total quantity difference across all items
- **New Configs**: Configurations only in NEW list (new opportunities)
- **Removed Configs**: Configurations only in OLD list (no longer available)
- **Avg Price Change**: Average list price difference

### Configuration Grouping

Items are grouped by:
- Model (e.g., iPhone 14 Pro Max)
- Capacity (e.g., 256GB)
- Lock Status (e.g., UNLOCKED)
- Grade (e.g., DLS B+)

This provides strategic insights at the product level rather than individual item tracking.

### Comparison Metrics

Each comparison includes:
- **Quantity Changes**: OLD qty → NEW qty (with % change)
- **Price Changes**: OLD price → NEW price (with % change)
- **Strategic Margins**: NEW list price vs OLD offer price
- **Status**: Matching, New, or Removed

## Deployment Scenarios

### Local Use (Your Computer Only)

Perfect for personal use or testing:

1. Run `./start_dashboard.sh` (macOS/Linux) or `python web_app.py` (Windows)
2. Access at http://localhost:5000
3. Press Ctrl+C to stop when done

### Team Use (Share on Local Network)

Allow team members to access from their computers:

1. Start the dashboard
2. Find your computer's IP address:
   - **macOS/Linux**: `ifconfig | grep "inet "` (look for 192.168.x.x)
   - **Windows**: `ipconfig` (look for IPv4 Address)
3. Share the URL: `http://YOUR_IP:5000` (e.g., http://192.168.1.100:5000)

**Note**: All users must be on the same network, and your firewall may need to allow port 5000.

### Global Deployment (Internet Access)

For worldwide access, deploy to a cloud service:

#### Option 1: Heroku (Easiest)

1. Create free account at https://heroku.com
2. Install Heroku CLI
3. Deploy:
```bash
heroku login
heroku create hyla-stock-comparison
git init
git add .
git commit -m "Initial deployment"
git push heroku main
heroku open
```

#### Option 2: DigitalOcean / AWS / Google Cloud

1. Create a virtual machine
2. Install Python and dependencies
3. Run web app
4. Configure firewall to allow port 5000
5. Use nginx as reverse proxy (recommended)

#### Option 3: PythonAnywhere (Simplest)

1. Create account at https://www.pythonanywhere.com
2. Upload project files
3. Configure web app in dashboard
4. Get public URL

## Advanced Configuration

### Change Port

Edit `web_app.py` line 161:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change 5000 to your port
```

### Increase File Size Limit

Edit `web_app.py` line 16:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB (adjust as needed)
```

### Custom Branding

Edit `templates/index.html`:
- Line 37: Change title
- Line 52: Change header text
- Colors can be modified using Tailwind CSS classes

### Enable HTTPS

For production use, configure nginx or Apache as a reverse proxy with SSL certificates:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### "Address already in use"

Another process is using port 5000:
```bash
# Find and kill the process (macOS/Linux)
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "Module not found" errors

Dependencies not installed:
```bash
pip install -r requirements.txt
```

### Files not uploading

Check file size limits in `web_app.py` (default 50MB)

### Comparison takes too long

Large files (>10k rows) may take 30-60 seconds. This is normal.

### Results not displaying

Check browser console (F12) for JavaScript errors. Try refreshing the page.

## File Structure

```
HYLA COMPARISON SKILL/
├── web_app.py                 # Flask web server
├── stock_comparison_tool.py   # Core comparison logic
├── requirements.txt           # Python dependencies
├── start_dashboard.sh         # Startup script
├── templates/
│   └── index.html            # Web interface
└── DASHBOARD_GUIDE.md        # This file
```

## Security Considerations

### For Internal Use

- Default configuration is secure for trusted internal networks
- Files are temporarily stored and auto-cleaned
- No data is logged or retained after download

### For Public Deployment

Add these security measures:

1. **Authentication**: Add login system
2. **Rate Limiting**: Prevent abuse
3. **File Validation**: Enhanced security checks
4. **HTTPS**: Encrypt all traffic
5. **Firewall**: Restrict access by IP
6. **Session Management**: Secure session handling

Example authentication (add to `web_app.py`):
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "secure_password_here"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')
```

## Performance Tips

1. **File Preparation**: Remove unnecessary columns before upload
2. **Browser**: Use Chrome or Firefox for best performance
3. **Network**: Faster internet = faster uploads
4. **Server Resources**: More RAM = faster processing

## Support & Maintenance

### Logs

Check console output for errors:
```bash
# Start with verbose logging
python web_app.py 2>&1 | tee dashboard.log
```

### Updates

Update dependencies periodically:
```bash
pip install --upgrade -r requirements.txt
```

### Backups

Important files to backup:
- `web_app.py`
- `stock_comparison_tool.py`
- `templates/index.html`

## Future Enhancements

Potential improvements:
- [ ] User authentication system
- [ ] Historical comparison tracking
- [ ] Email notifications
- [ ] Scheduled comparisons
- [ ] API endpoints
- [ ] Multi-file comparison
- [ ] Custom report templates
- [ ] Database integration
- [ ] Mobile app version

## Getting Help

1. Check this guide first
2. Review error messages in console
3. Check Python and pip versions
4. Verify all dependencies installed
5. Try with sample files first

## License

Internal tool for Hyla stock analysis.

---

**Version**: 1.0
**Last Updated**: November 2025
**Compatibility**: Python 3.8+, All modern browsers
