from visvis.vvmovie import images2avi as vv

images = vv.readAvi("//Users/Programmer/Desktop/peacock.avi", False)
vv.writeAvi("longpeacock.avi", images, duration=1)
