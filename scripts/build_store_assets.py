#!/usr/bin/env python3
"""
OmniSnap - Chrome Web Store & Multi-Browser Marketing Asset Pipeline
Generates high-resolution vector SVGs, compiles them into a native FigCraft project,
and renders pixel-perfect PNG store assets:
- Small Promo Tile: 440x280
- Large Promo Tile: 920x680
- Marquee Banner: 1400x560
- Store Screenshot 1: 1280x800 (Popup & Capture Modes)
- Store Screenshot 2: 1280x800 (Capture Viewer & Ultra-Long Page)
- Store Screenshot 3: 1280x800 (100% Free Annotation Studio)
- Store Screenshot 4: 1280x800 (Single Long Page PDF & Smart A4 Split)
- Store Screenshot 5: 1280x800 (Local Privacy & Settings Dashboard)
"""

import os
import json
import zipfile
import subprocess

STORE_DIR = "/Users/nishant/Documents/gravity_work/gravity_1/store"
DESIGN_DIR = "/Users/nishant/Documents/gravity_work/gravity_1/design"
os.makedirs(STORE_DIR, exist_ok=True)
os.makedirs(DESIGN_DIR, exist_ok=True)

# Common SVG Defs (Brand Gradients & Shadows)
DEFS = """
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F19"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1F2937"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="50%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#06B6D4"/>
      <stop offset="100%" stop-color="#3B82F6"/>
    </linearGradient>
    <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#CBD5E1"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="16" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="16" stdDeviation="24" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
  </defs>
"""

def generate_promo_small():
    # 440 x 280 Small Promo Tile
    svg = f"""<svg width="440" height="280" viewBox="0 0 440 280" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="440" height="280" fill="url(#bgGrad)"/>
  <circle cx="220" cy="110" r="130" fill="#4F46E5" opacity="0.18" filter="url(#glow)"/>
  
  <!-- Brand Icon Badge -->
  <g transform="translate(186, 40)" filter="url(#shadow)">
    <rect width="68" height="68" rx="18" fill="url(#primaryGrad)"/>
    <path d="M22 28h24M22 34h18M22 40h24M34 22v24" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  </g>

  <!-- Title & Subtitle -->
  <text x="220" y="146" font-family="-apple-system, Roboto, sans-serif" font-size="24" font-weight="800" fill="url(#textGrad)" text-anchor="middle" letter-spacing="-0.5">OmniSnap</text>
  <text x="220" y="174" font-family="-apple-system, Roboto, sans-serif" font-size="13" font-weight="600" fill="#06B6D4" text-anchor="middle">Full-Page Capture & Continuous PDF</text>

  <!-- Badges -->
  <g transform="translate(100, 204)">
    <rect width="110" height="26" rx="13" fill="#1F2937" stroke="#374151" stroke-width="1"/>
    <text x="55" y="17" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#10B981" text-anchor="middle">✓ 100% FREE</text>
  </g>
  <g transform="translate(225, 204)">
    <rect width="115" height="26" rx="13" fill="#1F2937" stroke="#374151" stroke-width="1"/>
    <text x="57" y="17" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#38BDF8" text-anchor="middle">⚡ NO TELEMETRY</text>
  </g>
</svg>"""
    return "promo_small_440x280.svg", svg, 440, 280

def generate_promo_marquee():
    # 1400 x 560 Marquee Banner
    svg = f"""<svg width="1400" height="560" viewBox="0 0 1400 560" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1400" height="560" fill="url(#bgGrad)"/>
  <circle cx="280" cy="280" r="320" fill="#4F46E5" opacity="0.15" filter="url(#glow)"/>
  <circle cx="1100" cy="280" r="300" fill="#06B6D4" opacity="0.12" filter="url(#glow)"/>

  <!-- Left Copy Block -->
  <g transform="translate(100, 110)">
    <g transform="translate(0, 0)">
      <rect width="80" height="80" rx="22" fill="url(#primaryGrad)" filter="url(#shadow)"/>
      <path d="M26 34h28M26 42h20M26 50h28M40 26v28" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
    </g>
    <text x="100" y="48" font-family="-apple-system, Roboto, sans-serif" font-size="36" font-weight="800" fill="url(#textGrad)">OmniSnap</text>
    <text x="100" y="74" font-family="-apple-system, Roboto, sans-serif" font-size="16" font-weight="600" fill="#06B6D4">The Definitive Cross-Browser Capture Engine</text>

    <text x="0" y="145" font-family="-apple-system, Roboto, sans-serif" font-size="44" font-weight="900" fill="#FFFFFF" letter-spacing="-1">One Continuous Long PDF.</text>
    <text x="0" y="195" font-family="-apple-system, Roboto, sans-serif" font-size="44" font-weight="900" fill="url(#cyanGrad)" letter-spacing="-1">Zero Splits. Zero Paywalls.</text>

    <text x="0" y="245" font-family="-apple-system, Roboto, sans-serif" font-size="16" fill="#94A3B8" width="550">
      Capture massive web pages of any height. Export 1 continuous seamless PDF or smart A4 split with clickable hyperlinks, 100% on-device.
    </text>

    <!-- Pill Badges -->
    <g transform="translate(0, 280)">
      <rect width="160" height="36" rx="18" fill="rgba(16, 185, 129, 0.15)" stroke="#10B981" stroke-width="1.5"/>
      <text x="80" y="23" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" fill="#10B981" text-anchor="middle">✓ Studio 100% Free</text>
    </g>
    <g transform="translate(175, 280)">
      <rect width="180" height="36" rx="18" fill="rgba(6, 182, 212, 0.15)" stroke="#06B6D4" stroke-width="1.5"/>
      <text x="90" y="23" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" fill="#38BDF8" text-anchor="middle">⚡ Zero Telemetry</text>
    </g>
    <g transform="translate(370, 280)">
      <rect width="180" height="36" rx="18" fill="rgba(99, 102, 241, 0.15)" stroke="#6366F1" stroke-width="1.5"/>
      <text x="90" y="23" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" fill="#A5B4FC" text-anchor="middle">🦀 Rust Core Engine</text>
    </g>
  </g>

  <!-- Right Visual Window Mockup -->
  <g transform="translate(750, 70)" filter="url(#shadow)">
    <rect width="550" height="420" rx="14" fill="#111827" stroke="#374151" stroke-width="1.5"/>
    <!-- Topbar -->
    <rect width="550" height="42" rx="14" fill="#1F2937"/>
    <circle cx="20" cy="21" r="5" fill="#EF4444"/>
    <circle cx="36" cy="21" r="5" fill="#F59E0B"/>
    <circle cx="52" cy="21" r="5" fill="#10B981"/>
    <rect x="180" y="10" width="220" height="22" rx="6" fill="#111827"/>
    <text x="290" y="25" font-family="monospace" font-size="11" fill="#94A3B8" text-anchor="middle">apple.com/shop/buy-mac</text>

    <!-- Content Slices Mockup -->
    <rect x="150" y="60" width="250" height="340" rx="6" fill="#FFFFFF" filter="url(#shadow)"/>
    <rect x="170" y="80" width="120" height="14" rx="3" fill="#0F172A"/>
    <rect x="170" y="105" width="210" height="6" rx="2" fill="#94A3B8"/>
    <rect x="170" y="118" width="160" height="6" rx="2" fill="#CBD5E1"/>
    <rect x="180" y="140" width="190" height="110" rx="6" fill="#F1F5F9" stroke="#E2E8F0"/>
    <circle cx="275" cy="195" r="30" fill="#3B82F6" opacity="0.3"/>
    
    <!-- Floating Toolbar -->
    <g transform="translate(160, 360)">
      <rect width="230" height="32" rx="16" fill="rgba(17, 24, 39, 0.95)" stroke="#4F46E5" stroke-width="1.5"/>
      <text x="115" y="20" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#38BDF8" text-anchor="middle">✓ Exported 1-Page PDF (11,390px)</text>
    </g>
  </g>
</svg>"""
    return "promo_marquee_1400x560.svg", svg, 1400, 560

def generate_promo_large():
    # 920 x 680 Large Promo Card
    svg = f"""<svg width="920" height="680" viewBox="0 0 920 680" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="920" height="680" fill="url(#bgGrad)"/>
  <circle cx="460" cy="220" r="260" fill="#4F46E5" opacity="0.16" filter="url(#glow)"/>

  <g transform="translate(415, 60)" filter="url(#shadow)">
    <rect width="90" height="90" rx="24" fill="url(#primaryGrad)"/>
    <path d="M30 40h30M30 48h22M30 56h30M45 30v30" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  </g>

  <text x="460" y="195" font-family="-apple-system, Roboto, sans-serif" font-size="34" font-weight="800" fill="url(#textGrad)" text-anchor="middle">OmniSnap</text>
  <text x="460" y="228" font-family="-apple-system, Roboto, sans-serif" font-size="16" font-weight="600" fill="#06B6D4" text-anchor="middle">Next-Generation Full-Page Capture & Studio</text>

  <!-- Feature Grid -->
  <g transform="translate(70, 280)">
    <!-- Card 1 -->
    <rect x="0" y="0" width="240" height="180" rx="12" fill="#111827" stroke="#374151" stroke-width="1.5"/>
    <text x="24" y="44" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">📄 Long Continuous PDF</text>
    <text x="24" y="75" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">Exports entire 10,000+ px pages onto 1 seamless PDF sheet with zero splitting.</text>
    <text x="24" y="150" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#10B981">✓ Included Free</text>

    <!-- Card 2 -->
    <rect x="270" y="0" width="240" height="180" rx="12" fill="#111827" stroke="#4F46E5" stroke-width="1.5"/>
    <text x="294" y="44" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">🎨 100% Free Studio</text>
    <text x="294" y="75" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">Crop, Badges (1-2-3), Privacy Blur, Text, Shapes, and Mockups. No subscription.</text>
    <text x="294" y="150" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#38BDF8">✓ Unlocked</text>

    <!-- Card 3 -->
    <rect x="540" y="0" width="240" height="180" rx="12" fill="#111827" stroke="#374151" stroke-width="1.5"/>
    <text x="564" y="44" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">🛡️ Zero Telemetry</text>
    <text x="564" y="75" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">100% on-device processing. No Google Analytics tracking or external calls.</text>
    <text x="564" y="150" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#F59E0B">✓ 100% Local</text>
  </g>

  <!-- Bottom CTA bar -->
  <g transform="translate(235, 520)">
    <rect width="450" height="54" rx="27" fill="url(#primaryGrad)" filter="url(#shadow)"/>
    <text x="225" y="33" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">Chrome • Edge • Brave • Firefox • Safari</text>
  </g>
</svg>"""
    return "promo_large_920x680.svg", svg, 920, 680

def generate_screenshot_1():
    # Screenshot 1: Action Popup & Capture Modes (1280x800)
    svg = f"""<svg width="1280" height="800" viewBox="0 0 1280 800" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1280" height="800" fill="url(#bgGrad)"/>
  <circle cx="640" cy="400" r="350" fill="#4F46E5" opacity="0.12" filter="url(#glow)"/>

  <!-- Marketing Header -->
  <text x="640" y="80" font-family="-apple-system, Roboto, sans-serif" font-size="34" font-weight="800" fill="url(#textGrad)" text-anchor="middle">Instant Capture Modes for Any Workflow</text>
  <text x="640" y="115" font-family="-apple-system, Roboto, sans-serif" font-size="16" font-weight="500" fill="#94A3B8" text-anchor="middle">Capture entire web pages, visible viewports, custom selections, or scrolling elements with 1 click</text>

  <!-- Center Popup Window -->
  <g transform="translate(460, 160)" filter="url(#shadow)">
    <rect width="360" height="520" rx="16" fill="#111827" stroke="#374151" stroke-width="2"/>
    
    <!-- Popup Header -->
    <rect width="360" height="60" rx="16" fill="#1F2937"/>
    <circle cx="36" cy="30" r="14" fill="url(#primaryGrad)"/>
    <text x="62" y="36" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">OmniSnap</text>

    <!-- Capture Mode 1 (Active) -->
    <g transform="translate(20, 80)">
      <rect width="320" height="80" rx="12" fill="linear-gradient(135deg, rgba(79, 70, 229, 0.25), rgba(6, 182, 212, 0.15))" stroke="#4F46E5" stroke-width="2"/>
      <circle cx="40" cy="40" r="18" fill="#4F46E5"/>
      <text x="40" y="45" font-family="-apple-system, sans-serif" font-size="14" fill="#FFFFFF" text-anchor="middle">📄</text>
      <text x="75" y="34" font-family="-apple-system, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Capture Entire Page</text>
      <text x="75" y="55" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Scrolls & stitches full length (⌥⇧P)</text>
    </g>

    <!-- Mode 2 -->
    <g transform="translate(20, 175)">
      <rect width="320" height="75" rx="12" fill="#1F2937" stroke="#374151" stroke-width="1"/>
      <circle cx="40" cy="37" r="16" fill="#374151"/>
      <text x="40" y="42" font-family="-apple-system, sans-serif" font-size="13" fill="#FFFFFF" text-anchor="middle">✂️</text>
      <text x="75" y="32" font-family="-apple-system, sans-serif" font-size="14" font-weight="600" fill="#FFFFFF">Selected Region</text>
      <text x="75" y="51" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Draw area on screen (⌥⇧S)</text>
    </g>

    <!-- Mode 3 -->
    <g transform="translate(20, 265)">
      <rect width="320" height="75" rx="12" fill="#1F2937" stroke="#374151" stroke-width="1"/>
      <circle cx="40" cy="37" r="16" fill="#374151"/>
      <text x="40" y="42" font-family="-apple-system, sans-serif" font-size="13" fill="#FFFFFF" text-anchor="middle">🖥️</text>
      <text x="75" y="32" font-family="-apple-system, sans-serif" font-size="14" font-weight="600" fill="#FFFFFF">Visible Viewport</text>
      <text x="75" y="51" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Current screen area (⌥⇧V)</text>
    </g>

    <!-- Footer Controls -->
    <g transform="translate(20, 460)">
      <text x="10" y="24" font-family="-apple-system, sans-serif" font-size="12" font-weight="600" fill="#94A3B8">Settings & Heuristics</text>
      <rect x="230" y="6" width="80" height="26" rx="6" fill="#374151"/>
      <text x="270" y="23" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#FFFFFF" text-anchor="middle">Options ⚙️</text>
    </g>
  </g>
</svg>"""
    return "screenshot1_action_popup_1280x800.svg", svg, 1280, 800

def generate_screenshot_2():
    # Screenshot 2: Capture Viewer & Ultra-Long Page (1280x800)
    svg = f"""<svg width="1280" height="800" viewBox="0 0 1280 800" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1280" height="800" fill="url(#bgGrad)"/>

  <!-- Top Marketing Heading -->
  <text x="640" y="65" font-family="-apple-system, Roboto, sans-serif" font-size="32" font-weight="800" fill="url(#textGrad)" text-anchor="middle">Ultra-Long Screenshot Review with Minimap Radar</text>
  <text x="640" y="98" font-family="-apple-system, Roboto, sans-serif" font-size="15" fill="#06B6D4" text-anchor="middle">Stitches 15,000+ px pages without browser memory limits. 1-Click Copy, Download PNG, or PDF.</text>

  <!-- Viewer Window Mockup -->
  <g transform="translate(100, 130)" filter="url(#shadow)">
    <rect width="1080" height="610" rx="12" fill="#0B0F19" stroke="#374151" stroke-width="1.5"/>

    <!-- Viewer Topbar -->
    <rect width="1080" height="56" rx="12" fill="#111827"/>
    <g transform="translate(20, 14)">
      <rect width="28" height="28" rx="6" fill="url(#primaryGrad)"/>
      <text x="38" y="16" font-family="-apple-system, sans-serif" font-size="13" font-weight="700" fill="#FFFFFF">MacBook Pro with Liquid Retina XDR - Apple</text>
      <text x="38" y="27" font-family="-apple-system, sans-serif" font-size="10" fill="#94A3B8">1200 × 11,390 px • apple.com/shop/buy-mac</text>
    </g>

    <!-- Topbar Actions -->
    <g transform="translate(680, 12)">
      <!-- Studio Btn -->
      <rect x="0" y="0" width="115" height="32" rx="8" fill="url(#primaryGrad)"/>
      <text x="57" y="20" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Edit in Studio</text>
      
      <!-- Copy Btn -->
      <rect x="125" y="0" width="105" height="32" rx="8" fill="#10B981"/>
      <text x="177" y="20" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">Copy Image</text>

      <!-- PDF Btn Combo -->
      <g transform="translate(240, 0)">
        <rect width="145" height="32" rx="8" fill="#1E1B4B" stroke="#4F46E5" stroke-width="1.5"/>
        <text x="72" y="20" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#C7D2FE" text-anchor="middle">Download PDF ▾</text>
      </g>
    </g>

    <!-- Main Viewport with Apple Long Page Preview -->
    <rect x="420" y="70" width="240" height="520" fill="#FFFFFF" filter="url(#shadow)"/>
    <rect x="435" y="90" width="120" height="12" rx="2" fill="#0F172A"/>
    <rect x="435" y="110" width="210" height="6" rx="2" fill="#94A3B8"/>
    <rect x="435" y="130" width="210" height="180" rx="4" fill="#F8FAFC" stroke="#E2E8F0"/>
    <circle cx="540" cy="220" r="40" fill="#3B82F6" opacity="0.3"/>
    <rect x="435" y="330" width="210" height="60" rx="4" fill="#0F172A"/>
    <rect x="435" y="410" width="210" height="160" rx="4" fill="#F1F5F9"/>

    <!-- Minimap Radar Panel (Bottom-Right) -->
    <g transform="translate(940, 420)">
      <rect width="110" height="170" rx="10" fill="rgba(17, 24, 39, 0.95)" stroke="#374151" stroke-width="1.5"/>
      <rect x="10" y="10" width="90" height="150" rx="4" fill="#000000"/>
      <!-- Lens -->
      <rect x="10" y="30" width="90" height="34" rx="3" fill="rgba(6, 182, 212, 0.2)" stroke="#06B6D4" stroke-width="2"/>
    </g>

    <!-- Floating Zoom Bar (Bottom-Center) -->
    <g transform="translate(440, 550)">
      <rect width="200" height="36" rx="18" fill="rgba(17, 24, 39, 0.95)" stroke="#374151" stroke-width="1.5"/>
      <text x="100" y="22" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">-   Fit (100%)   +</text>
    </g>
  </g>
</svg>"""
    return "screenshot2_long_screenshot_viewer_1280x800.svg", svg, 1280, 800

def generate_screenshot_3():
    # Screenshot 3: Free Annotation Studio (1280x800)
    svg = f"""<svg width="1280" height="800" viewBox="0 0 1280 800" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1280" height="800" fill="url(#bgGrad)"/>
  <circle cx="640" cy="400" r="320" fill="#7C3AED" opacity="0.12" filter="url(#glow)"/>

  <!-- Marketing Header -->
  <text x="640" y="65" font-family="-apple-system, Roboto, sans-serif" font-size="32" font-weight="800" fill="url(#textGrad)" text-anchor="middle">Full-Featured Annotation Studio — 100% Free</text>
  <text x="640" y="98" font-family="-apple-system, Roboto, sans-serif" font-size="15" fill="#10B981" text-anchor="middle">Crop, 1-2-3 Step Badges, Privacy Blur, Text, Shapes, and Browser Frames with ZERO subscriptions</text>

  <!-- Studio UI Mockup -->
  <g transform="translate(100, 130)" filter="url(#shadow)">
    <rect width="1080" height="610" rx="12" fill="#0B0F19" stroke="#374151" stroke-width="1.5"/>
    
    <!-- Topbar Toolbar -->
    <rect width="1080" height="52" rx="12" fill="#111827"/>
    <g transform="translate(20, 10)">
      <!-- Tool items -->
      <rect x="0" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="18" y="21" font-size="13" text-anchor="middle">✂️</text>
      <rect x="44" y="0" width="36" height="32" rx="6" fill="#4F46E5"/><text x="62" y="21" font-size="13" text-anchor="middle">↗️</text>
      <rect x="88" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="106" y="21" font-size="13" text-anchor="middle">🔲</text>
      <rect x="132" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="150" y="21" font-size="13" text-anchor="middle">T</text>
      <rect x="176" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="194" y="21" font-size="13" text-anchor="middle">①</text>
      <rect x="220" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="238" y="21" font-size="13" text-anchor="middle">💧</text>
      <rect x="264" y="0" width="36" height="32" rx="6" fill="#1F2937"/><text x="282" y="21" font-size="13" text-anchor="middle">🖼️</text>
    </g>

    <g transform="translate(930, 10)">
      <rect width="130" height="32" rx="8" fill="url(#primaryGrad)"/>
      <text x="65" y="20" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">Export Image ▾</text>
    </g>

    <!-- Canvas Workspace -->
    <rect x="280" y="90" width="520" height="470" rx="8" fill="#FFFFFF" filter="url(#shadow)"/>
    <rect x="310" y="120" width="220" height="16" rx="3" fill="#0F172A"/>
    <rect x="310" y="150" width="360" height="8" rx="2" fill="#94A3B8"/>
    <rect x="310" y="190" width="460" height="180" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>

    <!-- Annotations Demonstration -->
    <!-- 1. Number Badge ① -->
    <circle cx="330" cy="190" r="16" fill="#EF4444" stroke="#FFFFFF" stroke-width="2"/>
    <text x="330" y="195" font-family="-apple-system, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">1</text>
    <!-- Arrow -->
    <path d="M350 200 L430 240" stroke="#EF4444" stroke-width="4" stroke-linecap="round"/>
    <polygon points="430,240 415,230 425,245" fill="#EF4444"/>

    <!-- 2. Privacy Blur Patch -->
    <rect x="350" y="280" width="220" height="44" rx="6" fill="rgba(75, 85, 99, 0.7)" stroke="#6B7280" stroke-dasharray="4"/>
    <text x="460" y="307" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">🔒 PRIVACY BLURRED DATA</text>

    <!-- 3. Number Badge ② -->
    <circle cx="680" cy="270" r="16" fill="#10B981" stroke="#FFFFFF" stroke-width="2"/>
    <text x="680" y="275" font-family="-apple-system, sans-serif" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">2</text>
    <!-- Callout Box -->
    <rect x="620" y="310" width="130" height="40" rx="8" fill="#1E293B" stroke="#10B981" stroke-width="1.5"/>
    <text x="685" y="334" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#FFFFFF" text-anchor="middle">Verified CTA</text>
  </g>
</svg>"""
    return "screenshot3_free_annotation_studio_1280x800.svg", svg, 1280, 800

def generate_screenshot_4():
    # Screenshot 4: Single Long Page PDF & Smart A4 Split (1280x800)
    svg = f"""<svg width="1280" height="800" viewBox="0 0 1280 800" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1280" height="800" fill="url(#bgGrad)"/>
  <circle cx="640" cy="400" r="300" fill="#06B6D4" opacity="0.12" filter="url(#glow)"/>

  <!-- Marketing Header -->
  <text x="640" y="65" font-family="-apple-system, Roboto, sans-serif" font-size="32" font-weight="800" fill="url(#textGrad)" text-anchor="middle">Single Continuous Long Page PDF or Smart A4 Split</text>
  <text x="640" y="98" font-family="-apple-system, Roboto, sans-serif" font-size="15" fill="#38BDF8" text-anchor="middle">Preserves full screenshot height on 1 single seamless page without forced splitting</text>

  <!-- Comparison Container -->
  <g transform="translate(140, 140)">
    <!-- Mode A: Continuous 1-Page (Recommended) -->
    <g transform="translate(0, 0)" filter="url(#shadow)">
      <rect width="460" height="580" rx="14" fill="#111827" stroke="#4F46E5" stroke-width="2"/>
      <!-- Header Badge -->
      <rect x="24" y="24" width="220" height="30" rx="15" fill="rgba(79, 70, 229, 0.2)" stroke="#4F46E5"/>
      <text x="134" y="44" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#C7D2FE" text-anchor="middle">⭐ 1 CONTINUOUS LONG PAGE</text>

      <text x="24" y="85" font-family="-apple-system, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">Full Image Sheet (No Split)</text>
      <text x="24" y="110" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">Exports whole page (up to 50,000px) as 1 endless page.</text>

      <!-- Graphic representation: Long unbroken page -->
      <g transform="translate(160, 140)" filter="url(#shadow)">
        <rect width="140" height="380" rx="4" fill="#FFFFFF"/>
        <rect x="15" y="15" width="60" height="8" rx="2" fill="#0F172A"/>
        <rect x="15" y="30" width="110" height="4" rx="1" fill="#94A3B8"/>
        <rect x="15" y="40" width="90" height="4" rx="1" fill="#CBD5E1"/>
        <rect x="15" y="60" width="110" height="120" rx="3" fill="#F1F5F9"/>
        <rect x="15" y="195" width="110" height="60" rx="3" fill="#0F172A"/>
        <rect x="15" y="270" width="110" height="90" rx="3" fill="#E2E8F0"/>
      </g>
    </g>

    <!-- Mode B: Smart A4 Split -->
    <g transform="translate(540, 0)" filter="url(#shadow)">
      <rect width="460" height="580" rx="14" fill="#111827" stroke="#374151" stroke-width="1.5"/>
      <!-- Header Badge -->
      <rect x="24" y="24" width="180" height="30" rx="15" fill="#1F2937" stroke="#374151"/>
      <text x="114" y="44" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#94A3B8" text-anchor="middle">📄 SMART A4 / LETTER SPLIT</text>

      <text x="24" y="85" font-family="-apple-system, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">Whitespace Scanline Guard</text>
      <text x="24" y="110" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">Never cuts text lines or paragraphs in half across pages.</text>

      <!-- Graphic representation: Stack of A4 pages -->
      <g transform="translate(130, 150)" filter="url(#shadow)">
        <!-- Page 1 -->
        <rect x="0" y="0" width="180" height="160" rx="4" fill="#FFFFFF"/>
        <text x="90" y="90" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#64748B" text-anchor="middle">Page 1</text>
        <!-- Clean Cut Indicator -->
        <line x1="0" y1="180" x2="200" y2="180" stroke="#10B981" stroke-width="2" stroke-dasharray="4"/>
        <!-- Page 2 -->
        <rect x="0" y="200" width="180" height="160" rx="4" fill="#FFFFFF"/>
        <text x="90" y="290" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#64748B" text-anchor="middle">Page 2</text>
      </g>
    </g>
  </g>
</svg>"""
    return "screenshot4_continuous_pdf_export_1280x800.svg", svg, 1280, 800

def generate_screenshot_5():
    # Screenshot 5: Local Privacy & Settings Dashboard (1280x800)
    svg = f"""<svg width="1280" height="800" viewBox="0 0 1280 800" xmlns="http://www.w3.org/2000/svg">
{DEFS}
  <rect width="1280" height="800" fill="url(#bgGrad)"/>
  <circle cx="640" cy="400" r="300" fill="#10B981" opacity="0.12" filter="url(#glow)"/>

  <!-- Marketing Header -->
  <text x="640" y="65" font-family="-apple-system, Roboto, sans-serif" font-size="32" font-weight="800" fill="url(#textGrad)" text-anchor="middle">100% Local On-Device Processing & Privacy Guarantee</text>
  <text x="640" y="98" font-family="-apple-system, Roboto, sans-serif" font-size="15" fill="#10B981" text-anchor="middle">Zero tracking, zero analytics, and customizable capture heuristics for heavy single-page apps</text>

  <!-- Options Card Mockup -->
  <g transform="translate(240, 140)" filter="url(#shadow)">
    <rect width="800" height="580" rx="16" fill="#111827" stroke="#374151" stroke-width="1.5"/>

    <!-- Privacy Banner Card -->
    <g transform="translate(30, 30)">
      <rect width="740" height="90" rx="12" fill="rgba(16, 185, 129, 0.08)" stroke="#10B981" stroke-width="1.5"/>
      <circle cx="45" cy="45" r="20" fill="#10B981"/>
      <text x="45" y="52" font-size="16" text-anchor="middle">🛡️</text>
      <text x="80" y="38" font-family="-apple-system, sans-serif" font-size="16" font-weight="800" fill="#FFFFFF">100% Private & Offline Guarantee</text>
      <text x="80" y="62" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">OmniSnap runs strictly on your computer. We never transmit images, browsing history, or telemetry.</text>
    </g>

    <!-- PDF Settings Row -->
    <g transform="translate(30, 145)">
      <rect width="740" height="75" rx="10" fill="#1F2937" stroke="#4F46E5" stroke-width="1"/>
      <text x="25" y="34" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Paper size / PDF Mode</text>
      <text x="25" y="54" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">1 Continuous Long Page matches entire screenshot height without splitting</text>
      <rect x="480" y="20" width="235" height="35" rx="6" fill="#1E1B4B" stroke="#6366F1"/>
      <text x="597" y="42" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#C7D2FE" text-anchor="middle">1 Continuous Long Page ▾</text>
    </g>

    <!-- Heuristics Row -->
    <g transform="translate(30, 235)">
      <rect width="740" height="75" rx="10" fill="#1F2937" stroke="#374151" stroke-width="1"/>
      <text x="25" y="34" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Scroll Delay between slices</text>
      <text x="25" y="54" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Paces scroll speed for heavy SPAs (Twitter, Notion, Linear) to populate lazy images</text>
      <rect x="550" y="20" width="165" height="35" rx="6" fill="#111827" stroke="#374151"/>
      <text x="632" y="42" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" fill="#FFFFFF" text-anchor="middle">Balanced (60ms) ▾</text>
    </g>

    <!-- Sticky Suppression Row -->
    <g transform="translate(30, 325)">
      <rect width="740" height="75" rx="10" fill="#1F2937" stroke="#374151" stroke-width="1"/>
      <text x="25" y="34" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Adjust Sticky & Repeating Elements</text>
      <text x="25" y="54" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Hides duplicate floating headers across long pages</text>
      <rect x="670" y="26" width="45" height="24" rx="12" fill="#10B981"/>
      <circle cx="700" cy="38" r="9" fill="#FFFFFF"/>
    </g>

    <!-- Active Hyperlinks Row -->
    <g transform="translate(30, 415)">
      <rect width="740" height="75" rx="10" fill="#1F2937" stroke="#374151" stroke-width="1"/>
      <text x="25" y="34" font-family="-apple-system, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Preserve Clickable Hyperlinks in PDF</text>
      <text x="25" y="54" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">Converts page links into active PDF web links</text>
      <rect x="670" y="26" width="45" height="24" rx="12" fill="#10B981"/>
      <circle cx="700" cy="38" r="9" fill="#FFFFFF"/>
    </g>

    <!-- Keyboard Shortcuts Summary -->
    <g transform="translate(30, 510)">
      <text x="10" y="25" font-family="-apple-system, sans-serif" font-size="12" fill="#94A3B8">Global Shortcuts: ⌥⇧P (Full Page)  •  ⌥⇧S (Selected Region)  •  ⌥⇧V (Viewport)</text>
    </g>
  </g>
</svg>"""
    return "screenshot5_privacy_settings_1280x800.svg", svg, 1280, 800

def main():
    generators = [
        generate_promo_small,
        generate_promo_marquee,
        generate_promo_large,
        generate_screenshot_1,
        generate_screenshot_2,
        generate_screenshot_3,
        generate_screenshot_4,
        generate_screenshot_5
    ]

    print("====================================================")
    print(" Generating Chrome Web Store Graphics & FigCraft Assets")
    print("====================================================")

    generated_files = []

    for gen in generators:
        filename, content, w, h = gen()
        svg_path = os.path.join(STORE_DIR, filename)
        with open(svg_path, "w") as f:
            f.write(content)
        
        # Render to PNG using macOS QuickLook
        png_name = filename.replace(".svg", ".png")
        png_target = os.path.join(STORE_DIR, png_name)
        
        # Use qlmanage to render SVG
        subprocess.run(["qlmanage", "-t", "-s", str(max(w, h)), "-o", STORE_DIR, svg_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ql_out = svg_path + ".png"
        if os.path.exists(ql_out):
            # Resample to exact target dimension using sips
            subprocess.run(["sips", "-z", str(h), str(w), ql_out, "--out", png_target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(ql_out) and ql_out != png_target:
                os.remove(ql_out)
        
        print(f"  ✓ Created: {png_name} ({w}×{h} px)")
        generated_files.append((filename, png_name, w, h))

    # Compile into FigCraft native project: design/OmniSnap_Store_Showcase.figcraft
    figcraft_project = os.path.join(DESIGN_DIR, "OmniSnap_Store_Showcase.figcraft")
    figcraft_doc = {
        "document": {
            "id": "0:0",
            "name": "OmniSnap - Chrome Web Store Graphics Suite",
            "type": "DOCUMENT",
            "children": [
                {
                    "id": f"1:{idx}",
                    "name": item[1],
                    "type": "FRAME",
                    "width": item[2],
                    "height": item[3],
                    "svg_source": item[0]
                }
                for idx, item in enumerate(generated_files)
            ]
        }
    }

    with zipfile.ZipFile(figcraft_project, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("document.json", json.dumps(figcraft_doc, indent=2))
        thumb_src = os.path.join(STORE_DIR, "promo_small_440x280.png")
        if os.path.exists(thumb_src):
            z.write(thumb_src, "thumbnail.png")

    print(f"\n  ✓ Created FigCraft Master Project: {figcraft_project}")
    print("====================================================")

if __name__ == "__main__":
    main()
