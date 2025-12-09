# Implementation Plan - Recursive Image Search

The goal is to update `combine_images.py` to support searching for images recursively in a specified directory via a command-line argument.

## Proposed Changes

### [BENRINAPROGRAM]

#### [MODIFY] [combine_images.py](file://wsl.localhost/Ubuntu/home/haseg/BENRINAPROGRAM/combine_images.py)
- Import `sys` (already imported)
- Update `combine_images_grid` signature to accept `input_dir`.
- Replace `os.listdir` with `os.walk` to find files recursively.
- Store full paths in `all_image_files`.
- Adjust `Image.open` logic to use the full path directly (remove `os.path.join`).
- Update `main` block to:
    - Add a positional (or named) argument `input_dir` to `argparse`.
    - Pass this argument to `combine_images_grid`.

## Verification Plan

### Manual Verification
- Run the script without arguments to ensure default behavior (current directory) works.
- Run the script with a specific directory path (e.g., `.` or `input_images`) and verify it finds images recursively (if subdirs exist).
- Since I cannot easily see the output image visually, I will verify the console output which prints "選択された画像: [...]". I expect to see paths from subdirectories if any.
