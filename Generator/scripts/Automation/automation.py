import subprocess
import sys
import time
import threading

# ============================================================
#  KONFIGURATION – hier anpassen
# ============================================================
ANZAHL_DURCHLAEUFE       = 100           # Wie viele Durchläufe insgesamt
BLENDER_SKRIPT           =  "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\scripts\\Version6.3.py"
CONVERTER_SKRIPT         =  "D:\\Strohmo\\Synthetic Data\\Strohmo-Synthetic-Data\\Generator\\scripts\\Automation\\coco_to_yolo_per_image.py"
WARTE_SEKUNDEN_CONVERTER = 5          # Sekunden nach "Blender quit" bis Converter startet
STOP_SIGNAL              = "Cleaning temporary directory"  # Erkennungsstring im Terminal
# ============================================================


def run_generator():
    """Startet den Generator und gibt seine Ausgabe zeilenweise aus.
    Gibt True zurück, wenn das Stop-Signal erkannt wurde."""
    print(f"\n{'='*60}")
    print(f"  Starte Generator: {BLENDER_SKRIPT}")
    print(f"{'='*60}\n")

    process = subprocess.Popen(
        ["blenderproc", "run", BLENDER_SKRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    stop_erkannt = False
    for line in process.stdout:
        print(f"[Generator] {line}", end="")
        if STOP_SIGNAL in line:
            stop_erkannt = True

    process.wait()
    return stop_erkannt


def run_converter():
    """Startet den Converter und wartet bis er fertig ist."""
    print(f"\n{'='*60}")
    print(f"  Starte Converter: {CONVERTER_SKRIPT}")
    print(f"{'='*60}\n")

    process = subprocess.Popen(
        [sys.executable, CONVERTER_SKRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in process.stdout:
        print(f"[Converter] {line}", end="")

    process.wait()
    return_code = process.returncode
    if return_code == 0:
        print("\n[Converter] ✓ Erfolgreich abgeschlossen.")
    else:
        print(f"\n[Converter] ✗ Beendet mit Fehlercode {return_code}.")
    return return_code


def countdown(sekunden):
    """Zeigt einen sichtbaren Countdown im Terminal."""
    for i in range(sekunden, 0, -1):
        print(f"  Warte noch {i:>3} Sekunde(n)...", end="\r")
        time.sleep(1)
    print(" " * 40, end="\r")  # Zeile leeren


def main():
    print(f"\n{'#'*60}")
    print(f"  Automatisierung gestartet – {ANZAHL_DURCHLAEUFE} Durchläufe geplant")
    print(f"{'#'*60}\n")

    for durchlauf in range(1, ANZAHL_DURCHLAEUFE + 1):
        print(f"\n>>> Durchlauf {durchlauf} / {ANZAHL_DURCHLAEUFE}")

        # 1. Generator starten und auf Stop-Signal warten
        stop_erkannt = run_generator()

        if not stop_erkannt:
            print(f"\n[Warnung] Stop-Signal '{STOP_SIGNAL}' wurde in Durchlauf "
                  f"{durchlauf} nicht erkannt. Trotzdem weiter...")

        # 2. Warten bevor Converter startet
        print(f"\n[Info] 'Blender quit' erkannt – warte {WARTE_SEKUNDEN_CONVERTER}s vor Converter-Start.")
        countdown(WARTE_SEKUNDEN_CONVERTER)

        # 3. Converter starten und abwarten
        run_converter()

        if durchlauf < ANZAHL_DURCHLAEUFE:
            print(f"\n[Info] Durchlauf {durchlauf} abgeschlossen. Nächster startet sofort.\n")

    print(f"\n{'#'*60}")
    print(f"  Alle {ANZAHL_DURCHLAEUFE} Durchläufe abgeschlossen!")
    print(f"{'#'*60}\n")


if __name__ == "__main__":
    main()