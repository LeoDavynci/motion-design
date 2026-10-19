// A real 3D iPhone 15 Pro for the render page. Units are screen pixels: the camera is set so z=0 maps 1:1 to the 1920x1080 canvas,
// so a phone placed at (cx, cy) with height sh lands exactly where the 2D layout expects it, but with true thickness and perspective.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const SH = 1000, SW = SH * 393 / 852;                 // reference screen size (scaled per call)
const BZ = SW * 0.028, RING = SW * 0.012, R = SW * 0.14; // black bezel, titanium ring, screen corner radius (55pt of 393)
const BW = SW + 2 * (BZ + RING), BH = SH + 2 * (BZ + RING), RB = R + BZ + RING;
const T = BW * 0.1169;                                  // 8.25mm thick on a 70.6mm wide body

function roundedRect(w, h, r) {
  const s = new THREE.Shape(), x = -w / 2, y = -h / 2;
  s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.absarc(x + w - r, y + r, r, -Math.PI / 2, 0, false);
  s.lineTo(x + w, y + h - r); s.absarc(x + w - r, y + h - r, r, 0, Math.PI / 2, false);
  s.lineTo(x + r, y + h); s.absarc(x + r, y + h - r, r, Math.PI / 2, Math.PI, false);
  s.lineTo(x, y + r); s.absarc(x + r, y + r, r, Math.PI, Math.PI * 1.5, false);
  return s;
}
function planeGeo(w, h, r) { // flat rounded plate with 0..1 UVs
  const g = new THREE.ShapeGeometry(roundedRect(w, h, r), 48), p = g.attributes.position, uv = g.attributes.uv;
  for (let i = 0; i < p.count; i++) uv.setXY(i, (p.getX(i) + w / 2) / w, (p.getY(i) + h / 2) / h);
  return g;
}

export function createPhone3D(W, H) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.03).texture;
  const f = 1500, camera = new THREE.PerspectiveCamera(2 * Math.atan(H / 2 / f) * 180 / Math.PI, W / H, 10, 8000);
  camera.position.set(0, 0, f);
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-500, 700, 900); scene.add(key);
  const rim = new THREE.DirectionalLight(0xbcd0ff, 1.1); rim.position.set(700, -200, -300); scene.add(rim);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  const tex = new THREE.CanvasTexture(document.createElement('canvas')); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  const titanium = new THREE.MeshStandardMaterial({ color: 0xb3b4b9, metalness: 1, roughness: 0.36, envMapIntensity: 1.25 });
  const group = new THREE.Group(); scene.add(group);

  // titanium body: rounded-rect extrusion with a soft bevel so the edge catches light
  const bev = 7, body = new THREE.Mesh(new THREE.ExtrudeGeometry(roundedRect(BW, BH, RB), { depth: T - 2 * bev, bevelEnabled: true, bevelSize: bev, bevelThickness: bev, bevelSegments: 8, curveSegments: 40 }), titanium);
  body.geometry.translate(0, 0, -(T - 2 * bev) / 2); group.add(body);
  const front = T / 2 + bev;                                  // front face of the extrusion
  const bezel = new THREE.Mesh(planeGeo(SW + 2 * BZ, SH + 2 * BZ, R + BZ), new THREE.MeshStandardMaterial({ color: 0x07060a, roughness: 0.22, metalness: 0.1 })); bezel.position.z = front + 0.3; group.add(bezel);
  const screen = new THREE.Mesh(planeGeo(SW, SH, R), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false })); screen.position.z = front + 0.6; group.add(screen);
  const glass = new THREE.Mesh(planeGeo(SW, SH, R), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: 0.07, roughness: 0.04, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.03, envMapIntensity: 1.4 })); glass.position.z = front + 1; group.add(glass);
  const back = new THREE.Mesh(planeGeo(BW - 6, BH - 6, RB - 3), new THREE.MeshStandardMaterial({ color: 0xd7d8dc, roughness: 0.55, metalness: 0.15 })); back.rotation.y = Math.PI; back.position.z = -front - 0.3; group.add(back);
  const btn = (side, y0, hh) => { // side buttons sit proud of the titanium edge
    const m = new THREE.Mesh(new THREE.BoxGeometry(9, hh * SH, 16), titanium); m.position.set(side * (BW / 2 + 1), SH / 2 - (y0 + hh / 2) * SH, 0); m.geometry.translate(side * 1.5, 0, 0); group.add(m);
  };
  btn(-1, 0.145, 0.032); btn(-1, 0.215, 0.066); btn(-1, 0.30, 0.066); btn(1, 0.25, 0.10);

  return {
    canvas: renderer.domElement,
    // screenCanvas = 393:852 portrait canvas with the live screen; cx,cy,sh in 1920x1080 pixels; angles in degrees
    render(screenCanvas, { cx, cy, sh, sc = 1, rx = 0, ry = 0, rz = 0 }) {
      if (tex.image !== screenCanvas) { tex.image = screenCanvas; }
      tex.needsUpdate = true;
      group.position.set(cx - W / 2, H / 2 - cy, 0);
      group.scale.setScalar(sh / SH * sc);
      group.rotation.order = 'ZYX'; group.rotation.set(rx * Math.PI / 180, ry * Math.PI / 180, -rz * Math.PI / 180);
      renderer.render(scene, camera);
    }
  };
}
