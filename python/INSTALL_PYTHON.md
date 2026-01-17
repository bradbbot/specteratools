# Python Installation Fix

## The Problem

The system Python (`/usr/bin/python3`) from Command Line Tools has a minimum macOS version check that's causing it to crash with:
```
macOS 12 (1207) or later required, have instead 12 (1206) !
```

## Solution: Install Python from python.org

The easiest fix is to install Python from python.org, which includes tkinter and doesn't have this version check issue.

### Steps:

1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Download Python 3.11 or 3.12 for macOS
   - Choose the "macOS 64-bit universal2 installer" (works on Intel and Apple Silicon)

2. **Install Python**:
   - Run the installer
   - **Important**: Check "Add Python to PATH" during installation
   - Complete the installation

3. **Update the launcher**:
   - The `run_spectera_editor.command` will automatically find the new Python
   - Or it will be available as `python3` in your PATH

4. **Test**:
   ```bash
   python3 --version
   python3 -c "import tkinter; print('tkinter works!')"
   ```

5. **Run the app**:
   - Double-click `run_spectera_editor.command`
   - It should now work!

## Alternative: Use Homebrew Python (if you have Homebrew)

If you have Homebrew installed:

```bash
brew install python-tk
```

This installs Python with tkinter support. Then update the launcher to use:
```bash
/opt/homebrew/bin/python3  # Apple Silicon
# or
/usr/local/bin/python3     # Intel
```

## Why This Happens

The Command Line Tools Python was built with a minimum macOS version requirement that your system doesn't meet (even though you're on 12.7.6, something is reporting 12.6 to the binary). Python from python.org doesn't have this restriction.
