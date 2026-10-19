s = open('index.html', encoding='utf-8').read()


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, cnt)


# importmap for three.js + the 3D phone module
rep('<style>html,body{margin:0;background:#1c1522}canvas{display:block}</style></head>',
    '<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>\n<style>html,body{margin:0;background:#1c1522}canvas{display:block}</style></head>')
rep("import { BARS } from './assets/figma/profile_meta.js';", "import { BARS } from './assets/figma/profile_meta.js';\nimport { createPhone3D } from './lib/iphone3d.js';")
rep("const PO = mk(800, 1400); // shared offscreen for 3D phones", "const SCR = mk(786, 1704); // live screen texture for the 3D phone (2x of 393x852)\nlet P3 = null;")
rep("  await Promise.all([300, 400, 500, 600].map((w) => document.fonts.load(`${w} 100px Geist`)));", "  P3 = createPhone3D(W, H);\n  await Promise.all([300, 400, 500, 600].map((w) => document.fonts.load(`${w} 100px Geist`)));")

# replace the 2D phone + old phone3 with screen() + 3D phone3
a = s.index("// ---------- product: accurate iPhone 15 Pro")
b = s.index("function rig(t, t0, t1)")
new = """// ---------- product: the screen content is drawn to a texture; lib/iphone3d.js wraps it in a real 3D iPhone 15 Pro ----------
function screen(layers, o = {}) {
  const { t = 0, taps = [], island = false } = o, prev = ctx; ctx = SCR.getContext('2d');
  const sw = SCR.width, sh = SCR.height;
  ctx.save(); ctx.clearRect(0, 0, sw, sh); ctx.translate(sw / 2, sh / 2);
  ctx.fillStyle = '#f4efe7'; ctx.fillRect(-sw / 2, -sh / 2, sw, sh);
  for (const L of layers) {
    const draw = (im, a) => { if (!im) return; ctx.save(); ctx.globalAlpha *= a; ctx.drawImage(im, 4, 4, im.width - 8, im.height - 8, -sw / 2, -sh / 2, sw, sh); ctx.restore(); };
    if (L.cv) { // a Figma-built screen, optionally as a sheet sliding up over what is behind it
      const k = sw / 390, ty = (L.ty || 0) * k, rad = ty > 1 ? 46 * k : 0;
      if (L.scrim) { ctx.fillStyle = `rgba(14,10,22,${L.scrim})`; ctx.fillRect(-sw / 2, -sh / 2, sw, sh); }
      ctx.save(); ctx.beginPath(); ctx.roundRect(-sw / 2, -sh / 2 + ty, sw, sh - ty + 2, [rad, rad, 0, 0]); ctx.clip();
      ctx.drawImage(L.cv, 0, 0, 390, 844, -sw / 2, -sh / 2 + ty, sw, sh); ctx.restore();
      if (ty > 1) { ctx.fillStyle = 'rgba(255,255,255,0.55)'; ctx.beginPath(); ctx.roundRect(-sw * 0.045, -sh / 2 + ty + 8 * k, sw * 0.09, 4 * k, 2 * k); ctx.fill(); }
      continue;
    }
    draw(L.im, 1); if (L.im2) draw(L.im2, L.mix);
  }
  if (island) { ctx.fillStyle = '#000'; rr(-sw * 0.1575, -sh / 2 + sw * 0.028, sw * 0.315, sw * 0.092, sw * 0.046); ctx.fill(); }
  for (const [t0, tfx, tfy] of taps) { // the thumb: a soft white dot that glides in, presses, ripples and lifts away
    const u = t - t0; if (u < -0.9 || u > 0.9) continue;
    const px = (tfx - 0.5) * sw, py = (tfy - 0.5) * sh, m = ease((u + 0.9) / 0.9), fade = u < 0.45 ? 1 : 1 - clamp((u - 0.45) / 0.45);
    if (u >= 0) {
      const ring2 = ease(u / 0.8);
      ctx.strokeStyle = `rgba(255,255,255,${0.9 * (1 - ring2)})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(px, py, sw * (0.05 + 0.15 * ring2), 0, 7); ctx.stroke();
      ctx.strokeStyle = `rgba(22,18,28,${0.18 * (1 - ring2)})`; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(px, py, sw * (0.056 + 0.15 * ring2), 0, 7); ctx.stroke();
    }
    const bob = Math.sin((u + 0.9) * 7) * (1 - m) * sw * 0.012, ax = px + (1 - m) * sw * 0.34, ay = py + (1 - m) * sh * 0.2 + bob, press = clamp(u / 0.1) * (1 - clamp((u - 0.22) / 0.22)), R = sw * 0.05 * (1 - 0.2 * press);
    ctx.save(); ctx.globalAlpha = fade; ctx.shadowColor = 'rgba(10,6,20,0.32)'; ctx.shadowBlur = sw * 0.04; ctx.shadowOffsetY = sw * 0.012;
    ctx.fillStyle = 'rgba(255,255,255,0.96)'; ctx.beginPath(); ctx.arc(ax, ay, R, 0, 7); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = 'rgba(22,18,28,0.14)'; ctx.lineWidth = 2.5; ctx.stroke(); ctx.restore();
  }
  ctx.restore(); ctx = prev;
}
function phone3(layers, cx, cy, sh, o = {}) { // true 3D: yaw (ry), pitch (rx), roll (rot), thickness, reflections
  const { ry = 0, rx = 0, rot = 0, dx = 0, dy = 0, sc = 1, shadow = 0.42 } = o;
  screen(layers, o);
  P3.render(SCR, { cx: cx + dx, cy: cy + dy, sh, sc, rx, ry, rz: rot });
  ctx.save(); ctx.shadowColor = `rgba(8,4,14,${shadow})`; ctx.shadowBlur = 90; ctx.shadowOffsetY = 46; ctx.drawImage(P3.canvas, 0, 0); ctx.restore();
}
"""
s = s[:a] + new + s[b:]
s = s.replace("// Peepl launch film v5:", "// Peepl launch film v7:")
open('index.html', 'w', encoding='utf-8').write(s)
print('patched')
