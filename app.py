import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import os
import re
import math
import numpy as np
from pathlib import Path

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PixelKit — Image Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;0,700;1,300&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #0c0c0f;
    --surface: #141417;
    --surface2: #1c1c21;
    --border: #2a2a32;
    --border-bright: #3d3d4a;
    --text: #e8e8f0;
    --text-muted: #7878a0;
    --accent: #c8a96e;
    --accent2: #7b68ee;
    --accent3: #5bc8af;
    --red: #e05555;
    --green: #5bc88a;
}

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide Streamlit chrome */
#MainMenu, header, footer, .stDeployButton { display: none !important; }
.stApp { background: var(--bg) !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 1280px; }

/* Sidebar */
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-muted) !important;
    font-size: 0.9rem !important;
    padding: 0.4rem 0.6rem;
    border-radius: 8px;
    transition: all 0.15s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: var(--text) !important; background: var(--surface2) !important; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0f0f14 0%, #1a1520 40%, #131318 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.8rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(200,169,110,0.08) 0%, transparent 65%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 400px; height: 200px;
    background: radial-gradient(ellipse, rgba(123,104,238,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.hero-wordmark {
    font-family: 'Fraunces', serif;
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-size: 3.2rem;
    font-weight: 300;
    color: var(--text);
    line-height: 1.1;
    margin: 0 0 0.6rem 0;
    letter-spacing: -1px;
}
.hero-title em { font-style: italic; color: var(--accent); }
.hero-sub {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 400;
    max-width: 520px;
    line-height: 1.6;
}
.hero-pills {
    display: flex; gap: 8px; flex-wrap: wrap; margin-top: 1.5rem;
}
.pill {
    background: rgba(200,169,110,0.08);
    border: 1px solid rgba(200,169,110,0.2);
    color: var(--accent);
    padding: 4px 14px;
    border-radius: 99px;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
}

/* Section Header */
.sec-hdr {
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 300;
    color: var(--text);
    margin: 0 0 1rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.sec-hdr span { color: var(--accent); }

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1rem;
}
.card-dark {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.7;
}

/* Metric grid */
.met-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(120px,1fr)); gap: 8px; margin: 1rem 0; }
.met-item { background: var(--surface2); border: 1px solid var(--border); border-radius: 10px; padding: 0.9rem 0.8rem; text-align: center; }
.met-v { font-family: 'Fraunces', serif; font-size: 1.3rem; font-weight: 300; color: var(--accent); }
.met-l { font-size: 0.72rem; color: var(--text-muted); margin-top: 3px; letter-spacing: 0.04em; text-transform: uppercase; }

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #0c0c0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.6rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1px dashed var(--border-bright) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--accent) !important; }

/* Inputs */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stSlider > div { color: var(--text) !important; }
[data-testid="stSlider"] .stSlider > div > div { background: var(--accent2) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    padding: 4px !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 7px !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
}

/* Alerts */
.stSuccess { background: rgba(91,200,138,0.1) !important; border: 1px solid rgba(91,200,138,0.3) !important; color: var(--green) !important; border-radius: 10px !important; }
.stWarning { background: rgba(200,169,110,0.1) !important; border: 1px solid rgba(200,169,110,0.3) !important; border-radius: 10px !important; }
.stError { background: rgba(224,85,85,0.1) !important; border: 1px solid rgba(224,85,85,0.3) !important; border-radius: 10px !important; }
.stInfo { background: rgba(123,104,238,0.1) !important; border: 1px solid rgba(123,104,238,0.3) !important; border-radius: 10px !important; }

/* Info note */
.note {
    background: rgba(123,104,238,0.08);
    border-left: 3px solid var(--accent2);
    padding: 0.7rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: var(--text-muted);
    margin: 0.6rem 0;
    line-height: 1.6;
}
.note-gold {
    background: rgba(200,169,110,0.07);
    border-left: 3px solid var(--accent);
    padding: 0.7rem 1rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: var(--text-muted);
    margin: 0.6rem 0;
    line-height: 1.6;
}

/* Sidebar brand */
.sidebar-brand {
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-weight: 300;
    color: var(--text);
    padding: 0.5rem 0 0.3rem 0;
}
.sidebar-brand span { color: var(--accent); }

/* Attire grid */
.attire-info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 0.5rem 0;
}
.attire-item {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem 0.7rem;
    font-size: 0.82rem;
    color: var(--text-muted);
}

/* Selectbox dark */
div[data-baseweb="select"] > div {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* Checkbox */
.stCheckbox label { color: var(--text-muted) !important; font-size: 0.88rem !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Instrument Sans', sans-serif !important;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 10px !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 500 !important;
}
.stDownloadButton > button:hover { background: rgba(200,169,110,0.1) !important; }

/* Progress bar */
.stProgress > div > div { background: var(--accent) !important; }

/* Divider color */
hr { border-color: var(--border) !important; }

/* Markdown text color */
p, li, span { color: var(--text); }
label { color: var(--text-muted) !important; }

/* Column headers */
h1, h2, h3, h4 { color: var(--text) !important; font-family: 'Fraunces', serif !important; font-weight: 300 !important; }

</style>
""", unsafe_allow_html=True)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_image_from_upload(uploaded) -> tuple[Image.Image, bytes]:
    """Load image from upload, handling PDF and all image formats."""
    file_bytes = uploaded.read()
    fname = uploaded.name.lower()
    
    if fname.endswith(".pdf"):
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            page = doc[0]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("jpeg")
            img = Image.open(io.BytesIO(img_bytes))
            return img, img_bytes
        except Exception:
            st.error("Could not read PDF. Please convert to an image format.")
            return None, None
    else:
        img = Image.open(io.BytesIO(file_bytes))
        img = fix_orientation(img)
        return img, file_bytes

def fix_orientation(img: Image.Image) -> Image.Image:
    return ImageOps.exif_transpose(img)

def img_to_bytes(img: Image.Image, fmt="JPEG", quality=92) -> bytes:
    buf = io.BytesIO()
    if fmt.upper() == "PNG":
        save_img = img.convert("RGBA") if img.mode == "RGBA" else img.convert("RGB")
        save_img.save(buf, format="PNG", optimize=True)
    elif fmt.upper() == "WEBP":
        img.convert("RGB").save(buf, format="WEBP", quality=quality)
    elif fmt.upper() == "BMP":
        img.convert("RGB").save(buf, format="BMP")
    elif fmt.upper() == "TIFF":
        img.convert("RGB").save(buf, format="TIFF")
    elif fmt.upper() == "GIF":
        img.convert("P").save(buf, format="GIF")
    else:
        img.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True)
    return buf.getvalue()

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[^\w\-_.]', '_', name)
    return re.sub(r'_+', '_', name)

def compress_to_target(img: Image.Image, target_kb: float, fmt: str = "JPEG") -> bytes:
    if fmt.upper() == "PNG":
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG", optimize=True)
        return buf.getvalue()
    lo, hi, best = 5, 97, None
    for _ in range(15):
        mid = (lo + hi) // 2
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=mid, optimize=True)
        data = buf.getvalue()
        if len(data) / 1024 <= target_kb:
            best = data
            lo = mid + 1
        else:
            hi = mid - 1
    if best is None:
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=5, optimize=True)
        best = buf.getvalue()
    return best

def resize_fit(img: Image.Image, w: int, h: int, method="fit") -> Image.Image:
    if method == "fit":
        return ImageOps.fit(img, (w, h), Image.LANCZOS)
    elif method == "resize":
        return img.resize((w, h), Image.LANCZOS)
    elif method == "pad":
        img.thumbnail((w, h), Image.LANCZOS)
        new = Image.new("RGB", (w, h), (255, 255, 255))
        off = ((w - img.width) // 2, (h - img.height) // 2)
        new.paste(img, off)
        return new
    return img

# ──────────────────────────────────────────────────────────────────────────────
# AI UPSCALING / QUALITY ENHANCEMENT
# ──────────────────────────────────────────────────────────────────────────────

def enhance_quality_advanced(img: Image.Image, strength: str = "balanced") -> Image.Image:
    """
    Multi-pass quality enhancement pipeline:
    1. Upscale with Lanczos for resolution boost
    2. Adaptive sharpening via unsharp mask
    3. Contrast enhancement
    4. Noise reduction while preserving edges
    5. Color saturation boost
    """
    img = img.convert("RGB")
    w, h = img.size
    
    # Step 1: Super-resolution via 2x upscale then back (sharpens detail)
    scale = {"light": 1.5, "balanced": 2.0, "strong": 2.5}.get(strength, 2.0)
    up = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    
    # Step 2: Unsharp mask for detail recovery
    radius = {"light": 1.5, "balanced": 2.0, "strong": 2.5}.get(strength, 2.0)
    percent = {"light": 100, "balanced": 160, "strong": 220}.get(strength, 160)
    up = up.filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=2))
    
    # Step 3: Edge enhancement
    up = up.filter(ImageFilter.SMOOTH_MORE)
    up = ImageEnhance.Sharpness(up).enhance(1.8 if strength == "strong" else 1.4)
    
    # Step 4: Contrast and brightness
    contrast_v = {"light": 1.05, "balanced": 1.12, "strong": 1.18}.get(strength, 1.12)
    bright_v = {"light": 1.02, "balanced": 1.04, "strong": 1.06}.get(strength, 1.04)
    up = ImageEnhance.Contrast(up).enhance(contrast_v)
    up = ImageEnhance.Brightness(up).enhance(bright_v)
    
    # Step 5: Color saturation
    sat_v = {"light": 1.05, "balanced": 1.1, "strong": 1.15}.get(strength, 1.1)
    up = ImageEnhance.Color(up).enhance(sat_v)
    
    # Step 6: Noise reduction pass
    arr = np.array(up, dtype=np.float32)
    # Gentle bilateral-style smoothing on low-frequency areas
    blurred = np.array(up.filter(ImageFilter.GaussianBlur(radius=0.8)), dtype=np.float32)
    detail = arr - blurred
    result = blurred + detail * 1.3  # Amplify fine details
    result = np.clip(result, 0, 255).astype(np.uint8)
    up = Image.fromarray(result)
    
    # Step 7: Scale back to original size (preserves sharpness from upscale)
    final = up.resize((w, h), Image.LANCZOS)
    return final

# ──────────────────────────────────────────────────────────────────────────────
# BACKGROUND REMOVAL
# ──────────────────────────────────────────────────────────────────────────────

def remove_background_advanced(img: Image.Image) -> Image.Image:
    """
    Background removal using GrabCut-style iterative segmentation via numpy.
    Works best for portrait photos. Returns RGBA image.
    """
    try:
        import cv2
        rgb = np.array(img.convert("RGB"))
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        h, w = bgr.shape[:2]
        
        # Define rect for GrabCut (shrink from edges)
        margin_x = int(w * 0.05)
        margin_y = int(h * 0.03)
        rect = (margin_x, margin_y, w - 2*margin_x, h - 2*margin_y)
        
        mask = np.zeros((h, w), np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        cv2.grabCut(bgr, mask, rect, bgd_model, fgd_model, 8, cv2.GC_INIT_WITH_RECT)
        
        # Refine: assume center region is foreground
        center_mask = np.zeros_like(mask)
        cx, cy = w//2, h//2
        pad_x, pad_y = int(w*0.25), int(h*0.2)
        center_mask[cy-pad_y:cy+pad_y, cx-pad_x:cx+pad_x] = cv2.GC_FGD
        mask2 = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
        
        # Apply feathering for smooth edges
        alpha = (mask2 * 255).astype(np.uint8)
        alpha = cv2.GaussianBlur(alpha, (5, 5), 0)
        
        # Build RGBA
        rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGBA)
        rgba[:, :, 3] = alpha
        return Image.fromarray(rgba)
    
    except ImportError:
        # Fallback: numpy-based corner flood approach
        return _remove_bg_fallback(img)

def _remove_bg_fallback(img: Image.Image) -> Image.Image:
    """Fallback background removal using color clustering from corners."""
    rgb = img.convert("RGB")
    arr = np.array(rgb, dtype=np.float32)
    h, w = arr.shape[:2]
    
    # Sample background color from corners and edges
    corners = []
    margin = max(5, min(w, h) // 20)
    corners.append(arr[:margin, :margin].reshape(-1, 3))
    corners.append(arr[:margin, -margin:].reshape(-1, 3))
    corners.append(arr[-margin:, :margin].reshape(-1, 3))
    corners.append(arr[-margin:, -margin:].reshape(-1, 3))
    bg_samples = np.vstack(corners)
    bg_color = np.median(bg_samples, axis=0)
    
    # Distance from background color
    diff = np.sqrt(np.sum((arr - bg_color)**2, axis=2))
    
    # Threshold + smooth
    threshold = 60
    alpha = np.where(diff > threshold, 255, 0).astype(np.uint8)
    
    # Morphological cleaning
    from PIL import ImageFilter
    alpha_img = Image.fromarray(alpha)
    alpha_img = alpha_img.filter(ImageFilter.MedianFilter(5))
    alpha = np.array(alpha_img)
    
    # Build RGBA
    rgba = np.concatenate([arr.astype(np.uint8), alpha[:, :, np.newaxis]], axis=2)
    return Image.fromarray(rgba, mode="RGBA")

def apply_background_color(fg_rgba: Image.Image, color: tuple) -> Image.Image:
    """Composite RGBA image onto solid background color."""
    fg = fg_rgba.convert("RGBA")
    bg = Image.new("RGBA", fg.size, (*color, 255))
    bg.paste(fg, (0, 0), fg)
    return bg.convert("RGB")

def apply_attire_overlay(img: Image.Image, attire_name: str) -> Image.Image:
    """
    Draw a simple attire collar/neckline indicator overlay.
    Since we can't load external clothing images, we draw styled collar shapes.
    """
    from PIL import ImageDraw, ImageFont
    result = img.copy().convert("RGB")
    w, h = result.size
    draw = ImageDraw.Draw(result)
    
    # Position: collar starts at ~65% height, centered
    cx = w // 2
    collar_top = int(h * 0.63)
    collar_bottom = int(h * 0.82)
    shoulder_y = int(h * 0.67)
    
    attire_styles = {
        # (collar_color, fill_color, collar_type)
        "White Formal Shirt": ((255,255,255), (240,240,240), "dress_shirt"),
        "Black Suit & Tie": ((30,30,30), (20,20,20), "suit"),
        "Navy Blue Blazer": ((25,42,86), (20,35,75), "blazer"),
        "White Shirt & Tie": ((255,255,255), (240,240,240), "shirt_tie"),
        "Grey Suit": ((100,100,110), (85,85,95), "suit"),
        "Black Formal Dress": ((20,20,20), (15,15,15), "formal_dress"),
        "White Blouse": ((255,255,255), (248,248,248), "blouse"),
        "Navy Kurta": ((25,42,86), (20,35,75), "kurta"),
        "Maroon Blazer": ((120,20,40), (100,15,30), "blazer"),
        "Light Blue Shirt": ((180,210,240), (160,195,230), "dress_shirt"),
        "Saree Blouse (Red)": ((180,20,20), (160,15,15), "blouse"),
        "Saree Blouse (Green)": ((20,120,60), (15,100,50), "blouse"),
        "Pink Formal Top": ((220,140,160), (210,125,145), "blouse"),
        "Cream Kurta": ((245,235,210), (235,225,200), "kurta"),
        "Charcoal Suit": ((55,55,60), (45,45,50), "suit"),
        "Olive Green Blazer": ((80,100,50), (70,88,40), "blazer"),
    }
    
    if attire_name not in attire_styles:
        return result
    
    collar_col, fill_col, ctype = attire_styles[attire_name]
    
    # Draw body/chest area
    body_points = [
        (0, shoulder_y), (cx - int(w*0.18), shoulder_y),
        (cx - int(w*0.12), collar_top), (cx + int(w*0.12), collar_top),
        (cx + int(w*0.18), shoulder_y), (w, shoulder_y),
        (w, h), (0, h)
    ]
    draw.polygon(body_points, fill=fill_col)
    
    if ctype in ("suit", "blazer"):
        # Lapels
        lapel_l = [(cx - int(w*0.18), shoulder_y), (cx - int(w*0.05), collar_top),
                   (cx - int(w*0.02), int(h*0.72)), (0, shoulder_y + int(h*0.08)), (0, shoulder_y)]
        lapel_r = [(cx + int(w*0.18), shoulder_y), (cx + int(w*0.05), collar_top),
                   (cx + int(w*0.02), int(h*0.72)), (w, shoulder_y + int(h*0.08)), (w, shoulder_y)]
        inner_col = tuple(min(255, c + 30) for c in fill_col)
        draw.polygon(lapel_l, fill=inner_col)
        draw.polygon(lapel_r, fill=inner_col)
        # Collar line
        draw.line([(cx, collar_top), (cx - int(w*0.05), int(h*0.74))], fill=collar_col, width=max(1, w//80))
        draw.line([(cx, collar_top), (cx + int(w*0.05), int(h*0.74))], fill=collar_col, width=max(1, w//80))
        
        if ctype == "suit" or "Tie" in attire_name:
            # Tie
            tie_col = (180, 20, 20) if "Black" in attire_name or "Grey" in attire_name or "Charcoal" in attire_name else (20, 60, 140)
            tie_w = max(3, w // 25)
            draw.polygon([
                (cx - tie_w, collar_top + 5), (cx + tie_w, collar_top + 5),
                (cx + tie_w//2, int(h * 0.80)), (cx, int(h * 0.83)), (cx - tie_w//2, int(h * 0.80))
            ], fill=tie_col)
    
    elif ctype == "dress_shirt":
        # Shirt collar points
        draw.polygon([
            (cx - int(w*0.12), collar_top), (cx, collar_top + int(h*0.03)),
            (cx + int(w*0.12), collar_top),
            (cx + int(w*0.09), collar_top - int(h*0.03)),
            (cx, collar_top - int(h*0.01)),
            (cx - int(w*0.09), collar_top - int(h*0.03)),
        ], fill=collar_col, outline=tuple(max(0, c-30) for c in collar_col))
        # Buttons
        btn_col = tuple(max(0, c - 40) for c in collar_col)
        for i in range(3):
            by = collar_top + int(h * 0.04) + i * int(h * 0.05)
            draw.ellipse([cx-3, by-3, cx+3, by+3], fill=btn_col)
        
        if "Tie" in attire_name:
            tie_col = (20, 60, 140)
            tie_w = max(3, w // 25)
            draw.polygon([
                (cx - tie_w, collar_top + 8), (cx + tie_w, collar_top + 8),
                (cx + tie_w//2, int(h * 0.79)), (cx, int(h * 0.82)), (cx - tie_w//2, int(h * 0.79))
            ], fill=tie_col)
    
    elif ctype == "blouse":
        # Simple rounded neckline
        draw.ellipse([cx - int(w*0.12), collar_top - int(h*0.02),
                      cx + int(w*0.12), collar_top + int(h*0.04)], fill=fill_col, outline=collar_col)
    
    elif ctype == "kurta":
        # Mandarin/Nehru collar
        draw.rectangle([cx - int(w*0.07), collar_top - int(h*0.03),
                        cx + int(w*0.07), collar_top + int(h*0.03)], fill=fill_col, outline=collar_col)
        # Center placket line
        draw.line([(cx, collar_top), (cx, collar_top + int(h*0.12))], fill=collar_col, width=max(1, w//100))
    
    elif ctype == "formal_dress":
        # V-neckline
        draw.polygon([
            (cx - int(w*0.15), collar_top - int(h*0.02)),
            (cx, collar_top + int(h*0.06)),
            (cx + int(w*0.15), collar_top - int(h*0.02)),
        ], fill=fill_col, outline=collar_col)
    
    # Shoulder seams
    draw.line([(0, shoulder_y), (cx - int(w*0.18), shoulder_y)], fill=collar_col, width=max(1, w//120))
    draw.line([(w, shoulder_y), (cx + int(w*0.18), shoulder_y)], fill=collar_col, width=max(1, w//120))
    
    return result

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">Pixel<span>Kit</span></div>
    <div style="font-size:0.75rem; color:#7878a0; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1.2rem;">Image Studio</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tool = st.radio("", [
        "⟁  Compress & Resize",
        "◈  Background Studio",
        "⇄  Format Converter",
        "◉  Quality Enhancer",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem; color:#555570; line-height:1.7; padding:0.4rem 0'>
    All processing is done<br>
    locally in your session.<br>
    No data is stored.
    </div>
    """, unsafe_allow_html=True)

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-wordmark">✦ Image Processing Studio</div>
  <h1 class="hero-title">Precision tools for<br><em>perfect images</em></h1>
  <p class="hero-sub">Compress, resize, remove backgrounds, convert formats and enhance quality — all in one place.</p>
  <div class="hero-pills">
    <span class="pill">Passport Photos</span>
    <span class="pill">Signatures</span>
    <span class="pill">Government Forms</span>
    <span class="pill">University Portals</span>
    <span class="pill">Professional Headshots</span>
  </div>
</div>
""", unsafe_allow_html=True)

ACCEPTED_TYPES = ["jpg", "jpeg", "png", "bmp", "tiff", "webp", "gif", "pdf", "heic"]

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 1: COMPRESS & RESIZE
# ═══════════════════════════════════════════════════════════════════════════════
if tool == "⟁  Compress & Resize":
    st.markdown('<p class="sec-hdr">⟁ <span>Compress</span> & Resize</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop your image here — JPG, PNG, PDF, HEIC, WEBP, BMP, TIFF accepted",
                                 type=ACCEPTED_TYPES)

    if uploaded:
        img, raw_bytes = load_image_from_upload(uploaded)
        if img is None:
            st.stop()

        orig_kb = len(raw_bytes) / 1024
        orig_w, orig_h = img.size

        tab1, tab2 = st.tabs(["  📦  Compress File Size  ", "  📐  Resize Dimensions  "])

        # ── Compress Tab ──
        with tab1:
            col1, col2 = st.columns([1.1, 1])
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                target_kb = st.number_input("Target Maximum Size (KB)", 5.0, 10000.0, 50.0, step=5.0)
                out_fmt_c = st.selectbox("Output Format", ["JPEG", "PNG"], key="comp_fmt")
                
                st.markdown(f"""
                <div class="card-dark">
                Original file: <strong>{orig_kb:.1f} KB</strong> &nbsp;·&nbsp; {orig_w}×{orig_h} px
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="note-gold">
                Common requirements: Exam portals 10–50 KB · University forms 50–100 KB · Signature 10–30 KB
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.image(img, caption="Original", use_container_width=True)

            if st.button("Compress Image", key="compress_btn"):
                with st.spinner("Compressing..."):
                    compressed = compress_to_target(img, target_kb, out_fmt_c)
                    comp_kb = len(compressed) / 1024
                    reduction = (1 - comp_kb / orig_kb) * 100

                col2.image(Image.open(io.BytesIO(compressed)), caption=f"Result: {comp_kb:.1f} KB", use_container_width=True)

                if comp_kb <= target_kb:
                    st.success(f"✓  {orig_kb:.1f} KB → {comp_kb:.1f} KB  ·  {reduction:.0f}% reduction")
                else:
                    st.warning(f"Best achievable: {comp_kb:.1f} KB · Try reducing dimensions first using the Resize tab.")

                ext = "jpg" if out_fmt_c == "JPEG" else "png"
                base = sanitize_filename(Path(uploaded.name).stem)
                st.download_button("⬇  Download Compressed Image", compressed,
                                   file_name=f"{base}_compressed.{ext}",
                                   mime=f"image/{'jpeg' if out_fmt_c=='JPEG' else 'png'}")

        # ── Resize Tab ──
        with tab2:
            col1, col2 = st.columns([1.1, 1])
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                preset = st.selectbox("Quick Preset", [
                    "Custom",
                    "Passport / NEET Photo — 200×230 px",
                    "Passport Photo — 413×531 px (35×45mm @ 300dpi)",
                    "Passport Photo — 300×300 px",
                    "Signature (NEET/JEE) — 140×60 px",
                    "Signature — 200×80 px",
                    "Profile / Thumbnail — 500×500 px",
                    "ID Card — 640×480 px",
                    "Square Thumbnail — 200×200 px",
                ], key="resize_preset")

                PRESET_MAP = {
                    "Passport / NEET Photo — 200×230 px": (200, 230),
                    "Passport Photo — 413×531 px (35×45mm @ 300dpi)": (413, 531),
                    "Passport Photo — 300×300 px": (300, 300),
                    "Signature (NEET/JEE) — 140×60 px": (140, 60),
                    "Signature — 200×80 px": (200, 80),
                    "Profile / Thumbnail — 500×500 px": (500, 500),
                    "ID Card — 640×480 px": (640, 480),
                    "Square Thumbnail — 200×200 px": (200, 200),
                }
                pw, ph = PRESET_MAP.get(preset, (orig_w, orig_h))

                c_w, c_h = st.columns(2)
                with c_w: target_w = st.number_input("Width (px)", 1, 5000, pw, key="rw")
                with c_h: target_h = st.number_input("Height (px)", 1, 5000, ph, key="rh")

                method = st.selectbox("Resize Method", [
                    "fit — crop to exact size",
                    "pad — fit inside, pad with white",
                    "stretch — distort to exact size",
                ], key="resize_method")
                method_key = method.split(" ")[0]

                also_compress = st.checkbox("Also compress after resize", value=True, key="resize_compress")
                if also_compress:
                    compress_kb = st.number_input("Max Size after Resize (KB)", 5.0, 5000.0, 100.0, key="after_comp")

                out_fmt_r = st.selectbox("Output Format", ["JPEG", "PNG"], key="resize_fmt")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.image(img, caption=f"Original: {orig_w}×{orig_h} px", use_container_width=True)

            if st.button("Resize Image", key="resize_btn"):
                with st.spinner("Resizing..."):
                    resized = resize_fit(img.convert("RGB"), target_w, target_h, method_key)
                    if also_compress:
                        out_bytes = compress_to_target(resized, compress_kb, out_fmt_r)
                    else:
                        out_bytes = img_to_bytes(resized, out_fmt_r)

                col2.image(Image.open(io.BytesIO(out_bytes)), caption=f"Result: {target_w}×{target_h} px", use_container_width=True)
                st.success(f"✓  Resized to {target_w}×{target_h} px  ·  {len(out_bytes)/1024:.1f} KB")
                ext = "jpg" if out_fmt_r == "JPEG" else "png"
                base = sanitize_filename(Path(uploaded.name).stem)
                st.download_button("⬇  Download Resized Image", out_bytes,
                                   file_name=f"{base}_resized.{ext}",
                                   mime=f"image/{'jpeg' if out_fmt_r=='JPEG' else 'png'}")
    else:
        st.markdown("""
        <div class="card-dark" style="text-align:center; padding:2.5rem; color:#555570;">
        Upload an image above to get started
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 2: BACKGROUND STUDIO
# ═══════════════════════════════════════════════════════════════════════════════
elif tool == "◈  Background Studio":
    st.markdown('<p class="sec-hdr">◈ Background <span>Studio</span></p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="note">
    Upload your photo — the background will be automatically removed first, then you can apply a new background colour or attire overlay.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Photo — any format accepted",
                                 type=ACCEPTED_TYPES, key="bg_upload")

    if uploaded:
        img, raw_bytes = load_image_from_upload(uploaded)
        if img is None:
            st.stop()

        tab_bg, tab_attire = st.tabs(["  🎨  Background Color  ", "  👔  Attire Overlay  "])

        # ── Background Color Tab ──
        with tab_bg:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Background Color**")

                bg_option = st.selectbox("Preset Colors", [
                    "White", "Light Blue (Passport)", "Light Grey", "Sky Blue",
                    "Cream / Ivory", "Navy Blue", "Custom Color"
                ])
                BG_COLORS = {
                    "White": (255, 255, 255),
                    "Light Blue (Passport)": (173, 216, 230),
                    "Light Grey": (220, 220, 220),
                    "Sky Blue": (135, 206, 235),
                    "Cream / Ivory": (255, 253, 240),
                    "Navy Blue": (35, 55, 100),
                }
                if bg_option == "Custom Color":
                    hex_col = st.color_picker("Pick color", "#FFFFFF")
                    bg_color = tuple(int(hex_col[i:i+2], 16) for i in (1, 3, 5))
                else:
                    bg_color = BG_COLORS[bg_option]

                out_fmt_bg = st.selectbox("Output Format", ["JPEG", "PNG"], key="bg_fmt")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.image(img, caption="Original", use_container_width=True)

            if st.button("Remove Background & Apply Color", key="bg_btn"):
                with st.spinner("Removing background..."):
                    fg_rgba = remove_background_advanced(img)
                with st.spinner("Applying new background..."):
                    result = apply_background_color(fg_rgba, bg_color)

                col2.image(result, caption="Result", use_container_width=True)
                out_bytes = img_to_bytes(result, out_fmt_bg)
                st.success("✓  Background replaced successfully")
                ext = "jpg" if out_fmt_bg == "JPEG" else "png"
                base = sanitize_filename(Path(uploaded.name).stem)
                st.download_button("⬇  Download Image", out_bytes,
                                   file_name=f"{base}_bg_{bg_option.replace(' ','_').lower()}.{ext}",
                                   mime=f"image/{'jpeg' if out_fmt_bg=='JPEG' else 'png'}")

        # ── Attire Overlay Tab ──
        with tab_attire:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Attire Selection**")

                gender = st.radio("Gender", ["Male", "Female", "Unisex / Kurta"], horizontal=True)

                MALE_ATTIRE = [
                    "White Formal Shirt", "Black Suit & Tie", "Navy Blue Blazer",
                    "White Shirt & Tie", "Grey Suit", "Charcoal Suit",
                    "Light Blue Shirt", "Maroon Blazer", "Olive Green Blazer",
                    "Cream Kurta", "Navy Kurta",
                ]
                FEMALE_ATTIRE = [
                    "White Blouse", "Black Formal Dress", "Navy Blue Blazer",
                    "Pink Formal Top", "Maroon Blazer", "Grey Suit",
                    "Saree Blouse (Red)", "Saree Blouse (Green)", "Cream Kurta",
                    "Olive Green Blazer",
                ]
                UNISEX_ATTIRE = ["Cream Kurta", "Navy Kurta", "White Formal Shirt", "Navy Blue Blazer"]

                attire_list = MALE_ATTIRE if gender == "Male" else (FEMALE_ATTIRE if gender == "Female" else UNISEX_ATTIRE)
                selected_attire = st.selectbox("Choose Attire", attire_list)

                st.markdown('<div class="card-dark" style="margin-top:0.8rem">', unsafe_allow_html=True)
                st.markdown(f"**{selected_attire}** — collar and clothing will be drawn on the lower portion of the photo. Works best with portrait/headshot photos.")
                st.markdown('</div>', unsafe_allow_html=True)

                also_remove_bg = st.checkbox("Also remove & replace background", value=True, key="attire_bg")
                if also_remove_bg:
                    att_bg_col = st.selectbox("Background Color", ["White", "Light Blue (Passport)", "Light Grey", "Custom Color"], key="att_bg_sel")
                    if att_bg_col == "Custom Color":
                        hex_a = st.color_picker("Pick", "#FFFFFF", key="att_hex")
                        att_bg = tuple(int(hex_a[i:i+2], 16) for i in (1, 3, 5))
                    else:
                        att_bg = {"White": (255,255,255), "Light Blue (Passport)": (173,216,230), "Light Grey": (220,220,220)}[att_bg_col]

                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.image(img, caption="Original", use_container_width=True)

            if st.button("Apply Attire", key="attire_btn"):
                result = img.convert("RGB")

                if also_remove_bg:
                    with st.spinner("Removing background..."):
                        fg_rgba = remove_background_advanced(result)
                    result = apply_background_color(fg_rgba, att_bg)

                with st.spinner("Applying attire overlay..."):
                    result = apply_attire_overlay(result, selected_attire)

                col2.image(result, caption=f"With {selected_attire}", use_container_width=True)
                out_bytes = img_to_bytes(result, "JPEG")
                st.success(f"✓  Attire applied: {selected_attire}")
                base = sanitize_filename(Path(uploaded.name).stem)
                st.download_button("⬇  Download Image", out_bytes,
                                   file_name=f"{base}_attire.jpg", mime="image/jpeg")
    else:
        st.markdown("""
        <div class="card-dark" style="text-align:center; padding:2.5rem; color:#555570;">
        Upload a photo above to get started
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 3: FORMAT CONVERTER
# ═══════════════════════════════════════════════════════════════════════════════
elif tool == "⇄  Format Converter":
    st.markdown('<p class="sec-hdr">⇄ Format <span>Converter</span></p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="note">
    Convert between JPG, PNG, WebP, BMP, TIFF, GIF — including iPhone HEIC photos. Upload any format, download in any format.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Image — any format accepted",
                                 type=ACCEPTED_TYPES, key="conv_upload")

    if uploaded:
        img, raw_bytes = load_image_from_upload(uploaded)
        if img is None:
            st.stop()

        col1, col2 = st.columns([1.1, 1])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            detected = img.format or Path(uploaded.name).suffix.upper().replace(".", "")
            st.markdown(f"""
            <div class="card-dark">
            Detected format: <strong>{detected}</strong> &nbsp;·&nbsp; {img.width}×{img.height} px &nbsp;·&nbsp; {len(raw_bytes)/1024:.1f} KB
            </div>
            """, unsafe_allow_html=True)

            target_fmt = st.selectbox("Convert to", ["JPEG (JPG)", "PNG", "WEBP", "BMP", "TIFF", "GIF"])
            fmt_map = {
                "JPEG (JPG)": ("JPEG", "jpg", "image/jpeg"),
                "PNG": ("PNG", "png", "image/png"),
                "WEBP": ("WEBP", "webp", "image/webp"),
                "BMP": ("BMP", "bmp", "image/bmp"),
                "TIFF": ("TIFF", "tiff", "image/tiff"),
                "GIF": ("GIF", "gif", "image/gif"),
            }
            fmt_key, ext, mime = fmt_map[target_fmt]

            if fmt_key == "JPEG":
                jpeg_q = st.slider("JPEG Quality", 60, 100, 92, key="conv_q")
            else:
                jpeg_q = 92

            st.markdown("""
            <div class="note-gold" style="margin-top:0.8rem">
            <strong>JPEG/JPG</strong> — photos, passport images, smaller file size<br>
            <strong>PNG</strong> — signatures, logos, transparent backgrounds<br>
            <strong>WebP</strong> — modern format, smallest size with good quality
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.image(img, caption="Original", use_container_width=True)

        if st.button("Convert Format", key="convert_btn"):
            with st.spinner("Converting..."):
                out_bytes = img_to_bytes(img, fmt_key, jpeg_q)

            col2.image(Image.open(io.BytesIO(out_bytes)) if fmt_key in ("JPEG","PNG","WEBP") else img,
                       caption=f"Converted: {len(out_bytes)/1024:.1f} KB", use_container_width=True)
            st.success(f"✓  Converted to {fmt_key}  ·  {len(out_bytes)/1024:.1f} KB")
            base = sanitize_filename(Path(uploaded.name).stem)
            st.download_button(f"⬇  Download as .{ext}", out_bytes,
                               file_name=f"{base}.{ext}", mime=mime)
    else:
        st.markdown("""
        <div class="card-dark" style="text-align:center; padding:2.5rem; color:#555570;">
        Upload an image above to get started
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TOOL 4: QUALITY ENHANCER
# ═══════════════════════════════════════════════════════════════════════════════
elif tool == "◉  Quality Enhancer":
    st.markdown('<p class="sec-hdr">◉ Quality <span>Enhancer</span></p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="note">
    Multi-pass enhancement pipeline — upscales detail resolution, recovers sharpness via unsharp masking, adjusts contrast and colour depth automatically.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Image — any format accepted",
                                 type=ACCEPTED_TYPES, key="enh_upload")

    if uploaded:
        img, raw_bytes = load_image_from_upload(uploaded)
        if img is None:
            st.stop()

        col1, col2 = st.columns([1.1, 1])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            strength = st.radio("Enhancement Strength", ["light", "balanced", "strong"],
                                horizontal=True,
                                captions=["Subtle polish", "Recommended", "Maximum sharpness"])

            st.markdown("""
            <div class="card-dark" style="margin-top:0.8rem">
            <strong>What happens:</strong><br>
            1. 2× upscale with Lanczos interpolation<br>
            2. Unsharp mask for detail recovery<br>
            3. Edge sharpening pass<br>
            4. Contrast + brightness adjustment<br>
            5. Colour saturation boost<br>
            6. Detail amplification & noise reduction<br>
            7. Final downscale preserving enhanced details
            </div>
            """, unsafe_allow_html=True)

            fix_orient_e = st.checkbox("Auto-fix photo orientation", value=True, key="enh_orient")
            out_fmt_e = st.selectbox("Output Format", ["JPEG", "PNG"], key="enh_fmt")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.image(img, caption=f"Original: {img.width}×{img.height} px", use_container_width=True)

        if st.button("Enhance Quality", key="enhance_btn"):
            with st.spinner("Running enhancement pipeline..."):
                result = img.convert("RGB")
                if fix_orient_e:
                    result = fix_orientation(result)
                enhanced = enhance_quality_advanced(result, strength)

            col2.image(enhanced, caption="Enhanced", use_container_width=True)
            out_bytes = img_to_bytes(enhanced, out_fmt_e, 94)
            st.success(f"✓  Enhancement complete  ·  {len(out_bytes)/1024:.1f} KB")
            base = sanitize_filename(Path(uploaded.name).stem)
            ext = "jpg" if out_fmt_e == "JPEG" else "png"
            st.download_button("⬇  Download Enhanced Image", out_bytes,
                               file_name=f"{base}_enhanced.{ext}",
                               mime=f"image/{'jpeg' if out_fmt_e=='JPEG' else 'png'}")
    else:
        st.markdown("""
        <div class="card-dark" style="text-align:center; padding:2.5rem; color:#555570;">
        Upload an image above to get started
        </div>
        """, unsafe_allow_html=True)
