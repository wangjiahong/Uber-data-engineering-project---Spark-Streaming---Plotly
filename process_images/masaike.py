from PIL import Image
import numpy as np
import os

def average_color(image):
    """计算图片的平均颜色"""
    np_image = np.array(image)
    w, h, d = np_image.shape
    return tuple(np.average(np_image.reshape(w * h, d), axis=0))

def find_closest_tile(tile, tiles):
    """在瓷砖中找到与给定瓷砖颜色最接近的瓷砖"""
    min_dist = float('inf')
    selected_tile = None
    tile_avg_color = average_color(tile)
    for t in tiles:
        dist = np.sqrt(sum((a - b) ** 2 for a, b in zip(tile_avg_color, t['avg_color'])))
        if dist < min_dist:
            min_dist = dist
            selected_tile = t['image']
    return selected_tile

def create_color_matching_mosaic(target_image_path, tiles_folder, output_size, tiles_size):
    target_image = Image.open(target_image_path)
    target_image = target_image.resize(output_size)

    # 读取并缩放所有瓷砖图片
    tiles = []
    for img_name in os.listdir(tiles_folder):
        if img_name.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(tiles_folder, img_name)
            img = Image.open(img_path)
            img = img.resize(tiles_size)
            tiles.append({'image': img, 'avg_color': average_color(img)})

    mosaic = Image.new('RGB', output_size)

    # 为目标图像的每个瓷砖位置选择最合适的图片
    x_tiles_count = output_size[0] // tiles_size[0]
    y_tiles_count = output_size[1] // tiles_size[1]
    for y in range(y_tiles_count):
        for x in range(x_tiles_count):
            box = (x * tiles_size[0], y * tiles_size[1], (x + 1) * tiles_size[0], (y + 1) * tiles_size[1])
            region = target_image.crop(box)
            closest_tile = find_closest_tile(region, tiles)
            mosaic.paste(closest_tile, box)

    mosaic.save('mosaic_color_matched_output_2.png')

# 参数配置
create_color_matching_mosaic('./image.png', './output_download_pics', output_size=(10000, 10000), tiles_size=(200, 200))
