// Typed lines, shared by the hook (index.html) and the "Introducing Peepl" section (intro.html). Typing motion after the
// user's screen recordings: letters fade and sharpen in, the caret jumps after each one and blinks when idle, the line
// glides to stay centered. A line can scale (a snap or a cut-zoom), and leaves either letter by letter (fade + blur,
// left to right, drifting left) or as a whole (slides off to the left while fading).
//
// A line: { parts: [{ text, start, every, lime }], caretFrom, clearAt, slideOut?, scale?(t), beats?: [[t0, t1]],
//           zoomTo?: { k, left } }  — zoomTo: at scale k the finished line's left edge sits at `left` (screen px), as in
//           the Figma frame; the pan grows with the scale so the zoom heads straight there.
import { clamp, track } from '../lib/motion.js';

export const FADE = 0.09;      // each letter fades and sharpens in over this long
export const TRACK = 4;        // -0.04em letter-spacing at 100px
export const snapEase = (x) => (x < 0.5 ? 8 * x ** 4 : 1 - (-2 * x + 2) ** 4 / 2);   // hard in and out (quartic)
export const smooth = (x) => (x < 0.5 ? 4 * x ** 3 : 1 - (-2 * x + 2) ** 3 / 2);     // cubic in and out
export const easeOut = (x) => 1 - (1 - x) ** 3;

export function makeLines(stage, LINES, o = {}) {
  const { exitStep = 0.014, exitFade = 0.22, exitDrift = 110, slide = { dist: 1500, dur: 0.75 }, shadow = true } = o;
  const lines = LINES.map((L) => {
    const el = document.createElement('div');
    el.className = 'line';
    const caret = document.createElement('i');
    caret.className = 'caret';
    el.appendChild(caret);
    stage.appendChild(el);
    const chars = [];
    for (const p of L.parts) [...p.text].forEach((ch, i) => chars.push({ ch, at: p.start + i * p.every, lime: !!p.lime }));
    const spans = chars.map((c) => {
      const sp = document.createElement('span');
      sp.textContent = c.ch;
      if (c.lime) sp.className = 'lime';
      el.insertBefore(sp, caret);
      return sp;
    });
    const exitEnd = L.slideOut ? L.clearAt + slide.dur : L.clearAt + (chars.length - 1) * exitStep + exitFade;
    return { ...L, el, caret, chars, spans, exitEnd, widths: [0] };
  });

  // From the rendered letters themselves (layout ignores their opacity / blur), so centering matches exactly
  const measure = () => {
    for (const L of lines) {
      L.el.style.transform = 'none';
      const left = L.el.getBoundingClientRect().left;
      L.widths = [0, ...L.spans.map((sp) => sp.getBoundingClientRect().right - left)];
    }
  };

  const paint = (t) => {
    const active = lines.findIndex((L) => t >= L.caretFrom && t < L.clearAt);
    lines.forEach((L, li) => {
      let n = 0;
      while (n < L.chars.length && L.chars[n].at <= t) n++;
      const k = L.scale ? L.scale(t) : 1;
      // Text shadow (Figma: 0 4px 24px black 25%), divided by the line's scale so it looks the same at every size
      const drop = shadow ? `0 ${(4 / k).toFixed(2)}px ${(24 / k).toFixed(2)}px rgba(0, 0, 0, 0.25)` : '';
      L.chars.forEach((c, i) => {
        const a = clamp((t - c.at) / FADE);
        const out = L.slideOut ? 0 : clamp((t - (L.clearAt + i * exitStep)) / exitFade);
        const e = easeOut(a) * (1 - easeOut(out));
        const blur = a < 1 ? (1 - easeOut(a)) * 6 : out > 0 ? easeOut(out) * 10 : 0;
        const sp = L.spans[i];
        sp.style.opacity = e.toFixed(3);
        sp.style.color = blur > 0.01 ? 'transparent' : '';
        const glow = blur > 0.01 ? `0 0 ${blur.toFixed(2)}px ${c.lime ? 'var(--lime)' : 'var(--ink)'}` : '';
        sp.style.textShadow = [glow, drop].filter(Boolean).join(', ');
      });
      // The line glides to stay centered: a spring toward -width/2 after each key (stacked springs, pure in t).
      // Centered as Figma does it: the last letter's (negative) letter-spacing isn't part of the line's width.
      const keys = [[0, 0], ...L.chars.map((c, i) => [c.at, -(L.widths[i + 1] + TRACK) / 2])];
      const off = track(t, keys, 140, 24);
      // Leaving: the line drifts left while its letters fade, or slides off to the left as a whole while fading
      const leave = Number.isFinite(L.clearAt) ? clamp((t - L.clearAt) / (L.exitEnd - L.clearAt)) : 0;
      const drift = L.slideOut ? -slide.dist * leave ** 2.2 : -exitDrift * smooth(leave);
      L.el.style.opacity = L.slideOut ? (1 - smooth(leave)).toFixed(3) : '1';
      // A zoom heads for the Figma framing: a pan that grows with the scale lands the left edge at zoomTo.left
      let pan = 0;
      if (L.zoomTo) {
        const W = L.widths[L.chars.length] + TRACK;
        const panEnd = L.zoomTo.left - 960 + (L.zoomTo.k * W) / 2;
        pan = (panEnd * (k - 1)) / (L.zoomTo.k - 1);
      }
      L.el.style.transform = `translate(${960 + pan + drift}px, 540px) scale(${k}) translate(${off}px, -50%)`;
      // Caret: right after the last letter; solid while typing (and through a snap), blinking (1s) when idle
      L.caret.style.left = `${L.widths[n] + 4}px`;
      const snapped = (L.beats ?? []).reduce((m, [a, b]) => (t >= a ? Math.max(m, Math.min(t, b)) : m), 0);
      const last = Math.max(n ? L.chars[n - 1].at : L.caretFrom, snapped);
      const idle = t - last;
      const blinkOn = idle < 0.45 || ((idle - 0.45) % 1.0) >= 0.5;
      L.caret.style.opacity = li === active && blinkOn ? '1' : '0';
    });
  };

  return { lines, measure, paint };
}

// For a cut-zoom between two keystrokes, like the reference recording: the cut lands right after `lastKey`, and the
// next part starts typing at the normal pace with no pause. Returns { zoom: [t0, t1], next } (next = next key time).
export function cutAfter(lastKey, every, dur = 0.07) {
  const t0 = lastKey + every * 0.45;
  return { zoom: [t0, t0 + dur], next: Math.max(lastKey + every * 1.6, t0 + dur + 0.02) };
}
