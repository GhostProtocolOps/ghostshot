#!/usr/bin/env python3
import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGN_DIR = os.path.join(ROOT_DIR, "design")
os.makedirs(DESIGN_DIR, exist_ok=True)

svg_content = """<svg width="1280" height="520" viewBox="0 0 1280 520" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080C14"/>
      <stop offset="50%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#0A0F1D"/>
    </linearGradient>
    <linearGradient id="primaryGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="50%" stop-color="#4F46E5"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="accentCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>
    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="rgba(30, 41, 59, 0.85)"/>
      <stop offset="100%" stop-color="rgba(15, 23, 42, 0.95)"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="32" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="30" flood-color="#000000" flood-opacity="0.7"/>
    </filter>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255, 255, 255, 0.03)" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Background -->
  <rect width="1280" height="520" fill="url(#bgGrad)"/>
  <rect width="1280" height="520" fill="url(#grid)"/>

  <!-- Ambient Glow Orbs -->
  <circle cx="220" cy="220" r="260" fill="#4F46E5" opacity="0.22" filter="url(#glow)"/>
  <circle cx="980" cy="260" r="280" fill="#06B6D4" opacity="0.18" filter="url(#glow)"/>
  <circle cx="640" cy="460" r="220" fill="#10B981" opacity="0.12" filter="url(#glow)"/>

  <!-- Left Content Column -->
  <g transform="translate(80, 80)">
    <!-- Top Pill Badge -->
    <g transform="translate(0, 0)">
      <rect width="270" height="32" rx="16" fill="rgba(99, 102, 241, 0.15)" stroke="rgba(99, 102, 241, 0.4)" stroke-width="1"/>
      <circle cx="16" cy="16" r="4" fill="#38BDF8"/>
      <text x="30" y="21" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#E2E8F0" letter-spacing="0.5">NEXT-GEN BROWSER CAPTURE</text>
    </g>

    <!-- Main Title & Logo Lockup -->
    <g transform="translate(0, 52)">
      <!-- Brand Aperture Icon -->
      <g filter="url(#shadow)">
        <rect width="64" height="64" rx="18" fill="url(#primaryGrad)"/>
        <!-- Camera Aperture Geometry -->
        <circle cx="32" cy="32" r="16" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
        <circle cx="32" cy="32" r="7" fill="#FFFFFF"/>
        <line x1="32" y1="16" x2="43" y2="23" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="48" y1="32" x2="41" y2="43" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="32" y1="48" x2="21" y2="41" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <line x1="16" y1="32" x2="23" y2="21" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
      </g>
      <text x="82" y="47" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="46" font-weight="800" fill="url(#textGrad)" letter-spacing="-1">GhostShot</text>
      <rect x="312" y="18" width="58" height="24" rx="12" fill="rgba(6, 182, 212, 0.2)" stroke="#06B6D4" stroke-width="1"/>
      <text x="341" y="34" font-family="-apple-system, sans-serif" font-size="11" font-weight="700" fill="#38BDF8" text-anchor="middle">v1.0.0</text>
    </g>

    <!-- Tagline -->
    <text x="0" y="160" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="600" fill="url(#accentCyan)">Full-Page Scrolling Capture &amp; Annotation Studio</text>
    <text x="0" y="195" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="400" fill="#94A3B8">Ultra-tall 20,000+ px pages • Nested scroll containers • 1-Page continuous PDF • Zero telemetry</text>

    <!-- Feature Pills Strip -->
    <g transform="translate(0, 230)">
      <!-- Pill 1: 100% Free -->
      <g transform="translate(0, 0)">
        <rect width="130" height="34" rx="8" fill="rgba(16, 185, 129, 0.12)" stroke="rgba(16, 185, 129, 0.35)" stroke-width="1"/>
        <text x="65" y="22" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#10B981" text-anchor="middle">✓ 100% Free</text>
      </g>
      <!-- Pill 2: Zero Telemetry -->
      <g transform="translate(142, 0)">
        <rect width="145" height="34" rx="8" fill="rgba(6, 182, 212, 0.12)" stroke="rgba(6, 182, 212, 0.35)" stroke-width="1"/>
        <text x="72" y="22" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#06B6D4" text-anchor="middle">⚡ Zero Telemetry</text>
      </g>
      <!-- Pill 3: Cross Browser -->
      <g transform="translate(299, 0)">
        <rect width="140" height="34" rx="8" fill="rgba(99, 102, 241, 0.12)" stroke="rgba(99, 102, 241, 0.35)" stroke-width="1"/>
        <text x="70" y="22" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#A5B4FC" text-anchor="middle">🌐 Cross-Browser</text>
      </g>
    </g>

    <!-- Shortcuts Footer -->
    <g transform="translate(0, 305)">
      <text x="0" y="0" font-family="-apple-system, sans-serif" font-size="12" fill="#64748B">Shortcuts: <tspan fill="#CBD5E1" font-weight="600">⌥⇧P</tspan> Full Page  •  <tspan fill="#CBD5E1" font-weight="600">⌥⇧S</tspan> Crop Region  •  <tspan fill="#CBD5E1" font-weight="600">⌥⇧V</tspan> Viewport Area</text>
    </g>
  </g>

  <!-- Right Hero Visual Mockup Window -->
  <g transform="translate(680, 60)" filter="url(#shadow)">
    <!-- Browser Window Card -->
    <rect width="530" height="400" rx="16" fill="url(#cardGrad)" stroke="rgba(255, 255, 255, 0.1)" stroke-width="1"/>
    
    <!-- Window Header -->
    <rect width="530" height="42" rx="16" fill="rgba(15, 23, 42, 0.8)"/>
    <circle cx="24" cy="21" r="6" fill="#EF4444"/>
    <circle cx="44" cy="21" r="6" fill="#F59E0B"/>
    <circle cx="64" cy="21" r="6" fill="#10B981"/>
    
    <!-- Window Address Bar -->
    <rect x="90" y="10" width="350" height="22" rx="11" fill="rgba(255, 255, 255, 0.05)" stroke="rgba(255, 255, 255, 0.08)" stroke-width="1"/>
    <text x="265" y="25" font-family="-apple-system, sans-serif" font-size="10" fill="#94A3B8" text-anchor="middle">https://apple.com/shop/buy-mac/macbook-pro</text>

    <!-- Window Body Page Simulation -->
    <g transform="translate(24, 60)">
      <!-- Simulated Apple Page Header -->
      <rect width="482" height="30" rx="6" fill="rgba(255, 255, 255, 0.04)"/>
      <rect x="16" y="9" width="80" height="12" rx="3" fill="#6366F1" opacity="0.6"/>
      <rect x="110" y="11" width="40" height="8" rx="2" fill="#94A3B8" opacity="0.4"/>
      <rect x="160" y="11" width="50" height="8" rx="2" fill="#94A3B8" opacity="0.4"/>

      <!-- Big Hero Showcase Image -->
      <rect y="42" width="482" height="150" rx="8" fill="rgba(30, 41, 59, 0.6)" stroke="rgba(255, 255, 255, 0.06)" stroke-width="1"/>
      <text x="241" y="95" font-family="-apple-system, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">MacBook Pro with M4 Max</text>
      <text x="241" y="120" font-family="-apple-system, sans-serif" font-size="11" fill="#06B6D4" text-anchor="middle">11,390px Continuous Full-Height Capture</text>

      <!-- Scroll Slices Grid Mini Indicator -->
      <g transform="translate(0, 205)">
        <rect width="112" height="60" rx="6" fill="rgba(255, 255, 255, 0.03)" stroke="rgba(255, 255, 255, 0.05)"/>
        <text x="56" y="28" font-family="-apple-system, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">Slice 1..4</text>
        <text x="56" y="44" font-family="-apple-system, sans-serif" font-size="9" fill="#10B981" text-anchor="middle">✓ Stitched</text>

        <rect x="124" y="0" width="112" height="60" rx="6" fill="rgba(255, 255, 255, 0.03)" stroke="rgba(255, 255, 255, 0.05)"/>
        <text x="180" y="28" font-family="-apple-system, sans-serif" font-size="10" font-weight="700" fill="#FFFFFF" text-anchor="middle">Slice 5..8</text>
        <text x="180" y="44" font-family="-apple-system, sans-serif" font-size="9" fill="#10B981" text-anchor="middle">✓ Stitched</text>

        <rect x="248" y="0" width="112" height="60" rx="6" fill="rgba(99, 102, 241, 0.15)" stroke="#6366F1" stroke-width="1.5"/>
        <text x="304" y="28" font-family="-apple-system, sans-serif" font-size="10" font-weight="700" fill="#38BDF8" text-anchor="middle">Slice 9..12</text>
        <text x="304" y="44" font-family="-apple-system, sans-serif" font-size="9" fill="#F59E0B" text-anchor="middle">⚡ Capturing...</text>

        <rect x="370" y="0" width="112" height="60" rx="6" fill="rgba(255, 255, 255, 0.03)" stroke="rgba(255, 255, 255, 0.05)"/>
        <text x="426" y="28" font-family="-apple-system, sans-serif" font-size="10" font-weight="700" fill="#64748B" text-anchor="middle">Slice 13..15</text>
        <text x="426" y="44" font-family="-apple-system, sans-serif" font-size="9" fill="#64748B" text-anchor="middle">Queued</text>
      </g>
    </g>

    <!-- Floating HUD Capsule -->
    <g transform="translate(145, 335)" filter="url(#shadow)">
      <rect width="240" height="44" rx="22" fill="#1E293B" stroke="rgba(99, 102, 241, 0.6)" stroke-width="1.5"/>
      <circle cx="28" cy="22" r="12" fill="none" stroke="rgba(255, 255, 255, 0.15)" stroke-width="3"/>
      <circle cx="28" cy="22" r="12" fill="none" stroke="#06B6D4" stroke-width="3" stroke-dasharray="75" stroke-dashoffset="25"/>
      <text x="50" y="27" font-family="-apple-system, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">Capturing 80%</text>
      <text x="145" y="26" font-family="-apple-system, sans-serif" font-size="11" fill="#94A3B8">|  Tile 1/2</text>
      <rect x="195" y="11" width="32" height="22" rx="11" fill="rgba(239, 68, 68, 0.2)"/>
      <text x="211" y="25" font-family="-apple-system, sans-serif" font-size="10" font-weight="700" fill="#EF4444" text-anchor="middle">Esc</text>
    </g>
  </g>
</svg>"""

svg_path = os.path.join(DESIGN_DIR, "ghostshot_github_cover.svg")
png_path = os.path.join(DESIGN_DIR, "ghostshot_github_cover.png")

with open(svg_path, "w") as f:
    f.write(svg_content)

print(f"1. Saved SVG to {svg_path}")

subprocess.run(["qlmanage", "-t", "-s", "1280", "-o", DESIGN_DIR, svg_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ql_out = svg_path + ".png"
if os.path.exists(ql_out):
    subprocess.run(["sips", "-z", "520", "1280", ql_out, "--out", png_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(ql_out) and ql_out != png_path:
        os.remove(ql_out)
    print(f"2. Rendered PNG to {png_path} (1280x520)")
else:
    print("Warning: qlmanage output not found")
