import cv2
import pytesseract
from pytesseract import Output

from pdanonymizer import pipelines


def read_image(image_name):
    return cv2.imread(image_name)


def write_image(image_name, img):
    img_name = "out_image."
    img_ext = image_name.split(".")[-1]
    cv2.imwrite(img_name + img_ext, img)
    return img_name + img_ext


def image_to_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return gray


def get_image_data(image):
    return pytesseract.image_to_data(image, output_type=Output.DICT)


def get_n_boxes(data_dict):
    return len(data_dict['text'])


def draw_rects(img, data_dict, i):
    x, y, w, h = (data_dict['left'][i], data_dict['top'][i], data_dict['width'][i], data_dict['height'][i])
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
    return img


def handle_entities(n_boxes, data_dict, img, model_name="models/model_10000"):
    model = pipelines.load_model(model_name)

    for i in range(n_boxes):
        if int(data_dict['conf'][i]) > 50:
            sample_text = data_dict['text'][i]
            entity = pipelines.get_entities(model, sample_text)
            if entity:
                img = draw_rects(img, data_dict, i)


def hide_data_image(image_name="img.png"):
    img = read_image(image_name)
    gray = image_to_gray(img)

    data_dict = get_image_data(gray)
    n_boxes = get_n_boxes(data_dict)

    handle_entities(n_boxes, data_dict, img)
    out_file = write_image(image_name, img)
    return out_file


if __name__ == "__main__":
    hide_data_image()
