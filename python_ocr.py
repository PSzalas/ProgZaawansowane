import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\Aplikacje\Tesseract\tesseract.exe'


def read_text_from_image(image_path: str, method: str) -> str:

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    match method:
        case "median_blur":
            processed_image = cv2.medianBlur(gray_image, 3)
        case "gaussian_threshold":
            blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
            processed_image = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
        case "bilateral_threshold":
            filtered = cv2.bilateralFilter(gray_image, 5, 75, 75)
            processed_image = cv2.threshold(
                filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
        case "mediana_threshold":
            blurred = cv2.medianBlur(gray_image, 3)
            processed_image = cv2.threshold(
                blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
        case "adaptive_gaussian":
            blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
            processed_image = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 31, 2
            )
        case "adaptive_bilateral":
            filtered = cv2.bilateralFilter(gray_image, 9, 75, 75)
            processed_image = cv2.adaptiveThreshold(
                filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 31, 2
            )
        case "adaptive_median":
            blurred = cv2.medianBlur(gray_image, 3)
            processed_image = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 31, 2
            )
        case _:
            raise ValueError(f"Unknown preprocessing method: {method}")

    text = pytesseract.image_to_string(processed_image)

    return text


if __name__ == "__main__":
    images = [
        "image1.png",
        "image2.png"
    ]

    methods = [
        "median_blur",
        "gaussian_threshold",
        "bilateral_threshold",
        "mediana_threshold",
        "adaptive_gaussian",
        "adaptive_bilateral",
        "adaptive_median"
    ]

    for image_path in images:
        print(f"Procesuję zdjęcie: {image_path}")
        for method in methods:
            print(f"Metoda: {method}")
            try:
                result = read_text_from_image(image_path, method)
                print(f"Wyodrębniony tekst:\n{result}\n\n")
            except Exception as e:
                print(f"Błąd dla metody {method}: {e}\n\n")
