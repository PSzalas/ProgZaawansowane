import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'D:\Aplikacje\Tesseract\tesseract.exe'


def extract_text(image_path: str, preprocess_type: str = "thresh"):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)

    if preprocess_type == "thresh":
        _, processed_image = cv2.threshold(
            denoised_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )
    elif preprocess_type == "blur":
        processed_image = cv2.medianBlur(denoised_image, 3)
    elif preprocess_type == "adaptive":
        processed_image = cv2.adaptiveThreshold(
            denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    elif preprocess_type == "none":
        processed_image = denoised_image
    else:
        raise ValueError(f"Nieprawidłowy preprocess_type: {preprocess_type}")

    text = pytesseract.image_to_string(
        processed_image, config="--oem 3 --psm 6", lang="eng"
    )
    return text


if __name__ == "__main__":
    test_images = [
        "testImage1.jpg",
        "testImage2.png",
        "testImage3.jpg",
        "testImage4.jpg",
        "testImage5.jpg",
    ]

    for i, image_path in enumerate(test_images):
        print(f"\nProcesuję zdjęcie {i + 1}: {image_path}")
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")

            extracted_text = extract_text(image_path, preprocess_type="blur")
            print(f"Wyodrębniony tekst:\n{extracted_text}")
        except Exception as e:
            print(f"Błąd podczas procesowania zdjęcia {image_path}: {e}")
