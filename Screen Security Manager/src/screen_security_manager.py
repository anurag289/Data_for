import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import pygetwindow as gw
import win32gui
import threading
import time

print("entered")

CONFIG_FILE = "sensitive_windows.json"
monitoring = False
monitoring_thread = None


def save_sensitive_windows(selected_windows):
    """Save the list of sensitive windows to a file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(selected_windows, f)


def load_sensitive_windows():
    """Load the list of sensitive windows from a file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return []


def minimize_window(window_title):
    """Minimize the specified window by title."""
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.ShowWindow(hwnd, 6)  # SW_MINIMIZE


def list_active_windows():
    """Return a list of all active window titles."""
    return [w for w in gw.getAllTitles() if w.strip()]


def monitor_windows(sensitive_windows):
    """Monitor and minimize sensitive windows."""
    global monitoring
    while monitoring:
        active_windows = list_active_windows()
        for window in active_windows:
            if window in sensitive_windows:
                minimize_window(window)
        time.sleep(0.1)


def start_monitoring_thread(sensitive_windows):
    """Start monitoring in a separate thread."""
    global monitoring, monitoring_thread
    if not monitoring:
        monitoring = True
        monitoring_thread = threading.Thread(target=monitor_windows, args=(sensitive_windows,), daemon=True)
        monitoring_thread.start()


def stop_monitoring():
    """Stop the monitoring process."""
    global monitoring
    monitoring = False


def gui_app():
    """Main GUI application."""
    print("entered")
    root = tk.Tk()
    root.title("Sensitive Windows Manager")
    root.geometry("400x400")

    global sensitive_windows, active_windows, listbox
    sensitive_windows = load_sensitive_windows()  # Load saved sensitive windows
    active_windows = list_active_windows()  # Fetch active windows

    # Status Label
    global monitoring_status_label
    monitoring_status_label = ttk.Label(root, text="Monitoring Stopped", foreground="red", font=("Arial", 14))

    # Initially hide the status label
    monitoring_status_label.pack_forget()

    def save_and_start_monitoring():
        """Save the selected windows and start monitoring."""
        global sensitive_windows

        selected = [active_windows[i] for i in listbox.curselection()]
        if not selected:
            messagebox.showwarning("No Selection", "You must select at least one window to monitor.")
            return

        sensitive_windows = selected  # Update the global sensitive list
        save_sensitive_windows(sensitive_windows)  # Save to file
        start_monitoring_thread(sensitive_windows)  # Start monitoring
        messagebox.showinfo("Monitoring Started", "Monitoring is now active!")
        update_button_states()  # Update button states

    def stop_monitoring_and_update_status():
        """Stop monitoring and update the GUI."""
        stop_monitoring()
        messagebox.showinfo("Monitoring Stopped", "Monitoring has been stopped!")
        update_button_states()

    def stop_monitoring_and_update_status_2():
        """Stop monitoring and update the GUI."""
        stop_monitoring()
        messagebox.showinfo("Monitoring Stopped", "Monitoring has been stopped!")
        update_button_states()

    def update_sensitive_windows():
        """Update the sensitive windows list."""
        global sensitive_windows

        selected = [active_windows[i] for i in listbox.curselection()]
        if not selected:
            messagebox.showwarning("No Selection", "You must select at least one window to update the sensitive list.")
            return
        print("sensitive_windows before update", sensitive_windows)
        print("selected", selected)

        sensitive_windows = selected  # Update the global sensitive list
        print("sensitive_windows after update", sensitive_windows)
        save_sensitive_windows(sensitive_windows)  # Save to file
        messagebox.showinfo("Updated", f"Sensitive windows updated to: {', '.join(sensitive_windows)}")

        # Refresh the monitoring thread with the updated list

        print("monitor flagafter stopping", monitoring)
        print("sensitive_windows before starting thread", sensitive_windows)
        stop_monitoring_and_update_status_2()
        start_monitoring_thread(sensitive_windows)
        update_button_states()

    # Buttons
    global save_start_btn, stop_monitor_btn, update_windows_btn
    save_start_btn = ttk.Button(root, text="Save and Start Monitoring", state=tk.DISABLED,
                                command=save_and_start_monitoring)
    stop_monitor_btn = ttk.Button(root, text="Stop Monitoring", state=tk.DISABLED,
                                  command=stop_monitoring_and_update_status)
    update_windows_btn = ttk.Button(root, text="Update Sensitive Windows", state=tk.DISABLED,
                                    command=update_sensitive_windows)

    # Listbox for Active Windows
    ttk.Label(root, text="Select windows to mark as sensitive:").pack(pady=5)
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
    for i, window in enumerate(active_windows):
        listbox.insert(tk.END, window)
        if window in sensitive_windows:  # Pre-select saved sensitive windows
            listbox.select_set(i)
    listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def update_button_states():
        """Update button states based on current selections, monitoring state, and changes."""
        selected_items = listbox.curselection()
        selected_windows = [active_windows[i] for i in selected_items]

        print("selected_windows", selected_windows)
        print("selected_items", selected_items)
        print("monitoring", monitoring)

        # Enable Save and Start Monitoring only if windows are selected
        save_start_btn.config(state=tk.NORMAL if selected_items and not monitoring else tk.DISABLED)

        # Enable Stop Monitoring only if monitoring is active
        stop_monitor_btn.config(state=tk.NORMAL if monitoring else tk.DISABLED)

        # Enable Update Sensitive Windows only if monitoring is active and the selection differs from the saved list
        update_windows_btn.config(
            state=tk.NORMAL if monitoring and set(selected_windows) != set(sensitive_windows) else tk.DISABLED)

        # Update monitoring status label
        monitoring_status_label.config(text="Monitoring In Progress" if monitoring else "Monitoring Stopped",
                                       foreground="green" if monitoring else "red")

        # Show the status label if monitoring is active
        if monitoring:
            monitoring_status_label.pack(pady=10)  # Show status label when monitoring starts
        else:
            monitoring_status_label.pack_forget()  # Hide status label when monitoring is stopped

        # Hide the "Stop Monitoring" button initially
        if not monitoring:
            stop_monitor_btn.pack_forget()  # Hide button if not monitoring
        else:
            stop_monitor_btn.pack(pady=5)  # Show button if monitoring is active

    # Bind listbox selection to update button states dynamically
    listbox.bind("<<ListboxSelect>>", lambda e: update_button_states())

    # Place buttons
    save_start_btn.pack(pady=5)
    update_windows_btn.pack(pady=5)

    update_button_states()  # Initialize the button states
    root.mainloop()


if __name__ == "__main__":
    print("entered")
    gui_app()