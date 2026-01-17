# Spectera Base Station Settings Transfer Tool

A tool for transferring device settings between Sennheiser Spectera wireless base stations by mapping UIDs.

## Two Versions Available

- **Web Version** (this directory) - Runs in your browser, no installation needed
- **Python Desktop Version** (`python/` folder) - Cross-platform desktop application

Both versions have the same functionality. Choose based on your preference:
- **Web**: Easiest to use, works on any device with a browser
- **Python**: Desktop app, works offline, can be packaged as standalone executable

## ⚠️ IMPORTANT DISCLAIMER

**This software is experimental and provided "as-is" without any warranties.**

- **NOT FOR MISSION-CRITICAL USE**: This tool is experimental and should not be used in mission-critical or production environments where system failure could result in significant consequences.
- **NO LIABILITY**: The developer and contributors are not responsible for any problems, data loss, equipment damage, or other issues that may arise from the use of this software.
- **USE AT YOUR OWN RISK**: You assume all risks associated with using this tool. Always test thoroughly in a non-critical environment before use.
- **NO WARRANTY**: This software is provided without warranty of any kind, express or implied, including but not limited to the implied warranties of merchantability and fitness for a particular purpose.

**Always maintain backups of your original configuration files before using this tool.**

## Overview

This tool allows you to port portable device settings from one Spectera base station to another. Since portable devices must be re-paired to each base station (and receive new UIDs), this tool maps the old UIDs to new UIDs while preserving all device settings.

## Features

- **Simple Interface**: Easy-to-use GUI (Python) or web interface
- **Device Selection**: Checkbox list showing all devices with their names and UIDs
- **Select All**: Quick selection/deselection of all devices
- **UID Mapping**: Automatically maps source device UIDs to destination base station UIDs
- **Routing Preservation**: Copies audio routing (audiolinks, inputs, outputs) for transferred devices

## Quick Start

### Web Version
1. Open `index.html` in your web browser
2. Select source and target files
3. Choose devices to transfer
4. Download the output file

### Python Version
See `python/README.md` for detailed instructions.

**macOS**: Double-click `python/run_spectera_editor.command`  
**Windows**: Run `python python/spectera_editor.py`

## Usage

### Workflow Overview

Since portable devices must be re-paired to each base station (and get new UIDs), the workflow is:

1. **Pair devices to destination base station** → Devices get new UIDs for that base station
2. **Save configuration** → This becomes your "Target File" (has new UIDs)
3. **Use this tool** → Transfer settings from original base station (old UIDs) to destination (new UIDs)
4. **Load output file** → Into the destination base station

### How It Works

The tool:
1. Reads both JSON configuration files (source with old UIDs + all settings, target with new UIDs)
2. For each selected device from the source file:
   - **Takes all the settings** from the source device (volume, gain, routing, name, etc.)
   - **Replaces the UID** with the corresponding new UID from the target file
   - Maps by position: 1st source device → 1st target device UID, 2nd → 2nd, etc.
3. Copies audio routing (audiolinks, audioInputs, audioOutputs) for the transferred devices
4. Preserves the destination base station's base configuration
5. Generates a new JSON file ready to load into the destination base station

**In simple terms**: The tool copies all your device settings from the source file and applies the new UIDs from the target file to them.

## Operation Modes

### Transfer Selected Devices
- Select which devices to transfer using checkboxes
- Takes all settings from source devices
- Replaces UIDs with new UIDs from target file
- Copies all settings and routing for selected devices

### Transfer All Devices
- Automatically selects all devices
- Takes all settings from all source devices
- Replaces all UIDs with new UIDs from target file
- Copies all settings and routing for all devices

## Notes

- **Devices must be re-paired**: Portable devices get new UIDs when paired to a different base station
- **Mapping by position**: Devices are mapped by their position in the `pairedDevices` array
- **Order matters**: Pair devices to the destination base station in the same order as the original for best results
- **All settings preserved**: Volume, gain, routing, channel assignments, etc. are all copied
- **Audio routing copied**: The tool copies audiolinks and related audioInputs/audioOutputs

## Troubleshooting

**"No Target Devices" error**: The target file has no paired devices. You must pair devices to the destination base station first, then save that configuration.

**UIDs not mapping correctly**: Ensure devices are paired to the destination base station in the same order as they appear in the source file. The tool maps by position (first device to first device).

## Privacy & Security (Web Version)

- **100% Local Processing**: All file processing happens in your browser
- **No Server Upload**: Your files are never uploaded to any server
- **No Data Collection**: No analytics, tracking, or data collection
- **Works Offline**: Once loaded, the page works completely offline

## Documentation

- **Web Version**: See this README
- **Python Version**: See `python/README.md`
- **Deployment**: See `DEPLOY_TO_GITHUB.md` for GitHub Pages setup

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [GNU General Public License](LICENSE) for more details.

See disclaimer above for important usage warnings.
