# HYLA Stock Comparison - Web UI Guide

## Overview

The HYLA Stock Comparison web interface provides an intuitive, drag-and-drop experience for comparing stock lists. No command line knowledge required!

## Accessing the Application

### Local Development
```bash
python3 web_app.py
```
Then open: **http://localhost:5001**

### Production (Railway)
After deployment: **https://your-app-name.railway.app**

## Using the Web Interface

### Step 1: Upload Files

1. **OLD Stock List**:
   - Drag and drop your OLD Excel file into the left box
   - Or click the box to browse and select your file
   - File should be .xlsx or .xls format

2. **NEW Stock List**:
   - Drag and drop your NEW Excel file into the right box
   - Or click the box to browse and select your file
   - File should be .xlsx or .xls format

### Step 2: Compare

Once both files are uploaded, the "Compare Stock Lists" button will become active.
Click it to start the comparison process.

### Step 3: View Results

The dashboard will show:

**Key Statistics:**
- Total Configs (OLD → NEW)
- Matching Items
- Significant Changes
- Net Quantity Change

**Additional Metrics:**
- New Configurations added
- Removed Configurations
- Average Price Change

### Step 4: Download Results

Choose your preferred format:

1. **Excel Workbook** (green button)
   - Full detailed comparison in Excel format
   - Multiple sheets with different views
   - Ready for further analysis

2. **Dashboard (HTML)** (blue button)
   - Interactive HTML dashboard
   - Can be opened in any browser
   - Includes charts and visualizations

3. **Complete Package** (purple button)
   - ZIP file with all reports
   - Includes Excel, HTML, and text reports
   - Perfect for archiving

4. **Text Report** (gray button)
   - Plain text summary
   - Easy to read in any text editor
   - Great for quick reviews

### Step 5: New Comparison

Click the "New Comparison" button to start over with new files.

## Features

### Drag-and-Drop Interface
- Simply drag Excel files from your desktop
- Visual feedback when files are ready
- File size displayed

### Real-Time Progress
- Animated progress indicators
- Step-by-step status updates:
  1. Reading Excel files
  2. Comparing configurations
  3. Generating reports
  4. Creating dashboards

### Professional Results
- Clean, modern dashboard
- Color-coded statistics
- Easy-to-understand metrics
- Multiple export formats

### Error Handling
- Clear error messages
- Validation of file formats
- Automatic retry on temporary failures

## File Requirements

### Supported Formats
- Excel 2007+ (.xlsx)
- Excel 97-2003 (.xls)

### File Size Limit
- Maximum: 50MB per file
- Recommended: Under 10MB for fastest processing

### Required Columns
Your Excel files should contain these columns:
- Model
- Carrier
- Storage
- Color
- Grade
- Warranty
- List Price
- Available Qty

## Tips for Best Results

1. **File Naming**: Use clear names like "Stock_OLD.xlsx" and "Stock_NEW.xlsx"

2. **Data Quality**: Ensure your Excel files are:
   - Properly formatted
   - Free of merged cells in data rows
   - Have headers in the first row

3. **Internet Connection**: Required for:
   - Accessing the web interface
   - Downloading results
   - Using Railway deployment

4. **Browser Compatibility**: Works best with:
   - Chrome (recommended)
   - Firefox
   - Safari
   - Edge

## Keyboard Shortcuts

- **Escape**: Cancel/close error messages
- **Enter**: Submit when files are ready (on Compare button)

## Troubleshooting

### "Both OLD and NEW files are required"
- Make sure you've uploaded both files
- Check that files weren't cleared

### "Only Excel files (.xlsx, .xls) are allowed"
- Verify your file extension
- Try re-saving from Excel

### "Comparison failed"
- Check your Excel file format
- Verify required columns exist
- Check for data corruption

### Upload is slow
- Large files take longer
- Check your internet connection
- Consider compressing data

### Results don't download
- Check browser's download settings
- Disable popup blockers
- Try a different browser

## Mobile Support

The interface is responsive and works on:
- Tablets (iPad, Android tablets)
- Mobile phones (limited)

For best experience, use a desktop or tablet.

## Security

- Files are processed server-side
- Automatic cleanup of uploaded files
- No data is permanently stored
- Secure HTTPS connection (Railway deployment)

## Performance

**Typical Processing Times:**
- Small files (<1MB): 2-5 seconds
- Medium files (1-5MB): 5-15 seconds
- Large files (5-50MB): 15-60 seconds

## Support

Need help?
1. Check the error message displayed
2. Review the DASHBOARD_GUIDE.md for report details
3. See RAILWAY_DEPLOYMENT.md for deployment issues
4. Check Railway logs if deployed

## Local Development vs Production

### Local (localhost:5001)
- Debug mode enabled
- Detailed error messages
- Hot reload on code changes
- No HTTPS

### Production (Railway)
- Production mode
- Optimized performance
- Automatic HTTPS
- Better security

## What's Next?

After mastering the web interface, you can:
1. Customize the dashboard styling
2. Add authentication for team use
3. Implement user accounts
4. Add email notifications
5. Create API endpoints for automation

The web interface makes HYLA Stock Comparison accessible to everyone!
