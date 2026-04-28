"""
Создаёт иконку icon.ico для Network Learning Lab.
Требует: pip install pillow
"""
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

import struct
import zlib
import os

# ─── Путь ────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')


def make_with_pillow():
    """Красивая иконка через Pillow."""
    sizes = [16, 32, 48, 64, 256]
    images = []

    for sz in sizes:
        img = Image.new('RGBA', (sz, sz), (13, 17, 23, 255))
        d   = ImageDraw.Draw(img)

        scale = sz / 64

        def s(v):   return int(v * scale)
        def sc(v):  return int(v * scale + 0.5)

        # Background circle
        pad = s(3)
        d.ellipse([pad, pad, sz-pad, sz-pad],
                  fill=(22, 27, 34, 255), outline=(88, 166, 255, 255),
                  width=max(1, s(2)))

        # Root switch (gold square, top center)
        rx, ry = sz//2, s(16)
        rw, rh = sc(10), sc(7)
        d.rectangle([rx-rw, ry-rh, rx+rw, ry+rh],
                    fill=(58, 42, 0, 255), outline=(227, 179, 65, 255),
                    width=max(1, s(1)))
        if sz >= 32:
            d.text((rx, ry - rh - s(3)), '★',
                   fill=(227, 179, 65, 255), anchor='ms')

        # Left child switch (blue)
        lx, ly = s(18), s(42)
        lw, lh = sc(9), sc(6)
        d.rectangle([lx-lw, ly-lh, lx+lw, ly+lh],
                    fill=(13, 32, 64, 255), outline=(88, 166, 255, 255),
                    width=max(1, s(1)))

        # Right child switch (blue)
        rx2, ry2 = sz - s(18), s(42)
        d.rectangle([rx2-lw, ry2-lh, rx2+lw, ry2+lh],
                    fill=(13, 32, 64, 255), outline=(88, 166, 255, 255),
                    width=max(1, s(1)))

        # Bottom switch (blue)
        bx, by = sz//2, sz - s(16)
        bw, bh = sc(9), sc(6)
        d.rectangle([bx-bw, by-bh, bx+bw, by+bh],
                    fill=(13, 32, 64, 255), outline=(88, 166, 255, 255),
                    width=max(1, s(1)))

        # Forwarding lines (green)
        lw_line = max(1, s(2))
        d.line([(sz//2, s(16)+rh), (lx, ly-lh)],
               fill=(63, 185, 80, 255), width=lw_line)
        d.line([(sz//2, s(16)+rh), (rx2, ry2-lh)],
               fill=(63, 185, 80, 255), width=lw_line)
        d.line([(lx, ly+lh), (bx, by-bh)],
               fill=(63, 185, 80, 255), width=lw_line)

        # Blocked line (red dashed — simplified as thin red)
        d.line([(rx2, ry2+lh), (bx, by-bh)],
               fill=(248, 81, 73, 255), width=max(1, s(1)))

        images.append(img)

    images[0].save(OUT, format='ICO',
                   sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f'[OK] Иконка создана (Pillow): {OUT}')


def make_fallback():
    """Простая иконка в чистом Python (без зависимостей)."""
    # Создаём минимальный PNG 32x32 вручную, потом пакуем в ICO

    def _make_png_32():
        W = H = 32
        # RGBA данные: сетевой граф
        pixels = []
        BG = (13, 17, 23, 255)
        GOLD = (227, 179, 65, 255)
        BLUE = (88, 166, 255, 255)
        GREEN = (63, 185, 80, 255)
        RED = (248, 81, 73, 255)
        DARK = (22, 27, 34, 255)

        for y in range(H):
            row = []
            for x in range(W):
                # Default background
                col = BG

                cx, cy = W//2, H//2
                dist = ((x-cx)**2 + (y-cy)**2)**0.5
                if dist < 14:
                    col = DARK

                # Root switch box: 10..22 x, 3..9 y
                if 10 <= x <= 22 and 3 <= y <= 9:
                    col = (58, 42, 0, 255)
                if (x in (10, 22) and 3 <= y <= 9) or (y in (3, 9) and 10 <= x <= 22):
                    col = GOLD

                # Left child: 2..10 x, 19..25 y
                if 2 <= x <= 10 and 19 <= y <= 25:
                    col = (13, 32, 64, 255)
                if (x in (2, 10) and 19 <= y <= 25) or (y in (19, 25) and 2 <= x <= 10):
                    col = BLUE

                # Right child: 22..30 x, 19..25 y
                if 22 <= x <= 30 and 19 <= y <= 25:
                    col = (13, 32, 64, 255)
                if (x in (22, 30) and 19 <= y <= 25) or (y in (19, 25) and 22 <= x <= 30):
                    col = BLUE

                # Bottom: 10..22 x, 24..30 y
                if 10 <= x <= 22 and 24 <= y <= 30:
                    col = (13, 32, 64, 255)
                if (x in (10, 22) and 24 <= y <= 30) or (y in (24, 30) and 10 <= x <= 22):
                    col = BLUE

                # Green lines
                # Root to left: from (16,9) to (6,19) — rough
                t = (y - 9) / 10 if 9 <= y <= 19 else -1
                if 0 <= t <= 1:
                    lx_expected = int(16 + t * (6 - 16))
                    if abs(x - lx_expected) <= 1:
                        col = GREEN

                # Root to right
                t2 = (y - 9) / 10 if 9 <= y <= 19 else -1
                if 0 <= t2 <= 1:
                    lx2 = int(16 + t2 * (26 - 16))
                    if abs(x - lx2) <= 1:
                        col = GREEN

                # Left to bottom
                t3 = (y - 25) / 5 if 25 <= y <= 24 else -1

                # Red blocked line (right to bottom)
                t4 = (y - 25) / 5 if 25 <= y <= 30 else -1
                if 0 <= t4 <= 1:
                    lx4 = int(26 + t4 * (16 - 26))
                    if abs(x - lx4) <= 1:
                        col = RED

                row.append(col)
            pixels.append(row)

        # Build PNG
        def chunk(name, data):
            c = name + data
            return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

        sig = b'\x89PNG\r\n\x1a\n'
        ihdr_data = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
        # RGB (no alpha for simplicity)
        raw = b''
        for row in pixels:
            raw += b'\x00'
            for r, g, b, a in row:
                raw += bytes([r, g, b])
        compressed = zlib.compress(raw, 9)

        ihdr_data = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
        png = sig + chunk(b'IHDR', ihdr_data) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')
        return png

    png_data = _make_png_32()

    # ICO file format
    # Header: reserved(2) + type(2) + count(2)
    count = 1
    ico_header = struct.pack('<HHH', 0, 1, count)

    # Image directory entry: width(1) + height(1) + colorCount(1) + reserved(1)
    #   + planes(2) + bitCount(2) + bytesInRes(4) + imageOffset(4)
    img_size   = len(png_data)
    dir_size   = 16
    hdr_size   = 6
    img_offset = hdr_size + dir_size * count

    dir_entry = struct.pack('<BBBBHHII',
                            0, 0, 0, 0,   # 0 = use PNG size
                            1, 32,         # planes, bit count
                            img_size,
                            img_offset)

    with open(OUT, 'wb') as f:
        f.write(ico_header)
        f.write(dir_entry)
        f.write(png_data)

    print(f'[OK] Иконка создана (fallback PNG-in-ICO): {OUT}')


if __name__ == '__main__':
    if PIL_OK:
        make_with_pillow()
    else:
        print('[INFO] Pillow не установлен, создаём упрощённую иконку...')
        make_fallback()
