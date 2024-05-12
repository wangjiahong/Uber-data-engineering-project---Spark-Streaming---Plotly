# import requests
# import os

# def download_images(base_url, num_images, output_folder):
#     # 确保输出文件夹存在
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
#         print(f"Created folder: {output_folder}")

#     # 下载图片
#     for i in range(1, num_images + 1):
#         img_url = f"{base_url}"  # 指定图片大小为200x200像素
#         response = requests.get(img_url)
#         if response.status_code == 200:
#             img_path = os.path.join(output_folder, f'image_{i}.jpg')
#             with open(img_path, 'wb') as f:
#                 f.write(response.content)
#             print(f"Downloaded: {img_path}")
#         else:
#             print(f"Failed to download image {i} from {img_url}")

# # 配置参数
# base_url = "https://picsum.photos/200"
# num_images = 200
# output_folder = "./output_download_pics"

# # 执行下载
# download_images(base_url, num_images, output_folder)


import aiohttp
import asyncio
import os

async def download_image(session, url, idx, output_folder):
    async with session.get(url) as response:
        if response.status == 200:
            img_path = os.path.join(output_folder, f'image_{idx}.jpg')
            with open(img_path, 'wb') as f:
                f.write(await response.read())
            print(f"Downloaded: {img_path}")
        else:
            print(f"Failed to download image {idx} from {url}")

async def download_images(base_url, num_images, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    
    # Create a session and download images
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, base_url, i, output_folder) for i in range(1, num_images + 1)]
        await asyncio.gather(*tasks)

# Parameters
base_url = "https://picsum.photos/200"
num_images = 500
output_folder = "./output_download_pics"

# Run the asynchronous download
asyncio.run(download_images(base_url, num_images, output_folder))
