import traceback
from io import BytesIO

import cv2
import numpy as np
import requests
from skimage.metrics import structural_similarity

from core.image_comparator.ImageComparator import ImageComparator
from log.Logger import Logger

net_file_cache = {}


def read_file_from_url(url):
    """

    :param url:
    :return:
    """
    try:
        if url in net_file_cache:
            return net_file_cache[url]
        # 发送GET请求获取文件内容
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 根据换行符切割文件内容并返回列表
            lines = response.text.split('\n')
            net_file_cache[url] = lines
            return lines
        else:
            print(f"Failed to read file from URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class NetImageComparator(ImageComparator):
    def __init__(self, logger: Logger):
        # 用于缓存已下载图像的字典
        self.image_cache = {}
        self.logger = logger

    def download_image(self, url):
        """

        :param url:
        :return:
        """
        # 如果图像已经在缓存中，直接返回缓存的图像
        if url in self.image_cache:
            return BytesIO(self.image_cache[url])
        self.logger.print_log(f"正在下载图片：{url}")
        # 发送GET请求获取图片的二进制数据
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 将二进制数据转换为图像对象
            image_bytes = response.content
            # 将图像添加到缓存
            self.image_cache[url] = image_bytes

            image_bytes = BytesIO(image_bytes)

            return image_bytes
        else:
            # 如果请求失败，打印错误信息
            self.logger.print_log(f"Failed to download image: {url}. Status code: {response.status_code}")
            return None

    def compare_image(self, img, path_image):
        # 下载图片到内存
        try:
            downloaded_image = self.download_image(path_image)

            if downloaded_image:
                downloaded_image.seek(0)
                image_a = cv2.imdecode(np.frombuffer(downloaded_image.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
                downloaded_image.close()

                buffer_b = BytesIO()
                img.save(buffer_b, format="PNG")
                buffer_b.seek(0)

                # 使用内存中的图像数据
                image_b = cv2.imdecode(np.frombuffer(buffer_b.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)

                gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
                gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

                (score, diff) = structural_similarity(gray_a, gray_b, full=True)
                return score
            else:
                # 图片下载失败时的处理
                return 0
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.logger.print_log(f"对比图片错误：{path_image}")
            return 0

    def compare_with_path(self, path, images, lock_score, discard_score):
        """
            截图范围与文件路径内的所有图片对比
        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        select_name = ''
        score_temp = 0.00000000000000000000
        for img in images:
            for fileName in read_file_from_url(path + "list.txt"):
                score = self.compare_image(img, path + fileName)
                if score > score_temp:
                    score_temp = score
                    select_name = fileName.split('.')[0]
                if score_temp > lock_score:
                    break
        if score_temp < discard_score:
            select_name = None
        return select_name, score_temp
