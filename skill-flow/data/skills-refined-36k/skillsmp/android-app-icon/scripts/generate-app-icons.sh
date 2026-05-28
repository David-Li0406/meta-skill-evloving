#!/bin/sh
# Generate Android app icons from Iconify
# Usage: generate-app-icons.sh <icon-id>
#
# Examples:
#   generate-app-icons.sh arcticons:health-sync
#   generate-app-icons.sh mdi:heart-pulse
#
# Environment overrides:
#   ICON_BACKGROUND - Background color (default: auto-detect from colors.xml)
#   ICON_SCALE      - Scale factor (default: 1.15)
#   ICON_COLOR      - Foreground color (default: white)

set -e

ICON_ID="${1:?Usage: generate-app-icons.sh <icon-id> (e.g., arcticons:health-sync)}"

# Parse icon ID
ICON_COLLECTION=$(printf "%s" "$ICON_ID" | cut -d: -f1)
ICON_NAME=$(printf "%s" "$ICON_ID" | cut -d: -f2)

# Auto-detect or use overrides
ICON_COLOR="${ICON_COLOR:-white}"
ICON_SCALE="${ICON_SCALE:-1.15}"

# Auto-detect background color from project
if [ -z "$ICON_BACKGROUND" ]; then
    ICON_BACKGROUND=""

    # Step 1: Check themes.xml for colorPrimary (most common location)
    if [ -f "app/src/main/res/values/themes.xml" ]; then
        COLOR_REF=$(grep -E 'name="colorPrimary"' app/src/main/res/values/themes.xml 2>/dev/null | \
                    sed 's/.*>\([^<]*\)<.*/\1/' | head -1)

        if [ -n "$COLOR_REF" ]; then
            # Check if it's a reference (@color/name) or direct hex value
            case "$COLOR_REF" in
                @color/*)
                    # Extract color name from reference
                    COLOR_NAME=$(printf "%s" "$COLOR_REF" | sed 's/@color\///')

                    # Look up in colors.xml
                    if [ -f "app/src/main/res/values/colors.xml" ]; then
                        ICON_BACKGROUND=$(grep -E "name=\"${COLOR_NAME}\"" app/src/main/res/values/colors.xml 2>/dev/null | \
                                          sed 's/.*>\(#[^<]*\)<.*/\1/' | head -1)
                    fi
                    ;;
                \#*)
                    # Direct hex value
                    ICON_BACKGROUND="$COLOR_REF"
                    ;;
            esac
        fi
    fi

    # Step 2: Fallback - check colors.xml directly for colorPrimary
    if [ -z "$ICON_BACKGROUND" ] && [ -f "app/src/main/res/values/colors.xml" ]; then
        ICON_BACKGROUND=$(grep -E 'name="colorPrimary"' app/src/main/res/values/colors.xml 2>/dev/null | \
                          sed 's/.*>\(#[^<]*\)<.*/\1/' | head -1)
    fi

    # Step 3: Default fallback
    ICON_BACKGROUND="${ICON_BACKGROUND:-#4CAF50}"
fi

printf "Background color: %s\n" "$ICON_BACKGROUND"

# Paths
DRAWABLE_DIR="app/src/main/res/drawable"
MIPMAP_DIR="app/src/main/res/mipmap-anydpi-v26"
PLAYSTORE_DIR="fastlane/metadata/android/en-US/images"
TMP_DIR="/tmp/android-icons-$$"

# Cleanup on exit
mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

printf "=== Android App Icon Generator ===\n"
printf "Icon: %s\n" "$ICON_ID"
printf "Background: %s\n" "$ICON_BACKGROUND"
printf "Scale: %s\n" "$ICON_SCALE"
printf "\n"

# Check dependencies
printf "Checking dependencies...\n"
for cmd in curl python3 rsvg-convert; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        printf "Error: %s not found\n" "$cmd"
        if [ "$cmd" = "rsvg-convert" ]; then
            printf "Install with:\n"
            printf "  macOS:  brew install librsvg\n"
            printf "  Ubuntu: sudo apt install librsvg2-bin\n"
        fi
        exit 1
    fi
done
printf "✓ Dependencies OK\n\n"

# Step 1: Fetch icon from Iconify
printf "Step 1: Fetching icon from Iconify API...\n"
curl -s "https://api.iconify.design/${ICON_COLLECTION}.json?icons=${ICON_NAME}" > "$TMP_DIR/icon-data.json"

# Extract SVG body and metadata
python3 << PYEOF > "$TMP_DIR/icon-meta.txt"
import json, sys

with open('$TMP_DIR/icon-data.json') as f:
    data = json.load(f)

icon = data.get('icons', {}).get('$ICON_NAME', {})
if not icon:
    print("ERROR", file=sys.stderr)
    sys.exit(1)

body = icon.get('body', '')
width = icon.get('width', data.get('width', 24))
height = icon.get('height', data.get('height', 24))

print(f"WIDTH={width}")
print(f"HEIGHT={height}")

# Write body to separate file (may contain special chars)
with open('$TMP_DIR/icon-body.txt', 'w') as f:
    f.write(body)
PYEOF

if [ ! -f "$TMP_DIR/icon-meta.txt" ] || grep -q "ERROR" "$TMP_DIR/icon-meta.txt" 2>/dev/null; then
    printf "Error: Failed to fetch icon '%s'\n" "$ICON_ID"
    printf "Check that the icon ID is correct at: https://icon-sets.iconify.design/\n"
    exit 1
fi

# Parse the metadata safely (avoid eval of untrusted data)
WIDTH=$(grep '^WIDTH=' "$TMP_DIR/icon-meta.txt" | cut -d'=' -f2)
HEIGHT=$(grep '^HEIGHT=' "$TMP_DIR/icon-meta.txt" | cut -d'=' -f2)

# Validate that WIDTH and HEIGHT are numeric
if ! [[ "$WIDTH" =~ ^[0-9]+(\.[0-9]+)?$ ]] || ! [[ "$HEIGHT" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    printf "Error: Invalid width/height values from API\n"
    exit 1
fi

printf "✓ Fetched icon (viewBox: %sx%s)\n\n" "$WIDTH" "$HEIGHT"

# Step 2: Generate VectorDrawable foreground
printf "Step 2: Generating ic_launcher_foreground.xml...\n"
mkdir -p "$DRAWABLE_DIR"

python3 << PYEOF > "$DRAWABLE_DIR/ic_launcher_foreground.xml"
import re
import sys

# Read icon body from file (avoid code injection via variable interpolation)
with open('$TMP_DIR/icon-body.txt', 'r') as f:
    icon_body = f.read()

icon_width = float($WIDTH)
icon_height = float($HEIGHT)
user_scale = float($ICON_SCALE)

# Calculate scale to fit in 66dp safe zone (adaptive icon standard)
base_scale = 66.0 / max(icon_width, icon_height)
final_scale = base_scale * user_scale

# Calculate translation to center in 108dp canvas
translate_x = (108 - icon_width * final_scale) / 2
translate_y = (108 - icon_height * final_scale) / 2

def circle_to_path(cx, cy, r):
    """Convert SVG circle to path with two arcs."""
    cx, cy, r = float(cx), float(cy), float(r)
    return f"M {cx},{cy - r} A {r},{r} 0 1,0 {cx},{cy + r} A {r},{r} 0 1,0 {cx},{cy - r}"

def ellipse_to_path(cx, cy, rx, ry):
    """Convert SVG ellipse to path with two arcs."""
    cx, cy, rx, ry = float(cx), float(cy), float(rx), float(ry)
    return f"M {cx},{cy - ry} A {rx},{ry} 0 1,0 {cx},{cy + ry} A {rx},{ry} 0 1,0 {cx},{cy - ry}"

def rect_to_path(x, y, w, h):
    """Convert SVG rect to path."""
    x, y, w, h = float(x), float(y), float(w), float(h)
    return f"M {x},{y} h {w} v {h} h -{w} Z"

def line_to_path(x1, y1, x2, y2):
    """Convert SVG line to path."""
    return f"M {x1},{y1} L {x2},{y2}"

def polygon_to_path(points):
    """Convert SVG polygon points to path."""
    # Handle both "x,y x,y" and "x y x y" formats
    points = points.strip()
    if ',' in points:
        # Format: "x1,y1 x2,y2 ..."
        pairs = points.split()
    else:
        # Format: "x1 y1 x2 y2 ..."
        coords = points.split()
        pairs = [f"{coords[i]},{coords[i+1]}" for i in range(0, len(coords), 2)]
    return f"M {pairs[0]} " + " ".join(f"L {p}" for p in pairs[1:]) + " Z"

def polyline_to_path(points):
    """Convert SVG polyline points to path (no closing Z)."""
    points = points.strip()
    if ',' in points:
        pairs = points.split()
    else:
        coords = points.split()
        pairs = [f"{coords[i]},{coords[i+1]}" for i in range(0, len(coords), 2)]
    return f"M {pairs[0]} " + " ".join(f"L {p}" for p in pairs[1:])

def extract_attr(element, attr):
    """Extract attribute value from element string."""
    match = re.search(rf'{attr}="([^"]*)"', element)
    return match.group(1) if match else None

def has_stroke(element):
    """Check if element has stroke styling."""
    return 'stroke=' in element or 'stroke-width' in element

def get_fill_from_element(element):
    """Extract fill color, handling 'none' and 'currentColor'."""
    fill = extract_attr(element, 'fill')
    if fill is None:
        return "#FFFFFF"  # Default to white
    if fill.lower() == 'none':
        return "#00000000"  # Transparent
    if fill.lower() == 'currentcolor':
        return "#FFFFFF"  # Use white for currentColor
    return fill if fill.startswith('#') else "#FFFFFF"

def convert_element(element):
    """Convert SVG element to Android VectorDrawable path."""
    
    is_stroked = has_stroke(element)
    fill_color = "#00000000" if is_stroked else get_fill_from_element(element)
    
    stroke_attrs = ""
    if is_stroked:
        stroke_width = extract_attr(element, 'stroke-width') or '1'
        stroke_attrs = f'''
            android:strokeWidth="{stroke_width}"
            android:strokeColor="#FFFFFF"
            android:strokeLineCap="round"
            android:strokeLineJoin="round"'''
    
    # Circle
    if element.startswith('<circle'):
        cx = extract_attr(element, 'cx') or '0'
        cy = extract_attr(element, 'cy') or '0'
        r = extract_attr(element, 'r') or '0'
        path_data = circle_to_path(cx, cy, r)
        return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="{fill_color}"{stroke_attrs}/>'''
    
    # Ellipse
    if element.startswith('<ellipse'):
        cx = extract_attr(element, 'cx') or '0'
        cy = extract_attr(element, 'cy') or '0'
        rx = extract_attr(element, 'rx') or '0'
        ry = extract_attr(element, 'ry') or '0'
        path_data = ellipse_to_path(cx, cy, rx, ry)
        return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="{fill_color}"{stroke_attrs}/>'''
    
    # Rect
    if element.startswith('<rect'):
        x = extract_attr(element, 'x') or '0'
        y = extract_attr(element, 'y') or '0'
        w = extract_attr(element, 'width') or '0'
        h = extract_attr(element, 'height') or '0'
        path_data = rect_to_path(x, y, w, h)
        return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="{fill_color}"{stroke_attrs}/>'''
    
    # Line
    if element.startswith('<line'):
        x1 = extract_attr(element, 'x1') or '0'
        y1 = extract_attr(element, 'y1') or '0'
        x2 = extract_attr(element, 'x2') or '0'
        y2 = extract_attr(element, 'y2') or '0'
        path_data = line_to_path(x1, y1, x2, y2)
        return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="#00000000"
            android:strokeWidth="1"
            android:strokeColor="#FFFFFF"
            android:strokeLineCap="round"/>'''
    
    # Polygon
    if element.startswith('<polygon'):
        points = extract_attr(element, 'points') or ''
        if points:
            path_data = polygon_to_path(points)
            return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="{fill_color}"{stroke_attrs}/>'''
    
    # Polyline
    if element.startswith('<polyline'):
        points = extract_attr(element, 'points') or ''
        if points:
            path_data = polyline_to_path(points)
            return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="#00000000"
            android:strokeWidth="1"
            android:strokeColor="#FFFFFF"
            android:strokeLineCap="round"
            android:strokeLineJoin="round"/>'''
    
    # Path (just convert attributes)
    if element.startswith('<path'):
        path_data = extract_attr(element, 'd') or ''
        if path_data:
            # Extract fill-rule and convert to fillType
            fill_rule = extract_attr(element, 'fill-rule')
            fill_type_attr = ""
            if fill_rule == 'evenodd':
                fill_type_attr = '\n            android:fillType="evenOdd"'

            return f'''        <path
            android:pathData="{path_data}"
            android:fillColor="{fill_color}"{fill_type_attr}{stroke_attrs}/>'''
    
    # Unknown element - skip with comment
    return f"        <!-- Skipped unsupported element -->"

# Find all SVG shape elements (handle multi-line elements)
# First, normalize to single line per element
normalized = re.sub(r'>\s+<', '><', icon_body)
normalized = re.sub(r'\s+', ' ', normalized)

elements = re.findall(r'<(?:path|circle|ellipse|rect|line|polygon|polyline)[^>]*/>', normalized)
converted = [convert_element(el) for el in elements if el.strip()]

# Filter out empty/skipped elements
converted = [c for c in converted if 'Skipped' not in c]

print(f'''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <group
        android:scaleX="{final_scale:.4f}"
        android:scaleY="{final_scale:.4f}"
        android:translateX="{translate_x:.4f}"
        android:translateY="{translate_y:.4f}">
        <!-- Icon: $ICON_ID -->
        <!-- Original viewBox: {icon_width}x{icon_height} -->
{chr(10).join(converted)}
    </group>
</vector>''')
PYEOF

printf "✓ Created ic_launcher_foreground.xml\n\n"

# Step 3: Generate VectorDrawable background
printf "Step 3: Generating ic_launcher_background.xml...\n"

cat > "$DRAWABLE_DIR/ic_launcher_background.xml" << EOF
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="$ICON_BACKGROUND"
        android:pathData="M0,0h108v108h-108z" />
</vector>
EOF

printf "✓ Created ic_launcher_background.xml\n\n"

# Step 4: Create adaptive icon XMLs
printf "Step 4: Creating adaptive icon definitions...\n"
mkdir -p "$MIPMAP_DIR"

cat > "$MIPMAP_DIR/ic_launcher.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
EOF

cat > "$MIPMAP_DIR/ic_launcher_round.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
EOF

printf "✓ Created ic_launcher.xml\n"
printf "✓ Created ic_launcher_round.xml\n\n"

# Step 5: Generate Play Store icon
printf "Step 5: Generating Play Store icon (512x512 PNG)...\n"
mkdir -p "$PLAYSTORE_DIR"

# Fetch SVG directly from Iconify with color applied
curl -s "https://api.iconify.design/${ICON_COLLECTION}/${ICON_NAME}.svg?color=${ICON_COLOR}" > "$TMP_DIR/icon.svg"

# Convert Android color format (#AARRGGBB) to SVG format (#RRGGBB)
SVG_BACKGROUND="$ICON_BACKGROUND"
if [ -n "$ICON_BACKGROUND" ]; then
    # Check if color starts with # and has 9 chars (#AARRGGBB)
    if printf "%s" "$ICON_BACKGROUND" | grep -qE '^#[0-9A-Fa-f]{8}$'; then
        # Strip alpha channel (first 2 chars after #)
        SVG_BACKGROUND="#$(printf "%s" "$ICON_BACKGROUND" | cut -c4-9)"
    fi
fi

# Get the SVG content without the wrapper
SVG_INNER=$(cat "$TMP_DIR/icon.svg" | sed 's/<svg[^>]*>//g;s/<\/svg>//g')

# Extract viewBox and calculate proper scale/offset
VIEWBOX=$(grep -o 'viewBox="[^"]*"' "$TMP_DIR/icon.svg" | sed 's/viewBox="\([^"]*\)"/\1/')
if [ -n "$VIEWBOX" ]; then
    VB_WIDTH=$(printf "%s" "$VIEWBOX" | awk '{print $3}')
    VB_SIZE="${VB_WIDTH:-48}"
    ICON_SIZE=307
    SCALE=$(awk "BEGIN {printf \"%.2f\", $ICON_SIZE / $VB_SIZE}")
    OFFSET=$(awk "BEGIN {printf \"%.1f\", (512 - $ICON_SIZE) / 2}")
else
    SCALE="6.4"
    OFFSET="102.5"
fi

# Create composite SVG with background
cat > "$TMP_DIR/playstore.svg" << SVGEOF
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="$SVG_BACKGROUND"/>
  <g transform="translate($OFFSET, $OFFSET) scale($SCALE)">
    $SVG_INNER
  </g>
</svg>
SVGEOF

# Render to PNG
rsvg-convert -w 512 -h 512 "$TMP_DIR/playstore.svg" -o "$PLAYSTORE_DIR/icon.png"

# Verify PNG was created and has correct size
if [ -f "$PLAYSTORE_DIR/icon.png" ]; then
    PNG_INFO=$(file "$PLAYSTORE_DIR/icon.png")
    if printf "%s" "$PNG_INFO" | grep -q "512 x 512"; then
        printf "✓ Created icon.png (512x512)\n\n"
    else
        printf "⚠ Created icon.png but size may be incorrect\n"
        printf "   %s\n\n" "$PNG_INFO"
    fi
else
    printf "✗ Failed to create icon.png\n\n"
fi

# Step 6: Verification
printf "=== Verification ===\n"

ERRORS=0

check_file() {
    if [ -f "$1" ]; then
        printf "✓ %s\n" "$1"
        return 0
    else
        printf "✗ %s (MISSING)\n" "$1"
        return 1
    fi
}

check_file "$DRAWABLE_DIR/ic_launcher_foreground.xml" || ERRORS=$((ERRORS + 1))
check_file "$DRAWABLE_DIR/ic_launcher_background.xml" || ERRORS=$((ERRORS + 1))
check_file "$MIPMAP_DIR/ic_launcher.xml" || ERRORS=$((ERRORS + 1))
check_file "$MIPMAP_DIR/ic_launcher_round.xml" || ERRORS=$((ERRORS + 1))
check_file "$PLAYSTORE_DIR/icon.png" || ERRORS=$((ERRORS + 1))

printf "\n"

if [ "$ERRORS" -gt 0 ]; then
    printf "⚠ %d file(s) missing\n" "$ERRORS"
    exit 1
fi

printf "=== Generation Complete ===\n"
printf "\nNext steps:\n"
printf "  1. Review icons in Android Studio Resource Manager\n"
printf "  2. Build: ./gradlew assembleDebug\n"
printf "  3. Optional: Remove legacy raster icons:\n"
printf "     find app/src/main/res/mipmap-* -name '*.webp' -delete\n"
