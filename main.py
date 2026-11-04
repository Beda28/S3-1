import argparse
import cv2

from pathlib        import Path
from src.repository import load

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("image"   , type=Path)
    parser.add_argument("--no-gui", action="store_true")
    parser.add_argument("--out"   , type=Path, default=Path("outputs"))
    parser.add_argument("--blur"  , type=int , default=5)
    parser.add_argument("--low"   , type=int , default=50)
    parser.add_argument("--high"  , type=int , default=100)
    parser.add_argument("--ext"   , choices=("png", "jpg"), default="png")

    args = parser.parse_args()

    try:
        img = load(args.image)
        print(img)
    except (OSError, ValueError, cv2.error) as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())