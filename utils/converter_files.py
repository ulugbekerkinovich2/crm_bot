import pyheif
from PIL import Image

# def convert_heic_to_jpg(input_path):
#     output_path = input_path.rsplit('.', 1)[0] + ".jpg"
#     heif_file = pyheif.read(input_path)
#     image = Image.frombytes(
#         heif_file.mode,
#         heif_file.size,
#         heif_file.data,
#         "raw",
#         heif_file.mode,
#         heif_file.stride,
#     )
#     image.save(output_path, "JPEG")
#     print(f"✅ Convert qilingan: {output_path}")
#     return output_path


from pillow_heif import register_heif_opener
from PIL import Image

register_heif_opener()

def convert_heic_to_jpg(input_path):
    output_path = input_path.rsplit('.', 1)[0] + ".jpg"
    image = Image.open(input_path)
    image.save(output_path, "JPEG")
    print(f"✅ Convert qilingan: {output_path}")
    return output_path
