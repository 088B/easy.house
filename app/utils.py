from PIL import Image, ImageDraw

def points_to_mask(image: Image.Image, polygon):
    """
    Create a mask PNG where the polygon area is TRANSPARENT (alpha=0)
    and the rest is opaque (alpha=255). OpenAI expects transparent area to be edited.
    polygon: list of (x,y) tuples in image coordinate space.
    """
    w, h = image.size
    # Start opaque white background (R,G,B,A)
    mask = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(mask)
    # Draw polygon as fully transparent
    draw.polygon(polygon, fill=(0, 0, 0, 0))
    return mask
