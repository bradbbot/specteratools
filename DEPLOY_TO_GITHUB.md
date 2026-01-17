# Deploying to GitHub Pages

## Quick Setup

1. **Create a new repository on GitHub**
   - Go to https://github.com/new
   - Name it something like `spectera-editor` or `spectera-settings-transfer`
   - Make it public (required for free GitHub Pages)
   - Don't initialize with README (we already have files)

2. **Upload the web files**
   You need these 3 files:
   - `index.html`
   - `styles.css`
   - `app.js`
   
   You can either:
   - Use GitHub's web interface: Click "uploading an existing file" and drag the 3 files
   - Or use git commands (see below)

3. **Enable GitHub Pages**
   - Go to your repository Settings
   - Scroll to "Pages" in the left sidebar
   - Under "Source", select your branch (usually `main` or `master`)
   - Click Save
   - Your site will be live at: `https://yourusername.github.io/repository-name/`

## Using Git (Alternative Method)

If you prefer using git from the command line:

```bash
cd ~/Desktop/SpecteraEdit

# Initialize git (if not already done)
git init

# Add the web files
git add index.html styles.css app.js README_WEB.md

# Commit
git commit -m "Initial web version"

# Add your GitHub repository as remote (replace with your URL)
git remote add origin https://github.com/yourusername/your-repo-name.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Then enable GitHub Pages in the repository settings as described above.

## Testing Locally

Before deploying, you can test locally:
- Simply open `index.html` in your web browser
- Everything works offline - no server needed!

## What Gets Deployed

Only these files are needed for the web version:
- `index.html` - The main page
- `styles.css` - Styling
- `app.js` - All the functionality

You don't need to upload:
- The Python files (`spectera_editor.py`)
- The `.command` file
- The example JSON files (unless you want them as examples)

## Privacy Note

The web version runs entirely in the user's browser. Files are never uploaded to any server - everything is processed locally. This means:
- ✅ Completely private
- ✅ Works offline
- ✅ No data leaves the user's computer
