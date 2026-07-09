from pathlib import Path
from PIL import Image

# 変換対象の拡張子
TARGET_EXTENSIONS = {".png", ".jpg", ".jpeg"}

# WebPの品質
WEBP_QUALITY = 85


def convert_image_to_webp(image_path: Path) -> None:
    output_path = image_path.with_suffix(".webp")

    try:
        with Image.open(image_path) as img:
            # PNGの透明背景は維持、それ以外はRGBに変換
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            img.save(
                output_path,
                "WEBP",
                quality=WEBP_QUALITY,
                method=6
            )

        print(f"OK: {image_path.name} -> {output_path.name}")

    except Exception as e:
        print(f"NG: {image_path.name} / {e}")


def main() -> None:
    current_dir = Path(__file__).resolve().parent

    image_files = [
        path for path in current_dir.iterdir()
        if path.is_file() and path.suffix.lower() in TARGET_EXTENSIONS
    ]

    if not image_files:
        print("変換対象のPNG/JPEGファイルがありません。")
        return

    for image_path in image_files:
        convert_image_to_webp(image_path)

    print("変換が完了しました。")


if __name__ == "__main__":
    main()