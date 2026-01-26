import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


# Colors
PRIMAL_COLOR = '#e8f4e8'
DUAL_COLOR = '#e8e8f4'
SET_COLOR = '#fafafa'
SUBSET_COLOR = '#f0f0ff'
BORDER_COLOR = '#333333'

# Positions
POSITIONS = {
    'X': (1.7, 5.0),
    'Y': (1.7, 2.0),
    'Xpp': (6.5, 5.0),
    'Ypp': (6.5, 2.0),
}


def draw_background_regions(ax):
    """Draw the primal and bidual space background boxes."""
    primal_bg = FancyBboxPatch(
        (0.2, 1.0), 3.0, 5.0,
        boxstyle="round,pad=0.1,rounding_size=0.3",
        facecolor=PRIMAL_COLOR, edgecolor='#88aa88',
        linewidth=2, alpha=0.5
    )
    ax.add_patch(primal_bg)
    ax.text(1.7, 6.2, 'Primal Spaces', ha='center', va='bottom',
            fontsize=14, fontstyle='italic', color='#446644', fontweight='bold')

    dual_bg = FancyBboxPatch(
        (3.6, 1.0), 6.0, 5.0,
        boxstyle="round,pad=0.1,rounding_size=0.3",
        facecolor=DUAL_COLOR, edgecolor='#8888aa',
        linewidth=2, alpha=0.5
    )
    ax.add_patch(dual_bg)
    ax.text(6.5, 6.2, 'Bidual Spaces', ha='center', va='bottom',
            fontsize=14, fontstyle='italic', color='#444466', fontweight='bold')


def draw_set(ax, center, label, width=1.8, height=1.0):
    """Draw a simple ellipse set with label."""
    ellipse = mpatches.Ellipse(
        center, width, height,
        facecolor=SET_COLOR, edgecolor=BORDER_COLOR, linewidth=2
    )
    ax.add_patch(ellipse)
    ax.text(center[0], center[1], label, ha='center', va='center',
            fontsize=22, fontweight='bold')


def draw_nested_sets(ax, center, outer_label, inner_label,
                     outer_size=(3.2, 1.6), inner_size=(2.0, 1.0)):
    """Draw nested ellipses for X'' containing J_X(X)."""
    # Outer ellipse
    outer = mpatches.Ellipse(
        center, outer_size[0], outer_size[1],
        facecolor=SET_COLOR, edgecolor=BORDER_COLOR, linewidth=2
    )
    ax.add_patch(outer)

    # Inner ellipse (shifted slightly left)
    inner_center = (center[0] - 0.3, center[1])
    inner = mpatches.Ellipse(
        inner_center, inner_size[0], inner_size[1],
        facecolor=SUBSET_COLOR, edgecolor='#666688',
        linewidth=1.5, linestyle='--'
    )
    ax.add_patch(inner)

    # Labels - inner label centered, outer label inside but to the right
    ax.text(inner_center[0], inner_center[1], inner_label,
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(center[0] + 0.95, center[1], outer_label,
            ha='center', va='center', fontsize=20, fontweight='bold', color='#333333')

    return inner_center


def draw_arrow(ax, start, end, label, color='black',
               label_offset=(0, 0.3), fontsize=14, shrinkA=30, shrinkB=30):
    """Draw an arrow with a label."""
    arrow = FancyArrowPatch(
        start, end,
        arrowstyle='->',
        connectionstyle='arc3,rad=0',
        mutation_scale=22,
        color=color,
        linewidth=3,
        shrinkA=shrinkA, shrinkB=shrinkB
    )
    ax.add_patch(arrow)

    mid_x = (start[0] + end[0]) / 2 + label_offset[0]
    mid_y = (start[1] + end[1]) / 2 + label_offset[1]
    ax.text(mid_x, mid_y, label, ha='center', va='center',
            fontsize=fontsize, color=color, fontweight='bold')


def draw_isomorphism_arrows(ax, jx_center, jy_center):
    """Draw the green isomorphism arrows connecting X to J_X(X) and Y to J_Y(Y)."""
    # X ≅ J_X(X) - arrow at top of ellipses
    x_top = POSITIONS['X'][1] + 0.5
    jx_inner_top = POSITIONS['Xpp'][1] + 0.5
    ax.annotate(
        '', xy=(jx_center[0] - 0.3, jx_inner_top),
        xytext=(POSITIONS['X'][0], x_top),
        arrowprops=dict(
            arrowstyle='<->', color='#228822', lw=3,
            connectionstyle='arc3,rad=-0.2', shrinkA=0, shrinkB=0
        )
    )

    # Y ≅ J_Y(Y) - arrow at bottom of ellipses
    y_bottom = POSITIONS['Y'][1] - 0.5
    jy_inner_bottom = POSITIONS['Ypp'][1] - 0.5
    ax.annotate(
        '', xy=(jy_center[0] - 0.3, jy_inner_bottom),
        xytext=(POSITIONS['Y'][0], y_bottom),
        arrowprops=dict(
            arrowstyle='<->', color='#228822', lw=3,
            connectionstyle='arc3,rad=0.2', shrinkA=0, shrinkB=0
        )
    )


def main():
    """Generate the bidual space diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(0.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Background regions
    draw_background_regions(ax)

    # Primal spaces
    draw_set(ax, POSITIONS['X'], r'$X$')
    draw_set(ax, POSITIONS['Y'], r'$Y$')

    # Bidual spaces (nested)
    jx_center = draw_nested_sets(ax, POSITIONS['Xpp'], r"$X''$", r'$J_X(X)$')
    jy_center = draw_nested_sets(ax, POSITIONS['Ypp'], r"$Y''$", r'$J_Y(Y)$')

    # Operator arrows (T and T'')
    draw_arrow(ax, POSITIONS['X'], POSITIONS['Y'], r'$T$',
               color='#cc4444', label_offset=(-0.35, 0), fontsize=22)
    draw_arrow(ax, jx_center, jy_center, r"$T''$",
               color='#cc4444', label_offset=(-0.5, 0), fontsize=22, shrinkA=35, shrinkB=35)

    # Embedding arrows (J_X and J_Y)
    draw_arrow(ax, POSITIONS['X'], (jx_center[0] - 0.8, jx_center[1]), r'$J_X$',
               color='#4444cc', label_offset=(0, 0.35), fontsize=22, shrinkB=20)
    draw_arrow(ax, POSITIONS['Y'], (jy_center[0] - 0.8, jy_center[1]), r'$J_Y$',
               color='#4444cc', label_offset=(0, -0.4), fontsize=22, shrinkB=20)

    # Isomorphism arrows
    draw_isomorphism_arrows(ax, jx_center, jy_center)

    # Save
    plt.tight_layout()
    plt.savefig('figures/dual_of_dual.pdf', format='pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')


if __name__ == '__main__':
    main()