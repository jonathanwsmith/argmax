from typing import Optional, List

import requests
from requests import Session
from PIL import Image
from ultralytics.engine.model import Model
from ultralytics.engine.results import Results

from argmax.exception import ImageRetrievalException, ImageProcessingException
from argmax.exception.unsupported_type_exception import UnsupportedTypeException
from argmax.model import BoundingBox

from ultralytics import YOLO


class Detection:

    def __init__(self):
        self.session = Session()
        self.model: Model = YOLO(model="yolo11n.pt")

    def _get_image(self, url: str) -> Image:
        """
        Helper function to download and create an Image object from a url.
        :param url: Url to an image on the internet.
        :return: A PIL Image object
        :raise ImageRetrievalException: On any networking or image manipulation error.
        """
        image: Image = None
        try:
            response = self.session.request("GET", url=url, stream=True)
            image = Image.open(response.raw)
        except requests.exceptions.Timeout as e:
            raise ImageRetrievalException("Timeout while retrieving image.", e)
        except requests.exceptions.TooManyRedirects as e:
            raise ImageRetrievalException("Too many redirects while retrieving image.", e)
        except requests.exceptions.RequestException as e:
            raise ImageRetrievalException("Unknown error while retrieving image.", e)
        except IOError as e:
            raise ImageRetrievalException("Unable to open or parse the retrieved image.", e)

        return image

    def _process_image(self, img: Image, query: str) -> tuple[List[BoundingBox], float]:
        """
        Process image looking for object passed in.
        :param img: Image object to search
        :param query: Item to search for
        :return Optional[DetectionResult]: If object found returns all found instances and the time it took to inference
        :raise ImageProcessingException: Raised if there is any type of error processing the image.
        """
        bounding_boxes = []
        try:
            results: List[Results] = self.model(img, imgsz=img.size, verbose=False)
        except Exception as e:
            raise ImageProcessingException("Error running object detection on the image.", e)

        if len(results) > 0:
            result = results[0]
            for idx, cls in enumerate(result.boxes.cls):
                if query == result.names[int(cls)]:
                    box = result.boxes.xyxy[idx]
                    bounding_boxes.append(BoundingBox(x=int(box[..., 0]), y=int(box[..., 1]), width=int(box[..., 2] - box[..., 0]), height=int(box[..., 3] - box[..., 1])))

            if len(bounding_boxes) > 0:
                return bounding_boxes, float(result.speed['inference'])
            else:
                return [], float(result.speed['inference'])

        return [], 0.0

    def find(self, image_url: str, query: str) -> tuple[Optional[List[BoundingBox]], float]:
        """
        Downloads and image from the internet and then runs image detection to see if the image contains the query parameter.
        :param image_url: HTTP url for an image on the internet
        :param query: object to look for in the downloaded image
        :return:
        """
        if query not in self.model.names.values():
            raise UnsupportedTypeException(f"The object type '{query}' is not supported.")
        image: Image = self._get_image(image_url)
        return self._process_image(image, query)


# Development testing scaffold
if __name__ == "__main__":
    d = Detection()
    d.find(image_url="https://ultralytics.com/images/bus.jpg", query="person")
