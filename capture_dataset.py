import cv2
import os
from datetime import datetime

# ─────────────────────────────────────────
#  KONFIGURASI — edit sesuai kebutuhan
# ─────────────────────────────────────────
WEBCAM_INDEX   = 1         # ganti ke 1 atau 2 kalau webcam tidak muncul
SAVE_DIR       = "dataset"  # folder output
PART_CLASSES   = [          # daftar nama part — tambah/hapus sesuai kebutuhan
    "screw",
    "bolt",
    "nut",
    "gear",
]
# ─────────────────────────────────────────

# ── warna UI (BGR) ──
COL_BG       = (30, 30, 30)
COL_WHITE    = (240, 240, 240)
COL_YELLOW   = (0, 200, 255)
COL_GREEN    = (80, 200, 80)
COL_RED      = (80, 80, 220)
COL_BLUE     = (200, 140, 60)
COL_GRAY     = (140, 140, 140)


def make_dirs(classes):
    for cls in classes:
        os.makedirs(os.path.join(SAVE_DIR, cls), exist_ok=True)


def count_existing(cls):
    path = os.path.join(SAVE_DIR, cls)
    if not os.path.exists(path):
        return 0
    return len([f for f in os.listdir(path) if f.endswith(".jpg")])


def noop(_value):
    return None


def setup_crop_controls(window_name):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 420, 180)
    cv2.createTrackbar("Crop On", window_name, 1, 1, noop)
    cv2.createTrackbar("Crop Width", window_name, 672, 1920, noop)
    cv2.createTrackbar("Crop Height", window_name, 512, 1080, noop)


def read_crop_controls(window_name):
    crop_on = cv2.getTrackbarPos("Crop On", window_name)
    crop_width = cv2.getTrackbarPos("Crop Width", window_name)
    crop_height = cv2.getTrackbarPos("Crop Height", window_name)

    crop_width = max(2, crop_width)
    crop_height = max(2, crop_height)
    return crop_on, crop_width, crop_height


def crop_and_resize(frame, target_width, target_height):
    source_height, source_width = frame.shape[:2]
    target_ratio = target_width / target_height
    source_ratio = source_width / source_height

    if source_ratio > target_ratio:
        crop_width = int(source_height * target_ratio)
        crop_height = source_height
        start_x = (source_width - crop_width) // 2
        start_y = 0
    else:
        crop_width = source_width
        crop_height = int(source_width / target_ratio)
        start_x = 0
        start_y = (source_height - crop_height) // 2

    cropped = frame[start_y:start_y + crop_height, start_x:start_x + crop_width]
    return cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)


def draw_ui(frame, current_class, class_idx, total_classes, count, flash):
    h, w = frame.shape[:2]

    # ── top bar ──
    cv2.rectangle(frame, (0, 0), (w, 56), COL_BG, -1)

    # class indicator
    label = f"[{class_idx+1}/{total_classes}]  {current_class.upper()}"
    cv2.putText(frame, label, (14, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, COL_YELLOW, 2, cv2.LINE_AA)

    # photo count
    count_str = f"{count} foto"
    cv2.putText(frame, count_str, (w - 130, 36),
                cv2.FONT_HERSHEY_SIMPLEX, 0.85, COL_GREEN, 2, cv2.LINE_AA)

    # ── bottom bar ──
    cv2.rectangle(frame, (0, h - 52), (w, h), COL_BG, -1)

    hints = [
        ("SPACE", "foto"),
        ("N", "next class"),
        ("P", "prev class"),
        ("Q", "keluar"),
    ]
    x = 14
    for key, desc in hints:
        cv2.putText(frame, key, (x, h - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_YELLOW, 2, cv2.LINE_AA)
        x += len(key) * 12 + 4
        cv2.putText(frame, f"={desc}  ", (x, h - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, COL_GRAY, 1, cv2.LINE_AA)
        x += (len(desc) + 3) * 10

    # ── flash overlay saat foto diambil ──
    if flash > 0:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (255, 255, 255), -1)
        alpha = flash / 8.0
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.putText(frame, "SAVED!", (w // 2 - 60, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, COL_GREEN, 3, cv2.LINE_AA)

    cv2.putText(frame, "CTRL: use Crop On/Width/Height window", (14, h - 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, COL_WHITE, 1, cv2.LINE_AA)

    return frame


def main():
    make_dirs(PART_CLASSES)

    counts = {cls: count_existing(cls) for cls in PART_CLASSES}

    cap = cv2.VideoCapture(WEBCAM_INDEX)
    if not cap.isOpened():
        print(f"[ERROR] Webcam index {WEBCAM_INDEX} tidak bisa dibuka.")
        print("Coba ganti WEBCAM_INDEX ke 1 atau 2 di bagian atas script.")
        return

    # resolusi webcam
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    class_idx = 0
    flash     = 0

    print("\n── Dataset Capture ──────────────────────")
    print(f"  Folder output : {os.path.abspath(SAVE_DIR)}")
    print(f"  Part classes  : {', '.join(PART_CLASSES)}")
    print("  Crop settings : atur dari window Controls")
    print("  SPACE = foto  |  N = next  |  P = prev  |  Q = keluar")
    print("─────────────────────────────────────────\n")

    cv2.namedWindow("Dataset Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Dataset Capture", 900, 600)
    setup_crop_controls("Controls")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Gagal baca frame dari webcam.")
            break

        current_class = PART_CLASSES[class_idx]
        count         = counts[current_class]
        crop_on, crop_width, crop_height = read_crop_controls("Controls")

        if crop_on:
            display = crop_and_resize(frame, crop_width, crop_height)
            save_frame = display.copy()
        else:
            display = frame.copy()
            save_frame = frame.copy()

        draw_ui(display, current_class, class_idx,
                len(PART_CLASSES), count, flash)
        if flash > 0:
            flash -= 1

        status_text = f"Crop: {'ON' if crop_on else 'OFF'} | {crop_width} x {crop_height}"
        cv2.putText(display, status_text, (14, 68),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, COL_BLUE, 2, cv2.LINE_AA)

        cv2.imshow("Dataset Capture", display)
        key = cv2.waitKey(1) & 0xFF

        # ── SPACE: ambil foto ──
        if key == ord(" "):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename  = f"{current_class}_{timestamp}.jpg"
            save_path = os.path.join(SAVE_DIR, current_class, filename)
            cv2.imwrite(save_path, save_frame)
            flash = 8
            counts[current_class] += 1
            new_count = counts[current_class]
            print(f"  [{current_class}] foto #{new_count} → {save_path}")

        # ── N: next class ──
        elif key == ord("n") or key == ord("N"):
            class_idx = (class_idx + 1) % len(PART_CLASSES)
            print(f"\n  ▶ Ganti ke class: {PART_CLASSES[class_idx]}")

        # ── P: previous class ──
        elif key == ord("p") or key == ord("P"):
            class_idx = (class_idx - 1) % len(PART_CLASSES)
            print(f"\n  ◀ Ganti ke class: {PART_CLASSES[class_idx]}")

        # ── Q: keluar ──
        elif key == ord("q") or key == ord("Q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ── ringkasan ──
    print("\n── Ringkasan Dataset ────────────────────")
    total = 0
    for cls in PART_CLASSES:
        n = counts[cls]
        total += n
        bar = "█" * min(n, 40)
        print(f"  {cls:<12} {bar} {n} foto")
    print(f"\n  Total: {total} foto")
    print(f"  Disimpan di: {os.path.abspath(SAVE_DIR)}")
    print("─────────────────────────────────────────\n")


if __name__ == "__main__":
    main()