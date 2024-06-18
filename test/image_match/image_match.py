import time

import cv2
import numpy as np


def match_template(origin_image, match_image_list, save_image=False, early_termination=True, threshold=0.6):
    # 转换为灰度图
    image_gray = cv2.cvtColor(origin_image, cv2.COLOR_BGR2GRAY)
    found_list = []
    temp_scale = None
    for match_image in match_image_list:
        template_gray = cv2.cvtColor(match_image, cv2.COLOR_BGR2GRAY)
        # 获取模板的原始宽高
        template_height, template_width = template_gray.shape[:2]
        found = None
        # 定义缩放范围
        if temp_scale is None:
            scales = np.linspace(0.5, 1.5, 5)[::-1]
        else:
            scales = np.linspace(temp_scale - 0.4, temp_scale + 0.4, 5)[::-1]
        for scale in scales:
            resized = cv2.resize(template_gray, (int(template_width * scale), int(template_height * scale)))
            r = float(resized.shape[1]) / template_gray.shape[1]

            if resized.shape[0] > image_gray.shape[0] or resized.shape[1] > image_gray.shape[1]:
                continue

            result = cv2.matchTemplate(image_gray, resized, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if found is None or max_val > found[0]:
                found = (max_val, max_loc, r)
                temp_scale = scale
                if found[0] > threshold:
                    print(scales)
                    break

        if found is not None and found[0] >= threshold:
            max_val, max_loc, r = found
            print(f"Match found with value: {max_val}")
            start_x, start_y = int(max_loc[0]), int(max_loc[1])
            end_x, end_y = int((max_loc[0] + template_width * r)), int((max_loc[1] + template_height * r))
            found_list.append((start_x, start_y, end_x, end_y))
            if early_termination:
                break
        else:
            print("no found")
    if save_image and len(found_list) > 0:
        for found in found_list:
            # 在原图上绘制矩形框
            cv2.rectangle(origin_image, (found[0], found[1]), (found[2], found[3]), (0, 255, 0), 2)
        cv2.imwrite('result.png', origin_image)


if __name__ == '__main__':
    # 读取图像
    image_path = 'big.png'  # 替换为你的大图路径
    image = cv2.imread(image_path)

    template_path = ['s.png', 's1.png', 's2.png']  # 替换为你要查找的小图路径
    template_image = [cv2.imread(template) for template in template_path]

    start = time.time()
    match_template(image, template_image, save_image=True, early_termination=False)
    end = time.time()
    print(f"Match template time: {int((end - start) * 1000)}ms")
