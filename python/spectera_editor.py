#!/usr/bin/env python3
"""
Spectera Base Station Settings Transfer Tool
Transfers device settings from one base station to another.

Copyright (C) 2024
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Tuple, Optional, Set
import os
import copy
from datetime import datetime


class SpecteraEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Spectera Base Station Settings Transfer")
        self.root.geometry("850x750")
        
        self.source_data = None
        self.target_data = None
        self.source_file_path = None
        self.target_file_path = None
        self.device_checkboxes = {}
        self.select_all_var = None
        self.mode_var = tk.StringVar(value="transfer_selected")  # transfer_selected, transfer_all
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Source file (original base station with current settings)
        ttk.Label(file_frame, text="Source File (Original Base Station):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.source_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.source_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="Browse...", command=self.select_source_file).grid(row=0, column=2, pady=5)
        
        # Target file (destination base station with re-paired devices)
        ttk.Label(file_frame, text="Target File (Destination Base Station):").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.target_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.target_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(file_frame, text="Browse...", command=self.select_target_file).grid(row=1, column=2, pady=5)
        
        # Target device count indicator
        self.target_device_count_label = ttk.Label(file_frame, text="Number of Portable devices available: 0", foreground="gray")
        self.target_device_count_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        # Operation mode selection
        mode_frame = ttk.LabelFrame(main_frame, text="Operation Mode", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(
            mode_frame,
            text="Transfer Selected Devices (map settings from old UIDs to new UIDs)",
            variable=self.mode_var,
            value="transfer_selected",
            command=self.on_mode_change
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Radiobutton(
            mode_frame,
            text="Transfer All Devices (automatically transfer all devices)",
            variable=self.mode_var,
            value="transfer_all",
            command=self.on_mode_change
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Device selection section
        device_frame = ttk.LabelFrame(main_frame, text="Select Devices to Transfer", padding="10")
        device_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        device_frame.columnconfigure(0, weight=1)
        device_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Select all checkbox
        select_all_frame = ttk.Frame(device_frame)
        select_all_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.select_all_var = tk.BooleanVar()
        select_all_cb = ttk.Checkbutton(
            select_all_frame, 
            text="Select All", 
            variable=self.select_all_var,
            command=self.toggle_select_all
        )
        select_all_cb.grid(row=0, column=0, sticky=tk.W)
        
        # Scrollable device list with checkboxes
        list_container = ttk.Frame(device_frame)
        list_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(list_container)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Enable mouse wheel scrolling (works on both Windows and macOS)
        def _on_mousewheel(event):
            if event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
        # Bind for Windows and Mac
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Store reference to canvas
        self.device_canvas = canvas
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        self.generate_button = ttk.Button(
            button_frame, 
            text="Generate Output File", 
            command=self.generate_output,
            state="disabled"
        )
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
    def on_mode_change(self):
        """Update UI when operation mode changes"""
        mode = self.mode_var.get()
        if mode == "transfer_all":
            # Auto-select all devices
            self.select_all_var.set(True)
            self.toggle_select_all()
            self.update_status("All devices selected for transfer")
        
        # Both modes require target file (with new UIDs from re-paired devices)
        if not self.target_data:
            self.target_label.config(text="No file selected", foreground="gray")
        self.check_ready()
        
    def select_source_file(self):
        filename = filedialog.askopenfilename(
            title="Select Source Base Station File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.source_data = json.load(f)
                self.source_file_path = filename
                self.source_label.config(text=os.path.basename(filename), foreground="black")
                self.update_device_list()
                self.update_status(f"Loaded source file: {len(self.source_data.get('pairedDevices', []))} devices found")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load source file:\n{str(e)}")
                
    def select_target_file(self):
        filename = filedialog.askopenfilename(
            title="Select Target Base Station File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.target_data = json.load(f)
                self.target_file_path = filename
                self.target_label.config(text=os.path.basename(filename), foreground="black")
                device_count = len(self.target_data.get('pairedDevices', []))
                self.target_device_count_label.config(
                    text=f"Number of Portable devices available: {device_count}",
                    foreground="black" if device_count > 0 else "gray"
                )
                self.update_status(f"Loaded target file: {device_count} devices available")
                self.check_ready()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load target file:\n{str(e)}")
    
    def update_device_list(self):
        """Update the device list with checkboxes from source file"""
        # Clear existing checkboxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.device_checkboxes = {}
        
        if not self.source_data or 'pairedDevices' not in self.source_data:
            return
            
        devices = self.source_data['pairedDevices']
        for idx, device in enumerate(devices):
            uid = device.get('mtUid', 'Unknown')
            name = device.get('name', 'Unnamed')
            
            # Create checkbox for each device
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                self.scrollable_frame,
                text=f"{name} (UID: {uid})",
                variable=var
            )
            cb.grid(row=idx, column=0, sticky=tk.W, pady=2)
            
            self.device_checkboxes[idx] = {
                'uid': uid,
                'name': name,
                'device': device,
                'var': var
            }
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.device_canvas.configure(scrollregion=self.device_canvas.bbox("all"))
    
    def toggle_select_all(self):
        """Toggle selection of all devices"""
        select_all = self.select_all_var.get()
        for idx in self.device_checkboxes:
            self.device_checkboxes[idx]['var'].set(select_all)
    
    def check_ready(self):
        """Enable buttons based on loaded files and mode"""
        # Both modes require both files (source with old UIDs, target with new UIDs)
        ready = self.source_data is not None and self.target_data is not None
        
        self.generate_button.config(state="normal" if ready else "disabled")
        
        # Update target device count if target not loaded
        if self.target_data is None:
            self.target_device_count_label.config(text="Number of Portable devices available: 0", foreground="gray")
    
    def get_selected_devices(self) -> List[Dict]:
        """Get list of selected devices"""
        selected_devices = []
        for idx, checkbox_data in self.device_checkboxes.items():
            if checkbox_data['var'].get():
                selected_devices.append(checkbox_data['device'])
        return selected_devices
    
    def get_audiolink_ids_for_devices(self, devices: List[Dict]) -> Set[int]:
        """Get all audiolink IDs referenced by the given devices"""
        audiolink_ids = set()
        for device in devices:
            iem_id = device.get('iemAudiolinkId', -1)
            mic_id = device.get('micAudiolinkId', -1)
            if iem_id >= 0:
                audiolink_ids.add(iem_id)
            if mic_id >= 0:
                audiolink_ids.add(mic_id)
        return audiolink_ids
    
    def clone_devices_with_routing(self, selected_devices: List[Dict], output_data: Dict) -> Dict:
        """Clone selected devices with their audio routing"""
        import copy
        
        # Get audiolink IDs used by selected devices
        used_audiolink_ids = self.get_audiolink_ids_for_devices(selected_devices)
        
        # Copy audiolinks from source that are used by selected devices
        source_audiolinks = self.source_data.get('audiolinks', [])
        output_audiolinks = output_data.get('audiolinks', [])
        output_audiolink_ids = {link.get('audiolinkId') for link in output_audiolinks}
        
        for link in source_audiolinks:
            link_id = link.get('audiolinkId')
            if link_id in used_audiolink_ids and link_id not in output_audiolink_ids:
                output_audiolinks.append(copy.deepcopy(link))
                output_audiolink_ids.add(link_id)
        
        output_data['audiolinks'] = output_audiolinks
        
        # Copy/merge audioInputs that reference used audiolinks
        source_inputs = self.source_data.get('audioInputs', [])
        target_inputs = output_data.get('audioInputs', [])
        target_input_dict = {inp.get('inputId'): inp for inp in target_inputs}
        
        for source_input in source_inputs:
            iem_link_id = source_input.get('iemAudiolinkId', -1)
            if iem_link_id in used_audiolink_ids:
                input_id = source_input.get('inputId')
                if input_id in target_input_dict:
                    # Update existing input
                    target_input_dict[input_id].update(copy.deepcopy(source_input))
                else:
                    # Add new input
                    target_inputs.append(copy.deepcopy(source_input))
        
        output_data['audioInputs'] = list(target_input_dict.values())
        
        # Copy/merge audioOutputs that reference used audiolinks
        source_outputs = self.source_data.get('audioOutputs', [])
        target_outputs = output_data.get('audioOutputs', [])
        target_output_dict = {out.get('outputId'): out for out in target_outputs}
        
        for source_output in source_outputs:
            mic_link_id = source_output.get('micAudiolinkId', -1)
            if mic_link_id in used_audiolink_ids:
                output_id = source_output.get('outputId')
                if output_id in target_output_dict:
                    # Update existing output
                    target_output_dict[output_id].update(copy.deepcopy(source_output))
                else:
                    # Add new output
                    target_outputs.append(copy.deepcopy(source_output))
        
        output_data['audioOutputs'] = list(target_output_dict.values())
        
        return output_data
    
    def generate_output(self):
        """Generate the output file based on selected mode"""
        mode = self.mode_var.get()
        
        if mode == "transfer_all":
            # Auto-select all devices
            self.select_all_var.set(True)
            self.toggle_select_all()
            self.generate_transfer()
        else:  # transfer_selected
            self.generate_transfer()
    
    def generate_transfer(self):
        """Transfer device settings from source (old UIDs) to target (new UIDs)"""
        if not self.source_data or not self.target_data:
            messagebox.showerror("Error", "Please load both source and target files.")
            return
        
        selected_devices = self.get_selected_devices()
        
        if not selected_devices:
            messagebox.showwarning("No Selection", "Please select at least one device to transfer.")
            return
        
        target_devices = self.target_data.get('pairedDevices', [])
        
        if not target_devices:
            messagebox.showerror(
                "No Target Devices",
                "The target file has no paired devices.\n\n"
                "Workflow:\n"
                "1. Pair your devices to the backup base station\n"
                "2. Save that configuration file (this becomes your target file)\n"
                "3. Use this tool to transfer settings from primary base station\n"
                "4. Load the output file into the backup base station"
            )
            return
        
        # Start with target data
        output_data = copy.deepcopy(self.target_data)
        
        # Create UID mapping: map source devices to target devices by position
        uid_mapping = {}
        source_devices = self.source_data.get('pairedDevices', [])
        selected_uids = {d.get('mtUid') for d in selected_devices}
        
        if target_devices:
            # Map selected devices by their position in the source list
            mapped_count = 0
            for i, source_device in enumerate(source_devices):
                source_uid = source_device.get('mtUid')
                if source_uid in selected_uids:
                    if i < len(target_devices):
                        target_uid = target_devices[i].get('mtUid')
                        uid_mapping[source_uid] = target_uid
                        mapped_count += 1
                    else:
                        # Not enough target devices - keep original UID
                        uid_mapping[source_uid] = source_uid
            
            if mapped_count < len(selected_devices):
                messagebox.showwarning(
                    "Mapping Warning",
                    f"Only {mapped_count} of {len(selected_devices)} devices could be mapped to target UIDs.\n"
                    f"The remaining devices will keep their original UIDs."
                )
        else:
            # No target devices - keep original UIDs
            for device in selected_devices:
                uid_mapping[device.get('mtUid')] = device.get('mtUid')
        
        # Add selected devices with mapped UIDs
        output_devices = []
        for device in selected_devices:
            new_device = copy.deepcopy(device)
            source_uid = device.get('mtUid')
            if source_uid in uid_mapping:
                new_device['mtUid'] = uid_mapping[source_uid]
            output_devices.append(new_device)
        
        output_data['pairedDevices'] = output_devices
        
        # Copy routing for selected devices
        output_data = self.clone_devices_with_routing(selected_devices, output_data)
        
        # Save file
        mapped_count = sum(1 for s, t in uid_mapping.items() if s != t)
        self.save_output_file(output_data, f"Transferred {len(output_devices)} device(s), {mapped_count} UIDs mapped")
    
    def save_output_file(self, output_data: Dict, operation_description: str):
        """Save output file with timestamp default name"""
        # Generate default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"Spectera_Setup_{timestamp}.json"
        
        # Get directory from source file if available, otherwise use current directory
        initial_dir = os.path.dirname(self.source_file_path) if self.source_file_path else os.getcwd()
        
        output_filename = filedialog.asksaveasfilename(
            title="Save Output File",
            defaultextension=".json",
            initialfile=default_filename,
            initialdir=initial_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if output_filename:
            try:
                with open(output_filename, 'w') as f:
                    json.dump(output_data, f)  # Minified to match original base station format
                
                device_count = len(output_data.get('pairedDevices', []))
                self.update_status(f"Successfully saved: {os.path.basename(output_filename)}")
                
                messagebox.showinfo(
                    "Success",
                    f"Output file saved successfully!\n\n"
                    f"Operation: {operation_description}\n"
                    f"Devices: {device_count}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save output file:\n{str(e)}")
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = SpecteraEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
