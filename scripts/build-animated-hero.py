#!/usr/bin/env python3
"""Build the theme-aware animated profile hero from verified portfolio media."""

from __future__ import annotations

import base64
import html
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BUILD = ROOT / ".hero-build"

THEMES = {
    "dark": {
        "bg": "#071119", "bg2": "#0d1821", "panel": "#111f29",
        "ink": "#f2f5f7", "muted": "#aab9c4", "dim": "#6f8491",
        "line": "#d7e4ef", "accent": "#73e8c0", "blue": "#56c8e8",
        "gold": "#ffc45c", "veil": "#071119",
    },
    "light": {
        "bg": "#f7f4ed", "bg2": "#eaf1f5", "panel": "#ffffff",
        "ink": "#14232d", "muted": "#506571", "dim": "#71828b",
        "line": "#172631", "accent": "#087b5c", "blue": "#2788a8",
        "gold": "#a96700", "veil": "#f7f4ed",
    },
}

SCENES = [
    {
        "eyebrow": "ML / AI ENGINEER  ·  SPATIAL SYSTEMS",
        "title": ("I build AI systems", "that understand place."),
        "copy": ("From geographic evidence to tested agents, simulations,", "APIs, and decision interfaces."),
        "metrics": [("13", "systems shipped"), ("28", "typed agent tools"), ("800+", "tests in GeoChatBot")],
        "image": "photo.jpeg", "image_alt": "Portrait of Goshtasb Shahriari Mehr", "label": "END-TO-END OWNER",
    },
    {
        "eyebrow": "01 / GEOCHATBOT  ·  LIVE + OPEN SOURCE",
        "title": ("Private spatial AI,", "inside the browser."),
        "copy": ("An LLM plans against your own data; DuckDB-WASM", "computes locally; you approve before execution."),
        "metrics": [("ZERO", "backend uploads"), ("28", "validated tools"), ("5", "LLM providers")],
        "image": "geochatbot-poster.webp", "image_alt": "GeoChatBot live spatial analysis interface", "label": "LIVE SYSTEM  ↗",
    },
    {
        "eyebrow": "02 / LOCAL GLEAN  ·  PRIVACY-PRESERVING AGENT AI",
        "title": ("Agentic AI under", "real constraints."),
        "copy": ("A nine-node LangGraph pipeline that triages mail and drafts", "grounded replies on university infrastructure."),
        "metrics": [("96.7%", "triage accuracy"), ("~4s", "median draft"), ("~660", "automated tests")],
        "image": "local-glean-poster.webp", "image_alt": "Local Glean email assistant product interface", "label": "ON-PREMISE LLM",
    },
    {
        "eyebrow": "03 / DEPLOYED GEOSPATIAL RESEARCH PLATFORMS",
        "title": ("Research software,", "used in the field."),
        "copy": ("Offline collection, spatial statistics, governed access,", "and live maps for community-health research."),
        "metrics": [("11,319", "parcels served"), ("60+", "spatial analyses"), ("379", "solo commits")],
        "images": ["keystone-poster.webp", "fieldsurvey-poster.webp"], "label": "KEYSTONE + FIELDSURVEY",
    },
    {
        "eyebrow": "04 / RESEARCH → WORKING SOFTWARE",
        "title": ("Spatial depth.", "Engineering range."),
        "copy": ("Ph.D. dissertation defended at UF, M.Sc. Computer", "Engineering, and three peer-reviewed publications."),
        "metrics": [("48K", "households modeled"), ("4", "degrees"), ("3", "publications")],
        "image": "food-abm-poster.webp", "image_alt": "Urban food access simulation", "label": "OPEN THE FULL PORTFOLIO  ↗",
    },
]


def data_uri(name: str) -> str:
    path = ASSETS / name
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/webp"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def image_panel(scene: dict, theme: dict) -> str:
    if "images" in scene:
        left, right = (data_uri(name) for name in scene["images"])
        image_markup = f'''
        <image href="{left}" x="714" y="105" width="205" height="245" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipLeft)"/>
        <image href="{right}" x="929" y="105" width="205" height="245" preserveAspectRatio="xMidYMid slice" clip-path="url(#clipRight)"/>'''
    else:
        uri = data_uri(scene["image"])
        preserve = "xMidYMid slice"
        image_markup = f'<image href="{uri}" x="714" y="105" width="420" height="245" preserveAspectRatio="{preserve}" clip-path="url(#clipWide)"/>'

    return f'''
      <rect x="696" y="87" width="456" height="281" rx="20" fill="{theme['panel']}" stroke="{theme['line']}" stroke-opacity=".18"/>
      {image_markup}
      <rect x="714" y="319" width="420" height="31" fill="{theme['veil']}" fill-opacity=".88" clip-path="url(#clipWide)"/>
      <text x="730" y="340" fill="{theme['accent']}" font-size="11" font-weight="700" letter-spacing="1.25">{html.escape(scene['label'])}</text>
      <circle cx="1120" cy="334" r="4" fill="{theme['accent']}"/>
    '''


def scene_svg(scene: dict, index: int, theme_name: str) -> str:
    t = THEMES[theme_name]
    metrics = []
    for i, (value, label) in enumerate(scene["metrics"]):
        x = 70 + i * 196
        metrics.append(f'''
          <g transform="translate({x} 335)">
            <text fill="{t['ink']}" font-size="21" font-weight="680">{html.escape(value)}</text>
            <text y="22" fill="{t['dim']}" font-size="10.5" font-weight="600" letter-spacing=".6">{html.escape(label).upper()}</text>
          </g>''')
    progress = []
    for i in range(len(SCENES)):
        progress.append(f'<rect x="{70 + i * 45}" y="410" width="34" height="3" rx="1.5" fill="{t["accent"] if i == index else t["line"]}" fill-opacity="{1 if i == index else .16}"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="460" viewBox="0 0 1200 460">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{t['line']}" stroke-opacity=".045"/></pattern>
        <clipPath id="clipWide"><rect x="714" y="105" width="420" height="245" rx="12"/></clipPath>
        <clipPath id="clipLeft"><rect x="714" y="105" width="205" height="245" rx="12"/></clipPath>
        <clipPath id="clipRight"><rect x="929" y="105" width="205" height="245" rx="12"/></clipPath>
      </defs>
      <rect width="1200" height="460" rx="24" fill="url(#bg)"/><rect width="1200" height="460" rx="24" fill="url(#grid)"/>
      <g fill="none" stroke="{t['accent']}" stroke-opacity=".08"><path d="M760 6c86 44 99 110 184 122 86 12 142-27 249 11"/><path d="M734 28c93 43 112 117 205 132 98 16 159-24 254 18"/><path d="M720 54c87 36 117 115 216 139 102 25 171-13 257 30"/></g>
      <g font-family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">
        <text x="70" y="62" fill="{t['accent']}" font-size="12" font-weight="700" letter-spacing="1.8">GOSHTASB SHAHRIARI MEHR</text>
        <text x="1132" y="62" text-anchor="end" fill="{t['dim']}" font-size="11" font-weight="650" letter-spacing="1.2">{index + 1:02d} / {len(SCENES):02d}</text>
        <text x="70" y="116" fill="{t['blue']}" font-size="11.5" font-weight="680" letter-spacing="1.45">{html.escape(scene['eyebrow'])}</text>
        <text x="68" y="190" fill="{t['ink']}" font-size="54" font-weight="650" letter-spacing="-2.7">{html.escape(scene['title'][0])}</text>
        <text x="68" y="246" fill="{t['accent']}" font-size="54" font-weight="380" letter-spacing="-2.7">{html.escape(scene['title'][1])}</text>
        <text x="72" y="284" fill="{t['muted']}" font-size="15.5" font-weight="430">{html.escape(scene['copy'][0])}</text>
        <text x="72" y="307" fill="{t['muted']}" font-size="15.5" font-weight="430">{html.escape(scene['copy'][1])}</text>
        {''.join(metrics)}
        {image_panel(scene, t)}
        {''.join(progress)}
        <text x="1132" y="416" text-anchor="end" fill="{t['dim']}" font-size="10.5" font-weight="600" letter-spacing="1">PORTFOLIO · CV · LIVE SYSTEMS</text>
      </g>
    </svg>'''


def run() -> None:
    BUILD.mkdir(exist_ok=True)
    for theme in THEMES:
        pngs = []
        for index, scene in enumerate(SCENES):
            svg_path = BUILD / f"{theme}-{index}.svg"
            png_path = BUILD / f"{theme}-{index}.png"
            svg_path.write_text(scene_svg(scene, index, theme), encoding="utf-8")
            subprocess.run(["rsvg-convert", "-o", str(png_path), str(svg_path)], check=True)
            pngs.append(png_path)

        inputs = []
        for png in pngs:
            inputs.extend(["-loop", "1", "-t", "3", "-i", str(png)])
        filters = (
            "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.5[x1];"
            "[x1][2:v]xfade=transition=fade:duration=0.5:offset=5[x2];"
            "[x2][3:v]xfade=transition=fade:duration=0.5:offset=7.5[x3];"
            "[x3][4:v]xfade=transition=fade:duration=0.5:offset=10,"
            "fps=10,format=yuv420p[v]"
        )
        subprocess.run([
            "ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", filters, "-map", "[v]",
            "-c:v", "libwebp_anim", "-lossless", "0", "-quality", "78",
            "-loop", "0", "-an", str(ASSETS / f"hero-{theme}-animated.webp"),
        ], check=True)


if __name__ == "__main__":
    run()
