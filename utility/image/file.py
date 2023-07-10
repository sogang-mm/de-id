import os
import cv2
import torchvision.utils as vutils

from utility.image.visualize import draw_boxed_text


def save_cropped_faces(image_name:str, cropped_faces, save_dir):
    image_name.replace(".jpg", "")
    for idx, cropped_face in enumerate(cropped_faces):
        cv2.imwrite(os.path.join(save_dir, f"{image_name}_{idx}.jpg"), cropped_face)

def save_face_txt(path, face_regions):
    with open(path, "w") as file:
        for face_region in face_regions:
            file.write(face_region + "\n")
    return True

def save_tensort2image(image, path):
    """
    Save a image using PyTorch's save_image function.

    Args:
        image (torch.Tensor): An image tensor to save. Shape: [C, H, W]
        path (str): The path where the image will be saved.

    """
    # Check if the image tensor is on the GPU and if so send it back to the CPU
    image = image.cpu()

    # Unnormalize the image
    image = (image * 0.5) + 0.5

    # Add a dimension to the image tensor and save it
    vutils.save_image(image.unsqueeze(0), path)


def save_bbox_image_xywh(save_path, image, labels):
    for i, label in enumerate(labels):
        _, cls, conf, x, y, width, height = label

        left = int(x)
        top = int(y)
        right = int(x + width)
        bottom = int(y + height)

        txt_loc = (max(left + 2, 0), max(top + 2, 0))
        txt = 'i: {:.2f}'.format(conf)
        image = draw_boxed_text(image, txt, txt_loc, (0, 255, 0))

        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imwrite(save_path, image)


def save_bbox_image_yolo(save_path, image, labels):
    for label in labels:
        _, x, y, width, height = map(float, label.split(" "))

        left = int((x - width / 2) * image.shape[1])
        top = int((y - height / 2) * image.shape[0])
        right = int((x + width / 2) * image.shape[1])
        bottom = int((y + height / 2) * image.shape[0])

        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imwrite(save_path, image)