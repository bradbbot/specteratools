# Spectera Base Station Settings Transfer Tool

A web-based tool for transferring device settings between Sennheiser Spectera wireless base stations by mapping UIDs.

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

- **Simple Web Interface**: Works in any modern web browser
- **No Installation**: Runs entirely in your browser - no downloads or installations needed
- **Privacy**: All processing happens locally - your files never leave your computer
- **Device Selection**: Checkbox list showing all devices with their names and UIDs
- **Select All**: Quick selection/deselection of all devices
- **UID Mapping**: Automatically maps source device UIDs to destination base station UIDs
- **Routing Preservation**: Copies audio routing (audiolinks, inputs, outputs) for transferred devices

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- No additional software or plugins needed

## Usage

### Workflow Overview

Since portable devices must be re-paired to each base station (and get new UIDs), the workflow is:

1. **Pair devices to destination base station** → Devices get new UIDs for that base station
2. **Save configuration** → This becomes your "Target File" (has new UIDs)
3. **Use this tool** → Transfer settings from original base station (old UIDs) to destination (new UIDs)
4. **Load output file** → Into the destination base station

### Step-by-Step Instructions

1. **Prepare Target File**:
   - Pair all your devices to the destination base station
   - Export/save the configuration from the destination base station
   - This file contains the new UIDs assigned by the destination base station

2. **Prepare Source File**:
   - Export/save the configuration from your original base station
   - This file contains the old UIDs and all your device settings

3. **Use the Tool**:
   - Open the web application in your browser
   - Click "Browse..." next to "Source File (Original Base Station)" and select your original config
   - Click "Browse..." next to "Target File (Destination Base Station)" and select your destination config
   - Choose operation mode:
     - **Transfer Selected Devices**: Select which devices to transfer
     - **Transfer All Devices**: Automatically transfers all devices
   - Select devices (if using "Transfer Selected Devices")
   - Click "Generate Output File"
   - The file will automatically download
   - Load the downloaded file into your destination base station

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

## How It Works

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

## Notes

- **Devices must be re-paired**: Portable devices get new UIDs when paired to a different base station
- **Mapping by position**: Devices are mapped by their position in the `pairedDevices` array
- **Order matters**: Pair devices to the destination base station in the same order as the original for best results
- **All settings preserved**: Volume, gain, routing, channel assignments, etc. are all copied
- **Audio routing copied**: The tool copies audiolinks and related audioInputs/audioOutputs

## Troubleshooting

**"No Target Devices" error**: The target file has no paired devices. You must pair devices to the destination base station first, then save that configuration.

**UIDs not mapping correctly**: Ensure devices are paired to the destination base station in the same order as they appear in the source file. The tool maps by position (first device to first device).

**File won't load in base station**: Verify that:
- The target file was created after pairing devices to the destination base station
- The number of devices matches between source and target
- The output file is a valid JSON file

## Privacy & Security

- **100% Local Processing**: All file processing happens in your browser
- **No Server Upload**: Your files are never uploaded to any server
- **No Data Collection**: No analytics, tracking, or data collection
- **Works Offline**: Once loaded, the page works completely offline

## Technical Details

- **Technology**: Pure HTML, CSS, and JavaScript
- **No Dependencies**: No frameworks or libraries required
- **File Format**: JSON (Sennheiser Spectera configuration format)
- **Browser Compatibility**: Works in all modern browsers (Chrome, Firefox, Safari, Edge)

## Support

This is an experimental tool created to solve a specific workflow limitation. For official support, please contact Sennheiser.

## License

This tool is provided as-is for use with Sennheiser Spectera wireless systems. See disclaimer above.
