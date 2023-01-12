# PDF_Scanner

## WORKING
![Working](https://github.com/praveenr2998/PDF_Scanner/blob/main/Readme%20Images/Working%20Diagram.png?raw=true)

## DIRECTORY
![Directory](https://github.com/praveenr2998/PDF_Scanner/blob/main/Readme%20Images/directory%20structure.png?raw=true)

## SETUP AND EXECUTION 

```
git clone https://github.com/praveenr2998/PDF_Scanner.git
cd PDF_Scanner
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt 
```
#### config.py
![Config](https://github.com/praveenr2998/PDF_Scanner/blob/main/Readme%20Images/Config.png?raw=true)  

**file_path**     - Complete path of the PDF file to be processed   
**rotation**      - Rotation for each page, only 90 degree clockwise and 90 degree counter-clockwise rotation   
**split**         - Currently this parameter is dormant, the image will split by default  
**type_of_split** - Normal split or split after cropping page using AI  
**skip_pages**    - If title/index page need not be processed they can be skipped by entering number of pages to be skipped here  
  

After the config is updated 
```
cd code
python3 process_pdf.py
```
##OUTPUT
The output is generated as a PDF file and is stored in **../PDF_Scanner/data/output/** directory

## YOLO SPECIFIC CONFIGURATIONS
https://github.com/ultralytics/yolov5 - YOLOv5s is the model used for cropping pages  
Slight modifications are done to **code/yolov5/detect.py**  
The number of predictions perimage is limited to **1**  
Only if the accuracy is greater than **90** or **0.9** the page is cropped or else the source image is unaltered

## FUTURE WORK
1. Adding optional split functionality
2. Better accuracy while cropping images
3. Find orientation of pages in PDF automatically
4. Parallely processing PDFs 
