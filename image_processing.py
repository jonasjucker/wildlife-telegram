import os
import math
import sys
import logging
from PIL import Image
from natsort import natsorted

def images_from_folder(folder):
    images = natsorted([os.path.join(folder,images) for images in os.listdir(folder) if 'jpg' in images])

    # we want most recent images first
    images.reverse()
    return images

def load_images(image_names):
    return [Image.open(name) for name in image_names]

def dimensions_of_total_image(images):
    
    total_nr = len(images)
    logging.debug(f'Compute ratios for {total_nr} sub-images')
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
            logging.debug(f'Place sub-image at location:{location}')
            total_image.paste(small_image,location)
            location = (location[0] + sizes['image'][0], location[1])
            col += 1
        else:
            location = (0, location[1] + sizes['image'][1])
            logging.debug(f'Place sub-image at location:{location}')
            total_image.paste(small_image,location)
            location = (sizes['image'][0], location[1] )
            col = 1

    return total_image

def split_into_chunks(image_names,chunksize):
    return [image_names[i:i+chunksize] for i in range(0,len(image_names),chunksize)]

def collective_image(source,destination,chunksize,identifier=None):
    logging.info(f'Create collective image with {chunksize} sub-images')
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

if __name__ == '__main__' :
    from events import EventHandler
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        level=logging.DEBUG,
    )

    logger = logging.getLogger(__name__)
    event = EventHandler('photos','videos','test')
    event_names = event.list('p',ignore=['.gitkeep','test'])
    print(event_names)
    _ = collective_image('photos/2022-05-23_08','composites',25,identifier='y')
