import matplotlib.pyplot as plt
import seaborn as sns

def apply_visual_style():
    """
    Apply a modern, trending visual style for charts.
    Works great for both dark and light backgrounds.
    """

    # 🎨 Trending color palette (neon + gradient tones)
    sns.set_palette([
        "#00B4D8",  # neon aqua
        "#FF595E",  # coral red
        "#FFCA3A",  # yellow accent
        "#8AC926",  # lime green
        "#6A4C93",  # violet
        "#1982C4",  # bright blue
        "#FF6F61",  # soft red
    ])

    # 🖼️ General matplotlib style
    plt.style.use('seaborn-v0_8-darkgrid')

    # 🔧 Fine tuning for professional look
    plt.rcParams.update({
        'axes.facecolor': '#111217',     # dark background
        'figure.facecolor': '#0D0F12',
        'axes.edgecolor': '#CCCCCC',
        'axes.labelcolor': '#FFFFFF',
        'xtick.color': '#CCCCCC',
        'ytick.color': '#CCCCCC',
        'grid.color': '#333333',
        'font.size': 11,
        'axes.titleweight': 'bold',
        'axes.titlepad': 15,
        'legend.frameon': False,
        'figure.autolayout': True
    })

    print("✨ Modern visual style applied (Dark Mode + Neon Palette)")

