import cv2
from pathlib import Path
from extras.interrogate import default_interrogator as default_interrogator_photo
from extras.wd14tagger import default_interrogator as default_interrogator_anime

def load_image(image_path: Path) -> 'np.ndarray':
    """
    Loads an image, converts it from BGR to RGB, and returns it.
    """
    img = cv2.imread(str(image_path))  # Read image from file
    if img is None:  # Check if the image was loaded successfully
        raise ValueError(f"Image not found or invalid: {image_path}")
    return img[:, :, ::-1].copy()  # Convert BGR to RGB

def process_image(image_path: Path, interrogator) -> None:
    """
    Loads the image and applies the provided interrogator.
    """
    img = load_image(image_path)  # Load and convert the image
    print(interrogator(img))  # Apply the interrogator and print the result

# Image paths
photo_path = Path('./test_imgs/red_box.jpg')
anime_path = Path('./test_imgs/miku.jpg')

# Perform the interrogation for each image
process_image(photo_path, default_interrogator_photo)
process_image(anime_path, default_interrogator_anime)
