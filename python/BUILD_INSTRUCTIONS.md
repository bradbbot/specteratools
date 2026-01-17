# Building Standalone Applications

## macOS (.app bundle)

### Option 1: Native App Bundle (Recommended - Works on all macOS versions)

**This method creates a proper .app bundle without using PyInstaller or py2app, avoiding compatibility issues.**

**Prerequisites:**
- Python 3.6+ with tkinter (system Python at `/usr/bin/python3` works)
- No additional packages needed!

**Build Steps:**

1. **Run the build script**:
   ```bash
   ./create_app_bundle.sh
   ```

2. **Find your application**:
   - The built app will be at: `dist/SpecteraEditor.app`
   - You can double-click it to run
   - Move it to your Applications folder if desired

**Note:** This app bundle runs the Python script directly using the system Python. It requires Python 3 with tkinter to be installed, but doesn't bundle Python itself (avoiding compatibility issues).

### Option 2: py2app (Alternative - may have macOS version issues)

**Prerequisites:**
- Python 3.6+ with tkinter (system Python at `/usr/bin/python3` works)
- py2app (will be installed automatically if missing)

**Build Steps:**

1. **Run the py2app build script**:
   ```bash
   ./build_mac_py2app.sh
   ```
   
   Or if you get a permission error:
   ```bash
   bash build_mac_py2app.sh
   ```

2. **Find your application**:
   - The built app will be at: `dist/SpecteraEditor.app`
   - You can double-click it to run
   - Move it to your Applications folder if desired

### Option 2: PyInstaller (Requires macOS 12.7+)

**Note:** PyInstaller requires macOS 12.7 or later. If you're on macOS 12.6 or earlier, use Option 1 (py2app) instead.

**Prerequisites:**
- Python 3.6+ with tkinter (system Python at `/usr/bin/python3` works)
- PyInstaller (will be installed automatically if missing)
- macOS 12.7 or later

**Build Steps:**

1. **Install PyInstaller** (if not already installed):
   ```bash
   /usr/bin/python3 -m pip install pyinstaller --user
   ```

2. **Run the build script**:
   ```bash
   ./build_mac.sh
   ```

3. **Find your application**:
   - The built app will be at: `dist/SpecteraEditor.app`
   - You can double-click it to run

### Troubleshooting

**"macOS 12 (1207) or later required" error:**
- This means you're on macOS 12.6 or earlier
- **Solution:** Use Option 1 (py2app) instead: `./build_mac_py2app.sh`

**If py2app installation fails:**
  ```bash
  python3 -m pip install --upgrade pip
  /usr/bin/python3 -m pip install py2app --user
  ```

**If PyInstaller installation fails:**
  ```bash
  python3 -m pip install --upgrade pip
  /usr/bin/python3 -m pip install pyinstaller --user
  ```

## Windows (.exe)

### Prerequisites
- Python 3.6+ with tkinter (download from python.org)
- PyInstaller (will be installed automatically if missing)

### Build Steps

1. **Open Command Prompt or PowerShell** in the SpecteraEdit folder
   - Right-click in the folder → "Open in Terminal" or "Open PowerShell window here"

2. **Install PyInstaller** (if not already installed):
   ```cmd
   python -m pip install pyinstaller
   ```

3. **Run the build script**:
   ```cmd
   build_windows.bat
   ```
   
   Or manually:
   ```cmd
   python -m PyInstaller --name="SpecteraEditor" --windowed --onefile spectera_editor.py
   ```

4. **Find your executable**:
   - The built .exe will be at: `dist\SpecteraEditor.exe`
   - This is a standalone executable that can run on any Windows machine
   - You can distribute this single file (no Python installation needed on target machines)

### Troubleshooting

- **"Python is not recognized"**: 
  - Make sure Python is installed from python.org
  - Add Python to your PATH during installation
  - Or use the full path: `C:\Python3x\python.exe -m pip install pyinstaller`

- **"tkinter is missing"**: 
  - Install Python from python.org (not Microsoft Store version)
  - The python.org version includes tkinter by default

- **Antivirus warnings**: 
  - Some antivirus software flags PyInstaller executables
  - This is a false positive - you can add an exception
  - The executable is safe (it's your Python script bundled)

- **"Failed to execute script"**:
  - Make sure you're using `--windowed` flag (no console window)
  - Check that tkinter is properly installed: `python -c "import tkinter"`

## Testing the Built Applications

### macOS
1. Double-click `dist/SpecteraEditor.app`
2. If you get a security warning:
   - Go to System Preferences > Security & Privacy
   - Click "Open Anyway" next to the warning message
   - Or right-click the app and select "Open"

### Windows
1. Double-click `dist\SpecteraEditor.exe`
2. Windows Defender might show a warning (first run only)
3. Click "More info" then "Run anyway"

## Distribution

### macOS
- Share the entire `SpecteraEditor.app` folder
- Users can drag it to their Applications folder
- No installation needed

### Windows
- Share the single `SpecteraEditor.exe` file
- Users can run it directly
- No installation needed
