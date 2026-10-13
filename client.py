import gradio as gr
import requests
import os
import io
import json
from PIL import Image, ImageOps

SERVER_URL = "http://127.0.0.1:8000/predict"

# THEME

# Salmon accent palette (light to dark)
salmon = gr.themes.Color(
    name="salmon",
    c50="#FFF5F2", c100="#FFE8E2", c200="#FFD3C8", c300="#FFB5A7",
    c400="#FF9C8A", c500="#F28B79", c600="#E07462", c700="#C35E4D",
    c800="#9E4A3D", c900="#7A3A30", c950="#4A231D",
)

# Warm cocoa neutrals
cocoa = gr.themes.Color(
    name="cocoa",
    c50="#FFFBF9", c100="#FBF1EE", c200="#F2E1DC", c300="#E3CBC4",
    c400="#C9A9A0", c500="#A6857C", c600="#82655E", c700="#5E4843",
    c800="#3F302C", c900="#2E2321", c950="#211917",
)

custom_theme = gr.themes.Soft(
    primary_hue=salmon,
    secondary_hue=salmon,
    neutral_hue=cocoa,
    font=["Times New Roman", "serif"],
    radius_size=gr.themes.sizes.radius_lg,
).set(
    # Page background and text
    body_background_fill="#FFF5F2",
    body_background_fill_dark="#1F1715",
    body_text_color="#3B2A26",
    body_text_color_dark="#FBEDE8",
    body_text_color_subdued="#8A6A62",
    body_text_color_subdued_dark="#C9A9A0",

    # Surfaces
    background_fill_primary="#FFFFFF",
    background_fill_primary_dark="#2A201E",
    background_fill_secondary="#FFF9F7",
    background_fill_secondary_dark="#241B19",
    panel_background_fill="#FFFFFF",
    panel_background_fill_dark="#2A201E",

    # Blocks (image box, textboxes)
    block_background_fill="#FFFFFF",
    block_background_fill_dark="#2A201E",
    block_border_color="#FFD3C8",
    block_border_color_dark="#4A3530",
    block_label_background_fill="#FFE8E2",
    block_label_background_fill_dark="#4A3029",
    block_label_text_color="#C35E4D",
    block_label_text_color_dark="#FFF1EA",
    block_title_text_color="#C35E4D",
    block_title_text_color_dark="#FFF1EA",
    block_shadow="0 4px 18px rgba(242, 139, 121, 0.10)",
    block_shadow_dark="0 4px 18px rgba(0, 0, 0, 0.35)",

    # Inputs
    input_background_fill="#FFFBF9",
    input_background_fill_dark="#332724",
    input_border_color="#FFD3C8",
    input_border_color_dark="#5A413B",
    input_border_color_focus="#F28B79",
    input_border_color_focus_dark="#FFB5A7",

    # Borders and accent
    border_color_primary="#FFD3C8",
    border_color_primary_dark="#4A3530",
    border_color_accent="#F28B79",
    border_color_accent_dark="#FFB5A7",
    color_accent="#F28B79",
    color_accent_soft="#FFE8E2",
    color_accent_soft_dark="#3D2A26",

    # Links
    link_text_color="#E07462",
    link_text_color_dark="#FFB5A7",
    link_text_color_hover="#C35E4D",
    link_text_color_hover_dark="#FFD3C8",
    link_text_color_visited="#E07462",
    link_text_color_visited_dark="#FFB5A7",

    # Primary buttons
    button_primary_background_fill="#FFB5A7",
    button_primary_background_fill_dark="#FFB5A7",
    button_primary_background_fill_hover="#FF9C8A",
    button_primary_background_fill_hover_dark="#FFC4B8",
    button_primary_border_color="#FFB5A7",
    button_primary_border_color_dark="#FFB5A7",
    button_primary_text_color="#3B2A26",
    button_primary_text_color_dark="#2A1A16",

    # Secondary buttons
    button_secondary_background_fill="#FFFFFF",
    button_secondary_background_fill_dark="#2A201E",
    button_secondary_background_fill_hover="#FFF0EC",
    button_secondary_background_fill_hover_dark="#3D2A26",
    button_secondary_border_color="#FFB5A7",
    button_secondary_border_color_dark="#FFB5A7",
    button_secondary_text_color="#C35E4D",
    button_secondary_text_color_dark="#FFB5A7",

    # Loading spinner
    loader_color="#F28B79",
    loader_color_dark="#FFB5A7",
)


css = """
/* ---------- Webcam mirror fix ---------- */
#webcam-image video {
    transform: none !important;
}
#webcam-image img {
    transform: scaleX(-1) !important;
}

/* ---------- Page width ---------- */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* ---------- Header banner ---------- */
#hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    padding: 24px 28px;
    border-radius: 20px;
    background: linear-gradient(135deg, #FFE3DB 0%, #FFCFC3 55%, #FFB5A7 100%);
    color: #3B2A26;
    box-shadow: 0 6px 24px rgba(242, 139, 121, 0.22);
}
.dark #hero {
    background: linear-gradient(135deg, #3A2622 0%, #4E2F28 55%, #6A3B31 100%);
    color: #FFE8E2;
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.45);
}
#hero .hero-left {
    display: flex;
    align-items: center;
    gap: 16px;
}
#hero .hero-icon {
    width: 60px;
    height: 60px;
    display: grid;
    place-items: center;
    font-size: 32px;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.6);
}
.dark #hero .hero-icon {
    background: rgba(255, 181, 167, 0.15);
}
#hero h1 {
    margin: 0;
    font-size: 28px;
    line-height: 1.2;
    color: inherit;
}
#hero p {
    margin: 6px 0 0;
    font-size: 15px;
    opacity: 0.8;
    color: inherit;
}
#hero .hero-pill {
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    background: rgba(255, 255, 255, 0.7);
    color: #9E4A3D;
    white-space: nowrap;
}
.dark #hero .hero-pill {
    background: rgba(255, 181, 167, 0.15);
    color: #FFD3C8;
}

/* ---------- Card panels ---------- */
.card {
    background: var(--background-fill-primary) !important;
    border: 1px solid var(--border-color-primary) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: var(--block-shadow) !important;
}

#input-card,
#results-card {
    display: flex !important;
    flex-direction: column !important;
}
#input-tabs {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}
#input-tabs .tabitem:not([style*="none"]) {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}
#input-tabs .tabitem:not([style*="none"]) > div {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
}
#upload-image,
#webcam-image {
    flex: 1 1 auto !important;
}
#upload-btn,
#webcam-btn,
#clear-btn {
    margin-top: auto !important;
}


.dark [data-testid="block-label"],
.dark [data-testid="block-label"] *,
.dark [data-testid="block-info"] {
    color: #FFF1EA !important;
}

button[role="tab"],
.tab-nav button {
    font-size: 15px !important;
}
button[role="tab"][aria-selected="true"],
.tab-nav button.selected {
    color: #E07462 !important;
    border-bottom-color: #E07462 !important;
    background: transparent !important;
}
button[role="tab"][aria-selected="true"]::after,
.tab-nav button.selected::after {
    background: #E07462 !important;
}
.dark button[role="tab"][aria-selected="true"],
.dark .tab-nav button.selected {
    color: #FFB5A7 !important;
    border-bottom-color: #FFB5A7 !important;
}
.dark button[role="tab"][aria-selected="true"]::after,
.dark .tab-nav button.selected::after {
    background: #FFB5A7 !important;
}

/* ---------- Upload + webcam ---------- */
#upload-image .wrap,
#upload-image .wrap *,
#webcam-image .wrap,
#webcam-image .wrap *,
#webcam-image button,
#webcam-image button * {
    color: #E07462 !important;
}
.dark #upload-image .wrap,
.dark #upload-image .wrap *,
.dark #webcam-image .wrap,
.dark #webcam-image .wrap *,
.dark #webcam-image button,
.dark #webcam-image button * {
    color: #FFB5A7 !important;
}


#webcam-image *:not(svg):not(svg *):not([data-testid="block-label"]):not([data-testid="block-label"] *) {
    color: #E07462 !important;
}
.dark #webcam-image *:not(svg):not(svg *):not([data-testid="block-label"]):not([data-testid="block-label"] *) {
    color: #FFB5A7 !important;
}

#upload-image svg:not([data-testid="block-label"] svg),
#webcam-image svg:not([data-testid="block-label"] svg) {
    color: #E07462 !important;
}
.dark #upload-image svg:not([data-testid="block-label"] svg),
.dark #webcam-image svg:not([data-testid="block-label"] svg) {
    color: #FFB5A7 !important;
}
#upload-image svg:not([data-testid="block-label"] svg)[stroke]:not([stroke="none"]),
#upload-image svg:not([data-testid="block-label"] svg) [stroke]:not([stroke="none"]),
#webcam-image svg:not([data-testid="block-label"] svg)[stroke]:not([stroke="none"]),
#webcam-image svg:not([data-testid="block-label"] svg) [stroke]:not([stroke="none"]) {
    stroke: currentColor !important;
}
#upload-image svg:not([data-testid="block-label"] svg) [fill]:not([fill="none"]),
#webcam-image svg:not([data-testid="block-label"] svg) [fill]:not([fill="none"]) {
    fill: currentColor !important;
}

/* ---------- Buttons ---------- */
button.primary,
#clear-btn {
    font-weight: bold !important;
    font-size: 16px !important;
    border-radius: 14px !important;
    min-height: 48px !important;
}
#clear-btn {
    border-width: 1.5px !important;
}

/* ---------- Result textboxes ---------- */
#llm-output textarea,
#ocr-output textarea {
    font-family: Consolas, "Courier New", monospace !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
}
"""

def process_receipt(image_filepath, is_webcam):
    if not image_filepath:
        return "No image uploaded.", ""

    try:
        # High-performance PIL processing (memory optimization + resize)
        img = Image.open(image_filepath)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if is_webcam:
            img = ImageOps.mirror(img)

        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)

        filename = "webcam_scan.jpg" if is_webcam else os.path.basename(image_filepath)

        files = {"file": (filename, img_bytes, "image/jpeg")}
        response = requests.post(SERVER_URL, files=files)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                llm_output = data.get("llm_extracted_json", data.get("data", ""))
                raw_ocr = data.get("raw_ocr_text", data.get("raw_ocr", ""))

                # Strip markdown blocks if Gemini returns them
                if llm_output.startswith("```json"):
                    llm_output = llm_output.removeprefix("```json").removesuffix("```").strip()
                elif llm_output.startswith("```"):
                    llm_output = llm_output.removeprefix("```").removesuffix("```").strip()

                try:
                    # Convert the string into a Python dictionary
                    parsed_json = json.loads(llm_output)

                    # Create the exact string format requested
                    formatted_text = f"Merchant Name: {parsed_json.get('merchantName', 'Not Found')}\n"
                    formatted_text += f"Date: {parsed_json.get('date', 'Not Found')}\n"
                    formatted_text += f"Total: {parsed_json.get('totalAmount', '0.00')}"

                    llm_output = formatted_text
                except json.JSONDecodeError:
                    # Fallback just in case Gemini returns something weird
                    pass

                return str(raw_ocr), llm_output
            else:
                return "Backend Logic Error", str(data.get("message"))
        else:
            try:
                error_msg = response.json().get("message", "Unknown Server Error")
            except:
                error_msg = response.text
            return f"HTTP Error {response.status_code}", error_msg

    except requests.exceptions.ConnectionError:
        return "CONNECTION ERROR:", "Is your FastAPI server running in another terminal?"
    except Exception as e:
        return "UNKNOWN ERROR:", str(e)


# UI LAYOUT

HERO_HTML = """
<div id="hero">
  <div class="hero-left">
    <div class="hero-icon">🧾</div>
    <div>
      <h1>Automated Receipt Total & Expense Extractor</h1>
      <p>Edge AI client running on Windows 11 communicating with Ubuntu WSL FastAPI.</p>
    </div>
  </div>
  <div class="hero-pill">● Server: 127.0.0.1:8000</div>
</div>
"""

with gr.Blocks(css=css, theme=custom_theme, title="Receipt Extractor") as interface:
    gr.HTML(HERO_HTML)

    with gr.Row(equal_height=True):
        # ---------- LEFT CARD: input ----------
        with gr.Column(scale=1, elem_classes="card", elem_id="input-card"):
            with gr.Tabs(elem_id="input-tabs"):
                with gr.TabItem("Upload Digital Receipt"):
                    upload_input = gr.Image(sources=["upload"], type="filepath", elem_id="upload-image", height=380)
                    upload_btn = gr.Button("Submit Upload", variant="primary", elem_id="upload-btn")

                with gr.TabItem("Scan Physical Receipt"):
                    webcam_input = gr.Image(sources=["webcam"], type="filepath", elem_id="webcam-image", height=380)
                    webcam_btn = gr.Button("Submit Scan", variant="primary", elem_id="webcam-btn")

        # ---------- RIGHT CARD: results ----------
        with gr.Column(scale=1, elem_classes="card", elem_id="results-card"):
            llm_output = gr.Textbox(label="Gemini LLM Structured Data", lines=10, elem_id="llm-output")
            ocr_output = gr.Textbox(label="Raw OCR Text", lines=6, elem_id="ocr-output")
            clear_btn = gr.Button("Clear All", variant="secondary", elem_id="clear-btn")

    # Route buttons to the backend
    upload_btn.click(fn=lambda img: process_receipt(img, is_webcam=False), inputs=upload_input, outputs=[ocr_output, llm_output])
    webcam_btn.click(fn=lambda img: process_receipt(img, is_webcam=True), inputs=webcam_input, outputs=[ocr_output, llm_output])

    clear_btn.click(lambda: (None, None, "", ""), inputs=None, outputs=[upload_input, webcam_input, ocr_output, llm_output])

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)

