import numpy as np
import cv2
import os
import time
import subprocess
import shutil
from pdf2image import convert_from_path
from PIL import Image
from config import config_dict


class processPdf:
    def __init__(self) -> None:
        self.destination_path = "/output/" 
        pass

    def classic_process(self, source_file_path, skip_pages, angle_of_rotation = None):
        """
        Used to process PDFs normally, takes a page from PDF, applies rotation if necessary, splits page into half
        and stitches the split pages back to a PDF.

        :param source_file_path  : String - Source path of PDF file
        :param skip_pages        : Int - The int(page count) given here will be skipped in the PDF file
        :param angle_of_rotation : String - Options - L/R/None, left/right/no rotation for each page in the PDF
        """

        self.images = convert_from_path(source_file_path)
        processed_image_list = []
        
        if skip_pages > 0:
            processed_image_list.extend(self.images[0:skip_pages])

        for i in range(skip_pages, len(self.images)):
            cv_image = np.array(self.images[i])
            if angle_of_rotation is not None:
                cv_image = self.rotate_image(cv_image, angle_of_rotation) 
            height = cv_image.shape[0]
            width = cv_image.shape[1]

            # Cut the image in half
            width_cutoff = width // 2
            page_1 = cv_image[:, :width_cutoff]
            page_2 = cv_image[:, width_cutoff:]

            # Convert to opecv image to PIL image
            page_1 = Image.fromarray(page_1)
            page_2 = Image.fromarray(page_2)

            processed_image_list.extend([page_1.convert('RGB'), page_2.convert('RGB')])


        os.chdir("../data/output/")

        # converting the PIL images back to PDF
        processed_image_list[0].save(f'{source_file_path.split("/")[-1]}', save_all=True, append_images=processed_image_list[1 : ])
        os.chdir("../../code/")

    def rotate_image(self, img, angle_of_rotation):
        """
        Used to rotate the pages in PDF. Only 90 degree clockwise and 90 degree counter-clockwise rotation is done

        :param img               : cv2 image - The image to be rotated as a cv2 image
        :param angle_of_rotation : String - Options - L/R/None, left/right/no rotation for each page in the PDF
        """

        if angle_of_rotation == 'L':
            image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if angle_of_rotation == 'R':
            image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        return image

    def ai_process(self, source_file_path, skip_pages, angle_of_rotation = None):
        """
        Used to process PDFs using computer vision algorithms, takes a page from PDF, applies rotation if necessary, splits page into half
        and stitches the split pages back to a PDF.

        :param source_file_path  : String - Source path of PDF file
        :param skip_pages        : Int - The int(page count) given here will be skipped in the PDF file
        :param angle_of_rotation : String - Options - L/R/None, left/right/no rotation for each page in the PDF
        """

        self.images = convert_from_path(source_file_path)
        os.chdir("../data/unprocessed_images/")
        direct = os.getcwd()

        # Clearing up the unprocessed_images directory so that in each iteration no images are present inside it
        for f in os.listdir(direct):
            os.remove(os.path.join(direct, f))

        for idx in range(0, len(self.images)):
            cv_image = np.array(self.images[idx])
            # Rotating if needed
            if angle_of_rotation is not None:
                cv_image = self.rotate_image(cv_image, angle_of_rotation)
            cv2.imwrite(f"{idx}.jpg", cv_image)
        unprocessed_img_dir = os.getcwd()
        os.chdir("../../code/yolov5")
        
        # Clearing up exp directory so that in each iteration no images are present inside it
        shutil.rmtree("runs/detect/exp")
        
        # Yolo produces cropped pages having just one bbox per image and accuracy greater than 90% or 0.9 so anything less than 0.9 or 
        # 90% is not processed and the source image is stitched back to resultant PDF
        # Executing yolo code using CLI command
        execution_cmd = "python3 detect.py --weights best.pt --source " + unprocessed_img_dir + " --save-crop"
        subprocess.run(execution_cmd.split(" "))

        unprocessed_img_dir_files = os.listdir(unprocessed_img_dir)
        processed_img_dir_files = os.listdir("runs/detect/exp/crops/Page/")
        
        # Sort files in order
        unprocessed_img_dir_files = sorted( unprocessed_img_dir_files,
                        key = lambda x: os.path.getmtime(os.path.join(unprocessed_img_dir, x))
                        )

        # If files are present in exp/crops/Page/ it is taken else the source image from unprocessed_images directory is used for the resultant PDF
        processed_image_list = []
        if skip_pages > 0:
            for n in range(skip_pages):
                pil_image = Image.open(f"{unprocessed_img_dir}/{n}.jpg")
                processed_image_list.append(pil_image)
                unprocessed_img_dir_files.remove(f"{n}.jpg")

        # Splitting the cropped images and stitching it back to PDF
        for img in unprocessed_img_dir_files:
            if img in processed_img_dir_files:
                cv_image = cv2.imread(f"runs/detect/exp/crops/Page/{img}")
                width = cv_image.shape[1]

                # Cut the image in half
                width_cutoff = width // 2
                page_1 = cv_image[:, :width_cutoff]
                page_2 = cv_image[:, width_cutoff:]

                # Convert to opecv image to PIL image
                page_1 = Image.fromarray(page_1)
                page_2 = Image.fromarray(page_2)

                processed_image_list.extend([page_1.convert('RGB'), page_2.convert('RGB')])

            else:
                pil_image = Image.open(f"{unprocessed_img_dir}/{img}")
                processed_image_list.append(pil_image)
        
        os.chdir("../../data/output")
        # converting the PIL images back to PDF
        processed_image_list[0].save(f'{source_file_path.split("/")[-1]}', save_all=True, append_images=processed_image_list[1 : ])
        os.chdir("../../code/")



processPdf_obj = processPdf()

for key in config_dict:
    if config_dict[key]['type_of_split'] == 'NORMAL': 
        print("######### Processing PDFs Normally #########")
        print(f"Processing ========> {config_dict[key]['file_path']}")
        processPdf_obj.classic_process(source_file_path = config_dict[key]['file_path'], skip_pages = config_dict[key]['skip_pages'], angle_of_rotation = config_dict[key]['rotation'])
    else:
        print("######### Processing PDFs Using AI #########")
        print(f"Processing ========> {config_dict[key]['file_path']}")
        processPdf_obj.ai_process(source_file_path = config_dict[key]['file_path'], skip_pages = config_dict[key]['skip_pages'], angle_of_rotation = config_dict[key]['rotation'])