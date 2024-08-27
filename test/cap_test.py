from core.screentaker.CapScreenTaker import CapScreenTaker
from net.socket.NetImageComparator import NetImageComparator

if __name__ == '__main__':
    base_path = "http://1.15.138.227:9000/apex/images/"
    box = []
    screen_taker = CapScreenTaker()
    image_comparator = NetImageComparator(base_path)
    img = screen_taker.get_images_from_bbox([box])[0]
    # image_path, x, y, w, h = "bag.png", 780, 37, 1784, 78
    image_path, x, y, w, h = "bag.png", 0, 37, 1004, 78
    image_path = base_path + "licking/2560x1440/bag/" + image_path
    box = (int(x), int(y), int(w), int(h))
    score = image_comparator.compare_image(img, image_path)
