# SoundCheck Deployment Guide

## 🚀 Deploy to Streamlit Cloud

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

#### 1. Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### 2. Deploy Frontend to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set the following:
   - **Repository**: Your GitHub repo
   - **Branch**: main
   - **Main file path**: `frontend/app.py`
   - **App URL**: Choose your custom URL

#### 3. Configure Environment Variables
In Streamlit Cloud, add these secrets in the app settings:
```toml
# .streamlit/secrets.toml
[api]
backend_url = "https://your-backend-url.com"
```

#### 4. Deploy Backend (Options)

##### Option A: Railway
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Select the `backend` folder
4. Set environment variables
5. Deploy

##### Option B: Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r all_requirements.txt`
5. Set start command: `cd backend && python start_server.py`

##### Option C: Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Set buildpack to Python
4. Deploy backend folder

### Environment Variables for Backend
```bash
PORT=8000
CORS_ORIGINS=["https://your-streamlit-app.streamlit.app"]
```

### Testing Deployment
1. Visit your Streamlit app URL
2. Test the hearing test functionality
3. Verify API connectivity
4. Check all features work correctly

### Troubleshooting
- **API Connection Issues**: Check backend URL in secrets
- **CORS Errors**: Update CORS_ORIGINS in backend
- **Model Loading**: Ensure model files are included in deployment
- **Dependencies**: Verify all_requirements.txt file is complete

### Production Considerations
1. **Security**: Use HTTPS for all endpoints
2. **Rate Limiting**: Implement API rate limiting
3. **Monitoring**: Add logging and error tracking
4. **Backup**: Regular database backups if using persistent storage
5. **SSL**: Ensure SSL certificates are properly configured

### Support
For deployment issues, check:
- Streamlit Cloud documentation
- Backend hosting provider docs
- GitHub repository issues
