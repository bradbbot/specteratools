# Quick Start Guide

## The Simplest Way to Run (Recommended)

**Just double-click `run_spectera_editor.command`** - This works reliably on macOS!

1. Double-click `run_spectera_editor.command` in Finder
2. If you get a security warning, right-click and select "Open"
3. The application will launch

This is the most reliable method and avoids all the app bundle compatibility issues.

## Alternative: App Bundle (May Have Issues)

If you want a proper `.app` file, you can try:

```bash
./create_app_bundle.sh
```

Then double-click `dist/SpecteraEditor.app`

**Note:** Some macOS versions may have issues with shell script launchers in app bundles. If you get "Python quit unexpectedly", use the `.command` file instead.

## Why the .command file is better:

- ✅ Works on all macOS versions
- ✅ No compatibility issues
- ✅ Simple and reliable
- ✅ Uses system Python directly

The `.command` file is essentially a double-clickable script that works just like an app!
