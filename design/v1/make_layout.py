"""Generate an envelope layout, not manufacturing CAD or a physics simulation.

Run: python3 design/v1/make_layout.py
Requires Pillow for the PNG diagram. All dimensions are provisional millimetres.
"""

import csv
import json
import os
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
# x across body, y forward, z up. Envelopes include approximate connector space
# only where explicitly stated; mounts, bends, heat and loads remain unchecked.
PARTS = [
    dict(id="hip_l", label="Левое бедро", center=[-22, 0, 81], size=[34, 15, 30], zone="body", kind="servo"),
    dict(id="hip_r", label="Правое бедро", center=[22, 0, 81], size=[34, 15, 30], zone="body", kind="servo"),
    dict(id="battery", label="Аккумулятор 2S", center=[0, 0, 107], size=[50, 30, 18], zone="body", kind="battery"),
    dict(id="pi", label="Raspberry Pi", center=[0, -22, 105], size=[65, 6, 30], zone="body", kind="logic"),
    dict(id="esp32", label="ESP32", center=[0, 22, 108], size=[52, 7, 28], zone="body", kind="logic"),
    dict(id="servo_bec", label="UBEC приводов", center=[0, -18, 76], size=[50, 17, 10], zone="body", kind="power"),
    dict(id="logic_bec", label="UBEC логики", center=[0, 18, 75], size=[43, 17, 7], zone="body", kind="power"),
    dict(id="imu", label="IMU", center=[0, 0, 120], size=[20, 16, 4], zone="body", kind="logic"),
    dict(id="amp", label="Усилитель", center=[35, 0, 108], size=[3, 18, 18], zone="body", kind="audio"),
    dict(id="mic", label="Микрофон", center=[-35, 0, 108], size=[3, 14, 18], zone="body", kind="audio"),
    dict(id="speaker", label="Динамик", center=[0, 24, 86], size=[28, 5, 12], zone="body", kind="audio"),
    dict(id="head_yaw", label="Поворот головы", center=[0, 0, 137], size=[23, 12, 29], zone="neck", kind="servo"),
    dict(id="head_pitch", label="Наклон головы", center=[23, 0, 171], size=[12, 23, 29], zone="head", kind="servo"),
    dict(id="camera", label="Камера", center=[0, 12, 171], size=[25, 9, 24], zone="head", kind="logic"),
    dict(id="foot_l", label="Левая ступня", center=[-29, 0, 25], size=[34, 29, 15], zone="leg", kind="servo"),
    dict(id="foot_r", label="Правая ступня", center=[29, 0, 25], size=[34, 29, 15], zone="leg", kind="servo"),
]
SHELLS = [
    dict(id="body_shell", center=[0, 0, 94], size=[84, 58, 60]),
    dict(id="head_shell", center=[0, 0, 171], size=[76, 38, 42]),
    dict(id="sole_l", center=[-29, 0, 7], size=[48, 68, 14]),
    dict(id="sole_r", center=[29, 0, 7], size=[48, 68, 14]),
]
COLORS = {"servo": "#bd7c48", "battery": "#829972", "logic": "#628ca0", "power": "#b59a59", "audio": "#a48fa6"}


def bounds(part):
    return [(c - s / 2, c + s / 2) for c, s in zip(part["center"], part["size"])]


def overlaps(a, b):
    return all(min(ah, bh) > max(al, bl) for (al, ah), (bl, bh) in zip(bounds(a), bounds(b)))


def validate():
    collisions = [(a["id"], b["id"]) for a, b in combinations(PARTS, 2) if overlaps(a, b)]
    body_inner = [(-40, 40), (-27, 27), (66, 122)]
    outside = [p["id"] for p in PARTS if p["zone"] == "body" and any(lo < il or hi > ih for (lo, hi), (il, ih) in zip(bounds(p), body_inner))]
    with (ROOT / "bom.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    totals = {edge: sum(int(r["quantity"]) * int(r[f"unit_{edge}_rub"]) for r in rows) for edge in ("min", "max")}
    return dict(envelope_collisions=collisions, body_envelopes_outside_inner_volume=outside,
                bom_rub=totals, height_mm=192, overall_stance_width_mm=106,
                limitations="AABB check only; no mounting/connector/cable/structural/thermal/kinematic validation. Sizes are target envelopes, not certified selected-product dimensions.")


def font(size):
    candidates = [
        os.environ.get("ROBOT_FONT_PATH"),
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    raise RuntimeError("Install Arial/DejaVu Sans or set ROBOT_FONT_PATH to a Cyrillic-capable font.")


def draw_layout():
    im = Image.new("RGB", (1600, 1120), "#f6f4ef")
    d = ImageDraw.Draw(im)
    d.text((55, 35), "V1 · КОМПОНОВКА ВНУТРИ КОРПУСА", font=font(31), fill="#263238")
    d.text((55, 80), "Габаритные блоки · размеры предварительные · не чертёж для сборки", font=font(22), fill="#556168")
    scale = 3.4
    for origin_x, axis, title, selected in [
        (430, 0, "Спереди · ширина корпуса 84 мм", ["hip_l", "hip_r", "battery", "imu", "head_yaw", "head_pitch", "camera", "foot_l", "foot_r"]),
        (1180, 1, "Сбоку · глубина корпуса 58 мм", ["pi", "esp32", "battery", "servo_bec", "logic_bec", "speaker", "head_yaw", "camera", "foot_r"]),
    ]:
        bottom = 845
        d.text((origin_x - 260, 145), title, font=font(23), fill="#263238")
        def rectangle(part):
            bb = bounds(part)
            return (origin_x + bb[axis][0]*scale, bottom-bb[2][1]*scale,
                    origin_x + bb[axis][1]*scale, bottom-bb[2][0]*scale)
        for shell in SHELLS:
            d.rounded_rectangle(rectangle(shell), radius=12, outline="#7c8585", width=3)
        for x in (-29, 29) if axis == 0 else (0,):
            xx = origin_x + x*scale
            d.line((xx, bottom-34*scale, xx, bottom-64*scale), fill="#7c8585", width=13)
        for part_id in selected:
            p = next(p for p in PARTS if p["id"] == part_id)
            rect = rectangle(p)
            d.rounded_rectangle(rect, radius=5, fill=COLORS[p["kind"]], outline="#f6f4ef", width=2)
            # Compact IDs avoid illegible labels inside thin boards.
            if axis == 0 and part_id == "battery":
                d.text((rect[0]+12, rect[1]+14), "2S", font=font(22), fill="#172229")
            if axis == 1 and part_id in ("pi", "esp32"):
                xtext = rect[0]-100 if part_id == "pi" else rect[2]+15
                d.text((xtext, rect[1]+12), "Pi" if part_id == "pi" else "ESP32", font=font(22), fill="#263238")
        d.line((origin_x-205, bottom, origin_x+205, bottom), fill="#a8aeab", width=2)
        d.text((origin_x-60, bottom+18), "Высота 192 мм", font=font(22), fill="#263238")
    for i, (kind, label) in enumerate([("servo", "Сервоприводы"), ("battery", "Аккумулятор"), ("logic", "Платы / камера"), ("power", "Питание"), ("audio", "Аудио")]):
        x = 70 + (i % 3)*490
        y = 930 + (i // 3)*48
        d.rounded_rectangle((x, y, x+24, y+24), radius=4, fill=COLORS[kind])
        d.text((x+36, y-2), label, font=font(22), fill="#263238")
    d.text((55, 1060), "Оболочки показаны контуром. Крепления, провода и нагрузочная проверка — следующий этап.", font=font(22), fill="#556168")
    im.save(ROOT / "assets" / "internal-layout.png")


def write_scad():
    lines = ["// Provisional envelope model. NOT printable production parts.",
             "// All coordinates in mm: X across, Y forward, Z up.",
             "show_shells = true;", "show_parts = true;", "$fn = 32;"]
    for p in SHELLS:
        lines.append(f'if (show_shells) color([0.75,0.75,0.75,0.12]) translate({p["center"]}) cube({p["size"]}, center=true); // {p["id"]}')
    rgb = {key: [int(value[i:i+2], 16)/255 for i in (1, 3, 5)] for key, value in COLORS.items()}
    for p in PARTS:
        lines.append(f'if (show_parts) color({rgb[p["kind"]]}) translate({p["center"]}) cube({p["size"]}, center=true); // {p["id"]}')
    (ROOT / "layout.scad").write_text("\n".join(lines)+"\n", encoding="utf-8")


if __name__ == "__main__":
    result = validate()
    (ROOT / "layout.json").write_text(json.dumps(dict(parts=PARTS, shells=SHELLS, validation=result), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    if result["envelope_collisions"] or result["body_envelopes_outside_inner_volume"]:
        raise SystemExit(json.dumps(result, ensure_ascii=False))
    draw_layout()
    write_scad()
    print(json.dumps(result, ensure_ascii=False, indent=2))
