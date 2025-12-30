"""
Theme and styling configuration for the Matrix Inverter application.
"""

import tkinter as tk
from tkinter import ttk


# Color palette
COLORS = {
    "primary": "#2563eb",        # Blue
    "primary_dark": "#1d4ed8",   # Darker blue
    "secondary": "#64748b",      # Slate gray
    "success": "#16a34a",        # Green
    "danger": "#dc2626",         # Red
    "warning": "#d97706",        # Orange
    "background": "#f8fafc",     # Light gray
    "surface": "#ffffff",        # White
    "surface_dark": "#e2e8f0",   # Darker surface
    "text": "#1e293b",           # Dark text
    "text_secondary": "#64748b", # Secondary text
    "border": "#cbd5e1",         # Border color
    "accent": "#8b5cf6",         # Purple accent
}

# Font configurations
FONTS = {
    "heading": ("Segoe UI", 14, "bold"),
    "subheading": ("Segoe UI", 11, "bold"),
    "body": ("Segoe UI", 10),
    "small": ("Segoe UI", 9),
    "monospace": ("Consolas", 10),
    "monospace_large": ("Consolas", 11),
    "matrix": ("Consolas", 11, "bold"),
}

# Padding and spacing
SPACING = {
    "xs": 2,
    "sm": 5,
    "md": 10,
    "lg": 15,
    "xl": 20,
}


def apply_theme(root: tk.Tk) -> ttk.Style:
    """
    Apply custom theme styling to the application.
    
    Args:
        root: The root Tk window
        
    Returns:
        The configured ttk.Style object
    """
    style = ttk.Style(root)
    
    # Try to use clam as base theme (more customizable)
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    
    # Configure root window
    root.configure(bg=COLORS["background"])
    
    # Frame styles
    style.configure(
        "TFrame",
        background=COLORS["background"]
    )
    
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
        relief="flat"
    )
    
    # Label styles
    style.configure(
        "TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=FONTS["body"]
    )
    
    style.configure(
        "Heading.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=FONTS["heading"]
    )
    
    style.configure(
        "Subheading.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=FONTS["subheading"]
    )
    
    style.configure(
        "Secondary.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text_secondary"],
        font=FONTS["small"]
    )
    
    style.configure(
        "Matrix.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=FONTS["matrix"],
        padding=8
    )
    
    style.configure(
        "Result.TLabel",
        background=COLORS["surface_dark"],
        foreground=COLORS["primary"],
        font=FONTS["matrix"],
        padding=8
    )
    
    # LabelFrame styles
    style.configure(
        "TLabelframe",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=FONTS["subheading"]
    )
    
    style.configure(
        "TLabelframe.Label",
        background=COLORS["background"],
        foreground=COLORS["primary"],
        font=FONTS["subheading"]
    )
    
    style.configure(
        "Card.TLabelframe",
        background=COLORS["surface"],
        borderwidth=1,
        relief="solid"
    )
    
    style.configure(
        "Card.TLabelframe.Label",
        background=COLORS["surface"],
        foreground=COLORS["primary"],
        font=FONTS["subheading"]
    )
    
    # Button styles
    style.configure(
        "TButton",
        background=COLORS["secondary"],
        foreground=COLORS["text"],
        font=FONTS["body"],
        padding=(15, 8)
    )
    
    style.map(
        "TButton",
        background=[("active", COLORS["surface_dark"])]
    )
    
    style.configure(
        "Primary.TButton",
        background=COLORS["primary"],
        foreground="white",
        font=FONTS["subheading"],
        padding=(20, 10)
    )
    
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_dark"])]
    )
    
    style.configure(
        "Success.TButton",
        background=COLORS["success"],
        foreground="white",
        font=FONTS["body"],
        padding=(15, 8)
    )
    
    style.configure(
        "Danger.TButton",
        background=COLORS["danger"],
        foreground="white",
        font=FONTS["body"],
        padding=(15, 8)
    )
    
    # Entry styles
    style.configure(
        "TEntry",
        font=FONTS["matrix"],
        padding=5
    )
    
    style.configure(
        "Matrix.TEntry",
        font=FONTS["matrix"],
        padding=8
    )
    
    # Spinbox styles
    style.configure(
        "TSpinbox",
        font=FONTS["body"],
        padding=5
    )
    
    # Scrollbar styles
    style.configure(
        "TScrollbar",
        background=COLORS["surface_dark"],
        troughcolor=COLORS["background"]
    )
    
    return style


def create_styled_entry(parent: tk.Widget, width: int = 8) -> ttk.Entry:
    """
    Create a styled entry widget for matrix input.
    
    Args:
        parent: Parent widget
        width: Entry width in characters
        
    Returns:
        Configured Entry widget
    """
    entry = ttk.Entry(
        parent,
        width=width,
        justify="center",
        font=FONTS["matrix"]
    )
    return entry


def create_styled_label(
    parent: tk.Widget,
    text: str = "-",
    style_name: str = "Result.TLabel",
    width: int = 10
) -> ttk.Label:
    """
    Create a styled label widget for matrix display.
    
    Args:
        parent: Parent widget
        text: Initial text
        style_name: TTK style name
        width: Label width in characters
        
    Returns:
        Configured Label widget
    """
    label = ttk.Label(
        parent,
        text=text,
        width=width,
        anchor="center",
        style=style_name,
        relief="flat"
    )
    return label


def get_text_widget_config() -> dict:
    """
    Get configuration for text widgets (like the steps display).
    
    Returns:
        Dictionary of configuration options
    """
    return {
        "font": FONTS["monospace"],
        "bg": COLORS["surface"],
        "fg": COLORS["text"],
        "insertbackground": COLORS["primary"],
        "selectbackground": COLORS["primary"],
        "selectforeground": "white",
        "relief": "flat",
        "borderwidth": 1,
        "highlightthickness": 1,
        "highlightbackground": COLORS["border"],
        "highlightcolor": COLORS["primary"],
        "padx": 10,
        "pady": 10,
    }
