#!/usr/bin/env python3
"""Generate new/fixed skill icons for the UMMAN2005 profile."""
import os, textwrap

ASSETS = os.path.join(os.path.dirname(__file__), '..', 'assets')
BG_DARK = '#242938'
BG_LIGHT = '#F4F2ED'

def write_icon(name, auto_svg, dark_svg=None, light_svg=None):
    """Write auto/dark/light variants. dark/light default to same paths as auto."""
    if dark_svg is None:
        dark_svg = auto_svg
    if light_svg is None:
        light_svg = auto_svg
    for variant, content in [('auto', auto_svg), ('dark', dark_svg), ('light', light_svg)]:
        path = os.path.join(ASSETS, f'{name}-{variant}.svg')
        with open(path, 'w') as f:
            f.write(content)
    print(f'  ✓ {name}')

def themed_icon(name, icon_paths, dark_bg=BG_DARK, light_bg=BG_LIGHT, scale=1.0, tx=0, ty=0, extra_defs=''):
    """Wrap icon paths in a themed 256x256 rounded square background."""
    transform = f'translate({tx}, {ty}) scale({scale})' if (tx or ty or scale != 1.0) else f'scale({scale})'
    if scale == 1.0 and not tx and not ty:
        transform = ''
        g_open = ''
        g_close = ''
        inner = icon_paths
    else:
        g_open = f'<g transform="{transform}">'
        g_close = '</g>'
        inner = icon_paths

    def make(bg):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="{name}">
  <rect width="256" height="256" rx="60" fill="{bg}"/>
  {extra_defs}
  {g_open}
  {inner}
  {g_close}
</svg>'''
    return make(dark_bg), make(light_bg)

# ---------------------------------------------------------------------------
# 1. Kargo (https://kargo.io)
# Yellow/orange rocket/cargo container - use official Kargo "K" logo style
# Official brand: dark navy background, white "K" with orange accent
# ---------------------------------------------------------------------------
kargo_paths = '''<rect width="256" height="256" rx="60" fill="#0F172A"/>
  <!-- Kargo shield/hex icon - stylized K -->
  <path fill="#F97316" d="M128 36 L192 72 L192 144 L128 180 L64 144 L64 72 Z"/>
  <path fill="#0F172A" d="M128 52 L180 80 L180 140 L128 168 L76 140 L76 80 Z"/>
  <path fill="white" d="M104 88 L104 168 L118 168 L118 136 L145 168 L162 168 L134 132 L160 96 L143 96 L118 126 L118 88 Z"/>'''

kargo_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="kargo">
  <style>
    #kargo .kargo-bg {{ fill: #0F172A; }}
    @media (prefers-color-scheme: light) {{
      #kargo .kargo-bg {{ fill: #1E293B; }}
    }}
  </style>
  <rect class="kargo-bg" width="256" height="256" rx="60"/>
  <!-- Kargo hex-shield with K -->
  <path fill="#F97316" d="M128 36 L192 72 L192 144 L128 180 L64 144 L64 72 Z"/>
  <path fill="#0F172A" d="M128 52 L180 80 L180 140 L128 168 L76 140 L76 80 Z"/>
  <path fill="white" d="M104 88 L104 168 L118 168 L118 136 L145 168 L162 168 L134 132 L160 96 L143 96 L118 126 L118 88 Z"/>
</svg>'''

# ---------------------------------------------------------------------------
# 2. Kubescape (correct logo - the official ARMO shield icon)
# Source: /tmp/kubescape-official.svg (CNCF artwork)
# The icon is a hexagon with |< mark = exactly the Kubescape identity
# viewBox="0 0 126.9 117" - blue pentagon/hex with purple gradient and K icon
# ---------------------------------------------------------------------------
kubescape_inner = '''<path fill="#2916FC" d="M32.4 99.9c-1.1 0-2.2-.3-3.1-.8s-1.7-1.3-2.3-2.3L2.1 53.7c-.5-1-.8-2-.8-3.1s.3-2.2.8-3.1L27 4.4c.5-1 1.3-1.7 2.3-2.3 1-.5 2-.8 3.1-.8h49.7c1.1 0 2.2.3 3.1.8.9.5 1.7 1.3 2.3 2.3l24.9 43.1c.6 1 .8 2 .8 3.1s-.3 2.2-.8 3.1L87.5 96.8c-.6.9-1.3 1.7-2.3 2.3s-2 .8-3.1.8H32.4z"/>
  <path fill="#ffffff" d="M82.1 2.6c.9 0 1.7.2 2.5.7.8.4 1.4 1.1 1.8 1.8l24.9 43.1c.4.8.7 1.6.7 2.5s-.2 1.7-.7 2.5L86.4 96.3c-.4.8-1.1 1.4-1.8 1.8-.8.4-1.6.7-2.5.7H32.4c-.9 0-1.7-.2-2.5-.7s-1.4-1.1-1.8-1.8L3.2 53.2c-.4-.8-.7-1.6-.7-2.5s.2-1.7.7-2.5L28.1 5.1c.4-.8 1.1-1.4 1.8-1.8.8-.4 1.6-.7 2.5-.7H82.1M82.1 0H32.4c-1.3 0-2.6.4-3.7 1-1.1.7-2.1 1.6-2.7 2.7L1 46.8C.4 48 0 49.3 0 50.7s.4 2.7 1 3.8L26 97.6c.7 1.1 1.6 2.1 2.7 2.7 1.1.7 2.4 1 3.7 1h49.7c1.3 0 2.6-.4 3.7-1 1.1-.7 2.1-1.6 2.7-2.7l25.1-43.1c.7-1.1 1-2.4 1-3.8s-.4-2.7-1-3.8L88.5 3.8c-.7-1.1-1.6-2.1-2.7-2.7C84.7.4 83.4 0 82.1 0z"/>
  <path fill="#ffffff" d="M54.3 25v49.6c0 .7-.3 1.3-.8 1.8-.5.5-1.1.8-1.8.8h-9.5c-.7 0-1.3-.3-1.8-.8s-.8-1.1-.8-1.8V25c0-.7.3-1.3.8-1.8s1.1-.8 1.8-.8h9.5c.7 0 1.3.3 1.8.8s.8 1.1.8 1.8zm26.3 1.4L67.8 45.6c-.3.4-.4.9-.4 1.3s.1 1 .3 1.4l14.8 25.1c.2.4.3.8.3 1.3 0 .4-.1.9-.3 1.3-.2.4-.5.7-.9.9s-.8.3-1.3.3H69.5c-.4 0-.9-.1-1.3-.3-.4-.2-.7-.6-.9-.9L52.6 49.4c-.2-.4-.3-.8-.3-1.3 0-.5.2-.9.4-1.3l14.7-23.1c.2-.4.6-.7.9-.9.4-.2.8-.3 1.2-.3h9c.4 0 .9.1 1.3.4.4.2.7.6.9 1 .2.4.3.9.3 1.3 0 .4-.1.8-.4 1.2z"/>
  <defs>
    <linearGradient id="ks-grad" x1="69.82" y1="71.44" x2="110.69" y2="71.44" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF7879"/>
      <stop offset="0.5" stop-color="#AE52AA"/>
      <stop offset="1" stop-color="#5529E0"/>
    </linearGradient>
  </defs>
  <path fill="url(#ks-grad)" d="M110.7 59.5L91.8 92.1H81.8l-9.2-16-2.7-4.7 4.7-8.1 3.8-6.6 3.4-6h23.9z"/>'''

kubescape_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="kubescape">
  <style>
    #kubescape .ks-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #kubescape .ks-bg {{ fill: #F4F2ED; }}
    }}
  </style>
  <rect class="ks-bg" width="256" height="256" rx="60"/>
  <g transform="translate(64, 72) scale(1.068)">
    {kubescape_inner}
  </g>
</svg>'''

# ---------------------------------------------------------------------------
# 3. OPA (Open Policy Agent) - Official colors: blue/white
# Official icon: circle with OPA shield - blue octagon
# ---------------------------------------------------------------------------
opa_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="opa">
  <style>
    #opa .opa-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #opa .opa-bg {{ fill: #F4F2ED; }}
    }}
  </style>
  <rect class="opa-bg" width="256" height="256" rx="60"/>
  <!-- OPA official icon: blue circle with white O-P-A text and shield -->
  <circle cx="128" cy="128" r="88" fill="#2667FF"/>
  <path fill="white" d="M128 56L168 76V116C168 148 148 168 128 176C108 168 88 148 88 116V76Z"/>
  <path fill="#2667FF" d="M128 68L160 84V116C160 144 144 160 128 166C112 160 96 144 96 116V84Z"/>
  <!-- OPA text -->
  <text x="128" y="134" text-anchor="middle" font-family="Arial Black,sans-serif" font-weight="900" font-size="34" fill="white">OPA</text>
</svg>'''

# ---------------------------------------------------------------------------
# 4. Kyverno - Official colors: teal/dark blue
# Logo is a stylized shield with checkmark
# ---------------------------------------------------------------------------
kyverno_svg_raw = open('/tmp/kyverno-official.svg').read()
# The kyverno SVG uses color #7DF3E1 (teal) on various shapes

kyverno_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="kyverno">
  <style>
    #kyverno .kyverno-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #kyverno .kyverno-bg {{ fill: #F4F2ED; }}
    }}
  </style>
  <rect class="kyverno-bg" width="256" height="256" rx="60"/>
  <g transform="translate(20, 14) scale(0.636)">
    <svg viewBox="0 0 337.46475 428.49896" xmlns="http://www.w3.org/2000/svg">
      <path fill="#7DF3E1" d="M303.02856,166.04816a80.384,80.384,0,0,0,13.44825-10.37128c.79419-.76227,1.55041-1.53052,2.30078-2.30078a82.04885,82.04885,0,0,0,7.9292-9.37811,63.42407,63.42407,0,0,0,6.26928-10.76539,48.6159,48.6159,0,0,0,4.35877-16.39782c1.48279-19.39118-9.96729-38.67493-35.62195-54.22687L198.55737,0l-120.26,115.22662L0,190.2478l108.60107,65.90778a111.60534,111.60534,0,0,0,57.76172,16.41577c24.92212,0,48.80127-8.803,66.41919-25.68646,19.15833-18.36218,25.51929-42.128,13.697-61.87146a49.0086,49.0086,0,0,0-6.7987-8.86865,89.32561,89.32561,0,0,0,19.28576,2.14355c.05164,0,.10144.004.15113.004a85.01244,85.01244,0,0,0,30.9707-5.7937A80.536,80.536,0,0,0,303.02856,166.04816ZM202.44543,225.85583c-19.3197,18.51-50.39855,21.23664-75.69982,5.89936L51.61328,186.14752l67.44336-64.64239,76.41687,46.38617C223.01074,184.58405,221.49072,207.60742,202.44543,225.85583Zm8.93348-82.21734-70.64722-42.8888,64.40723-61.76837L274.5083,81.09558c25.94006,15.72455,29.31006,37.04126,10.55042,55.017A60.70506,60.70506,0,0,1,211.37891,143.63849Zm29.86572,190.0401c-19.5763,18.75629-46.17029,29.08777-74.88184,29.08777A123.81616,123.81616,0,0,1,102.2561,344.5733L0,282.51672V307.194l108.60107,65.90778a111.60536,111.60536,0,0,0,57.76172,16.41571c24.92212,0,48.80127-8.80292,66.41919-25.6864,12.87708-12.34162,19.99024-27.12934,19.67981-41.49311l-.00207-1.79126A87.09493,87.09493,0,0,1,241.24463,333.67859Z"/>
    </svg>
  </g>
</svg>'''

# ---------------------------------------------------------------------------
# 5. Backstage (Spotify Backstage) - official teal/green color
# ---------------------------------------------------------------------------
backstage_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="backstage">
  <style>
    #backstage .backstage-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #backstage .backstage-bg {{ fill: #F4F2ED; }}
    }}
  </style>
  <rect class="backstage-bg" width="256" height="256" rx="60"/>
  <!-- Backstage Spotify-style: two overlapping rounded rectangles in official teal -->
  <rect x="56" y="56" width="64" height="144" rx="32" fill="#9BF0E1"/>
  <rect x="96" y="56" width="104" height="96" rx="32" fill="#00BFA5"/>
  <rect x="96" y="116" width="104" height="84" rx="32" fill="#00BFA5" opacity="0.7"/>
</svg>'''

# ---------------------------------------------------------------------------
# 6. Trivy - colored version (official Aqua colors: cyan/teal on dark)
# Current version uses #00C2E0 - that IS the correct Trivy color already
# User wants a "colored" icon = the cyan paths on a proper colored background
# Let's give it the official Aqua dark navy bg (#012749) instead of #242938
# ---------------------------------------------------------------------------
trivy_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="trivy">
  <style>
    #trivy .trivy-bg {{ fill: #012749; }}
    @media (prefers-color-scheme: light) {{
      #trivy .trivy-bg {{ fill: #E0F7FA; }}
    }}
  </style>
  <rect class="trivy-bg" width="256" height="256" rx="60"/>
  <g transform="translate(48, 48) scale(6.667)">
    <path d="M4.375 7.311 1.962 5.918a.1.1 0 0 1 0-.174L11.828.047a.343.343 0 0 1 .344 0l9.864 5.696a.1.1 0 0 1 0 .175L19.624 7.31a.962.962 0 0 1-.052-.074c-.914-1.478-2.124-2.592-3.596-3.31-4.088-1.994-9.164-.505-11.6 3.385ZM12.262 23.899v-3.14c5.693-2.087 9.01-7.766 7.588-12.985l2.436-1.42a.1.1 0 0 1 .151.088v11.645a.1.1 0 0 1-.05.087l-9.973 5.812a.1.1 0 0 1-.152-.087Zm-.559-3.141v3.14a.1.1 0 0 1-.151.086l-9.933-5.81a.114.114 0 0 1-.056-.099V6.436a.1.1 0 0 1 .15-.087l2.44 1.41c-1.455 5.307 1.846 10.993 7.55 13ZM7.013 8.834 4.807 7.561c2.306-3.665 7.094-5.066 10.95-3.186 1.385.676 2.526 1.727 3.39 3.124l.04.062-2.195 1.268a5.57 5.57 0 0 0-2.429-2.307c-2.603-1.27-5.901-.253-7.552 2.311Zm9.337 5.2c.813-1.371 1.088-2.99.798-4.685l2.255-1.314c1.245 4.86-1.864 10.169-7.14 12.192v-3.072c1.86-.67 3.272-1.747 4.087-3.12ZM4.6 8.018l2.27 1.31c-.225 1.571.112 3.204.951 4.606.919 1.536 2.225 2.629 3.881 3.25v3.045C6.327 18.25 3.297 13.042 4.601 8.017Zm5.303 2.486-2.459-1.42c1.52-2.34 4.53-3.268 6.9-2.112a5.075 5.075 0 0 1 2.216 2.108l-2.471 1.427a2.311 2.311 0 0 0-2.03-1.195c-.825 0-1.645.43-2.156 1.192Zm4.338.522 2.443-1.408c.22 1.51-.043 2.945-.765 4.162-.735 1.238-1.998 2.224-3.658 2.856v-2.631c1.25-.691 1.968-1.771 1.98-2.979ZM8.25 13.676A6.576 6.576 0 0 1 7.34 9.6l2.446 1.412c-.016 1.271.73 2.437 1.917 2.997v2.624a6.977 6.977 0 0 1-3.453-2.956Zm3.853-.148-.137.073-.157-.075c-1.023-.504-1.524-1.606-1.557-2.417a1.99 1.99 0 0 1 .004-.23 2.153 2.153 0 0 1 1.163-.957c.508-.178 1.034-.153 1.444.071.6.327.84.797.86.86.008.156.004.253.004.256-.038.981-.63 1.863-1.624 2.419Z" fill="#00C2E0"/>
  </g>
</svg>'''

trivy_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="trivy">
  <rect width="256" height="256" rx="60" fill="#E0F7FA"/>
  <g transform="translate(48, 48) scale(6.667)">
    <path d="M4.375 7.311 1.962 5.918a.1.1 0 0 1 0-.174L11.828.047a.343.343 0 0 1 .344 0l9.864 5.696a.1.1 0 0 1 0 .175L19.624 7.31a.962.962 0 0 1-.052-.074c-.914-1.478-2.124-2.592-3.596-3.31-4.088-1.994-9.164-.505-11.6 3.385ZM12.262 23.899v-3.14c5.693-2.087 9.01-7.766 7.588-12.985l2.436-1.42a.1.1 0 0 1 .151.088v11.645a.1.1 0 0 1-.05.087l-9.973 5.812a.1.1 0 0 1-.152-.087Zm-.559-3.141v3.14a.1.1 0 0 1-.151.086l-9.933-5.81a.114.114 0 0 1-.056-.099V6.436a.1.1 0 0 1 .15-.087l2.44 1.41c-1.455 5.307 1.846 10.993 7.55 13ZM7.013 8.834 4.807 7.561c2.306-3.665 7.094-5.066 10.95-3.186 1.385.676 2.526 1.727 3.39 3.124l.04.062-2.195 1.268a5.57 5.57 0 0 0-2.429-2.307c-2.603-1.27-5.901-.253-7.552 2.311Zm9.337 5.2c.813-1.371 1.088-2.99.798-4.685l2.255-1.314c1.245 4.86-1.864 10.169-7.14 12.192v-3.072c1.86-.67 3.272-1.747 4.087-3.12ZM4.6 8.018l2.27 1.31c-.225 1.571.112 3.204.951 4.606.919 1.536 2.225 2.629 3.881 3.25v3.045C6.327 18.25 3.297 13.042 4.601 8.017Zm5.303 2.486-2.459-1.42c1.52-2.34 4.53-3.268 6.9-2.112a5.075 5.075 0 0 1 2.216 2.108l-2.471 1.427a2.311 2.311 0 0 0-2.03-1.195c-.825 0-1.645.43-2.156 1.192Zm4.338.522 2.443-1.408c.22 1.51-.043 2.945-.765 4.162-.735 1.238-1.998 2.224-3.658 2.856v-2.631c1.25-.691 1.968-1.771 1.98-2.979ZM8.25 13.676A6.576 6.576 0 0 1 7.34 9.6l2.446 1.412c-.016 1.271.73 2.437 1.917 2.997v2.624a6.977 6.977 0 0 1-3.453-2.956Zm3.853-.148-.137.073-.157-.075c-1.023-.504-1.524-1.606-1.557-2.417a1.99 1.99 0 0 1 .004-.23 2.153 2.153 0 0 1 1.163-.957c.508-.178 1.034-.153 1.444.071.6.327.84.797.86.86.008.156.004.253.004.256-.038.981-.63 1.863-1.624 2.419Z" fill="#0097A7"/>
  </g>
</svg>'''

# ---------------------------------------------------------------------------
# 7. Talos (Sidero Labs) - official logo: stylized 'T' or ring/gear shape
# Talos brand: dark navy/black bg, neon cyan/teal ring icon
# ---------------------------------------------------------------------------
talos_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="talos">
  <style>
    #talos .talos-bg {{ fill: #1A1D23; }}
    @media (prefers-color-scheme: light) {{
      #talos .talos-bg {{ fill: #F0F4F8; }}
    }}
  </style>
  <rect class="talos-bg" width="256" height="256" rx="60"/>
  <!-- Talos: concentric rings - the official icon look -->
  <circle cx="128" cy="128" r="80" fill="none" stroke="#FFE400" stroke-width="18"/>
  <circle cx="128" cy="128" r="52" fill="none" stroke="#FFE400" stroke-width="12"/>
  <circle cx="128" cy="128" r="24" fill="#FFE400"/>
</svg>'''

talos_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="talos">
  <rect width="256" height="256" rx="60" fill="#F0F4F8"/>
  <circle cx="128" cy="128" r="80" fill="none" stroke="#1A1D23" stroke-width="18"/>
  <circle cx="128" cy="128" r="52" fill="none" stroke="#1A1D23" stroke-width="12"/>
  <circle cx="128" cy="128" r="24" fill="#1A1D23"/>
</svg>'''

# ---------------------------------------------------------------------------
# 8. Cilium - colored version (the honeycomb should show the orange/yellow on proper bg)
# Current cilium already has orange (#F4941C) paths but uses dark themed bg
# "Use colored icon of Cilium" = use official Cilium white bg with orange icon
# ---------------------------------------------------------------------------
cilium_colored_paths = '''<g transform="translate(48.0, 48.0) scale(6.66667)">
    <path d="M13.607 14.583h-3.215l-1.626-2.764 1.626-2.802h3.215l1.626 2.802-1.626 2.764ZM14.186 8H9.799l-2.2 3.813 2.2 3.787h4.387l2.213-3.787L14.186 8Zm-4.387 8.4-2.2 3.813L9.799 24h4.387l2.213-3.787-2.213-3.813H9.799Zm-1.034 3.819 1.627-2.802h3.215l1.626 2.802-1.626 2.765h-3.215l-1.627-2.765ZM9.799 0l-2.2 3.813 2.2 3.787h4.387l2.213-3.787L14.186 0H9.799ZM8.765 3.819l1.627-2.802h3.215l1.626 2.802-1.626 2.764h-3.215L8.765 3.819Zm8.234 8.581-2.2 3.813 2.2 3.787h4.388l2.213-3.787-2.213-3.813h-4.388Zm-1.034 3.819 1.627-2.802h3.215l1.626 2.802-1.626 2.765h-3.215l-1.627-2.765ZM16.999 4l-2.2 3.813 2.2 3.787h4.388L23.6 7.813 21.387 4h-4.388Zm-1.034 3.819 1.627-2.802h3.215l1.626 2.802-1.626 2.764h-3.215l-1.627-2.764ZM2.599 12.4l-2.2 3.813L2.599 20h4.387l2.213-3.787L6.986 12.4H2.599Zm-1.034 3.819 1.627-2.802h3.214l1.627 2.802-1.627 2.765H3.192l-1.627-2.765ZM2.599 4l-2.2 3.813 2.2 3.787h4.387l2.213-3.787L6.986 4H2.599ZM1.565 7.819l1.627-2.802h3.214l1.627 2.802-1.627 2.764H3.192L1.565 7.819Z" fill="#F4941C" />
  </g>'''

cilium_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="cilium">
  <style>
    #cilium .cilium-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #cilium .cilium-bg {{ fill: #FFFFFF; }}
    }}
  </style>
  <rect class="cilium-bg" width="256" height="256" rx="60"/>
  {cilium_colored_paths}
</svg>'''

cilium_dark = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="cilium">
  <rect width="256" height="256" rx="60" fill="#242938"/>
  {cilium_colored_paths}
</svg>'''

cilium_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="cilium">
  <rect width="256" height="256" rx="60" fill="#FFFFFF"/>
  {cilium_colored_paths}
</svg>'''

# ---------------------------------------------------------------------------
# 9. HAProxy - official brand: HAProxy logo uses 'H' in stylized look
# Brand colors: dark/navy bg, white/blue H logo
# ---------------------------------------------------------------------------
haproxy_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="haproxy">
  <style>
    #haproxy .ha-bg {{ fill: #1E2A3A; }}
    @media (prefers-color-scheme: light) {{
      #haproxy .ha-bg {{ fill: #F0F4F8; }}
    }}
  </style>
  <rect class="ha-bg" width="256" height="256" rx="60"/>
  <!-- HAProxy stylized H - based on official brand guide -->
  <rect x="60" y="70" width="36" height="116" rx="6" fill="white"/>
  <rect x="160" y="70" width="36" height="116" rx="6" fill="white"/>
  <rect x="60" y="110" width="136" height="36" rx="6" fill="white"/>
</svg>'''

haproxy_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="haproxy">
  <rect width="256" height="256" rx="60" fill="#F0F4F8"/>
  <rect x="60" y="70" width="36" height="116" rx="6" fill="#1E2A3A"/>
  <rect x="160" y="70" width="36" height="116" rx="6" fill="#1E2A3A"/>
  <rect x="60" y="110" width="136" height="36" rx="6" fill="#1E2A3A"/>
</svg>'''

# ---------------------------------------------------------------------------
# 10. CSS - new 2024 logo (rebeccapurple #663399, rounded square, "CSS" white text)
# ---------------------------------------------------------------------------
css_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="css">
  <rect width="256" height="256" rx="60" fill="#663399"/>
  <text x="128" y="152" text-anchor="middle" font-family="Arial Black,Helvetica Neue,sans-serif" font-weight="900" font-size="88" fill="white" letter-spacing="-3">CSS</text>
</svg>'''

# CSS uses its own colored bg, same in auto/dark/light
css_dark = css_auto.replace('id="css"', 'id="css"')
css_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="css">
  <rect width="256" height="256" rx="60" fill="#663399"/>
  <text x="128" y="152" text-anchor="middle" font-family="Arial Black,Helvetica Neue,sans-serif" font-weight="900" font-size="88" fill="white" letter-spacing="-3">CSS</text>
</svg>'''

# ---------------------------------------------------------------------------
# 11. Bootstrap - official B logo (purple gradient) - refresh to official style
# Official: purple background with "B" and curly braces {{}}
# ---------------------------------------------------------------------------
bootstrap_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="bootstrap">
  <defs>
    <linearGradient id="bs-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#9013FE"/>
      <stop offset="1" stop-color="#6610F2"/>
    </linearGradient>
  </defs>
  <rect width="256" height="256" rx="60" fill="url(#bs-grad)"/>
  <!-- Bootstrap official B mark -->
  <path fill="white" d="M88 60h48c26 0 44 12 44 34 0 14-8 24-20 28 16 4 26 16 26 32 0 24-18 42-48 42H88V60zm20 58h26c14 0 22-6 22-18s-8-18-22-18H108v36zm0 58h28c16 0 26-8 26-22s-10-22-26-22H108v44z"/>
</svg>'''

# Bootstrap uses its own colored bg
bootstrap_dark = bootstrap_auto
bootstrap_light = bootstrap_auto

# ---------------------------------------------------------------------------
# 12. Nix (nix package manager, different from NixOS the OS)
# Use the Nix snowflake/lambda icon on themed bg
# ---------------------------------------------------------------------------
nix_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="nix">
  <style>
    #nix .nix-bg {{ fill: #242938; }}
    @media (prefers-color-scheme: light) {{
      #nix .nix-bg {{ fill: #F4F2ED; }}
    }}
  </style>
  <rect class="nix-bg" width="256" height="256" rx="60"/>
  <!-- Nix lambda (λ) symbol in Nix blue -->
  <text x="128" y="158" text-anchor="middle" font-family="DejaVu Serif,Georgia,serif" font-size="140" fill="#5277C3" font-weight="bold">λ</text>
</svg>'''

nix_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="nix">
  <rect width="256" height="256" rx="60" fill="#F4F2ED"/>
  <text x="128" y="158" text-anchor="middle" font-family="DejaVu Serif,Georgia,serif" font-size="140" fill="#5277C3" font-weight="bold">λ</text>
</svg>'''

# ---------------------------------------------------------------------------
# 13. UV (Astral uv python package manager)
# Official brand: dark bg, red/coral UV letters
# ---------------------------------------------------------------------------
uv_auto = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="uv">
  <style>
    #uv .uv-bg {{ fill: #1A1A1A; }}
    @media (prefers-color-scheme: light) {{
      #uv .uv-bg {{ fill: #F5F5F5; }}
    }}
  </style>
  <rect class="uv-bg" width="256" height="256" rx="60"/>
  <text x="128" y="162" text-anchor="middle" font-family="Arial Black,Helvetica Neue,sans-serif" font-weight="900" font-size="110" fill="#DE3163" letter-spacing="-4">uv</text>
</svg>'''

uv_light = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" id="uv">
  <rect width="256" height="256" rx="60" fill="#F5F5F5"/>
  <text x="128" y="162" text-anchor="middle" font-family="Arial Black,Helvetica Neue,sans-serif" font-weight="900" font-size="110" fill="#DE3163" letter-spacing="-4">uv</text>
</svg>'''

# ---------------------------------------------------------------------------
# Write all icons
# ---------------------------------------------------------------------------
print("Writing icons...")

write_icon('kargo', kargo_auto)
write_icon('kubescape', kubescape_auto)
write_icon('opa', opa_auto)
write_icon('kyverno', kyverno_auto)
write_icon('backstage', backstage_auto)
write_icon('trivy', trivy_auto, trivy_auto, trivy_light)
write_icon('talos', talos_auto, talos_auto, talos_light)
write_icon('cilium', cilium_auto, cilium_dark, cilium_light)
write_icon('haproxy', haproxy_auto, haproxy_auto, haproxy_light)
write_icon('css', css_auto, css_dark, css_light)
write_icon('bootstrap', bootstrap_auto, bootstrap_dark, bootstrap_light)
write_icon('nix', nix_auto, nix_auto, nix_light)
write_icon('uv', uv_auto, uv_auto, uv_light)

print("\nDone! Run 'go run build.go' to rebuild api/index.go")
