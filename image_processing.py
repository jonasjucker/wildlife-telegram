import os
import math
import sys
from PIL import Image

def images_from_folder(folder):
    return [os.path.join(folder,images) for images in os.listdir(folder) if 'jpg' in images]

def load_images(image_names):
    return [Image.open(name) for name in image_names]

def dimensions_of_total_image(images):
    
    total_nr = len(images)
    print(total_nr)
    sizes = {}
    sizes['x'] = math.ceil(math.sqrt(total_nr))
    sizes['y'] = math.ceil(math.sqrt(total_nr))

    orig_size = images[0].size
    shrink_size = (int(orig_size[0]/sizes['x']), int(orig_size[1]/sizes['y']))

    sizes['total'] = orig_size
    sizes['image'] = shrink_size

    return sizes

def compose_image(images, sizes):
    total_image =  Image.new('RGB',sizes['total'], (250,250,250))
    location = (0,0)
    col = 0
    for image in images:
        small_image = image.resize(sizes['image'])
        if col < sizes['x']:
            print(location)
            total_image.paste(small_image,location)
            location = (location[0] + sizes['image'][0], location[1])
            col += 1
        else:
            location = (0, location[1] + sizes['image'][1])
            print(location)
            total_image.paste(small_image,location)
            location = (sizes['image'][0], location[1] )
            col = 1

    return total_image

def split_into_chunks(image_names,chunksize):
    return [image_names[i:i+chunksize] for i in range(0,len(image_names),chunksize)]

def collective_image(source,destination,chunksize,identifier=None):
    image_chunks = split_into_chunks(images_from_folder(source), chunksize)
    names = []
    count = 0
    for chunk in image_chunks:
        if identifier:
            names.append(os.path.join(destination,f'{identifier}_composite_{count}.jpg'))
        else:
            names.append(os.path.join(destination,f'composite_{count}.jpg'))

        images = load_images(chunk)
        dims = dimensions_of_total_image(images)
        image = compose_image(images,dims)
        image.save(names[-1])
        count+=1

    return names
