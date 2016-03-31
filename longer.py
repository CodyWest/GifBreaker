from visvis.vvmovie import images2avi as vv

images = vv.readAvi("//Users/Programmer/Desktop/peacock.avi", False)
ix = 0
wait = 30
bloom = 40
new_images = []
for image in images:
    ix = ix+1
    if ix == wait:
        for i in range(bloom):
            new_images.append(new_images[-1])
    else:
        new_images.append(image)
            
vv.writeAvi("mooshpeacock.avi", new_images, duration=.1)
