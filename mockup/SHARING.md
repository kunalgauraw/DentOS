# How to Share DentOS Mockup for Feedback

## Option 1: Share as ZIP File (Easiest)

### Steps:
1. **Create ZIP file:**
   - Right-click on `C:\Dev\DentOS\mockup` folder
   - Select "Send to" → "Compressed (zipped) folder"
   - This creates `mockup.zip`

2. **Share via:**
   - **Email:** Attach the ZIP file
   - **WhatsApp:** Send as document
   - **Google Drive / OneDrive:** Upload and share link
   - **WeTransfer:** Upload and get shareable link

3. **Recipient opens:**
   - Download and extract ZIP
   - Open `index.html` in browser

**Pros:** Simple, no internet required for viewing
**Cons:** Recipient needs to download and extract

---

## Option 2: GitHub Pages (Free Hosting)

### Steps:
1. **Create GitHub account** (if not already): https://github.com

2. **Create new repository:**
   - Name: `dentos-mockup`
   - Make it **Public**

3. **Upload mockup files:**
   - Upload all files from `mockup/` folder

4. **Enable GitHub Pages:**
   - Go to Settings → Pages
   - Source: Deploy from branch
   - Branch: `main` / `root`
   - Save

5. **Share URL:**
   ```
   https://yourusername.github.io/dentos-mockup/
   ```

**Pros:** Free, always accessible, easy to update
**Cons:** Requires GitHub account, public by default

---

## Option 3: Netlify Drop (Instant, Free)

### Steps:
1. Go to https://app.netlify.com/drop

2. **Drag & drop** the entire `mockup` folder

3. **Get instant URL** like:
   ```
   https://random-name-12345.netlify.app
   ```

4. **Share the URL** via WhatsApp, Email, etc.

**Pros:** Instant, no account needed, free
**Cons:** URL expires after some time (unless you create account)

---

## Option 4: Local Network Sharing

If reviewer is on same WiFi network:

### Steps:
1. **Open Command Prompt** in mockup folder

2. **Start simple server:**
   ```
   python -m http.server 8080
   ```
   Or if Python not installed:
   ```
   npx serve
   ```

3. **Find your IP address:**
   ```
   ipconfig
   ```
   Look for IPv4 Address (e.g., 192.168.1.100)

4. **Share URL:**
   ```
   http://192.168.1.100:8080
   ```

**Pros:** No internet upload needed
**Cons:** Only works on same network

---

## Option 5: VS Code Live Share

If reviewer has VS Code:

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Use "Share" feature to get public URL

---

## Recommended Approach

| Scenario | Best Option |
|----------|-------------|
| Quick share to 1-2 people | **Netlify Drop** |
| Share with team permanently | **GitHub Pages** |
| Share via WhatsApp/Email | **ZIP file** |
| Demo in same office | **Local Network** |

---

## Collecting Feedback

Ask reviewers to note:

1. **Screen name** (e.g., "Patient Registration")
2. **What's wrong** or **What's missing**
3. **Suggestion** for improvement

Example feedback format:
```
Screen: Patient Registration
Issue: Blood group field should be mandatory
Suggestion: Add dropdown with common blood groups
```

---

## Quick Command to Create ZIP

Run in Command Prompt:
```cmd
cd C:\Dev\DentOS
powershell Compress-Archive -Path mockup -DestinationPath DentOS-Mockup.zip
```

This creates `DentOS-Mockup.zip` ready to share!
