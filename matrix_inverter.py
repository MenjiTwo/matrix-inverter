#!/usr/bin/env python3
"""
Matrix Inverter - A cross-platform GUI application for inverting matrices.
"""

import subprocess
import sys
import os
import platform

# Application version
VERSION = "1.0.2"

def check_and_install_requirements():
    """Check if required packages are installed and install them if missing."""
    required_packages = {
        'numpy': 'numpy',
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if (missing_packages):
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '--quiet', *missing_packages
            ])
            print("Packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install packages: {e}")
            print("Please run: pip install -r requirements.txt")
            sys.exit(1)


# Auto-install requirements before importing
check_and_install_requirements()

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from typing import List, Tuple
import urllib.request
import json
import threading

from theme import (
    apply_theme,
    create_styled_entry,
    create_styled_label,
    COLORS,
    FONTS,
    SPACING
)

# GitHub repository for update checking
GITHUB_REPO = "MenjiTwo/matrix-inverter"


def get_asset_name_for_os() -> str:
    """Get the correct asset name for the current operating system."""
    system = platform.system().lower()
    if system == "windows":
        return "matrix-inverter-windows.exe"
    elif system == "darwin":
        return "matrix-inverter-macos"
    else:  # Linux and others
        return "matrix-inverter-linux"


def download_update(download_url: str, asset_name: str) -> bool:
    """
    Download the update to the same directory as the current executable.
    
    Returns True if successful, False otherwise.
    """
    try:
        # Determine download location
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            current_dir = os.path.dirname(sys.executable)
            current_name = os.path.basename(sys.executable)
        else:
            # Running as script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            current_name = asset_name
        
        # New file path (add _new suffix to avoid overwriting while running)
        new_file_path = os.path.join(current_dir, f"{asset_name}_new")
        
        # Show progress dialog
        progress_window = tk.Toplevel()
        progress_window.title("Downloading Update")
        progress_window.geometry("350x100")
        progress_window.resizable(False, False)
        progress_window.transient()
        progress_window.grab_set()
        
        ttk.Label(
            progress_window, 
            text="Downloading update, please wait...",
            padding=10
        ).pack()
        
        progress_bar = ttk.Progressbar(
            progress_window, 
            mode='indeterminate',
            length=300
        )
        progress_bar.pack(pady=10)
        progress_bar.start(10)
        
        progress_window.update()
        
        # Download the file
        request = urllib.request.Request(
            download_url, 
            headers={"User-Agent": "Matrix-Inverter"}
        )
        
        with urllib.request.urlopen(request, timeout=60) as response:
            with open(new_file_path, 'wb') as out_file:
                out_file.write(response.read())
        
        # Make executable on Unix systems
        if platform.system().lower() != "windows":
            os.chmod(new_file_path, 0o755)
        
        progress_window.destroy()
        
        # Instructions for the user
        if platform.system().lower() == "windows":
            instructions = (
                f"Update downloaded successfully!\n\n"
                f"The new version has been saved as:\n"
                f"{new_file_path}\n\n"
                f"To complete the update:\n"
                f"1. Close this application\n"
                f"2. Delete the old file ({current_name})\n"
                f"3. Rename '{asset_name}_new' to '{current_name}'\n"
                f"4. Run the new version"
            )
        else:
            instructions = (
                f"Update downloaded successfully!\n\n"
                f"The new version has been saved as:\n"
                f"{new_file_path}\n\n"
                f"To complete the update, run these commands:\n"
                f"1. Close this application\n"
                f"2. mv '{new_file_path}' '{os.path.join(current_dir, asset_name)}'\n"
                f"3. Run the new version"
            )
        
        messagebox.showinfo("Update Downloaded", instructions)
        return True
        
    except Exception as e:
        try:
            progress_window.destroy()
        except:
            pass
        messagebox.showerror(
            "Download Failed",
            f"Failed to download update: {str(e)}\n\n"
            f"Please download manually from the releases page."
        )
        return False


def check_for_updates(show_no_update_message: bool = False) -> None:
    """Check GitHub releases for a newer version."""
    def _check():
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            request = urllib.request.Request(url, headers={"User-Agent": "Matrix-Inverter"})
            with urllib.request.urlopen(request, timeout=5) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get("tag_name", "").lstrip("v")
                release_url = data.get("html_url", "")
                assets = data.get("assets", [])
                
                if latest_version and latest_version != VERSION:
                    # Compare versions
                    if latest_version > VERSION:
                        # Find the correct asset for this OS
                        asset_name = get_asset_name_for_os()
                        download_url = None
                        
                        for asset in assets:
                            if asset.get("name") == asset_name:
                                download_url = asset.get("browser_download_url")
                                break
                        
                        show_update_dialog(latest_version, release_url, download_url, asset_name)
                elif show_no_update_message:
                    messagebox.showinfo(
                        "Up to Date",
                        f"You're running the latest version (v{VERSION})."
                    )
        except Exception:
            # Silently fail - don't bother user if update check fails
            if show_no_update_message:
                messagebox.showwarning(
                    "Update Check Failed",
                    "Could not check for updates. Please check your internet connection."
                )
    
    # Run in background thread to not block UI
    thread = threading.Thread(target=_check, daemon=True)
    thread.start()


def show_update_dialog(new_version: str, release_url: str, download_url: str = None, asset_name: str = None) -> None:
    """Show a dialog informing user about the new version."""
    import webbrowser
    
    if download_url:
        # Offer automatic download
        result = messagebox.askyesnocancel(
            "Update Available",
            f"A new version is available!\n\n"
            f"Current version: v{VERSION}\n"
            f"New version: v{new_version}\n\n"
            f"Would you like to download it automatically?\n\n"
            f"Yes = Auto-download\n"
            f"No = Open download page\n"
            f"Cancel = Skip update"
        )
        
        if result is True:
            # Auto-download
            download_update(download_url, asset_name)
        elif result is False:
            # Open browser
            webbrowser.open(release_url)
    else:
        # No direct download available, open browser
        result = messagebox.askyesno(
            "Update Available",
            f"A new version is available!\n\n"
            f"Current version: v{VERSION}\n"
            f"New version: v{new_version}\n\n"
            f"Would you like to open the download page?"
        )
        
        if result:
            webbrowser.open(release_url)


# Unicode subscript digits for formatting
SUBSCRIPT_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def to_subscript(n: int) -> str:
    """Convert a number to Unicode subscript."""
    return str(n).translate(SUBSCRIPT_DIGITS)


class MatrixInverterApp:
    """Main application class for the Matrix Inverter."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Matrix Inverter")
        self.root.geometry("1000x800")
        self.root.minsize(850, 650)
        
        # Apply theme
        self.style = apply_theme(root)
        
        # Matrix size
        self.matrix_size = tk.IntVar(value=3)
        self.show_latex = tk.BooleanVar(value=False)
        self.input_entries: List[List[ttk.Entry]] = []
        self.result_labels: List[List[ttk.Label]] = []
        self.steps: List[str] = []
        
        # Store last calculated matrices for LaTeX display
        self.last_input_matrix: np.ndarray = None
        self.last_inverse_matrix: np.ndarray = None
        
        self.create_widgets()
        self.create_matrix_grid()
    
    def create_widgets(self):
        """Create the main UI widgets."""
        # Main container
        container = ttk.Frame(self.root, padding=SPACING["lg"])
        container.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(container)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, SPACING["lg"]))
        
        title_label = ttk.Label(
            header_frame,
            text="🔢 Matrix Inverter",
            style="Heading.TLabel"
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Calculate inverse matrices with step-by-step solutions",
            style="Secondary.TLabel"
        )
        subtitle_label.pack(side=tk.LEFT, padx=(SPACING["md"], 0))
        
        # Version and update check
        version_frame = ttk.Frame(header_frame)
        version_frame.pack(side=tk.RIGHT)
        
        version_label = ttk.Label(
            version_frame,
            text=f"v{VERSION}",
            style="Secondary.TLabel"
        )
        version_label.pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
        
        update_btn = ttk.Button(
            version_frame,
            text="🔄 Check Updates",
            command=lambda: check_for_updates(show_no_update_message=True)
        )
        update_btn.pack(side=tk.LEFT)

        # Size selection frame
        size_frame = ttk.LabelFrame(
            container,
            text="⚙️ Settings",
            padding=SPACING["md"]
        )
        size_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, SPACING["md"]))
        
        ttk.Label(
            size_frame,
            text="Dimensions (N × N):",
            style="Subheading.TLabel"
        ).pack(side=tk.LEFT, padx=(0, SPACING["md"]))
        
        size_spinbox = ttk.Spinbox(
            size_frame,
            from_=2,
            to=10,
            textvariable=self.matrix_size,
            width=5,
            font=FONTS["body"],
            command=self.create_matrix_grid
        )
        size_spinbox.pack(side=tk.LEFT)
        size_spinbox.bind('<Return>', lambda e: self.create_matrix_grid())
        
        # LaTeX toggle checkbox
        latex_check = ttk.Checkbutton(
            size_frame,
            text="📐 LaTeX Format",
            variable=self.show_latex,
            command=self.toggle_latex_view
        )
        latex_check.pack(side=tk.LEFT, padx=(SPACING["lg"], 0))
        
        # Matrix frames container
        self.matrices_frame = ttk.Frame(container)
        self.matrices_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, SPACING["md"]))
        self.matrices_frame.columnconfigure(0, weight=1)
        self.matrices_frame.columnconfigure(1, weight=0)
        self.matrices_frame.columnconfigure(2, weight=1)
        container.rowconfigure(2, weight=1)
        
        # Input matrix frame
        self.input_frame = ttk.LabelFrame(
            self.matrices_frame,
            text="📥 Input Matrix",
            padding=SPACING["md"]
        )
        self.input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, SPACING["sm"]))
        
        # Arrow between matrices
        arrow_frame = ttk.Frame(self.matrices_frame)
        arrow_frame.grid(row=0, column=1, sticky="ns", padx=SPACING["sm"])
        
        arrow_label = ttk.Label(
            arrow_frame,
            text="→",
            font=("Segoe UI", 24),
            foreground=COLORS["primary"]
        )
        arrow_label.pack(expand=True)
        
        # Result matrix frame
        self.result_frame = ttk.LabelFrame(
            self.matrices_frame,
            text="📤 Inverse Matrix",
            padding=SPACING["md"]
        )
        self.result_frame.grid(row=0, column=2, sticky="nsew", padx=(SPACING["sm"], 0))
        
        # Determinant display under result frame
        self.det_frame = ttk.Frame(self.matrices_frame)
        self.det_frame.grid(row=1, column=2, sticky="ew", padx=(SPACING["sm"], 0), pady=(SPACING["sm"], 0))
        
        self.det_label = ttk.Label(
            self.det_frame,
            text="Determinant: —",
            style="Subheading.TLabel"
        )
        self.det_label.pack(anchor="center")
        
        # LaTeX display frame (hidden by default)
        self.latex_frame = ttk.LabelFrame(
            container,
            text="📐 LaTeX Matrix View",
            padding=SPACING["md"]
        )
        
        # LaTeX display canvas with scrollbars
        latex_container = ttk.Frame(self.latex_frame)
        latex_container.pack(fill=tk.BOTH, expand=True)
        
        self.latex_canvas = tk.Canvas(
            latex_container,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            height=150
        )
        self.latex_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        latex_scrollbar = ttk.Scrollbar(
            latex_container,
            orient=tk.HORIZONTAL,
            command=self.latex_canvas.xview
        )
        latex_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.latex_canvas.configure(xscrollcommand=latex_scrollbar.set)
        
        # Buttons frame
        button_frame = ttk.Frame(container)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, SPACING["md"]))
        
        # Center the buttons
        button_container = ttk.Frame(button_frame)
        button_container.pack(expand=True)
        
        ttk.Button(
            button_container,
            text="✨ Calculate Inverse",
            command=self.calculate_inverse,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=SPACING["sm"])
        
        ttk.Button(
            button_container,
            text="🔄 Clear All",
            command=self.clear_matrices,
            style="Danger.TButton"
        ).pack(side=tk.LEFT, padx=SPACING["sm"])
        
        # Steps frame
        steps_frame = ttk.LabelFrame(
            container,
            text="📝 Elementary Row Operations",
            padding=SPACING["md"]
        )
        steps_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        container.rowconfigure(4, weight=1)
        
        # Create steps table container with scrollbar
        self.steps_container = ttk.Frame(steps_frame)
        self.steps_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.steps_canvas = tk.Canvas(
            self.steps_container,
            bg=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"]
        )
        self.steps_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.steps_container,
            orient=tk.VERTICAL,
            command=self.steps_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame inside canvas for table
        self.steps_table_frame = ttk.Frame(self.steps_canvas, style="Card.TFrame")
        self.steps_canvas_window = self.steps_canvas.create_window(
            (0, 0),
            window=self.steps_table_frame,
            anchor="nw"
        )
        
        # Bind resize events
        self.steps_table_frame.bind("<Configure>", self._on_frame_configure)
        self.steps_canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Initialize empty table
        self._create_steps_table_header()
    
    def _on_frame_configure(self, event):
        """Update scroll region when frame size changes."""
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Update frame width when canvas size changes."""
        self.steps_canvas.itemconfig(self.steps_canvas_window, width=event.width)
    
    def _create_steps_table_header(self):
        """Create the table header for steps."""
        # Clear existing widgets
        for widget in self.steps_table_frame.winfo_children():
            widget.destroy()
        
        # Configure columns
        self.steps_table_frame.columnconfigure(0, weight=1, minsize=100)
        self.steps_table_frame.columnconfigure(1, weight=2, minsize=200)
        
        # Header row
        header_type = tk.Label(
            self.steps_table_frame,
            text="Type",
            font=FONTS["subheading"],
            bg=COLORS["primary"],
            fg="white",
            padx=20,
            pady=10,
            anchor="center"
        )
        header_type.grid(row=0, column=0, sticky="nsew")
        
        header_operation = tk.Label(
            self.steps_table_frame,
            text="Operation",
            font=FONTS["subheading"],
            bg=COLORS["primary"],
            fg="white",
            padx=20,
            pady=10,
            anchor="center"
        )
        header_operation.grid(row=0, column=1, sticky="nsew")
    
    def _on_entry_focus_in(self, event):
        """Clear the entry if it contains only '0' when focused."""
        entry = event.widget
        if entry.get() == "0":
            entry.delete(0, tk.END)
    
    def _on_entry_focus_out(self, event):
        """Restore '0' if entry is empty when focus is lost."""
        entry = event.widget
        if entry.get().strip() == "":
            entry.insert(0, "0")
    
    def create_matrix_grid(self):
        """Create the input and output matrix grids based on selected size."""
        # Clear existing widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        self.input_entries = []
        self.result_labels = []
        
        size = self.matrix_size.get()
        
        # Create input grid
        input_grid = ttk.Frame(self.input_frame)
        input_grid.pack(expand=True, pady=SPACING["sm"])
        
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = create_styled_entry(input_grid, width=8)
                entry.grid(row=i, column=j, padx=SPACING["xs"], pady=SPACING["xs"])
                entry.insert(0, "0")
                # Bind focus events for QoL
                entry.bind("<FocusIn>", self._on_entry_focus_in)
                entry.bind("<FocusOut>", self._on_entry_focus_out)
                row_entries.append(entry)
            self.input_entries.append(row_entries)
        
        # Create result grid
        result_grid = ttk.Frame(self.result_frame)
        result_grid.pack(expand=True, pady=SPACING["sm"])
        
        for i in range(size):
            row_labels = []
            for j in range(size):
                label = create_styled_label(result_grid, text="—", width=10)
                label.grid(row=i, column=j, padx=SPACING["xs"], pady=SPACING["xs"])
                row_labels.append(label)
            self.result_labels.append(row_labels)
        
        # Reset stored matrices
        self.last_input_matrix = None
        self.last_inverse_matrix = None
        
        # Update LaTeX view if visible
        if self.show_latex.get():
            self.update_latex_display()
    
    def toggle_latex_view(self):
        """Toggle the LaTeX matrix view."""
        if self.show_latex.get():
            self.latex_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, SPACING["md"]), in_=self.matrices_frame.master)
            # Move matrices frame and subsequent elements down
            self.matrices_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(0, SPACING["md"]))
            self.latex_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(SPACING["md"], 0), in_=self.matrices_frame.master)
            self.update_latex_display()
        else:
            self.latex_frame.grid_forget()
    
    def _draw_latex_matrix(self, matrix: np.ndarray, x: int, y: int, title: str) -> int:
        """
        Draw a matrix in LaTeX-style format with brackets.
        
        Args:
            matrix: The matrix to draw
            x: Starting x position
            y: Starting y position
            title: Title above the matrix
            
        Returns:
            The x position after the matrix (for chaining)
        """
        n = matrix.shape[0]
        
        # Calculate cell dimensions based on content
        cell_size = 60  # Equal width and height for each cell
        padding = 15    # Padding inside cells
        bracket_width = 12
        bracket_thickness = 2
        
        # Calculate total matrix dimensions
        matrix_width = n * cell_size
        matrix_height = n * cell_size
        
        # Draw title centered above matrix
        title_x = x + bracket_width + matrix_width // 2
        self.latex_canvas.create_text(
            title_x, y,
            text=title,
            font=FONTS["subheading"],
            fill=COLORS["primary"]
        )
        y += 30
        
        # Draw left bracket (square bracket style)
        bracket_left_x = x
        self.latex_canvas.create_line(
            bracket_left_x + bracket_width, y,
            bracket_left_x, y,
            bracket_left_x, y + matrix_height,
            bracket_left_x + bracket_width, y + matrix_height,
            width=bracket_thickness,
            fill=COLORS["text"]
        )
        
        # Draw cell grid lines (light) and values
        content_start_x = x + bracket_width + padding
        content_start_y = y
        
        for i in range(n):
            for j in range(n):
                # Calculate cell center
                cell_center_x = content_start_x + j * cell_size + cell_size // 2
                cell_center_y = content_start_y + i * cell_size + cell_size // 2
                
                # Get formatted value
                value = matrix[i, j]
                display_value = self.format_number(value)
                
                # Draw value centered in cell
                self.latex_canvas.create_text(
                    cell_center_x, cell_center_y,
                    text=display_value,
                    font=FONTS["matrix"],
                    fill=COLORS["text"],
                    anchor="center"
                )
        
        # Draw right bracket
        bracket_right_x = x + bracket_width + matrix_width + padding * 2
        self.latex_canvas.create_line(
            bracket_right_x, y,
            bracket_right_x + bracket_width, y,
            bracket_right_x + bracket_width, y + matrix_height,
            bracket_right_x, y + matrix_height,
            width=bracket_thickness,
            fill=COLORS["text"]
        )
        
        return bracket_right_x + bracket_width + 20

    def update_latex_display(self):
        """Update the LaTeX-style matrix display."""
        self.latex_canvas.delete("all")
        
        if self.last_input_matrix is None:
            # Show placeholder
            self.latex_canvas.create_text(
                10, 75,
                text="Calculate inverse to see LaTeX format",
                font=FONTS["body"],
                fill=COLORS["text_secondary"],
                anchor="w"
            )
            return
        
        # Calculate required canvas height based on matrix size
        n = self.last_input_matrix.shape[0]
        cell_size = 60
        required_height = n * cell_size + 50  # Extra for title
        self.latex_canvas.configure(height=max(150, required_height))
        
        # Draw input matrix
        x_offset = 30
        y_offset = 15
        x_offset = self._draw_latex_matrix(
            self.last_input_matrix, x_offset, y_offset, "Input Matrix (A)"
        )
        
        # Draw arrow
        arrow_y = y_offset + 30 + (n * cell_size) // 2
        x_offset += 20
        self.latex_canvas.create_text(
            x_offset, arrow_y,
            text="→",
            font=("Segoe UI", 24, "bold"),
            fill=COLORS["primary"]
        )
        x_offset += 50
        
        # Draw inverse matrix
        if self.last_inverse_matrix is not None:
            x_offset = self._draw_latex_matrix(
                self.last_inverse_matrix, x_offset, y_offset, "Inverse Matrix (A⁻¹)"
            )
        
        # Update scroll region
        self.latex_canvas.configure(scrollregion=self.latex_canvas.bbox("all"))
    
    def get_matrix(self) -> np.ndarray:
        """Get the matrix values from input entries."""
        size = self.matrix_size.get()
        matrix = []
        
        for i in range(size):
            row = []
            for j in range(size):
                try:
                    value = float(self.input_entries[i][j].get())
                    row.append(value)
                except ValueError:
                    raise ValueError(f"Invalid value at position ({i+1}, {j+1})")
            matrix.append(row)
        
        return np.array(matrix, dtype=float)
    
    def format_number(self, value: float) -> str:
        """Format a number for display."""
        if abs(value) < 1e-10:
            return "0"
        elif abs(value - round(value)) < 1e-10:
            return str(int(round(value)))
        else:
            return f"{value:.4f}"
    
    def gauss_jordan_inverse(self, matrix: np.ndarray) -> Tuple[np.ndarray, List[Tuple[int, str]]]:
        """
        Calculate matrix inverse using Gauss-Jordan elimination.
        
        Returns the inverse matrix and a list of steps performed.
        
        Step notation (using subscripts):
        - Type 1: Eᵢ,ⱼ - Swap rows i and j
        - Type 2: Eᵢ(k) - Multiply row i by scalar k
        - Type 3: Eᵢ,ⱼ(k) - Add k times row j to row i
        """
        n = matrix.shape[0]
        steps: List[Tuple[int, str]] = []
        
        # Create augmented matrix [A | I]
        augmented = np.hstack([matrix.copy(), np.eye(n)])
        
        # Forward elimination (to get upper triangular form)
        for col in range(n):
            # Find pivot
            max_row = col
            for row in range(col + 1, n):
                if abs(augmented[row, col]) > abs(augmented[max_row, col]):
                    max_row = row
            
            # Swap rows if necessary
            if max_row != col:
                augmented[[col, max_row]] = augmented[[max_row, col]]
                steps.append((1, f"E{to_subscript(col+1)},{to_subscript(max_row+1)}"))
            
            # Check for zero pivot
            if abs(augmented[col, col]) < 1e-10:
                raise np.linalg.LinAlgError("Matrix is singular")
            
            # Scale pivot row to make pivot = 1
            pivot = augmented[col, col]
            if abs(pivot - 1.0) > 1e-10:
                scalar = 1.0 / pivot
                augmented[col] = augmented[col] * scalar
                steps.append((2, f"E{to_subscript(col+1)}({self.format_number(scalar)})"))
            
            # Eliminate all other entries in this column
            for row in range(n):
                if row != col and abs(augmented[row, col]) > 1e-10:
                    factor = -augmented[row, col]
                    augmented[row] = augmented[row] + factor * augmented[col]
                    steps.append((3, f"E{to_subscript(row+1)},{to_subscript(col+1)}({self.format_number(factor)})"))
        
        # Extract inverse from augmented matrix
        inverse = augmented[:, n:]
        
        return inverse, steps
    
    def display_steps(self, steps: List[Tuple[int, str]]):
        """Display the steps in a styled table format."""
        # Reset table with header
        self._create_steps_table_header()
        
        # Add each step as a row
        for i, (step_type, operation) in enumerate(steps):
            row_num = i + 1
            
            # Alternate row colors
            if i % 2 == 0:
                bg_color = COLORS["surface"]
            else:
                bg_color = COLORS["surface_dark"]
            
            # Type cell
            type_label = tk.Label(
                self.steps_table_frame,
                text=str(step_type),
                font=FONTS["matrix"],
                bg=bg_color,
                fg=COLORS["text"],
                padx=20,
                pady=8,
                anchor="center"
            )
            type_label.grid(row=row_num, column=0, sticky="nsew")
            
            # Operation cell
            operation_label = tk.Label(
                self.steps_table_frame,
                text=operation,
                font=FONTS["matrix"],
                bg=bg_color,
                fg=COLORS["primary"],
                padx=20,
                pady=8,
                anchor="center"
            )
            operation_label.grid(row=row_num, column=1, sticky="nsew")
        
        # Update scroll region
        self.steps_table_frame.update_idletasks()
        self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))
    
    def calculate_inverse(self):
        """Calculate and display the inverse matrix."""
        try:
            matrix = self.get_matrix()
            self.last_input_matrix = matrix.copy()
            
            # Calculate determinant
            det = np.linalg.det(matrix)
            self.det_label.config(text=f"Determinant: {det:.6f}")
            
            # Check if matrix is singular
            if np.abs(det) < 1e-10:
                messagebox.showerror(
                    "Error",
                    "Matrix is singular (determinant ≈ 0).\nIt cannot be inverted."
                )
                self.clear_result()
                return
            
            # Calculate inverse using Gauss-Jordan with steps
            inverse, steps = self.gauss_jordan_inverse(matrix)
            self.last_inverse_matrix = inverse.copy()
            
            # Display steps
            self.display_steps(steps)
            
            # Display result
            size = self.matrix_size.get()
            for i in range(size):
                for j in range(size):
                    value = inverse[i, j]
                    display_value = self.format_number(value)
                    self.result_labels[i][j].config(text=display_value)
            
            # Update LaTeX display if visible
            if self.show_latex.get():
                self.update_latex_display()
            
            messagebox.showinfo("Success", "Matrix inverse calculated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except np.linalg.LinAlgError as e:
            messagebox.showerror("Calculation Error", f"Cannot invert matrix: {e}")
    
    def clear_result(self):
        """Clear the result matrix display."""
        for row in self.result_labels:
            for label in row:
                label.config(text="—")
        
        # Reset stored inverse
        self.last_inverse_matrix = None
        
        # Reset steps table
        self._create_steps_table_header()
        
        # Update LaTeX display
        if self.show_latex.get():
            self.update_latex_display()
    
    def clear_matrices(self):
        """Clear both input and result matrices."""
        for row in self.input_entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        
        self.last_input_matrix = None
        self.clear_result()
        self.det_label.config(text="Determinant: —")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    
    # Set app icon (optional - will use default if not available)
    try:
        root.iconbitmap("icon.ico")
    except tk.TclError:
        pass
    
    app = MatrixInverterApp(root)
    check_for_updates()
    root.mainloop()


if __name__ == "__main__":
    main()
