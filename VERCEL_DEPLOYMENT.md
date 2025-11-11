# Deploying to Vercel

This guide will help you deploy your AI Agent to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your Gemini API key
3. Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Push Your Code to Git

Make sure your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket).

## Step 2: Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your Git repository
4. Vercel will automatically detect it's a Python project

## Step 3: Configure Environment Variables

**This is the most important step!**

1. In your Vercel project settings, go to **Settings** → **Environment Variables**
2. Add a new environment variable:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your actual Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
   - **Environment:** Select all (Production, Preview, Development)
3. Click "Save"

## Step 4: Configure Build Settings

Vercel should automatically detect the Python runtime, but verify:

1. Go to **Settings** → **General**
2. Under "Build & Development Settings":
   - **Framework Preset:** Other
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
   - **Install Command:** `pip install -r requirements.txt`

## Step 5: Deploy

1. Click "Deploy" button
2. Wait for the build to complete
3. Your app will be live at `https://your-project.vercel.app`

## Step 6: Verify Deployment

1. Visit your deployed URL
2. Try sending a message in the chat
3. If you see an error about API key, double-check Step 3

## Troubleshooting

### Error: "Gemini API key not configured"

**Solution:** Make sure you've added `GEMINI_API_KEY` in Vercel's Environment Variables:
1. Go to Settings → Environment Variables
2. Verify the variable is set for all environments
3. Redeploy after adding the variable

### Error: "Module not found"

**Solution:** Check that `requirements.txt` includes all dependencies:
```bash
fastapi==0.115.0
uvicorn[standard]==0.32.0
google-generativeai==0.8.3
python-dotenv==1.0.1
pydantic==2.9.2
```

### Error: "index.html not found"

**Solution:** Make sure `index.html` is in the same directory as `app.py`

## Important Notes

1. **Never commit your `.env` file** - It's already in `.gitignore`
2. **Environment variables are encrypted** in Vercel
3. **Redeploy after changing environment variables** - Changes take effect on next deployment
4. **Free tier limitations** - Vercel's free tier has execution time limits (10 seconds for Hobby plan)

## Alternative: Using Vercel CLI

You can also deploy using the Vercel CLI:

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variable
vercel env add GEMINI_API_KEY

# Redeploy
vercel --prod
```

## Support

If you encounter issues:
1. Check Vercel's build logs
2. Verify environment variables are set correctly
3. Check that all files are in the repository
4. Ensure `vercel.json` is configured correctly

