"""
raindrop_augmentation.py
────────────────────────────────────────────────────────────────────────────────
Post-Processing: Regentropfen-Effekt auf gerenderte BlenderProc-Bilder anwenden.

Konfigurierte Pfade:
    Bilder:  D:/Strohmo/Synthetic Data/.../coco_data/images/     (000000.jpg, ...)
    Labels:  D:/Strohmo/Synthetic Data/.../coco_data/yolo_labels/ (000000.txt, ...)

Verwendung:
    # Standard (mittlere Intensität, alle Bilder):
    python raindrop_augmentation.py

    # Intensität wählen:
    python raindrop_augmentation.py --intensity leicht
    python raindrop_augmentation.py --intensity stark

    # Nur bestimmte Bilder (Bereich):
    python raindrop_augmentation.py --from-index 0 --to-index 499

    # Reproduzierbar:
    python raindrop_augmentation.py --seed 42

    # Eigene Pfade (überschreibt Standardpfade):
    python raindrop_augmentation.py --images "C:/anderer/pfad/images" --labels "C:/anderer/pfad/labels"

    # Einzelne Parameter feinjustieren:
    python raindrop_augmentation.py --min-drops 5 --max-drops 20 --drop-opacity 0.25

Abhängigkeiten:
    pip install opencv-python numpy tqdm
"""

import argparse
import random
import sys
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm


# ─────────────────────────────────────────────────────────────────────────────
# Standardpfade  ←  hier anpassen falls sich etwas ändert
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_IMAGES_DIR = Path(
    r"D:\Strohmo\Synthetic Data\Strohmo-Synthetic-Data\Generator\output\coco_data\images"
)
DEFAULT_LABELS_DIR = Path(
    r"D:\Strohmo\Synthetic Data\Strohmo-Synthetic-Data\Generator\output\coco_data\yolo_labels"
)

# Dateiname-Format: 000000.jpg, 000001.jpg, ...
IMAGE_EXTENSION  = ".jpg"
LABEL_EXTENSION  = ".json"
INDEX_DIGITS     = 6          # Anzahl der Stellen (z. B. 6 → 000000)


# ─────────────────────────────────────────────────────────────────────────────
# Intensitäts-Voreinstellungen
# ─────────────────────────────────────────────────────────────────────────────
INTENSITY_PRESETS = {
    "leicht": dict(
        min_drops=3,
        max_drops=12,
        min_radius=6,
        max_radius=25,
        blur_strength=15,
        refraction_strength=3,
        drop_opacity=0.20,
        streak_probability=0.10,
    ),
    "mittel": dict(
        min_drops=10,
        max_drops=30,
        min_radius=8,
        max_radius=40,
        blur_strength=21,
        refraction_strength=5,
        drop_opacity=0.30,
        streak_probability=0.25,
    ),
    "stark": dict(
        min_drops=25,
        max_drops=60,
        min_radius=10,
        max_radius=55,
        blur_strength=27,
        refraction_strength=8,
        drop_opacity=0.40,
        streak_probability=0.40,
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# Hilfsfunktionen
# ─────────────────────────────────────────────────────────────────────────────

def _make_odd(value: int) -> int:
    """Stellt sicher, dass ein Kernel-Wert ungerade und >= 3 ist."""
    k = max(3, int(value))
    return k if k % 2 == 1 else k + 1


def _apply_refraction(image: np.ndarray, mask: np.ndarray, strength: int) -> np.ndarray:
    """Simuliert Lichtbrechung durch Verschieben von Pixeln innerhalb der Tropfenmaske."""
    h, w = image.shape[:2]
    shift_x = random.randint(-strength, strength)
    shift_y = random.randint(-strength, strength)

    M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    shifted = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
    return (image * (1 - mask_3ch) + shifted * mask_3ch).astype(np.uint8)


def _draw_raindrop(
    image: np.ndarray,
    x: int, y: int, radius: int,
    blur_strength: int,
    refraction_strength: int,
    opacity: float,
) -> np.ndarray:
    """Zeichnet einen einzelnen runden/ovalen Regentropfen."""
    h, w = image.shape[:2]
    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(w, x + radius), min(h, y + radius)
    if x2 <= x1 or y2 <= y1:
        return image

    # Ovale Maske (leicht zufällige Verformung)
    roi_mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(
        roi_mask, (x, y),
        (radius, int(radius * random.uniform(0.70, 1.0))),
        angle=random.randint(0, 360),
        startAngle=0, endAngle=360,
        color=255, thickness=-1,
    )
    mask_crop = roi_mask[y1:y2, x1:x2]

    # Blur + Refraktion
    roi = image[y1:y2, x1:x2].copy()
    k = _make_odd(blur_strength)
    blurred = cv2.GaussianBlur(roi, (k, k), 0)
    refracted = _apply_refraction(blurred, mask_crop, refraction_strength)

    # Glanzpunkt (primär)
    hx = x - radius // 4 - x1
    hy = y - radius // 4 - y1
    hr = max(1, radius // 5)
    cv2.circle(refracted, (hx, hy), hr, (255, 255, 255), -1)
    refracted = cv2.GaussianBlur(refracted, (_make_odd(hr * 2), _make_odd(hr * 2)), 0)

    # Glanzpunkt (sekundär, kleiner)
    cv2.circle(refracted, (hx + 2, hy + 2), max(1, hr // 2), (220, 235, 255), -1)

    # Dunkler Rand (Oberflächenspannung)
    cv2.ellipse(
        refracted, (x - x1, y - y1),
        (max(1, radius - 1), max(1, int((radius - 1) * random.uniform(0.70, 1.0)))),
        angle=0, startAngle=0, endAngle=360,
        color=(160, 175, 185), thickness=1,
    )

    # Mit Deckkraft einblenden
    mask_f  = (mask_crop.astype(np.float32) / 255.0) * opacity
    mask_3ch = np.stack([mask_f] * 3, axis=-1)
    blended  = (roi.astype(np.float32) * (1 - mask_3ch) +
                refracted.astype(np.float32) * mask_3ch).astype(np.uint8)

    result = image.copy()
    result[y1:y2, x1:x2] = blended
    return result


def _draw_streak(
    image: np.ndarray,
    x: int, y: int, radius: int,
    blur_strength: int,
    opacity: float,
) -> np.ndarray:
    """Zeichnet einen nach unten laufenden Schlieren-Tropfen."""
    h, w = image.shape[:2]
    streak_length = random.randint(radius * 2, radius * 5)

    x1, y1 = max(0, x - radius), max(0, y - radius)
    x2, y2 = min(w, x + radius), min(h, y + radius + streak_length)
    if x2 <= x1 or y2 <= y1:
        return image

    roi  = image[y1:y2, x1:x2].copy()
    mask = np.zeros(roi.shape[:2], dtype=np.uint8)
    lw   = max(2, radius // 3)

    cv2.circle(mask, (x - x1, y - y1), radius, 255, -1)
    cv2.rectangle(mask,
                  (x - x1 - lw, y - y1),
                  (x - x1 + lw, y - y1 + streak_length),
                  255, -1)

    k       = _make_odd(blur_strength)
    blurred = cv2.GaussianBlur(roi, (k, k), 0)
    mask_f  = (mask.astype(np.float32) / 255.0) * opacity
    mask_3ch = np.stack([mask_f] * 3, axis=-1)
    blended  = (roi.astype(np.float32) * (1 - mask_3ch) +
                blurred.astype(np.float32) * mask_3ch).astype(np.uint8)

    # Glanzlinie
    cv2.line(blended,
             (x - x1 - lw + 1, y - y1),
             (x - x1 - lw + 1, y - y1 + streak_length),
             (235, 245, 255), 1)

    result = image.copy()
    result[y1:y2, x1:x2] = blended
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Haupt-Augmentierungsfunktion
# ─────────────────────────────────────────────────────────────────────────────

def apply_raindrops(image: np.ndarray, seed: int = None, **params) -> np.ndarray:
    """
    Legt zufällige Regentropfen auf ein BGR-Bild und gibt das Ergebnis zurück.
    Das Eingabebild wird nicht verändert.
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    h, w   = image.shape[:2]
    result = image.copy()
    n      = random.randint(params["min_drops"], params["max_drops"])

    for _ in range(n):
        x      = random.randint(0, w - 1)
        y      = random.randint(0, h - 1)
        radius = random.randint(params["min_radius"], params["max_radius"])

        if random.random() < params["streak_probability"]:
            result = _draw_streak(
                result, x, y, radius,
                params["blur_strength"],
                params["drop_opacity"],
            )
        else:
            result = _draw_raindrop(
                result, x, y, radius,
                params["blur_strength"],
                params["refraction_strength"],
                params["drop_opacity"],
            )

    return result


# ─────────────────────────────────────────────────────────────────────────────
# Datei-Pipeline
# ─────────────────────────────────────────────────────────────────────────────

def index_to_filename(index: int, ext: str) -> str:
    """000 → '000000.jpg' (je nach INDEX_DIGITS)"""
    return str(index).zfill(INDEX_DIGITS) + ext


def collect_image_files(images_dir: Path, from_index: int = None, to_index: int = None):
    """
    Gibt sortierte Liste aller Bild-Dateien zurück.
    Bei from_index / to_index wird auf den angegebenen Bereich eingeschränkt.
    """
    all_files = sorted(images_dir.glob(f"*{IMAGE_EXTENSION}"))

    if not all_files:
        print(f"[FEHLER] Keine {IMAGE_EXTENSION}-Dateien gefunden in:\n  {images_dir}", file=sys.stderr)
        sys.exit(1)

    if from_index is not None or to_index is not None:
        lo = from_index if from_index is not None else 0
        hi = to_index   if to_index   is not None else 999_999
        all_files = [
            f for f in all_files
            if lo <= int(f.stem) <= hi
        ]
        if not all_files:
            print(f"[FEHLER] Keine Bilder im Bereich {lo:06d}–{hi:06d} gefunden.", file=sys.stderr)
            sys.exit(1)

    return all_files


def process_dataset(
    images_dir: Path,
    labels_dir: Path,
    params: dict,
    seed: int = None,
    from_index: int = None,
    to_index: int = None,
):
    """Verarbeitet alle Bilder; Labels bleiben unberührt."""
    image_files = collect_image_files(images_dir, from_index, to_index)

    # ── Konsolen-Header ──
    range_str = ""
    if from_index is not None or to_index is not None:
        lo = from_index if from_index is not None else int(image_files[0].stem)
        hi = to_index   if to_index   is not None else int(image_files[-1].stem)
        range_str = f"  Bereich:      {lo:06d} – {hi:06d}\n"

    print(f"\n{'─'*62}")
    print(f"  Raindrop Augmentation  ·  BlenderProc Post-Processing")
    print(f"{'─'*62}")
    print(f"  Bilder-Ordner: {images_dir}")
    print(f"  Labels-Ordner: {labels_dir}")
    print(f"  Bilder:        {len(image_files)}")
    print(range_str, end="")
    print(f"  Tropfen:       {params['min_drops']}–{params['max_drops']} pro Bild")
    print(f"  Radius:        {params['min_radius']}–{params['max_radius']} px")
    print(f"  Blur:          {params['blur_strength']}")
    print(f"  Refraktion:    ±{params['refraction_strength']} px")
    print(f"  Deckkraft:     {params['drop_opacity']:.0%}")
    print(f"  Schlieren:     {params['streak_probability']:.0%} Wahrscheinlichkeit")
    print(f"  Seed:          {seed if seed is not None else 'zufällig'}")
    print(f"  Originale:     werden überschrieben")
    print(f"{'─'*62}\n")

    stats = {"processed": 0, "skipped": 0, "errors": []}

    for img_path in tqdm(image_files, desc="Verarbeite", unit="Bild"):
        try:
            # ── Zugehöriges Label prüfen (nur Warnung, kein Abbruch) ──
            label_path = labels_dir / (img_path.stem + LABEL_EXTENSION)
            if not label_path.exists():
                tqdm.write(f"  [WARNUNG] Kein Label für {img_path.name}")

            # ── Bild laden ──
            image = cv2.imread(str(img_path))
            if image is None:
                stats["skipped"] += 1
                stats["errors"].append(f"Laden fehlgeschlagen: {img_path.name}")
                continue

            # ── Deterministischer Seed pro Bild ──
            img_seed = None
            if seed is not None:
                img_seed = (seed + int(img_path.stem)) % (2**32)

            # ── Regentropfen anwenden ──
            augmented = apply_raindrops(image, seed=img_seed, **params)

            # ── Überschreiben (JPEG, Qualität 95) ──
            cv2.imwrite(str(img_path), augmented, [cv2.IMWRITE_JPEG_QUALITY, 95])
            stats["processed"] += 1

        except Exception as exc:
            stats["skipped"] += 1
            stats["errors"].append(f"{img_path.name}: {exc}")

    # ── Zusammenfassung ──
    print(f"\n{'─'*62}")
    print(f"  ✓ Erfolgreich verarbeitet: {stats['processed']} Bilder")
    if stats["skipped"]:
        print(f"  ✗ Übersprungen:            {stats['skipped']} Bilder")
        for err in stats["errors"]:
            print(f"    → {err}")
    print(f"{'─'*62}\n")
    return stats


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Regentropfen-Post-Processing für BlenderProc YOLO-Datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Pfade (optional – Standardwerte oben definiert)
    parser.add_argument(
        "--images", type=Path, default=DEFAULT_IMAGES_DIR,
        metavar="PFAD",
        help=f"Pfad zum images/-Ordner (Standard: {DEFAULT_IMAGES_DIR})",
    )
    parser.add_argument(
        "--labels", type=Path, default=DEFAULT_LABELS_DIR,
        metavar="PFAD",
        help=f"Pfad zum yolo_labels/-Ordner (Standard: {DEFAULT_LABELS_DIR})",
    )

    # Intensität
    parser.add_argument(
        "--intensity", choices=["leicht", "mittel", "stark"], default="mittel",
        help="Voreinstellung für Tropfen-Intensität (Standard: mittel)",
    )

    # Bildbereich
    parser.add_argument("--from-index", type=int, default=None, metavar="N",
                        help="Erster Bildindex (z. B. 0 → 000000.jpg)")
    parser.add_argument("--to-index",   type=int, default=None, metavar="N",
                        help="Letzter Bildindex (z. B. 499 → 000499.jpg)")

    # Reproduzierbarkeit
    parser.add_argument("--seed", type=int, default=None,
                        help="Zufalls-Seed (gleicher Seed = gleiche Tropfen)")

    # Manuelle Feinsteuerung (überschreiben --intensity)
    parser.add_argument("--min-drops",           type=int,   metavar="N")
    parser.add_argument("--max-drops",           type=int,   metavar="N")
    parser.add_argument("--min-radius",          type=int,   metavar="PX")
    parser.add_argument("--max-radius",          type=int,   metavar="PX")
    parser.add_argument("--blur-strength",       type=int,   metavar="N")
    parser.add_argument("--refraction-strength", type=int,   metavar="PX")
    parser.add_argument("--drop-opacity",        type=float, metavar="0.0-1.0")
    parser.add_argument("--streak-probability",  type=float, metavar="0.0-1.0")

    return parser.parse_args()


def main():
    args   = parse_args()
    params = INTENSITY_PRESETS[args.intensity].copy()

    # Manuelle Überschreibungen
    overrides = {
        "min_drops":            args.min_drops,
        "max_drops":            args.max_drops,
        "min_radius":           args.min_radius,
        "max_radius":           args.max_radius,
        "blur_strength":        args.blur_strength,
        "refraction_strength":  args.refraction_strength,
        "drop_opacity":         args.drop_opacity,
        "streak_probability":   args.streak_probability,
    }
    for key, val in overrides.items():
        if val is not None:
            params[key] = val

    process_dataset(
        images_dir=args.images,
        labels_dir=args.labels,
        params=params,
        seed=args.seed,
        from_index=args.from_index,
        to_index=args.to_index,
    )


if __name__ == "__main__":
    main()