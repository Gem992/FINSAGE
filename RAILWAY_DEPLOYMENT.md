# Railway Deployment Guide for Finsage

## 🚀 Quick Deployment Steps

### 1. Push to GitHub (if not already done)
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy to Railway

#### Option A: Deploy from GitHub (Recommended)
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `finsage - Copy` repository
6. Railway will automatically detect it's a Django project

#### Option B: Deploy from Local Files
1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from folder"
3. Upload your project folder

### 3. Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Railway will automatically create a `DATABASE_URL` environment variable

### 4. Set Environment Variables
In Railway dashboard → Variables tab, add:
```
DEBUG=False
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALLOWED_HOSTS=*.railway.app,your-domain.com
```

### 5. Deploy
Railway will automatically:
- Install dependencies from `requirements.txt`
- Run migrations
- Start your Django app with Gunicorn

## 📋 Files Created/Modified

### New Files:
- `Procfile` - Tells Railway how to run your app
- `runtime.txt` - Specifies Python version
- `.gitignore` - Excludes sensitive files from git
- `.env.example` - Template for environment variables

### Modified Files:
- `requirements.txt` - Added production dependencies
- `finsage_project/settings.py` - Production-ready settings

## 🔧 Production Dependencies Added

- `gunicorn` - WSGI server for production
- `psycopg2-binary` - PostgreSQL adapter
- `whitenoise` - Static file serving
- `python-decouple` - Environment variable management
- `dj-database-url` - Database URL parsing

## 🛡️ Security Features Added

- Environment-based configuration
- PostgreSQL database (more secure than SQLite)
- HTTPS enforcement
- Security headers
- Static file optimization

## 🌐 Custom Domain (Optional)

1. In Railway dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` environment variable

## 📊 Monitoring

Railway provides:
- Real-time logs
- Performance metrics
- Automatic deployments from git pushes
- Health checks

## 🔄 Updates

To update your app:
```bash
git add .
git commit -m "Update app"
git push origin main
```
Railway will automatically redeploy!

## 🆘 Troubleshooting

### Common Issues:

1. **App Crashes Immediately (Python Encoding Error)**
   - **FIXED**: Removed `runtime.txt` - let Railway auto-detect Python version
   - **FIXED**: Updated `Procfile` with proper port binding
   - **FIXED**: Added `railway.toml` for better configuration
   - Redeploy after these fixes

2. **Build Fails**
   - Check Railway logs for specific errors
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

3. **Database Connection Error**
   - **IMPORTANT**: Add PostgreSQL database first:
     - Go to Railway dashboard → "New" → "Database" → "PostgreSQL"
     - Railway will auto-create `DATABASE_URL` environment variable
   - Verify PostgreSQL service is running
   - Check `DATABASE_URL` environment variable exists

4. **Static Files Not Loading**
   - Run `python manage.py collectstatic` locally
   - Check `STATIC_ROOT` setting

5. **Port Binding Issues**
   - **FIXED**: Updated Procfile to use `$PORT` environment variable
   - Railway automatically assigns port via `$PORT` env var

6. **Migration Errors**
   - **FIXED**: Procfile now runs migrations automatically before starting
   - Check Railway logs for migration errors

7. **Healthcheck Failures**
   - **FIXED**: Added dedicated `/health/` endpoint
   - **FIXED**: Healthcheck tests database connectivity
   - **FIXED**: Updated railway.toml with proper healthcheck settings
   - **FIXED**: Increased timeout to 300 seconds
   - Healthcheck runs every 30 seconds

### Useful Commands:
```bash
# Local testing with production settings
python manage.py collectstatic
python manage.py migrate
DEBUG=False python manage.py runserver

# Test healthcheck endpoint locally
curl http://localhost:8000/health/
# Should return: {"status": "healthy", "service": "finsage", "database": "connected", "timestamp": "..."}
```

## 💰 Cost

- **Free tier**: 500 hours/month, $5 usage credit
- **Pro**: $5/month + usage
- **Database**: Included in both plans

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] App accessible via Railway URL
- [ ] Database migrations run
- [ ] Static files served correctly

## 🎉 You're Live!

Your Finsage finance tracker is now deployed and accessible worldwide!

**Next Steps:**
- Set up custom domain (optional)
- Configure monitoring alerts
- Set up automated backups
- Consider adding SSL certificate

---

**Need Help?** Check Railway's documentation or contact their support.
