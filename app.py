import streamlit as st
from PIL import Image
import io
import math
import base64

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FrameFlow – Your Memories, Better Designed",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
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
    max-width: 880px !important;
    margin: 0 auto !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
    padding-bottom: 40px !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"],
.stDeployButton { display: none !important; visibility: hidden !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

/* ── Header ── */
.ff-header {
    text-align: center;
    padding: 44px 0 28px;
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
.ff-tagline { font-size: 1.3rem; font-weight: 600; color: #F8FAFC; margin-bottom: 6px; }
.ff-desc    { font-size: 0.875rem; color: #94A3B8; }

/* ── Card (via native container) ── */
.ff-card {
    background: #1E293B;
    border-radius: 16px;
    padding: 24px 22px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 14px;
    border: 1px solid #334155;
    transition: box-shadow 0.2s;
}
.ff-card:hover { box-shadow: 0 8px 32px rgba(99,102,241,0.1); }

/* ── Hide empty markdown wrappers (orphan div tags) ── */
[data-testid="stMarkdownContainer"]:has(> div:empty),
.stMarkdown:empty {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* ── Style native st.container blocks as cards ── */
.section-card > div[data-testid="stVerticalBlock"] {
    background: #1E293B;
    border-radius: 16px;
    padding: 24px 22px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin-bottom: 14px;
    border: 1px solid #334155;
}

/* ── Status Bar ── */
.ff-status {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 13px 18px;
    font-size: 0.875rem;
    font-weight: 500;
    color: #94A3B8;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.3s;
}
.ff-status.ready  { border-color: rgba(99,102,241,0.4); color: #818CF8; background: rgba(99,102,241,0.08); }
.ff-status.success{ border-color: rgba(16,185,129,0.4); color: #34D399;  background: rgba(16,185,129,0.08); }

/* ── Upload Zone ── */
[data-testid="stFileUploader"] {
    background: #0F172A !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px !important;
    transition: border-color 0.25s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #6366F1 !important; }
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: #64748B !important; }

/* ── Thumbnail Grid ── */
.thumb-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 16px 0 10px;
}
.thumb-item {
    position: relative;
    width: 92px;
    flex-shrink: 0;
}
.thumb-item img {
    width: 92px;
    height: 72px;
    object-fit: cover;
    border-radius: 10px;
    border: 1.5px solid #334155;
    display: block;
    transition: transform 0.2s, box-shadow 0.2s;
}
.thumb-item:hover img {
    transform: scale(1.04);
    box-shadow: 0 6px 20px rgba(99,102,241,0.3);
    border-color: #6366F1;
}
.thumb-num {
    position: absolute;
    bottom: 4px;
    left: 5px;
    background: rgba(15,23,42,0.75);
    color: #F8FAFC;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 5px;
    pointer-events: none;
}
.thumb-count {
    font-size: 0.8rem;
    color: #64748B;
    margin-top: 4px;
    font-weight: 500;
}

/* ── Settings Labels ── */
.ff-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #64748B;
    text-transform: uppercase;
    margin-bottom: 7px;
}
.ff-badge {
    display: inline-block;
    background: linear-gradient(135deg, #10B981, #059669);
    color: white;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 2px 8px;
    border-radius: 20px;
    margin-top: 5px;
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
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
}

/* Remove / secondary buttons (target secondary type) */
[data-testid="baseButton-secondary"] {
    background: #0F172A !important;
    border: 1px solid #334155 !important;
    box-shadow: none !important;
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
}
[data-testid="baseButton-secondary"]:hover {
    border-color: #EF4444 !important;
    color: #EF4444 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Redo button specifically */
.btn-regen [data-testid="baseButton-secondary"]:hover {
    border-color: #6366F1 !important;
    color: #818CF8 !important;
}

/* ── Preview empty ── */
.ff-preview-empty {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    border: 1px dashed #334155;
    border-radius: 14px;
    padding: 70px 20px;
    text-align: center;
}
.ff-preview-empty .icon { font-size: 2.8rem; margin-bottom: 10px; opacity: 0.4; }
.ff-preview-empty p { font-size: 0.9rem; font-weight: 500; color: #475569; }

/* ── Images ── */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
}

/* ── Divider ── */
.ff-divider { height: 1px; background: linear-gradient(90deg,transparent,#334155,transparent); margin: 10px 0 18px; }

/* ── Column spacing ── */
[data-testid="column"] { padding: 0 5px !important; }

/* ── Footer ── */
.ff-footer {
    text-align: center;
    padding: 22px 0 16px;
    font-size: 0.76rem;
    color: #475569;
    border-top: 1px solid #1E293B;
    margin-top: 16px;
}
.ff-footer span { color: #6366F1; font-weight: 600; }

/* ── Section title ── */
.ff-section-title {
    font-size: 0.93rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-bottom: 14px;
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

LAYOUT_OPTIONS = ["Classic Split", "Mosaic", "Grid", "Triptych", "Feature Hero"]

EXPORT_OPTIONS = {"Standard (1x)": 85, "Better Quality (2x)": 95, "Maximum Quality (3x)": 100}

MIN_IMAGES = {"Classic Split": 3, "Mosaic": 3, "Grid": 4, "Triptych": 3, "Feature Hero": 4}

# ─── Session State ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stored_images": [],   # list of {name, bytes, b64_thumb}
        "collage_buf": None,
        "preview_img": None,
        "show_success": False,
        "generating": False,
        "uploader_key": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def make_thumb_b64(img_bytes: bytes, size=(184, 144)) -> str:
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    w, h = img.size
    ratio = min(size[0]/w, size[1]/h)
    img = img.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()

def fit_image(img, w, h):
    img = img.convert("RGBA")
    sr = img.width / img.height
    tr = w / h
    if sr > tr:
        nw = int(img.height * tr)
        l = (img.width - nw) // 2
        img = img.crop((l, 0, l+nw, img.height))
    else:
        nh = int(img.width / tr)
        t = (img.height - nh) // 2
        img = img.crop((0, t, img.width, t+nh))
    return img.resize((w, h), Image.LANCZOS)

def make_canvas(W, H):
    return Image.new("RGBA", (W, H), (15, 23, 42, 255))

def generate_classic(images, W, H, b):
    c = make_canvas(W, H)
    mw = int(W/PHI); sw = W-mw; sh = int(H/PHI)
    imgs = [images[i%len(images)] for i in range(3)]
    c.paste(fit_image(imgs[0], mw-b*2, H-b*2), (b, b))
    c.paste(fit_image(imgs[1], sw-b*2, sh-b*2), (mw+b, b))
    c.paste(fit_image(imgs[2], sw-b*2, H-sh-b*2), (mw+b, sh+b))
    return c.convert("RGB")

def generate_mosaic(images, W, H, b):
    c = make_canvas(W, H); n = min(len(images), 6)
    r1h = int(H*(1/PHI)); r2h = H-r1h
    if n <= 3:
        cw = (W-b*(n+1))//n
        for i in range(n): c.paste(fit_image(images[i], cw, H-b*2), (b+i*(cw+b), b))
    else:
        top_n = min(n, 3); cw = (W-b*(top_n+1))//top_n
        for i in range(top_n): c.paste(fit_image(images[i], cw, r1h-b), (b+i*(cw+b), b))
        bi = images[top_n:n]; bn = len(bi)
        if bn:
            bw = (W-b*(bn+1))//bn
            for i, img in enumerate(bi): c.paste(fit_image(img, bw, r2h-b), (b+i*(bw+b), r1h+b))
    return c.convert("RGB")

def generate_grid(images, W, H, b):
    n = min(len(images), 9); cols = math.ceil(math.sqrt(n)); rows = math.ceil(n/cols)
    cw = (W-b*(cols+1))//cols; ch = (H-b*(rows+1))//rows
    c = make_canvas(W, H)
    for idx in range(n):
        row=idx//cols; col=idx%cols
        c.paste(fit_image(images[idx], cw, ch), (b+col*(cw+b), b+row*(ch+b)))
    return c.convert("RGB")

def generate_triptych(images, W, H, b):
    pw = (W-b*4)//3; c = make_canvas(W, H)
    imgs = [images[i%len(images)] for i in range(3)]
    for i, img in enumerate(imgs): c.paste(fit_image(img, pw, H-b*2), (b+i*(pw+b), b))
    return c.convert("RGB")

def generate_feature(images, W, H, b):
    hw = int(W*0.58); sw = W-hw-b*3; c = make_canvas(W, H)
    imgs = [images[i%len(images)] for i in range(4)]
    c.paste(fit_image(imgs[0], hw-b, H-b*2), (b, b))
    sh = (H-b*4)//3
    for i in range(3): c.paste(fit_image(imgs[i+1], sw, sh), (hw+b*2, b+i*(sh+b)))
    return c.convert("RGB")

GENERATORS = {
    "Classic Split": generate_classic, "Mosaic": generate_mosaic,
    "Grid": generate_grid, "Triptych": generate_triptych, "Feature Hero": generate_feature,
}

def build_collage(stored, layout, quality_key, border_px):
    imgs = [Image.open(io.BytesIO(s["bytes"])) for s in stored]
    W, H = QUALITY_OPTIONS[quality_key]
    collage = GENERATORS[layout](imgs, W, H, border_px)
    buf = io.BytesIO()
    collage.save(buf, format="PNG", optimize=True)
    buf.seek(0)
    preview = collage.copy()
    if preview.width > 860:
        r = 860/preview.width
        preview = preview.resize((860, int(preview.height*r)), Image.LANCZOS)
    return buf, preview

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-header">
  <div class="ff-logo">FRAMEFLOW</div>
  <div class="ff-tagline">Your Memories, Better Designed</div>
  <div class="ff-desc">No design skills needed — we handle the layout for you.</div>
</div>
""", unsafe_allow_html=True)

# ─── Dynamic Status Bar ───────────────────────────────────────────────────────
n_stored = len(st.session_state.stored_images)
min_req = MIN_IMAGES.get(
    st.session_state.get("layout_style_val", "Classic Split"), 3
)

if st.session_state.show_success:
    status_cls, status_icon, status_msg = "success", "✅", "Collage generated! Click <strong>'Download'</strong> to save."
elif n_stored == 0:
    status_cls, status_icon, status_msg = "", "💡", "Upload images to get started"
elif n_stored < min_req:
    status_cls, status_icon, status_msg = "", "📸", f"{n_stored} image{'s' if n_stored>1 else ''} selected — add {min_req-n_stored} more"
else:
    status_cls, status_icon, status_msg = "ready", "📸", f"{n_stored} of 10 images selected — ready to generate"

st.markdown(f"""
<div class="ff-status {status_cls}">
  <span style="font-size:1.1rem">{status_icon}</span>
  <span>{status_msg}</span>
</div>
""", unsafe_allow_html=True)

# ─── Upload Section ───────────────────────────────────────────────────────────
with st.container():
    st.markdown("""
    <div class="ff-card">
      <div class="ff-section-title">📂 Upload Photos</div>
      <div style="text-align:center;padding:6px 0 14px;">
        <div style="font-size:2rem;margin-bottom:6px;">📸</div>
        <div style="font-size:1rem;font-weight:600;color:#F8FAFC;margin-bottom:4px;">Drop your photos here</div>
        <div style="font-size:0.8rem;color:#64748B;">Upload 3–10 images • JPG, PNG, WebP supported</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    new_files = st.file_uploader(
        "Upload Photos",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"file_uploader_{st.session_state.uploader_key}",
    )

    # Merge new uploads into stored_images (avoid duplicates by name)
    if new_files:
        existing_names = {s["name"] for s in st.session_state.stored_images}
        added = 0
        for f in new_files:
            if f.name not in existing_names and len(st.session_state.stored_images) < 10:
                raw = f.read()
                st.session_state.stored_images.append({
                    "name": f.name,
                    "bytes": raw,
                    "b64_thumb": make_thumb_b64(raw),
                })
                existing_names.add(f.name)
                added += 1
        if added:
            st.session_state.show_success = False
            st.session_state.collage_buf = None
            st.session_state.preview_img = None
            st.rerun()

    # ── Thumbnail Grid ────────────────────────────────────────────────
    if st.session_state.stored_images:
        thumbs_html = f'<div class="thumb-count">{len(st.session_state.stored_images)} of 10 images selected</div><div class="thumb-grid">'
        for i, item in enumerate(st.session_state.stored_images):
            thumbs_html += f'<div class="thumb-item"><img src="data:image/jpeg;base64,{item["b64_thumb"]}" title="{item["name"]}"/><span class="thumb-num">{i+1}</span></div>'
        thumbs_html += "</div>"
        st.markdown(thumbs_html, unsafe_allow_html=True)

        # Callbacks for reliable state updates
        def remove_img(idx):
            st.session_state.stored_images.pop(idx)
            st.session_state.show_success = False
            st.session_state.collage_buf = None
            st.session_state.preview_img = None
            st.session_state.uploader_key += 1
        
        def clear_all():
            st.session_state.stored_images = []
            st.session_state.show_success = False
            st.session_state.collage_buf = None
            st.session_state.preview_img = None
            st.session_state.uploader_key += 1

        # Remove buttons (one per image)
        n = len(st.session_state.stored_images)
        rm_cols = st.columns(min(n, 5))
        for i in range(min(n, 5)):
            with rm_cols[i]:
                st.button(f"✕ #{i+1}", key=f"rm_{i}", on_click=remove_img, args=(i,), type="secondary", use_container_width=True)
                
        if n > 5:
            rm_cols2 = st.columns(n - 5)
            for j in range(n - 5):
                i = 5 + j
                with rm_cols2[j]:
                    st.button(f"✕ #{i+1}", key=f"rm_{i}", on_click=remove_img, args=(i,), type="secondary", use_container_width=True)

        # Clear all
        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
        _, col_clear, _ = st.columns([3, 1, 3])
        with col_clear:
            st.button("🗑 Clear All", on_click=clear_all, type="secondary", use_container_width=True)

# ─── Settings Panel ───────────────────────────────────────────────────────────
st.markdown('<div class="ff-card"><div class="ff-section-title">⚙️ Settings</div></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="ff-label">Output Quality</div>', unsafe_allow_html=True)
    quality_key = st.selectbox("Quality", list(QUALITY_OPTIONS.keys()), index=2, label_visibility="collapsed")
    if "2K" in quality_key:
        st.markdown('<span class="ff-badge">Recommended</span>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ff-label">Layout Style</div>', unsafe_allow_html=True)
    layout_style = st.selectbox("Layout", LAYOUT_OPTIONS, index=0, label_visibility="collapsed")
    st.session_state["layout_style_val"] = layout_style

with col3:
    st.markdown('<div class="ff-label">Border Width</div>', unsafe_allow_html=True)
    border_width = st.slider("Border", 0, 40, 10, 2, format="%dpx", label_visibility="collapsed")
    st.markdown(f'<div style="font-size:0.75rem;color:#64748B;margin-top:3px;">{border_width}px gap</div>', unsafe_allow_html=True)

# ─── Generate Button ──────────────────────────────────────────────────────────
_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    generate_clicked = st.button("✨ Create My Collage", use_container_width=True)

# ─── Generate Logic ───────────────────────────────────────────────────────────
if generate_clicked:
    stored = st.session_state.stored_images
    min_req = MIN_IMAGES.get(layout_style, 3)
    if not stored or len(stored) < min_req:
        st.warning(f"Please upload at least **{min_req} photos** for the **{layout_style}** layout.")
    elif len(stored) > 10:
        st.warning("Please use a maximum of **10 photos**.")
    else:
        with st.spinner("✨ Generating your collage…"):
            try:
                buf, preview = build_collage(stored, layout_style, quality_key, border_width)
                st.session_state.collage_buf = buf.read()
                st.session_state.preview_img = preview
                st.session_state.show_success = True
                st.rerun()
            except Exception as e:
                st.error(f"Something went wrong: {e}")

# ─── Preview Section ──────────────────────────────────────────────────────────
st.markdown('<div class="ff-card"><div class="ff-section-title" style="margin-bottom:4px;">🖼️ Collage Preview</div></div>', unsafe_allow_html=True)

col_t, col_r1, col_r2 = st.columns([3, 1, 1])
with col_t:
    st.write("")
with col_r1:
    if st.session_state.collage_buf:
        st.markdown('<div class="btn-regen">', unsafe_allow_html=True)
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

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ff-footer">
  Made with ❤️ by <span>FrameFlow</span> &bull; Beautiful collages in seconds
</div>
""", unsafe_allow_html=True)
