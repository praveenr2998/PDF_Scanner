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
        processed_image_list[0].save(f'{source_file_path.split("/")[-1]}', save_all=True, append_images=processed_image_list[1 : -1])

    def rotate_image(self, img, angle_of_rotation):
        if angle_of_rotation == 'L':
            image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        if angle_of_rotation == 'R':
            image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        return image

    def ai_process(self, source_file_path, skip_pages, angle_of_rotation = None):
        self.images = convert_from_path(source_file_path)
        os.chdir("../data/unprocessed_images/")
        direct = os.getcwd()
        for f in os.listdir(direct):
            os.remove(os.path.join(direct, f))
        for idx in range(0, len(self.images)):
            cv_image = np.array(self.images[idx])
            if angle_of_rotation is not None:
                cv_image = self.rotate_image(cv_image, angle_of_rotation)
            cv2.imwrite(f"{idx}.jpg", cv_image)
        unprocessed_img_dir = os.getcwd()
        os.chdir("../../code/yolov5")
        print("########", os.listdir("runs/detect"))
        shutil.rmtree("runs/detect/exp")
        execution_cmd = "python3 detect.py --weights best.pt --source " + unprocessed_img_dir + " --save-crop"
        subprocess.run(execution_cmd.split(" "))

        unprocessed_img_dir_files = os.listdir(unprocessed_img_dir)
        processed_img_dir_files = os.listdir("runs/detect/exp/crops/Page/")
        
        # Sort files in order
        unprocessed_img_dir_files = sorted( unprocessed_img_dir_files,
                        key = lambda x: os.path.getmtime(os.path.join(unprocessed_img_dir, x))
                        )

        processed_image_list = []
        if skip_pages > 0:
            for n in range(skip_pages):
                pil_image = Image.open(f"{unprocessed_img_dir}/{n}.jpg")
                processed_image_list.append(pil_image)
                unprocessed_img_dir_files.remove(f"{n}.jpg")

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
        processed_image_list[0].save(f'{source_file_path.split("/")[-1]}', save_all=True, append_images=processed_image_list[1 : -1])


            








        
            
             





  





processPdf_obj = processPdf()


for key in config_dict:
    if config_dict[key]['type_of_split'] == 'NORMAL': 
        print("######### Processing PDFs Normally #########")
        processPdf_obj.classic_process(source_file_path = config_dict[key]['file_path'], skip_pages = config_dict[key]['skip_pages'], angle_of_rotation = config_dict[key]['rotation'])
    else:
        print("######### Processing PDFs Using AI #########")
        processPdf_obj.ai_process(source_file_path = config_dict[key]['file_path'], skip_pages = config_dict[key]['skip_pages'], angle_of_rotation = config_dict[key]['rotation'])