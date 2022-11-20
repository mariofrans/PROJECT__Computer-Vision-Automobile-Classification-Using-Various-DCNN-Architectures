import os, io, math
import pandas as pd
from rembg.bg import remove
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

########################################################################################################################################

PATH_DATA = 'BINUS Sem 8/Mario/data'
PATH_DATA_REMOVED_BG = 'BINUS Sem 8/Mario/data_remove_bg'

########################################################################################################################################

def remove_bg(path_input_output):

    path_input, path_output = path_input_output

    # load image
    image = Image.open(path_input)

    # remove background
    with io.BytesIO() as buf:
        image.save(buf, 'jpeg')
        image = buf.getvalue()
        image = remove(image)

    # convert into icon
    image = Image.open(io.BytesIO(image))
    image = image.convert("RGBA")

    # change background to white
    background = Image.new(image.mode[:-1], image.size, (255, 255, 255))
    background.paste(image, image.split()[-1]) 
    image = background

    # convert back to jpeg
    image = image.convert('RGB')
    image.save(path_output, 'JPEG')

########################################################################################################################################

# get all files in original directory
files = [i for i in os.listdir(PATH_DATA) if '.DS_Store' not in i]

# generate df of original and final directories
df = pd.DataFrame()

for file in files:
    df_file = pd.DataFrame()
    images = [i for i in os.listdir(f'{PATH_DATA}/{file}') if '.DS_Store' not in i]
    df_file['path_original'] = [f'{PATH_DATA}/{file}/{i}' for i in images]
    df_file['path_remove_bg'] = [f'{PATH_DATA_REMOVED_BG}/{file}/{i}' for i in images]
    # df_file['path_remove_bg'] = [i.replace('.jpg', '.png') for i in list(df_file['path_remove_bg'])]
    df = pd.concat([df, df_file])

########################################################################################################################################

# if __name__ == '__main__':

#     # split df into chunks of n sizes each
#     n = 25
#     list_df_chunks = [df[i:i+n].copy() for i in range(0, len(df), n)]

#     count = 0

#     for i in range(len(list_df_chunks)):

#         df_chunk = list_df_chunks[i]
        
#         count += len(df_chunk)
#         print('Completed:', count, '/', len(df))

#         # collect multiprocessing parameters
#         list_path_original, list_path_remove_bg = list(df_chunk['path_original']), list(df_chunk['path_remove_bg'])
#         list_path_input_output = [[list_path_original[j], list_path_remove_bg[j]] for j in range(len(df_chunk))]

#         # start multiprocessing
#         p = Pool(processes=len(df))
#         p.map(remove_bg, list_path_input_output)
#         p.close()

        