# src/visual_style.py
import matplotlib.pyplot as plt
import seaborn as sns
import random

PALETTES = {
    "vibrant_tech": ["#00B8A9", "#F6416C", "#FFDE7D", "#6A2C70", "#355C7D"],
    "pastel_soft": ["#A1C4FD", "#C2E9FB", "#FDCB82", "#F8A1D1", "#A0E7E5"],
    "dark_neon": ["#00F5D4", "#9B5DE5", "#F15BB5", "#FEE440", "#00BBF9"],
    "earth_tone": ["#6B4226", "#D9BF77", "#AC6C82", "#3E5C76", "#9BC1BC"],
    "modern_blue": ["#2EC4B6", "#E71D36", "#FF9F1C", "#011627", "#CBF3F0"]
}

def randomize_palette():
    """Randomly select and apply a modern color palette."""
    name, palette = random.choice(list(PALETTES.items()))
    sns.set_palette(palette)
    plt.rcParams.update({
        'figure.facecolor': '#f8f9fa',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#CCCCCC',
        'axes.grid': True,
        'grid.color': '#EEEEEE',
        'grid.linestyle': '--',
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.labelcolor': '#333333',
        'xtick.color': '#555555',
        'ytick.color': '#555555',
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial'],
        'figure.autolayout': True
    })
    print(f"✅ Applied random style: '{name}' with colors {palette}")

def apply_visual_style(style_name="vibrant_tech"):
    """Apply a specific named color style."""
    palette = PALETTES.get(style_name, PALETTES["vibrant_tech"])
    sns.set_palette(palette)
    plt.rcParams.update({
        'figure.facecolor': '#f8f9fa',
        'axes.facecolor': 'white',
        'axes.edgecolor': '#CCCCCC',
        'axes.grid': True,
        'grid.color': '#EEEEEE',
        'grid.linestyle': '--',
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
        'axes.labelcolor': '#333333',
        'xtick.color': '#555555',
        'ytick.color': '#555555',
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial'],
        'figure.autolayout': True
    })
    print(f"✅ Applied '{style_name}' style with colors {palette}")
    return
