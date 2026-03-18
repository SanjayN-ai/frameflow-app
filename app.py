import streamlit as st
from PIL import Image, ImageDraw
import io
import math

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FrameFlow – Your Memories, Better Designed",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    color: #F8FAFC !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding-top: 0 !important;
    max-width: 860px !important;
    margin: 0 auto !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"],
.stDeployButton { display: none !important; visibility: hidden !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

/* ── Header ── */
.ff-header {
    text-align: center;
    padding: 48px 0 32px;
}
.ff-logo {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    background: linear-gradient(135deg, #818CF8, #6366F1, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 10px;
}
.ff-tagline {
    font-size: 1.35rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 8px;
}
.ff-desc {
    font-size: 0.9rem;
    color: #94A3B8;
    font-weight: 400;
}

/* ── Cards ── */
.ff-card {
    background: #1E293B;
    border-radius: 16px;
    padding: 28px 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 16px;
    border: 1px solid #334155;
    transition: box-shadow 0.2s;
}
.ff-card:hover {
    box-shadow: 0 8px 32px rgba(99,102,241,0.12);
}

/* ── Upload Zone ── */
.ff-upload-label {
    font-size: 1.15rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 6px;
}
.ff-upload-sub {
    font-size: 0.82rem;
    color: #64748B;
    margin-bottom: 18px;
}

[data-testid="stFileUploader"] {
    background: #0F172A !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    transition: border-color 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366F1 !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploader"] > div {
    color: #94A3B8 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #94A3B8 !important;
}

/* ── Settings Labels ── */
.ff-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #64748B;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.ff-badge {
    display: inline-block;
    background: linear-gradient(135deg, #10B981, #059669);
    color: white;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 6px;
    text-transform: uppercase;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #0F172A !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    font-size: 0.875rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
[data-testid="stSelectbox"] svg { fill: #64748B !important; }

/* ── Slider ── */
[data-testid="stSlider"] > div { padding: 0 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #6366F1 !important;
    border-color: #6366F1 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
    color: #F8FAFC !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
    background: linear-gradient(135deg, #6366F1, #4F46E5) !important;
    color: #F8FAFC !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
}

/* Regenerate button (secondary) */
.regen-btn .stButton > button {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    box-shadow: none !important;
    color: #94A3B8 !important;
}
.regen-btn .stButton > button:hover {
    border-color: #6366F1 !important;
    color: #F8FAFC !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Banners ── */
.ff-banner-success {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    font-size: 0.84rem;
    color: #34D399;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Preview Section ── */
.ff-preview-empty {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    border: 1px dashed #334155;
    border-radius: 14px;
    padding: 70px 20px;
    text-align: center;
    color: #475569;
}
.ff-preview-empty .icon { font-size: 2.8rem; margin-bottom: 12px; opacity: 0.5; }
.ff-preview-empty p { font-size: 0.95rem; font-weight: 500; color: #64748B; }

/* ── Images ── */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

/* ── Section divider ── */
.ff-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #334155, transparent);
    margin: 8px 0 20px;
}

/* ── Footer ── */
.ff-footer {
    text-align: center;
    padding: 24px 0 20px;
    font-size: 0.76rem;
    color: #475569;
    border-top: 1px solid #1E293B;
    margin-top: 16px;
}
.ff-footer span { color: #6366F1; font-weight: 600; }

/* ── Column spacing ── */
[data-testid="column"] { padding: 0 6px !important; }

/* ── Info chip ── */
.ff-info-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    color: #818CF8;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ─── Constants ────────────────────────────────────────────────────────────────
PHI = 1.618033988749895

QUALITY_OPTIONS = {
    "HD (1280 × 792px)": (1280, 792),
    "Full HD (1920 × 1188px)": (1920, 1188),
    "2K (2560 × 1582px)": (2560, 1582),
    "4K (3840 × 2376px)": (3840, 2376),
}

LAYOUT_OPTIONS = [
    "Classic Split",
    "Mosaic",
    "Grid",
    "Triptych",
    "Feature Hero",
]

EXPORT_OPTIONS = {
    "Standard (1x)": 85,
    "Better Quality (2x)": 95,
    "Maximum Quality (3x)": 100,
}

MIN_IMAGES = {
    "Classic Split": 3,
    "Mosaic": 3,
    "Grid": 4,
    "Triptych": 3,
    "Feature Hero": 4,
}

# ─── Image Processing ─────────────────────────────────────────────────────────
def fit_image(img, w, h):
    img = img.convert("RGBA")
    src_r = img.width / img.height
    tgt_r = w / h
    if src_r > tgt_r:
        new_w = int(img.height * tgt_r)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        new_h = int(img.width / tgt_r)
        top = (img.height - new_h) // 2
        img = img.crop((0, top, img.width, top + new_h))
    return img.resize((w, h), Image.LANCZOS)

def make_canvas(W, H):
    return Image.new("RGBA", (W, H), (15, 23, 42, 255))  # #0F172A

def generate_classic(images, W, H, b):
    canvas = make_canvas(W, H)
    main_w = int(W / PHI)
    side_w = W - main_w
    sub_h = int(H / PHI)
    imgs = [images[i % len(images)] for i in range(3)]
    canvas.paste(fit_image(imgs[0], main_w - b * 2, H - b * 2), (b, b))
    canvas.paste(fit_image(imgs[1], side_w - b * 2, sub_h - b * 2), (main_w + b, b))
    canvas.paste(fit_image(imgs[2], side_w - b * 2, H - sub_h - b * 2), (main_w + b, sub_h + b))
    return canvas.convert("RGB")

def generate_mosaic(images, W, H, b):
    canvas = make_canvas(W, H)
    n = min(len(images), 6)
    row1_h = int(H * (1 / PHI))
    row2_h = H - row1_h
    if n <= 3:
        col_w = (W - b * (n + 1)) // n
        for i in range(n):
            x = b + i * (col_w + b)
            canvas.paste(fit_image(images[i], col_w, H - b * 2), (x, b))
    else:
        top_n = min(n, 3)
        col_w_top = (W - b * (top_n + 1)) // top_n
        for i in range(top_n):
            x = b + i * (col_w_top + b)
            canvas.paste(fit_image(images[i], col_w_top, row1_h - b), (x, b))
        bot_imgs = images[top_n:n]
        bot_n = len(bot_imgs)
        if bot_n:
            col_w_bot = (W - b * (bot_n + 1)) // bot_n
            for i, img in enumerate(bot_imgs):
                x = b + i * (col_w_bot + b)
                canvas.paste(fit_image(img, col_w_bot, row2_h - b), (x, row1_h + b))
    return canvas.convert("RGB")

def generate_grid(images, W, H, b):
    n = min(len(images), 9)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    cell_w = (W - b * (cols + 1)) // cols
    cell_h = (H - b * (rows + 1)) // rows
    canvas = make_canvas(W, H)
    for idx in range(n):
        row = idx // cols
        col = idx % cols
        canvas.paste(fit_image(images[idx], cell_w, cell_h),
                     (b + col * (cell_w + b), b + row * (cell_h + b)))
    return canvas.convert("RGB")

def generate_triptych(images, W, H, b):
    panel_w = (W - b * 4) // 3
    canvas = make_canvas(W, H)
    imgs = [images[i % len(images)] for i in range(3)]
    for i, img in enumerate(imgs):
        canvas.paste(fit_image(img, panel_w, H - b * 2), (b + i * (panel_w + b), b))
    return canvas.convert("RGB")

def generate_feature(images, W, H, b):
    hero_w = int(W * 0.58)
    strip_w = W - hero_w - b * 3
    canvas = make_canvas(W, H)
    imgs = [images[i % len(images)] for i in range(4)]
    canvas.paste(fit_image(imgs[0], hero_w - b, H - b * 2), (b, b))
    strip_h = (H - b * 4) // 3
    for i in range(3):
        canvas.paste(fit_image(imgs[i + 1], strip_w, strip_h),
                     (hero_w + b * 2, b + i * (strip_h + b)))
    return canvas.convert("RGB")

GENERATORS = {
    "Classic Split": generate_classic,
    "Mosaic": generate_mosaic,
    "Grid": generate_grid,
    "Triptych": generate_triptych,
    "Feature Hero": generate_feature,
}

def build_collage(files, layout, quality_key, border_px):
    imgs = [Image.open(f) for f in files]
    W, H = QUALITY_OPTIONS[quality_key]
    collage = GENERATORS[layout](imgs, W, H, border_px)
    buf = io.BytesIO()
    collage.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    preview = collage.copy()
    if preview.width > 860:
        ratio = 860 / preview.width
        preview = preview.resize((860, int(preview.height * ratio)), Image.LANCZOS)
    return buf, preview

# ─── Session State ────────────────────────────────────────────────────────────
for key in ["collage_buf", "preview_img", "show_success"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "show_success" else False

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-header">
  <div class="ff-logo">FRAMEFLOW</div>
  <div class="ff-tagline">Your Memories, Better Designed</div>
  <div class="ff-desc">No design skills needed — we handle the layout for you.</div>
</div>
""", unsafe_allow_html=True)

# ─── Success Banner ───────────────────────────────────────────────────────────
if st.session_state.show_success:
    st.markdown("""
    <div class="ff-banner-success">
      ✅ &nbsp;Collage generated successfully! Click <strong>'Download'</strong> to save.
    </div>
    """, unsafe_allow_html=True)

# ─── Upload Section ───────────────────────────────────────────────────────────
st.markdown('<div class="ff-card">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding-bottom:16px;">
  <div style="font-size:2.4rem; margin-bottom:10px;">📸</div>
  <div class="ff-upload-label">Drop your photos here</div>
  <div class="ff-upload-sub">Upload 3–10 images to get started</div>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload Photos",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Settings Panel ───────────────────────────────────────────────────────────
st.markdown('<div class="ff-card">', unsafe_allow_html=True)
st.markdown('<div style="font-size:0.95rem; font-weight:600; color:#F8FAFC; margin-bottom:18px;">⚙️ Settings</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ff-label">Output Quality</div>', unsafe_allow_html=True)
    quality_key = st.selectbox("Quality", list(QUALITY_OPTIONS.keys()),
                               index=2, label_visibility="collapsed")
    if "2K" in quality_key:
        st.markdown('<span class="ff-badge">Recommended</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ff-label">Layout Style</div>', unsafe_allow_html=True)
    layout_style = st.selectbox("Layout", LAYOUT_OPTIONS,
                                index=0, label_visibility="collapsed")

with col3:
    st.markdown('<div class="ff-label">Border Width</div>', unsafe_allow_html=True)
    border_width = st.slider("Border", 0, 40, 10, 2,
                             format="%dpx", label_visibility="collapsed")
    st.markdown(f'<div style="font-size:0.78rem; color:#64748B; margin-top:4px;">{border_width}px gap</div>',
                unsafe_allow_html=True)

# ─── Layout info row ──────────────────────────────────────────────────────────
st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
col4, col5 = st.columns([1, 1])
with col4:
    st.markdown('<div class="ff-label">Export Quality</div>', unsafe_allow_html=True)
    export_quality = st.selectbox("Export", list(EXPORT_OPTIONS.keys()),
                                  index=1, label_visibility="collapsed")
with col5:
    n_up = len(uploaded_files) if uploaded_files else 0
    min_req = MIN_IMAGES.get(layout_style, 3)
    if n_up < min_req:
        status_html = f'<div style="font-size:0.83rem; color:#64748B; padding-top:26px;">📂 Add {min_req - n_up} more photo{"s" if min_req-n_up>1 else ""} for <em>{layout_style}</em></div>'
    else:
        status_html = f'<div style="font-size:0.83rem; color:#34D399; padding-top:26px;">✓ {n_up} photo{"s" if n_up>1 else ""} ready</div>'
    st.markdown(status_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Generate Button ──────────────────────────────────────────────────────────
_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    generate_clicked = st.button("✨ Create My Collage", use_container_width=True)

# ─── Generate Logic ───────────────────────────────────────────────────────────
if generate_clicked:
    min_req = MIN_IMAGES.get(layout_style, 3)
    if not uploaded_files or len(uploaded_files) < min_req:
        st.warning(f"Please upload at least **{min_req} photos** for the **{layout_style}** layout.")
    elif len(uploaded_files) > 10:
        st.warning("Please upload a maximum of **10 photos**.")
    else:
        with st.spinner("Creating your collage…"):
            try:
                buf, preview = build_collage(uploaded_files, layout_style, quality_key, border_width)
                st.session_state.collage_buf = buf.read()
                st.session_state.preview_img = preview
                st.session_state.show_success = True
                st.rerun()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ─── Preview Section ──────────────────────────────────────────────────────────
st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
st.markdown('<div class="ff-card">', unsafe_allow_html=True)

col_t, col_r1, col_r2 = st.columns([3, 1.1, 1.1])
with col_t:
    st.markdown('<div style="font-size:0.95rem; font-weight:600; color:#F8FAFC; padding-top:8px;">🖼️ Collage Preview</div>',
                unsafe_allow_html=True)
with col_r1:
    if st.session_state.collage_buf:
        st.markdown('<div class="regen-btn">', unsafe_allow_html=True)
        if st.button("🔄 Redo", use_container_width=True):
            st.session_state.collage_buf = None
            st.session_state.preview_img = None
            st.session_state.show_success = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
with col_r2:
    if st.session_state.collage_buf:
        st.download_button(
            label="⬇️ Download",
            data=st.session_state.collage_buf,
            file_name="frameflow_collage.png",
            mime="image/png",
            use_container_width=True,
        )

st.markdown('<div class="ff-divider"></div>', unsafe_allow_html=True)

if st.session_state.preview_img:
    st.image(st.session_state.preview_img, use_container_width=True)
else:
    st.markdown("""
    <div class="ff-preview-empty">
      <div class="icon">✨</div>
      <p>Your collage will appear here ✨</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-footer">
  Made with ❤️ by <span>FrameFlow</span> &bull; Beautiful collages in seconds
</div>
""", unsafe_allow_html=True)
