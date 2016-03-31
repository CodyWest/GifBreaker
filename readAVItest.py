from visvis.vvmovie import images2avi as vv

images = vv.readAvi("//Users/Programmer/Desktop/peacock.avi", False)
image = images[0]
print(image.size)
