# Railway Deployment Guide

## Quick Deploy to Railway

### Prerequisites
- A Railway account (free tier available at https://railway.app)
- GitHub account (optional, for automatic deployments)

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - HYLA Stock Comparison Tool"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and deploy!

3. **Configure (if needed):**
   - Railway will automatically use the `requirements.txt`
   - It will run `python3 web_app.py` (defined in Procfile)
   - Your app will be live at a Railway-provided URL

### Option 2: Deploy from Local Directory

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Generate Domain:**
   ```bash
   railway domain
   ```

## Configuration Files Included

- **requirements.txt**: Python dependencies
- **Procfile**: Tells Railway how to run the app
- **railway.json**: Railway-specific configuration
- **runtime.txt**: Specifies Python version

## Environment Variables (Optional)

Railway automatically sets `PORT`, but you can add:
- `MAX_CONTENT_LENGTH`: Max upload size (default: 50MB)

## Post-Deployment

Once deployed, your app will be available at:
```
https://your-app-name.railway.app
```

### Features Available:
- Drag-and-drop file upload
- Real-time comparison processing
- Multiple export formats (Excel, HTML, ZIP, Text)
- Professional dashboard with statistics
- Automatic cleanup of old files

## Monitoring

Railway provides:
- Automatic HTTPS
- Real-time logs
- Usage metrics
- Automatic restarts on failure

## Cost

Railway offers:
- **Free tier**: $5 credit/month
- **Pro tier**: $5/month + usage

The HYLA Stock Comparison tool is lightweight and should run comfortably within the free tier for moderate usage.

## Local Development

To run locally:
```bash
python3 web_app.py
```

Then visit: http://localhost:5001

## Troubleshooting

### Port Issues
If you see "Address already in use":
```bash
# Find and kill the process
lsof -ti:5001 | xargs kill -9

# Or change the port
export PORT=5002
python3 web_app.py
```

### Missing Dependencies
```bash
pip3 install -r requirements.txt
```

### Upload Issues
Make sure your Excel files are:
- Valid .xlsx or .xls format
- Under 50MB
- Contain the expected columns (Model, Carrier, Storage, Color, etc.)

## Support

For Railway-specific issues: https://railway.app/help
For app-specific issues: Check the logs in Railway dashboard
