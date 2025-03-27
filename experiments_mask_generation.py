# https://github.com/sail-sg/EditAnything/blob/main/sam2groundingdino_edit.py

import numpy as np
from PIL import Image
from extras.inpaint_mask import SAMOptions, generate_mask_from_image

# Load image safely using a context manager
with Image.open("cat.webp") as original_image:
    image = np.asarray(original_image, dtype=np.uint8)

# Configure SAM options
sam_options = SAMOptions(
    dino_prompt="eye",
    dino_box_threshold=0.3,
    dino_text_threshold=0.25,
    dino_erode_or_dilate=0,
    dino_debug=False,
    max_detections=2,
    model_type="vit_b",
)

# Generate the mask
mask_image, *_ = generate_mask_from_image(image, sam_options=sam_options)

# Convert and display the mask
Image.fromarray(mask_image).show()
