# =============================================================================
# convert2webp.py - 画像(PNG/JPEG)を WebP に変換するスクリプト
# =============================================================================
#
# 【概要】
#   このスクリプトと同じフォルダにある .png / .jpg / .jpeg をすべて
#   WebP に変換し、同じフォルダに「元のファイル名.webp」として保存します。
#   元の画像ファイルは削除・変更されません。
#   (同名の .webp がすでにある場合は上書きされます)
#
# 【事前準備】(初回のみ)
#   画像処理ライブラリ Pillow が必要です。
#     pip install Pillow
#
# 【使い方】
#   1. 変換したい画像をこのスクリプトと同じフォルダ
#      (assets/images/original/) に置く
#   2. このフォルダで次のコマンドを実行する
#        python convert2webp.py
#      (どのフォルダから実行しても、スクリプトのあるフォルダを対象にします)
#   3. 「OK: xxx.jpg -> xxx.webp」と表示されれば変換成功
#      「NG: ...」と表示された場合は、そのファイルの変換に失敗しています
#
# 【出力例】
#   202608_kaggle-competition.jpg -> 202608_kaggle-competition.webp
#
# 【設定の変更】
#   - 画質を変えたい場合   : 下の WEBP_QUALITY を変更 (0-100, 大きいほど高画質)
#   - 対象の拡張子を変える : 下の TARGET_EXTENSIONS を変更
#
# 【補足】
#   変換後の .webp は、サイトで使う場所(assets/images/ など)へ
#   手動で移動・コピーして利用してください。
# =============================================================================

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