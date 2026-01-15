# Deployment Guide - VOC Dashboard on Render

## 📋 Prerequisites
- GitHub account (free from github.com)
- Render account (free from render.com)
- VS Code with Git installed

## Step 1️⃣: Create GitHub Repository

### Option A: Using VS Code (Recommended)
1. Open VS Code
2. Open terminal: `Ctrl + `` (backtick)
3. Navigate to your project folder:
   ```bash
   cd "c:\Users\Harish.B\Desktop\VOC DASHBOARD"
   ```

4. Initialize Git repo:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: VOC Dashboard"
   ```

5. Create repo on GitHub.com:
   - Go to https://github.com/new
   - Create repo name: `voc-dashboard`
   - Copy the commands and run in VS Code terminal:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/voc-dashboard.git
   git branch -M main
   git push -u origin main
   ```

### Option B: Using GitHub Web
1. Go to https://github.com/new
2. Create new repository: `voc-dashboard`
3. Copy the HTTPS URL
4. In VS Code terminal:
   ```bash
   git clone https://github.com/YOUR_USERNAME/voc-dashboard.git
   cd voc-dashboard
   ```
5. Copy all your dashboard files into this folder
6. Push to GitHub:
   ```bash
   git add .
   git commit -m "Add VOC Dashboard files"
   git push origin main
   ```

---

## Step 2️⃣: Deploy to Render

### Create Web Service on Render

1. **Go to Render.com**
   - Sign up (free) at https://render.com
   - Click "New +" → Select "Web Service"

2. **Connect GitHub**
   - Select "GitHub" as the repository source
   - Authorize Render to access GitHub
   - Select your `voc-dashboard` repository

3. **Configure Service**
   - **Name:** `voc-dashboard` (or your preferred name)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free (for testing)

4. **Add Environment Variables** (if needed)
   - Leave as default for now

5. **Click "Create Web Service"**

### Render will automatically:
✅ Install Python dependencies  
✅ Deploy your app  
✅ Assign a free subdomain  
✅ Enable HTTPS  

---

## Step 3️⃣: Access Your Dashboard

After deployment completes (5-10 minutes):

Your dashboard will be live at:
```
https://voc-dashboard.onrender.com
```

(The exact URL depends on your chosen name)

---

## 🔄 Update Dashboard

After making changes locally:

```bash
# In your project folder
git add .
git commit -m "Update: [describe changes]"
git push origin main
```

Render will **automatically redeploy** your changes! 🚀

---

## 📊 Make Dashboard Accessible to Others

Once deployed, share this link:
```
https://voc-dashboard.onrender.com
```

**No installation needed** - they just open the link in any browser!

---

## 🛠️ Troubleshooting

### Dashboard not loading?
1. Check Render logs: Dashboard → Logs tab
2. Ensure `latest_t_mapped.csv` is in repo
3. Verify `Original Code.html` filename (with space)

### CSV data not showing?
1. Make sure `latest_t_mapped.csv` is committed to GitHub
2. Verify file path in app.py matches your filename

### Free plan limitations?
- Render spins down inactive apps after 15 minutes
- First request after sleep takes 30 seconds
- Upgrade to paid plan for instant access

---

## 📝 File Checklist

Before pushing to GitHub, ensure you have:
- ✅ `Original Code.html` (dashboard)
- ✅ `latest_t_mapped.csv` (data)
- ✅ `app.py` (Flask server)
- ✅ `requirements.txt` (dependencies)
- ✅ `Procfile` (Render config)
- ✅ `README.md` (documentation)

---

## 🎉 You're Done!

Your VOC Dashboard is now live and shareable with the world! 🌍

For questions or support, check:
- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com
- GitHub Help: https://docs.github.com
