LegalMetro-Hackathon: Design

Color Palette (WCAG 2.1 AA Compliant)

┌──────────────┬──────────────────┬─────────┬────────────────────────┐
│    Usage     │      Color       │   Hex   │      When to Use       │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Primary      │ Metrology Blue   │ #1976D2 │ Buttons, active states │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Success      │ Compliance Green │ #388E3C │ PASS indicators        │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Error        │ Alert Amber      │ #F57C00 │ FAIL indicators        │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Background   │ Paper White      │ #FAFAFA │ Main canvas, cards     │
├──────────────┼──────────────────┼─────────┼────────────────────────┤
│ Text Primary │ Dark Charcoal    │ #212121 │ Body text, labels      │
└──────────────┴──────────────────┴─────────┴────────────────────────┘

Typography (Use Google Fonts)

- Headers: Roboto Slab (Bold, 24px)
- Body: Roboto (Regular, 16px)
- Monospace: Roboto Mono (14px for timestamps/JSON)
- Implement in Streamlit:
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&family=Roboto+Slab:wght@600&family=Roboto+Mono&display=swap');
.stApp { font-family: 'Roboto', sans-serif; }
h1, h2, h3 { font-family: 'Roboto Slab', serif; }
.code, pre { font-family: 'Roboto Mono', monospace; }
</style>
""", unsafe_allow_html=True)

Layout & Components

Scan Screen (Main)

+--------------------------------------------------+
| [Logo] LegalMetro-Hackathon                      |
|                                                  |
|  [📁 Upload]  [📷 Camera]                        |
|                                                  |
|  +------------------------------------------+    |
|  |   [ IMAGE PREVIEW WITH BOXES ]           |    |
|  +------------------------------------------+    |
|                                                  |
|  FIELD     | STATUS  | DETAILS                |
|  ----------|---------|--------------------------|
|  MRP       | ✅ PASS | ₹ 199.00                 |
|  Quantity  | ❌ FAIL | 500 (missing unit)       |
|  Manufacturer| ✅ PASS| ABC Foods Ltd            |
|  Date      | ⚠️ UNCERTAIN| 03/24 (low conf)     |
|                                                  |
|  [📊 History]  [🔄 Rescan]                        |
+--------------------------------------------------+

Key UX Rules

- PASS/FAIL: Always show icon + text + color (never color alone)
- Loading State: st.spinner("Analyzing label...") during processing
- Error Messages: Actionable (e.g., "Image too blurry - retake with better light")
- Accessibility:
  - Minimum 4.5:1 color contrast (use WebAIM checker (https://webaim.org/resources/contrastchecker/))
  - Touch targets ≥48x48dp
  - Alt text for all images (e.g., "Label showing MRP ₹199.00")