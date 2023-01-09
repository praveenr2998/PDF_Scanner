# Each pdf file should be given as a dictionary of dictionaries

config_dict = {

    1 : {
        "file_path"     : "/home/praveen/Desktop/Projects/PDF_Scanner/data/raw_data/Womens_Equality.PDF",       # Path of PDF file
        "rotation"      : "L",       # Does the pages in PDF file require rotation - Options : None/L/R
        "split"         : "Y",       # Does the pages require split - Options : Y/N
        "type_of_split" : "AI",       # The type of split - Options : AI/NORMAL
        "skip_pages"    : 0        # The title/index pages need not be splitted, enter the page count - Options 0/{any number} 
    },

    # 2 : {
    #     "file_path"     : "",       # Path of PDF file
    #     "rotation"      : "",       # Does the pages in PDF file require rotation - Options : None/L/R
    #     "split"         : "",       # Does the pages require split - Options : Y/N
    #     "type_of_split" : "",       # The type of split - Options : AI/NORMAL
    #     "skip_pages"    : 1        # The title/index pages need not be splitted, enter the page count 
    # },



}