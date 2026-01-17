// Spectera Base Station Settings Transfer Tool
// Web version - runs entirely in the browser

let sourceData = null;
let targetData = null;
let deviceCheckboxes = {};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updateStatus('Ready');
});

function setupEventListeners() {
    // File inputs
    document.getElementById('source-file').addEventListener('change', handleSourceFile);
    document.getElementById('target-file').addEventListener('change', handleTargetFile);
    
    // Mode selection
    document.querySelectorAll('input[name="mode"]').forEach(radio => {
        radio.addEventListener('change', handleModeChange);
    });
    
    // Select all checkbox
    document.getElementById('select-all').addEventListener('change', toggleSelectAll);
    
    // Generate button
    document.getElementById('generate-btn').addEventListener('click', generateOutput);
}

function handleSourceFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            sourceData = JSON.parse(e.target.result);
            document.getElementById('source-filename').textContent = file.name;
            document.getElementById('source-filename').classList.add('has-file');
            updateDeviceList();
            updateStatus(`Loaded source file: ${sourceData.pairedDevices?.length || 0} devices found`);
            checkReady();
        } catch (error) {
            alert(`Failed to load source file:\n${error.message}`);
        }
    };
    reader.readAsText(file);
}

function handleTargetFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            targetData = JSON.parse(e.target.result);
            document.getElementById('target-filename').textContent = file.name;
            document.getElementById('target-filename').classList.add('has-file');
            
            const deviceCount = targetData.pairedDevices?.length || 0;
            const countLabel = document.getElementById('target-device-count');
            countLabel.textContent = `Number of Portable devices available: ${deviceCount}`;
            if (deviceCount > 0) {
                countLabel.classList.add('has-devices');
            } else {
                countLabel.classList.remove('has-devices');
            }
            
            updateStatus(`Loaded target file: ${deviceCount} devices available`);
            checkReady();
        } catch (error) {
            alert(`Failed to load target file:\n${error.message}`);
        }
    };
    reader.readAsText(file);
}

function handleModeChange(event) {
    if (event.target.value === 'transfer_all') {
        document.getElementById('select-all').checked = true;
        toggleSelectAll();
        updateStatus('All devices selected for transfer');
    }
    checkReady();
}

function updateDeviceList() {
    const deviceList = document.getElementById('device-list');
    deviceCheckboxes = {};
    
    if (!sourceData || !sourceData.pairedDevices || sourceData.pairedDevices.length === 0) {
        deviceList.innerHTML = '<p class="placeholder">No devices found in source file</p>';
        return;
    }
    
    deviceList.innerHTML = '';
    
    sourceData.pairedDevices.forEach((device, idx) => {
        const uid = device.mtUid || 'Unknown';
        const name = device.name || 'Unnamed';
        
        const item = document.createElement('div');
        item.className = 'device-item';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `device-${idx}`;
        checkbox.dataset.index = idx;
        checkbox.addEventListener('change', () => checkReady());
        
        const label = document.createElement('label');
        label.htmlFor = `device-${idx}`;
        label.textContent = `${name} (UID: ${uid})`;
        
        item.appendChild(checkbox);
        item.appendChild(label);
        deviceList.appendChild(item);
        
        deviceCheckboxes[idx] = {
            checkbox: checkbox,
            device: device
        };
    });
}

function toggleSelectAll() {
    const selectAll = document.getElementById('select-all').checked;
    Object.values(deviceCheckboxes).forEach(item => {
        item.checkbox.checked = selectAll;
    });
    checkReady();
}

function getSelectedDevices() {
    const selected = [];
    Object.values(deviceCheckboxes).forEach(item => {
        if (item.checkbox.checked) {
            selected.push(item.device);
        }
    });
    return selected;
}

function checkReady() {
    const ready = sourceData !== null && targetData !== null;
    const generateBtn = document.getElementById('generate-btn');
    generateBtn.disabled = !ready;
}

function getAudiolinkIdsForDevices(devices) {
    const audiolinkIds = new Set();
    devices.forEach(device => {
        const iemId = device.iemAudiolinkId;
        const micId = device.micAudiolinkId;
        if (iemId !== undefined && iemId >= 0) audiolinkIds.add(iemId);
        if (micId !== undefined && micId >= 0) audiolinkIds.add(micId);
    });
    return audiolinkIds;
}

function cloneDevicesWithRouting(selectedDevices, outputData) {
    // Get audiolink IDs used by selected devices
    const usedAudiolinkIds = getAudiolinkIdsForDevices(selectedDevices);
    
    // Copy audiolinks from source that are used by selected devices
    const sourceAudiolinks = sourceData.audiolinks || [];
    const outputAudiolinks = outputData.audiolinks || [];
    const outputAudiolinkIds = new Set(outputAudiolinks.map(link => link.audiolinkId));
    
    sourceAudiolinks.forEach(link => {
        const linkId = link.audiolinkId;
        if (usedAudiolinkIds.has(linkId) && !outputAudiolinkIds.has(linkId)) {
            outputAudiolinks.push(JSON.parse(JSON.stringify(link)));
            outputAudiolinkIds.add(linkId);
        }
    });
    
    outputData.audiolinks = outputAudiolinks;
    
    // Copy/merge audioInputs that reference used audiolinks
    const sourceInputs = sourceData.audioInputs || [];
    const targetInputs = outputData.audioInputs || [];
    const targetInputDict = {};
    targetInputs.forEach(inp => {
        targetInputDict[inp.inputId] = JSON.parse(JSON.stringify(inp));
    });
    
    sourceInputs.forEach(sourceInput => {
        const iemLinkId = sourceInput.iemAudiolinkId;
        if (usedAudiolinkIds.has(iemLinkId)) {
            const inputId = sourceInput.inputId;
            if (targetInputDict[inputId]) {
                Object.assign(targetInputDict[inputId], JSON.parse(JSON.stringify(sourceInput)));
            } else {
                targetInputDict[inputId] = JSON.parse(JSON.stringify(sourceInput));
            }
        }
    });
    
    outputData.audioInputs = Object.values(targetInputDict);
    
    // Copy/merge audioOutputs that reference used audiolinks
    const sourceOutputs = sourceData.audioOutputs || [];
    const targetOutputs = outputData.audioOutputs || [];
    const targetOutputDict = {};
    targetOutputs.forEach(out => {
        targetOutputDict[out.outputId] = JSON.parse(JSON.stringify(out));
    });
    
    sourceOutputs.forEach(sourceOutput => {
        const micLinkId = sourceOutput.micAudiolinkId;
        if (usedAudiolinkIds.has(micLinkId)) {
            const outputId = sourceOutput.outputId;
            if (targetOutputDict[outputId]) {
                Object.assign(targetOutputDict[outputId], JSON.parse(JSON.stringify(sourceOutput)));
            } else {
                targetOutputDict[outputId] = JSON.parse(JSON.stringify(sourceOutput));
            }
        }
    });
    
    outputData.audioOutputs = Object.values(targetOutputDict);
    
    return outputData;
}

function generateOutput() {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    
    if (mode === 'transfer_all') {
        document.getElementById('select-all').checked = true;
        toggleSelectAll();
    }
    
    let selectedDevices = getSelectedDevices();
    
    if (selectedDevices.length === 0) {
        alert('Please select at least one device to transfer.');
        return;
    }
    
    const targetDevices = targetData.pairedDevices || [];
    
    if (targetDevices.length === 0) {
        alert(
            'The target file has no paired devices.\n\n' +
            'Workflow:\n' +
            '1. Pair your devices to the destination base station\n' +
            '2. Save that configuration file (this becomes your target file)\n' +
            '3. Use this tool to transfer settings from original base station\n' +
            '4. Load the output file into the destination base station'
        );
        return;
    }
    
    // Start with target data
    const outputData = JSON.parse(JSON.stringify(targetData));
    
    // Create UID mapping: map source devices to target devices by position
    const uidMapping = {};
    const sourceDevices = sourceData.pairedDevices || [];
    const selectedUids = new Set(selectedDevices.map(d => d.mtUid));
    
    let mappedCount = 0;
    sourceDevices.forEach((sourceDevice, i) => {
        const sourceUid = sourceDevice.mtUid;
        if (selectedUids.has(sourceUid)) {
            if (i < targetDevices.length) {
                const targetUid = targetDevices[i].mtUid;
                uidMapping[sourceUid] = targetUid;
                mappedCount++;
            } else {
                uidMapping[sourceUid] = sourceUid;
            }
        }
    });
    
    if (mappedCount < selectedDevices.length) {
        const warning = `Only ${mappedCount} of ${selectedDevices.length} devices could be mapped to target UIDs.\n` +
                       `The remaining devices will keep their original UIDs.`;
        if (!confirm(warning + '\n\nContinue anyway?')) {
            return;
        }
    }
    
    // Add selected devices with mapped UIDs
    const outputDevices = [];
    selectedDevices.forEach(device => {
        const newDevice = JSON.parse(JSON.stringify(device));
        const sourceUid = device.mtUid;
        if (uidMapping[sourceUid] !== undefined) {
            newDevice.mtUid = uidMapping[sourceUid];
        }
        outputDevices.push(newDevice);
    });
    
    outputData.pairedDevices = outputDevices;
    
    // Copy routing for selected devices
    cloneDevicesWithRouting(selectedDevices, outputData);
    
    // Generate filename with timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19).replace('T', '_');
    const filename = `Spectera_Setup_${timestamp}.json`;
    
    // Download file
    const blob = new Blob([JSON.stringify(outputData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    const mappedCountFinal = Object.entries(uidMapping).filter(([sourceUid, targetUid]) => {
        return sourceUid != targetUid;
    }).length;
    
    updateStatus(`Successfully saved: ${filename}`);
    alert(
        `Output file saved successfully!\n\n` +
        `Operation: Transferred ${outputDevices.length} device(s), ${mappedCountFinal} UIDs mapped\n` +
        `Devices: ${outputDevices.length}`
    );
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}
