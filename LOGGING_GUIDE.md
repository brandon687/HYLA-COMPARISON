# HYLA Stock Comparison Tool - Logging & Debugging Guide

## Overview

The application has comprehensive logging built-in to track every transaction and debug issues in production.

## How Logging Works

### 1. **Every Request Gets a Session ID**
Each comparison request is assigned a unique session ID (timestamp format: `YYYYMMDD_HHMMSS`).

Example: `[20251113_123045]` = Request on Nov 13, 2025 at 12:30:45

### 2. **What Gets Logged**

#### **Startup Logs:**
```
================================================================================
HYLA Stock Comparison Tool - Starting
Upload folder: /tmp/xyz123
Max file size: 50.0MB
================================================================================
```

#### **Comparison Request Logs:**
```
[20251113_123045] Starting new comparison request
[20251113_123045] Files received: OLD='old_stock.xlsx', NEW='new_stock.xlsx'
[20251113_123045] Saving files to: /tmp/xyz123
[20251113_123045] File sizes: OLD=2.34MB, NEW=2.56MB
[20251113_123045] Starting StockComparator
[20251113_123045] Comparison completed successfully
[20251113_123045] Summary stats: 1112 old configs, 1092 new configs, 43 significant changes
[20251113_123045] Generating Top 20 Movers PDF
[20251113_123045] PDF generated: Comparison_20251113_123045_Top10.pdf
[20251113_123045] Text report loaded: 25678 characters
[20251113_123045] Comparison request completed successfully
```

#### **Download Logs:**
```
[20251113_123045] Download requested: pdf
[20251113_123045] Found 5 files for session
[20251113_123045] Serving file: Comparison_20251113_123045_Top10.pdf (245.67KB)
[20251113_123045] Download completed: pdf
```

#### **Error Logs:**
```
[20251113_123045] ERROR during comparison:
[20251113_123045] Exception type: KeyError
[20251113_123045] Exception message: 'List Price Change %'
[20251113_123045] Full traceback:
Traceback (most recent call last):
  File "/app/web_app.py", line 453, in compare_files
    ...
```

## Viewing Logs on Railway

### **1. Railway Dashboard Logs (Real-Time)**

**Access:**
1. Go to https://railway.app/dashboard
2. Click on your project: **HYLA-COMPARISON**
3. Click on the **Deployment** tab
4. Click **"View Logs"**

**What You'll See:**
- Real-time log stream
- All `logger.info()`, `logger.warning()`, and `logger.error()` messages
- Timestamps for each log entry
- Session IDs to track individual requests

**Filter by Session:**
- Use Railway's search feature to filter by session ID
- Example: Search for `[20251113_123045]` to see all logs for that specific transaction

### **2. Railway Build Logs**

**Access:** Same location, but select **"Build Logs"** tab

**What You'll See:**
- Application startup logs
- Dependency installation
- Any errors during deployment

### **3. Historical Logs**

Railway keeps logs for:
- **Last 7 days** on Free tier
- **30+ days** on paid tiers

## What Each Log Level Means

| Level | Purpose | Example |
|-------|---------|---------|
| **INFO** | Normal operations | File uploaded, comparison completed |
| **WARNING** | Something unusual but not breaking | Invalid file extension, empty filename |
| **ERROR** | Something broke | Comparison failed, file not found |

## Common Error Scenarios & How to Debug

### **Error: "File not found"**
**Logs to check:**
```
[SESSION_ID] File not found for type: pdf
```
**Cause:** File generation failed or wrong session ID
**Solution:** Check earlier logs for PDF generation errors

### **Error: "Comparison failed"**
**Logs to check:**
```
[SESSION_ID] ERROR during comparison:
[SESSION_ID] Exception type: ...
[SESSION_ID] Full traceback: ...
```
**Cause:** Bad Excel format, missing columns, corrupted data
**Solution:** Check the full traceback for specific error

### **Error: "Invalid file extensions"**
**Logs to check:**
```
[SESSION_ID] Invalid file extensions
```
**Cause:** User uploaded non-Excel file
**Solution:** User education - only .xlsx/.xls allowed

## Tracking User Activity

### **How to Monitor Usage:**
1. Count log entries starting with "Starting new comparison request"
2. Each entry = 1 user transaction
3. Session IDs are unique per request

### **Example Log Analysis:**
```bash
# Count total comparisons today
grep "Starting new comparison request" | grep "20251113" | wc -l

# Find failed comparisons
grep "ERROR during comparison"

# Track specific user session
grep "[20251113_123045]"
```

## Production Monitoring Best Practices

### **1. Set Up Log Alerts (Railway)**
- Go to Railway → Settings → Notifications
- Enable alerts for:
  - Error rate spikes
  - Deployment failures
  - Resource limits

### **2. Regular Log Review**
- Check logs daily for ERROR entries
- Monitor file size trends
- Track comparison completion rates

### **3. Performance Monitoring**
Key metrics to watch:
- File upload sizes (logged)
- Comparison completion times
- Download frequencies

## Log Retention

**Current Setup:**
- Logs go to **stdout** (Railway captures automatically)
- No local log files (ephemeral containers)
- All logs stored in Railway's logging system

**To Export Logs:**
1. Railway Dashboard → Logs
2. Copy/paste relevant entries
3. Or use Railway CLI: `railway logs`

## Debugging a Failed Transaction

**Step-by-Step:**

1. **Get the session ID** from user (or find in logs by timestamp)

2. **Search Railway logs** for that session ID:
   ```
   [20251113_123045]
   ```

3. **Look for the error:**
   - Find the "ERROR during comparison" entry
   - Check the exception type and message
   - Review the full traceback

4. **Identify the cause:**
   - Column name mismatch? → Fix data structure
   - File corruption? → Ask user to re-upload
   - Missing dependency? → Update requirements.txt

5. **Verify the fix:**
   - Deploy updated code
   - Monitor logs for same session pattern
   - Confirm error is resolved

## Integration with External Monitoring (Optional)

If you want more advanced monitoring, you can integrate:
- **Sentry** for error tracking
- **LogDNA** for log aggregation
- **Datadog** for full observability

## Summary

✅ **Every transaction is logged** with unique session ID
✅ **Full error tracebacks** captured for debugging
✅ **Railway shows all logs** in real-time
✅ **Search by session ID** to track specific transactions
✅ **No log data is lost** (Railway handles persistence)

**When something breaks:**
1. Check Railway logs
2. Find the session ID
3. Review the error traceback
4. Fix and redeploy

Your logging is production-ready! 🎉
