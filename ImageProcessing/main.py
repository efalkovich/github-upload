from PIL import Image
import os


def images_processing(path, n):
    root_name = 'TransformedImagesDir'
    path_to_root = path + '/../' + root_name
    if root_name not in os.listdir(path + '/..'):
        os.mkdir(path_to_root)

    lst_direct = os.listdir(path)
    for direct in lst_direct:
        path_to_imgs = path + '/' + direct
        imgs_dir = os.listdir(path_to_imgs)
        if direct not in os.listdir(path_to_root):
            os.mkdir(path_to_root + '/' + direct)
        for img_fn in imgs_dir:
            img = Image.open(path_to_imgs + '/' + img_fn)
            img_width = img.width
            img_height = img.height
            pixels = img.load()
            unic_colors = {}
            for i in range(img_width):
                for j in range(img_height):
                    pixel = pixels[i, j]
                    if pixel not in unic_colors.keys():
                        unic_colors[pixel] = 1
                    else:
                        unic_colors[pixel] += 1

            max_color = max(unic_colors, key=unic_colors.get)

            top = 0
            left = 0
            rigth = 0
            bottom = 0
            isStart = True
            for i in range(img_width):
                for j in range(img_height):
                    if pixels[i, j] != max_color:
                        if isStart:
                            top = j
                            bottom = j
                            left = i
                            rigth = i
                            isStart = False
                            continue
                        if j > bottom:
                            bottom = j
                        if j < top:
                            top = j
                        if i > rigth:
                            rigth = i

            bottom += 1
            rigth += 1
            img = img.crop((left, top, rigth, bottom))
            new_size_img = max((bottom - top, rigth - left))

            l_marg = 0
            t_marg = 0

            if bottom - top > rigth - left:
                l_marg = (bottom - top - (rigth - left)) // 2
            else:
                t_marg = (rigth - left - (bottom - top)) // 2
            bg = Image.new('RGB', (new_size_img, new_size_img), max_color)
            bg.paste(img, (l_marg, t_marg))
            bg = bg.resize((n, n), 4)
            bg_pixs = bg.load()
            for i in range(n):
                for j in range(n):
                    pix_val = bg_pixs[i, j]
                    if pix_val == max_color:
                        bg.putpixel((i, j), (255, 255, 255))
                    else:
                        bg.putpixel((i, j), (0, 0, 0))
            bg.save(path_to_root + '/' + direct + '/' + img_fn.split('.')[0] + '.png')
            print('Done: ' + direct + '/' + img_fn.split('.')[0] + '.png')



images_processing('a172308b-ea18-45ae-aa73-7592672613d4', 150)
