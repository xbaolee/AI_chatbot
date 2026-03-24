# Chatbot Deployment Guide

## 📋 Prerequisites
Before deploying, ensure your project folder contains:
- ✅ `app.py` (Flask application)
- ✅ `requirements.txt` (dependencies)
- ✅ `templates/index.html` (HTML interface)
- ✅ `static/style.css` (styling)
- ✅ `neural_network_model.pkl` (trained model)
- ✅ `tfidf_vectorizer.pkl` (TF-IDF vectorizer)
- ✅ `Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv` (dataset)

---

## 🚀 Deployment Options (Free)

### Option 1: Render.com (RECOMMENDED - Easiest)
Best for Python Flask apps, free tier includes:
- 0.5 GB RAM
- Free SSL certificate
- Auto-deploys from GitHub

**Steps:**
1. Push your code to GitHub (create a repo)
2. Go to [Render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Name:** chatbot
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment

**Your app will be live at:** `https://your-app-name.onrender.com`

---

### Option 2: Railway.app
Great alternative with generous free tier

**Steps:**
1. Go to [Railway.app](https://railway.app)
2. Click "Start Project"
3. Select "Deploy from GitHub"
4. Connect your GitHub account
5. Select your repo
6. Click "Deploy"
7. Configure environment variables if needed
8. Your app is live!

---

### Option 3: PythonAnywhere
Easiest for beginners, web hosting specifically for Python

**Steps:**
1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Sign up (free account)
3. Upload your project files (or clone from GitHub)
4. Create a new web app → Select Flask
5. Upload your files to the project directory
6. Edit `/var/www/your_username_pythonanywhere_com_wsgi.py`:
```python
import sys
path = '/home/your_username/chatbot'
if path not in sys.path:
    sys.path.append(path)
from app import app as application
```
7. Reload the web app
8. Your app is live at: `https://your_username.pythonanywhere.com`

---

## 🔧 GitHub Setup (Required for Render/Railway)

### Create GitHub Repository:
1. Go to [GitHub.com](https://github.com) and login
2. Click "New repository"
3. Name it `chatbot-deployment`
4. Make it **Public**
5. Click "Create repository"

### Upload Files:
```bash
# Initialize git in your project folder
git init

# Add all files
git add .

# Commit files
git commit -m "Initial chatbot deployment"

# Add remote (copy the link from GitHub)
git remote add origin https://github.com/YOUR_USERNAME/chatbot-deployment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🧪 Test Locally First

Before deploying, test your app locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open: `http://localhost:5000`

---

## ⚠️ Common Issues & Solutions

### Issue: Models not loading
**Solution:** Make sure `neural_network_model.pkl` and `tfidf_vectorizer.pkl` are in the same folder as `app.py`

### Issue: Dataset not found
**Solution:** Upload the CSV file to your deployment platform's file system or modify `app.py` to handle missing CSV gracefully

### Issue: App crashes on startup
**Solution:** Check the logs on your hosting platform (Render/Railway has a "Logs" tab)

### Issue: NLTK data missing
**Solution:** The app downloads required NLTK data automatically. If it fails, add this to `app.py` startup or use a Procfile

---

## 📦 Create Procfile (Optional but Recommended)

Create a file named `Procfile` (no extension) in your project root:
```
web: gunicorn app:app
```

---

## 🌐 Custom Domain (Free Options)

Both Render and Railway give you free subdomains. For custom domains:
- Check your hosting platform's documentation
- Most free tiers support free `.onrender.com` or `.railway.app` domains
- Paid custom domains typically cost $10-15/year

---

## 📊 Monitoring Your App

After deployment:
1. Open your app URL
2. Test the chatbot with various questions
3. Check logs for errors
4. Monitor performance in your hosting dashboard

---

## 🔒 Security Notes

- The free tier models are loaded from local files
- In production, consider:
  - Adding rate limiting
  - Using environment variables for sensitive data
  - Implementing user authentication if needed

---

## 📝 Deployment Checklist

- [ ] All files uploaded (app.py, requirements.txt, models, csv)
- [ ] GitHub repository created and public
- [ ] Git pushed to GitHub
- [ ] Hosting platform selected
- [ ] Build command configured
- [ ] Start command configured
- [ ] App deployed successfully
- [ ] Tested chatbot in web interface

---

## 💡 Next Steps

1. Share your deployed URL with others
2. Monitor logs for any errors
3. Update your models as needed
4. Consider adding features like:
   - User feedback collection
   - Chat history
   - Analytics dashboard
   - Multi-language support

---

**Need Help?** Check your platform's documentation or contact support!
