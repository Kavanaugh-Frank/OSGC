import os
import math
import uuid
import rasterio
import pandas as pd
import georasters as gr
from flask import Flask, request, jsonify
from os import listdir
from os.path import isfile, join
from osgeo import gdal

app = Flask(__name__)

@app.route('/')
def index():
    print(request.values)
    upper_left_x = float(request.values.get("ux", 0))
    upper_left_y = float(request.values.get("uy", 0))
    lower_right_x = float(request.values.get('lx', 0))
    lower_right_y = float(request.values.get('ly', 0))
    
    xl = math.ceil(abs(upper_left_x))
    yl = math.ceil(abs(upper_left_y))
    x2 = math.ceil(abs(lower_right_x))
    y2 = math.ceil(abs(lower_right_y))
    
    # Look up image files containing the coordinates
    file1 = look_up_image_file(upper_left_x, upper_left_y, determine_position(upper_left_x), determine_position(upper_left_y))
    file2 = look_up_image_file(lower_right_x, lower_right_y, determine_position(lower_right_x), determine_position(lower_right_y))
    
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    
    if file1 == file2:
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, file1, projWin=window)
        img = rasterio.open(cropped_file_name)
        full_img = img.read()
        df = pd.DataFrame(full_img[0])
        img.close()
        os.remove(cropped_file_name)
    elif (xl == x2 and yl == y2 + 1) or (xl == x2 + 1 and yl == y2):
        files_to_merge = [file1, file2]
        merged_file_name = str(uuid.uuid4()) + '.tif'
        g = gdal.Warp(merged_file_name, files_to_merge, format="GTiff")
        g = None
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, merged_file_name, projWin=window)
        img = rasterio.open(cropped_file_name)
        full_img = img.read()
        df = pd.DataFrame(full_img[0])
        img.close()
        os.remove(merged_file_name)
        os.remove(cropped_file_name)
    elif (xl == x2 + 1 and yl == y2 + 1):
        file3 = look_up_image_file(lower_right_x, upper_left_y, determine_position(lower_right_x), determine_position(upper_left_y))
        file4 = look_up_image_file(upper_left_x, lower_right_y, determine_position(upper_left_x), determine_position(lower_right_y))
        merged_file_name = str(uuid.uuid4()) + '.tif'
        files_to_merge = [file1, file2, file3, file4] 
        g = gdal.Warp(merged_file_name, files_to_merge, format="GTiff")
        g = None
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, merged_file_name, projWin=window)
        img = rasterio.open(cropped_file_name)
        full_img = img.read()
        df = pd.DataFrame(full_img[0])
        img.close()
        os.remove(merged_file_name)
        os.remove(cropped_file_name)
    
    json_data = df.to_json(orient='values')
    print(json_data)
    return jsonify(json_data)

@app.route('/ougs/')
def ougs():
    print(request.values)
    upper_left_x = float(request.values.get('ux', 0))
    upper_left_y = float(request.values.get('uy', 0))
    lower_right_x = float(request.values.get('lx', 0))
    lower_right_y = float(request.values.get('ly', 0))
    rx = float(request.values.get('rx', 0))
    ry = float(request.values.get('ry', 0))
    
    xl = math.ceil(abs(upper_left_x))
    yl = math.ceil(abs(upper_left_y))
    x2 = math.ceil(abs(lower_right_x))
    y2 = math.ceil(abs(lower_right_y))
    
    file1 = look_up_image_file(upper_left_x, upper_left_y, determine_position(upper_left_x), determine_position(upper_left_y))
    file2 = look_up_image_file(lower_right_x, lower_right_y, determine_position(lower_right_x), determine_position(lower_right_y))
    
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    
    if file1 == file2:
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, file1, projWin=window)
        cropped = gr.from_file(cropped_file_name)
        df = cropped.to_pandas()
        df1 = modify_df_ougs(df, rx, ry)
        os.remove(cropped_file_name)
    elif (xl == x2 and yl == y2 + 1) or (xl == x2 + 1 and yl == y2):
        files_to_mosaic = [file1, file2]
        merged_file_name = str(uuid.uuid4()) + '.tif'
        g = gdal.Warp(merged_file_name, files_to_mosaic, format="GTiff")
        g = None
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, merged_file_name, projWin=window)
        cropped = gr.from_file(cropped_file_name)
        df = cropped.to_pandas()
        df1 = modify_df_ougs(df, rx, ry)
        os.remove(merged_file_name)
        os.remove(cropped_file_name)
    elif (xl == x2 + 1 and yl == y2 + 1):
        file3 = look_up_image_file(lower_right_x, upper_left_y, determine_position(lower_right_x), determine_position(upper_left_y))
        file4 = look_up_image_file(upper_left_x, lower_right_y, determine_position(upper_left_x), determine_position(lower_right_y))
        merged_file_name = str(uuid.uuid4()) + '.tif'
        files_to_mosaic = [file1, file2, file3, file4]
        g = gdal.Warp(merged_file_name, files_to_mosaic, format="GTiff")
        g = None
        cropped_file_name = str(uuid.uuid4()) + '.tif'
        gdal.Translate(cropped_file_name, merged_file_name, projWin=window)
        cropped = gr.from_file(cropped_file_name)
        df = cropped.to_pandas()
        df1 = modify_df_ougs(df, rx, ry)
        os.remove(merged_file_name)
        os.remove(cropped_file_name)
    
    json_data = df1.to_json(orient='values')
    print(json_data)
    return jsonify(json_data)

def modify_df_ougs(df, rx, ry):
    lst = df.iloc[-1].tolist()
    row = int(lst[0]) + 1
    col = int(lst[1]) + 1
    df['row'] = df['row'].apply(lambda x: (x * 32.8084) + rx)
    df['col'] = df['col'].apply(lambda x: (x * 32.8084) + ry)
    df['value'] = df['value'].apply(lambda x: x * 3.28084)
    df = df.drop(['x', 'y'], axis=1)
    df = df.rename(columns={'col': 'x', 'row': 'y'})
    df1 = pd.DataFrame({"x": [row], "y": [col]})
    df1 = pd.concat([df1, df])
    df1 = df1.round(2)
    return df1

def look_up_image_file(x, y, xpos, ypos):
    xceil = math.ceil(abs(x))
    yceil = math.ceil(abs(y))
    if x >= 100:
        look_up_file_str = f"{ypos}{yceil}{xpos}{xceil}.tif"
    else:
        look_up_file_str = f"{ypos}{yceil}{xpos}0{xceil}.tif"
    only_files = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
    for f in only_files:
        if look_up_file_str in f:
            return f
    return "notfound"

def determine_position(coord):
    if coord < 0:
        return 'w'
    else:
        return 'e'

if __name__ == "__main__":
    app.run(debug=True)
