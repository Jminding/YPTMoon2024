import glob
import os
import cv2

def resize(filename: str, dim: tuple) -> None:
    """
    Resizes an image to the specified dimensions.
    :param filename: The name of the file to resize/path of files.
    :param dim: The dimensions to resize to.
    """
    img_names = glob.glob(filename)
    for i, path in enumerate(img_names):
        if "_resized" in path:
            continue
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        print(path)
        cv2.imwrite(path, resized)

SIZE_730 = (730, 730)
SIZE_1000 = (1000, 1000)
SIZE_1300 = (1300, 1300)

if __name__ == "__main__":
    resize("./test_data_synthetic/*.jpg", SIZE_1000)