import cv2

from core.screentaker.CapScreenTaker import CapScreenTaker
from log import LogFactory
from net.socket.NetImageComparator import NetImageComparator

if __name__ == '__main__':
    LogFactory.init_logger()
    base_path = "http://1.15.138.227:9000/apex/images/"
    screen_taker = CapScreenTaker({
        "width": 2560,
        "height": 1440,
        "frame_rate": 144,
        "format": "MJPG"
    })
    image_comparator = NetImageComparator(base_path)
    image_path, x, y, w, h = "bag_cap.png", 779, 37, 897, 75
    box = (int(x), int(y), int(w), int(h))
    image_path = base_path + "licking/2560x1440/bag/" + image_path
    # 显示两张图片
    while True:
        img = screen_taker.get_images_from_bbox([box])[0]
        # 显示这帧内容
        score = image_comparator.compare_image(img, image_path)
        print(score)
        # 如果按下 'q' 键则退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # 释放摄像头并关闭所有窗口
    cv2.destroyAllWindows()
