#!/bin/bash
# Spectera Editor Launcher for macOS
# Double-click this file to run the application

cd "$(dirname "$0")"

# Try multiple Python locations to find one that works
# Priority: python.org Python (has tkinter) > PATH python3 > others
PYTHON_CMD=""

# Try python.org Python first (usually in /Library/Frameworks)
# Check for 3.12, 3.11, 3.10, etc.
for version in 3.12 3.11 3.10 3.9; do
    if [ -f "/Library/Frameworks/Python.framework/Versions/${version}/bin/python3" ]; then
        # Test if it has tkinter
        if "/Library/Frameworks/Python.framework/Versions/${version}/bin/python3" -c "import tkinter" 2>/dev/null; then
            PYTHON_CMD="/Library/Frameworks/Python.framework/Versions/${version}/bin/python3"
            break
        fi
    fi
done

# Try Current symlink
if [ -z "$PYTHON_CMD" ] && [ -f "/Library/Frameworks/Python.framework/Versions/Current/bin/python3" ]; then
    if "/Library/Frameworks/Python.framework/Versions/Current/bin/python3" -c "import tkinter" 2>/dev/null; then
        PYTHON_CMD="/Library/Frameworks/Python.framework/Versions/Current/bin/python3"
    fi
fi

# Try python3 from PATH (test if it has tkinter)
if [ -z "$PYTHON_CMD" ] && command -v python3 &> /dev/null; then
    if python3 -c "import tkinter" 2>/dev/null; then
        PYTHON_CMD="python3"
    fi
fi

# Try Homebrew Python (last resort, usually doesn't have tkinter)
if [ -z "$PYTHON_CMD" ]; then
    if [ -f "/opt/homebrew/bin/python3" ]; then
        PYTHON_CMD="/opt/homebrew/bin/python3"
    elif [ -f "/usr/local/bin/python3" ]; then
        PYTHON_CMD="/usr/local/bin/python3"
    fi
fi

# If no working Python found, show error
if [ -z "$PYTHON_CMD" ]; then
    osascript -e 'display dialog "Python 3 with tkinter is required.\n\nThe system Python has compatibility issues.\n\nPlease install Python from python.org:\nhttps://www.python.org/downloads/\n\nSee INSTALL_PYTHON.md for details." buttons {"OK"} default button "OK" with icon stop' 2>/dev/null || echo "ERROR: Please install Python from python.org"
    exit 1
fi

# Run the Python script
exec "$PYTHON_CMD" spectera_editor.py
