import streamlit as st
from PIL import Image, ImageDraw, ImageFilter
import io
import math
import random

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FrameFlow – Elegance in Every Frame",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F7F7FA !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding-top: 0 !important;
    max-width: 900px !important;
    margin: 0 auto !important;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── Header ── */
.ff-header {
    text-align: center;
    padding: 36px 0 18px;
    border-bottom: 1px solid #EBEBF0;
    margin-bottom: 28px;
}
.ff-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    background: linear-gradient(135deg, #C9A847 0%, #E8C96A 50%, #B8922F 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.ff-tagline {
    font-family: 'Inter', sans-serif;
    font-style: italic;
    font-size: 0.82rem;
    color: #9494A8;
    margin-top: 4px;
    letter-spacing: 0.04em;
}

/* ── Info Banner ── */
.ff-banner-info {
    background: #EEF0FF;
    border: 1px solid #D4D8FF;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 0.83rem;
    color: #5558A8;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.ff-banner-success {
    background: #EDFAF3;
    border: 1px solid #B2E8CE;
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 0.83rem;
    color: #1A8252;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Upload Card ── */
.ff-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 28px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 18px;
}

/* ── Settings Grid ── */
.ff-settings-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    color: #8888A0;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ff-badge {
    display: inline-block;
    background: linear-gradient(135deg, #22C990, #1BAB7B);
    color: white;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 6px;
}

/* ── Preview Section ── */
.ff-preview-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}
.ff-preview-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #222235;
}
.ff-preview-empty {
    background: linear-gradient(135deg, #F0F0F8, #EAEAF4);
    border-radius: 14px;
    padding: 60px 20px;
    text-align: center;
    color: #AAAABD;
}
.ff-preview-empty .icon {
    font-size: 3rem;
    margin-bottom: 10px;
    opacity: 0.4;
}
.ff-preview-empty p {
    font-size: 0.95rem;
    margin: 0;
    font-weight: 500;
}
.ff-preview-empty small {
    font-size: 0.78rem;
    opacity: 0.7;
}

/* ── Footer ── */
.ff-footer {
    text-align: center;
    padding: 24px 0 16px;
    border-top: 1px solid #EBEBF0;
    margin-top: 10px;
    font-size: 0.78rem;
    color: #9494AA;
}
.ff-footer a {
    color: #7B6EE0;
    text-decoration: none;
    font-weight: 500;
}

/* ── Streamlit Widget Overrides ── */
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 2px dashed #C8C8E0 !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #7B6EE0 !important;
}
[data-testid="stFileUploader"] label {
    display: none !important;
}

/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    border: 1px solid #DDDDED !important;
    border-radius: 10px !important;
    background: #FAFAFA !important;
    font-size: 0.88rem !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #7B6EE0 !important;
    box-shadow: 0 0 0 3px rgba(123,110,224,0.12) !important;
}

/* Slider */
[data-testid="stSlider"] > div > div > div {
    color: #7B6EE0 !important;
}
[data-testid="stSlider"] .stSlider > div {
    padding: 0 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7B6EE0, #6355C9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(123,110,224,0.32) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #7B6EE0, #6355C9) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(123,110,224,0.32) !important;
}

/* Images */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.10) !important;
}

/* Column gaps */
[data-testid="column"] {
    padding: 0 8px !important;
}

/* Card backgrounds for settings */
.settings-card {
    background: white;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    height: 100%;
}

</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
PHI = 1.618033988749895

QUALITY_OPTIONS = {
    "HD (1280 × 792px)": (1280, 792),
    "Full HD (1920 × 1188px)": (1920, 1188),
    "2K (2560 × 1582px) ⭐ Best": (2560, 1582),
    "4K (3840 × 2376px)": (3840, 2376),
}

LAYOUT_OPTIONS = [
    "Golden Ratio (Classic)",
    "Mosaic (Artistic)",
    "Grid (Symmetric)",
    "Triptych (Three Panels)",
    "Feature (Hero + Strips)",
]

EXPORT_OPTIONS = {
    "1x – Standard": 85,
    "2x – Better Quality": 95,
    "3x – Maximum Quality": 100,
}

# ─── Collage Generation ───────────────────────────────────────────────────────
def fit_image(img: Image.Image, w: int, h: int) -> Image.Image:
    """Crop-fit image into target (w, h) rectangle."""
    img = img.convert("RGBA")
    src_ratio = img.width / img.height
    tgt_ratio = w / h
    if src_ratio > tgt_ratio:
        new_w = int(img.height * tgt_ratio)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / tgt_ratio)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((w, h), Image.LANCZOS)


def add_borders(canvas: Image.Image, border_px: int, color=(255, 255, 255)) -> Image.Image:
    """Add white borders around all blocks by drawing rectangles on a copy."""
    if border_px <= 0:
        return canvas
    draw = ImageDraw.Draw(canvas)
    bw = border_px
    # borders on edges
    draw.rectangle([0, 0, canvas.width - 1, bw - 1], fill=color)
    draw.rectangle([0, canvas.height - bw, canvas.width - 1, canvas.height - 1], fill=color)
    draw.rectangle([0, 0, bw - 1, canvas.height - 1], fill=color)
    draw.rectangle([canvas.width - bw, 0, canvas.width - 1, canvas.height - 1], fill=color)
    return canvas


def generate_golden_ratio(images, W, H, border):
    """Classic 3-image golden ratio layout."""
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    b = border
    main_w = int(W / PHI)
    side_w = W - main_w
    sub_h = int(H / PHI)

    imgs = [images[i % len(images)] for i in range(3)]
    canvas.paste(fit_image(imgs[0], main_w - b * 2, H - b * 2), (b, b))
    canvas.paste(fit_image(imgs[1], side_w - b * 2, sub_h - b * 2), (main_w + b, b))
    canvas.paste(fit_image(imgs[2], side_w - b * 2, H - sub_h - b * 2), (main_w + b, sub_h + b))
    return canvas.convert("RGB")


def generate_mosaic(images, W, H, border):
    """Mosaic layout using up to 6 images."""
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    b = border
    n = min(len(images), 6)

    # Row proportions using golden ratio
    row1_h = int(H * (1 / PHI))
    row2_h = H - row1_h

    if n <= 3:
        col_w = (W - b * (n + 1)) // n
        for i in range(n):
            x = b + i * (col_w + b)
            canvas.paste(fit_image(images[i], col_w, row1_h - b * 2 + row2_h), (x, b))
    else:
        # Top row: 3 equal images
        top_n = min(n, 3)
        col_w_top = (W - b * (top_n + 1)) // top_n
        for i in range(top_n):
            x = b + i * (col_w_top + b)
            canvas.paste(fit_image(images[i], col_w_top, row1_h - b), (x, b))

        # Bottom row: remaining images
        bot_imgs = images[top_n:n]
        bot_n = len(bot_imgs)
        if bot_n == 0:
            return canvas.convert("RGB")
        col_w_bot = (W - b * (bot_n + 1)) // bot_n
        for i, img in enumerate(bot_imgs):
            x = b + i * (col_w_bot + b)
            canvas.paste(fit_image(img, col_w_bot, row2_h - b), (x, row1_h + b))

    return canvas.convert("RGB")


def generate_grid(images, W, H, border):
    """Symmetric grid layout."""
    n = min(len(images), 9)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    b = border
    cell_w = (W - b * (cols + 1)) // cols
    cell_h = (H - b * (rows + 1)) // rows
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    for idx in range(n):
        row = idx // cols
        col = idx % cols
        x = b + col * (cell_w + b)
        y = b + row * (cell_h + b)
        canvas.paste(fit_image(images[idx], cell_w, cell_h), (x, y))
    return canvas.convert("RGB")


def generate_triptych(images, W, H, border):
    """Three equal vertical panels."""
    b = border
    panel_w = (W - b * 4) // 3
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    imgs = [images[i % len(images)] for i in range(3)]
    for i, img in enumerate(imgs):
        x = b + i * (panel_w + b)
        canvas.paste(fit_image(img, panel_w, H - b * 2), (x, b))
    return canvas.convert("RGB")


def generate_feature(images, W, H, border):
    """Hero image on left, 3 strip images stacked on right."""
    b = border
    hero_w = int(W * 0.58)
    strip_w = W - hero_w - b * 3
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    imgs = [images[i % len(images)] for i in range(4)]
    canvas.paste(fit_image(imgs[0], hero_w - b, H - b * 2), (b, b))
    strip_h = (H - b * 4) // 3
    for i in range(3):
        y = b + i * (strip_h + b)
        canvas.paste(fit_image(imgs[i + 1], strip_w, strip_h), (hero_w + b * 2, y))
    return canvas.convert("RGB")


LAYOUT_GENERATORS = {
    "Golden Ratio (Classic)": generate_golden_ratio,
    "Mosaic (Artistic)": generate_mosaic,
    "Grid (Symmetric)": generate_grid,
    "Triptych (Three Panels)": generate_triptych,
    "Feature (Hero + Strips)": generate_feature,
}

MIN_IMAGES = {
    "Golden Ratio (Classic)": 3,
    "Mosaic (Artistic)": 3,
    "Grid (Symmetric)": 4,
    "Triptych (Three Panels)": 3,
    "Feature (Hero + Strips)": 4,
}


def build_collage(uploaded_files, layout, quality_key, border_px, export_quality_key):
    imgs = [Image.open(f) for f in uploaded_files]
    W, H = QUALITY_OPTIONS[quality_key]
    border = border_px
    gen_fn = LAYOUT_GENERATORS[layout]
    collage = gen_fn(imgs, W, H, border)

    # Encode to PNG bytes
    buf = io.BytesIO()
    q = EXPORT_OPTIONS[export_quality_key]
    collage.save(buf, format="PNG", optimize=True)
    buf.seek(0)

    # Return a smaller preview (max 900px wide)
    preview = collage.copy()
    max_w = 900
    if preview.width > max_w:
        ratio = max_w / preview.width
        preview = preview.resize((max_w, int(preview.height * ratio)), Image.LANCZOS)

    return buf, preview


# ─── Session State ────────────────────────────────────────────────────────────
if "collage_buf" not in st.session_state:
    st.session_state.collage_buf = None
if "preview_img" not in st.session_state:
    st.session_state.preview_img = None
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-header">
  <div class="ff-logo">FRAMEFLOW</div>
  <div class="ff-tagline">Elegance in every frame.</div>
</div>
""", unsafe_allow_html=True)

# ─── Info Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-banner-info">
  ℹ️ &nbsp;Golden Ratio <strong>(φ = 1.618)</strong> creates naturally balanced compositions.
  Your images will be arranged using these mathematically pleasing proportions.
</div>
""", unsafe_allow_html=True)

# ─── Success Banner ───────────────────────────────────────────────────────────
if st.session_state.show_success:
    st.markdown("""
    <div class="ff-banner-success">
      ✅ &nbsp;Collage generated successfully! Click <strong>"Download PNG"</strong> to save.
    </div>
    """, unsafe_allow_html=True)

# ─── Upload Card ──────────────────────────────────────────────────────────────
st.markdown('<div class="ff-card">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding: 8px 0 18px;">
  <div style="font-size:2.2rem;">⬆️</div>
  <div style="font-size:1.15rem; font-weight:600; color:#222235; margin:8px 0 4px;">Drag &amp; drop your images here</div>
  <div style="font-size:0.8rem; color:#AAAABD;">JPG, PNG, WebP • Max 15MB each • 3–10 images</div>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload Images",
    type=["jpg", "jpeg", "png", "webp", "gif"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Settings ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ff-settings-label">Output Quality</div>', unsafe_allow_html=True)
    quality_key = st.selectbox(
        "Output Quality",
        list(QUALITY_OPTIONS.keys()),
        index=2,
        label_visibility="collapsed",
    )
    if "2K" in quality_key or "Best" in quality_key:
        st.markdown('<span class="ff-badge">BEST</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ff-settings-label">Layout Style</div>', unsafe_allow_html=True)
    layout_style = st.selectbox(
        "Layout Style",
        LAYOUT_OPTIONS,
        index=1,
        label_visibility="collapsed",
    )

with col3:
    st.markdown('<div class="ff-settings-label">Border Width</div>', unsafe_allow_html=True)
    border_width = st.slider(
        "Border Width",
        min_value=0,
        max_value=40,
        value=10,
        step=2,
        format="%dpx",
        label_visibility="collapsed",
    )
    st.markdown(f'<div style="font-size:0.8rem; color:#9494A8;">{border_width}px</div>', unsafe_allow_html=True)

# ─── Second Settings Row ──────────────────────────────────────────────────────
col4, col5, _ = st.columns(3)

with col4:
    st.markdown('<div class="ff-settings-label" style="margin-top:14px;">Export Quality</div>', unsafe_allow_html=True)
    export_quality = st.selectbox(
        "Export Quality",
        list(EXPORT_OPTIONS.keys()),
        index=1,
        label_visibility="collapsed",
    )
    st.markdown('<div style="font-size:0.74rem; font-style:italic; color:#AAAABD; margin-top:4px;">High quality for sharing</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="ff-settings-label" style="margin-top:14px;">Layout Info</div>', unsafe_allow_html=True)
    min_imgs = MIN_IMAGES.get(layout_style, 3)
    n_uploaded = len(uploaded_files) if uploaded_files else 0
    if n_uploaded < min_imgs:
        remaining = min_imgs - n_uploaded
        info_text = f"Add {remaining} more image{'s' if remaining > 1 else ''} for this layout"
    else:
        info_text = f"✓ Ready — {n_uploaded} image{'s' if n_uploaded > 1 else ''} added"
    st.markdown(f'<div style="font-size:0.85rem; color:#666680; padding-top:6px;">{info_text}</div>', unsafe_allow_html=True)

# ─── Generate Button ──────────────────────────────────────────────────────────
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
col_gen1, col_gen2, col_gen3 = st.columns([1, 2, 1])
with col_gen2:
    generate_clicked = st.button("✨ Generate Collage", use_container_width=True)

# ─── Collage Generation Logic ─────────────────────────────────────────────────
if generate_clicked:
    min_required = MIN_IMAGES.get(layout_style, 3)
    if not uploaded_files or len(uploaded_files) < min_required:
        st.warning(f"⚠️ Please upload at least **{min_required} images** for the **{layout_style}** layout.")
    elif len(uploaded_files) > 10:
        st.warning("⚠️ Please upload a maximum of **10 images**.")
    else:
        with st.spinner("🎨 Crafting your collage with golden ratio proportions…"):
            try:
                buf, preview = build_collage(
                    uploaded_files, layout_style, quality_key, border_width, export_quality
                )
                st.session_state.collage_buf = buf.read()
                st.session_state.preview_img = preview
                st.session_state.show_success = True
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error generating collage: {e}")

# ─── Preview Section ──────────────────────────────────────────────────────────
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Header row with title and download button
col_prev_title, col_prev_btn1, col_prev_btn2 = st.columns([3, 1.2, 1.2])
with col_prev_title:
    st.markdown('<div style="font-size:1.1rem; font-weight:600; color:#222235; padding-top:10px;">🖼️ Collage Preview</div>', unsafe_allow_html=True)

with col_prev_btn1:
    if st.session_state.collage_buf:
        if st.button("🔄 Regenerate", use_container_width=True):
            st.session_state.collage_buf = None
            st.session_state.preview_img = None
            st.session_state.show_success = False
            st.rerun()

with col_prev_btn2:
    if st.session_state.collage_buf:
        st.download_button(
            label="⬇️ Download PNG",
            data=st.session_state.collage_buf,
            file_name="frameflow_collage.png",
            mime="image/png",
            use_container_width=True,
        )

# Preview canvas
st.markdown('<div style="margin-top:14px;">', unsafe_allow_html=True)
if st.session_state.preview_img:
    st.image(st.session_state.preview_img, use_container_width=True, caption="")
else:
    st.markdown("""
    <div class="ff-preview-empty">
      <div class="icon">🖼️</div>
      <p>Add 3 or more images</p>
      <small>Your FrameFlow collage will appear here</small>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-footer">
  <a href="#">FrameFlow</a> &bull; Using φ (1.618) proportions for naturally balanced compositions
</div>
""", unsafe_allow_html=True)
