import sys

THEME_TOKENS = {
    "colors": {
        "primary": "hsl(var(--primary))",
        "secondary": "hsl(var(--secondary))",
        "background": "bg-background",
        "card": "bg-card",
        "border": "border-border",
        "accent": "hsl(var(--accent))"
    },
    "gradients": {
        "hero": "gradient-hero",
        "card": "gradient-card",
        "accent": "gradient-accent"
    },
    "effects": {
        "glass": "backdrop-blur-md bg-white/10",
        "shadow_soft": "shadow-soft",
        "shadow_medium": "shadow-medium"
    }
}

def get_ux_template(name):
    return f"""
    <!-- UX Standard {name} -->
    <div className="{{THEME_TOKENS['effects']['glass']}} {{THEME_TOKENS['colors']['border']}} {{THEME_TOKENS['effects']['shadow_soft']}} p-6 rounded-lg">
        <h2 className="text-primary font-bold tracking-tight">{name}</h2>
    </div>
    """

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(get_ux_template(sys.argv[1]))
    else:
        print("Usage: python ux_theme.py <component_name>")
