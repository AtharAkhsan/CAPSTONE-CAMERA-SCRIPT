# CAPSTONE Camera Script

This project is a simple webcam dataset capture tool built with Python and OpenCV. It opens your camera, lets you switch between part classes, and saves captured images into class folders.

## Requirements

- Python 3.11 or newer
- A working webcam
- `opencv-python`

## Setup

If you already have the virtual environment in this folder, activate it first:

```powershell
.venv\Scripts\activate
```

If you do not have the package installed yet, install it with:

```powershell
pip install opencv-python
```

## Run

Start the script with:

```powershell
python capture_dataset.py
```

If `python` does not use the virtual environment on your machine, run it directly with:

```powershell
.venv\Scripts\python.exe capture_dataset.py
```

## Controls

- `SPACE` = take a photo
- `N` = next class
- `P` = previous class
- `Q` = quit

## Output

Images are saved in the `dataset` folder, grouped by class name:

- `dataset/screw`
- `dataset/bolt`
- `dataset/nut`
- `dataset/gear`

## Webcam Note

If the camera does not open, change `WEBCAM_INDEX` at the top of `capture_dataset.py` from `0` to `1` or `2`.

## Customize Classes

Edit `PART_CLASSES` in `capture_dataset.py` to add or remove object classes before capturing data.