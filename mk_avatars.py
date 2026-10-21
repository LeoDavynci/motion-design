from PIL import Image, ImageDraw
N = [138, 104, 136, 122, 120, 110, 134, 134, 130]
S = 256
for i, n in enumerate(N):
    im = Image.open(f'assets/figma/av/a{i}.png').convert('RGBA')
    f = 60 / n; w = int(1024 * f); o = (1024 - w) // 2
    c = im.crop((o, o, o + w, o + w)).resize((S, S), Image.LANCZOS)
    # figma circle fill behind (pink-gold radial) shows through transparent pixels
    bg = Image.new('RGBA', (S, S), (232, 194, 46, 255))
    bg.alpha_composite(c)
    m = Image.new('L', (S * 4, S * 4), 0); ImageDraw.Draw(m).ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255); m = m.resize((S, S), Image.LANCZOS)
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0)); out.paste(bg, (0, 0), m)
    # white ring (2px of 60 -> ~8.5px of 256)
    ring = Image.new('L', (S * 4, S * 4), 0); d = ImageDraw.Draw(ring); d.ellipse((0, 0, S * 4 - 1, S * 4 - 1), fill=255); d.ellipse((34, 34, S * 4 - 35, S * 4 - 35), fill=0); ring = ring.resize((S, S), Image.LANCZOS)
    out.paste((255, 255, 255, 255), (0, 0), ring)
    out.save(f'assets/figma/av/z{i}.png')
sheet = Image.new('RGBA', (S * 9, S), (60, 60, 70, 255))
for i in range(9): sheet.alpha_composite(Image.open(f'assets/figma/av/z{i}.png'), (S * i, 0))
sheet.convert('RGB').save('assets/figma/av/sheet.png'); print('ok')
