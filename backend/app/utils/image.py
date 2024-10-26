
import ast


def parse_images(images_data):
    try:
        return ast.literal_eval(images_data) if isinstance(images_data, str) else images_data
    except (ValueError, SyntaxError):
        return []


def get_image_url(images, size):
    return next((img['url'] for img in images if img.get('height') == size and img.get('width') == size), None)
