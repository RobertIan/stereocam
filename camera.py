import picamera
import logging
import argparse
import time
import io


class App:

    def __init__(self, imformat, vcodec, res, exposure, rate, iteration, outputfile):
        # setup log
        datlog = logging.getLogger('cameralog')
        hdlr = logging.FileHandler('../log/cameralog.log')
        formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s', "%m/%d/%Y:%H:%M:%S.%f")
        hdlr.setFormatter(formatter)
        datlog.addHandler(hdlr)
        datlog.setLevel(logging.INFO)

        ##datlog.info("camera initiated stack n= ",str(itterations)," format= ",str(imformat)," output to=",str(outputfile))
        self.n = int(iteration)
        self.out = '../data/','camera_',str(time.asctime()),'/',outputfile

        # setup camera
        self.camera = picamera.PiCamera()
        self.camera.resolution = tuple(int(item) for item in res.split('x') if item.strip())
        self.imformat = imformat
        self.vcodec = vcodec
        self.camera.exposure_mode = exposure
        self.camera.framerate = int(rate)

        logging.info('camera exposure setting:'+str(self.camera.exposure_mode))
        logging.info('camera shutter speed:'+str(self.camera.shutter_speed))
        time.sleep(2)

    def capimage(self):
        self.camera.capture('%s.%s' % (self.out, self.imformat))


    def capimagestack(self):
        self.camera.capture_sequence((str(self.out)+'_%04d.jpg' % i for i in range(self.n)), use_video_port=False)

    def capvideo(self):
        self.camera.start_recording('%s.%s' % (str(self.out), 'mkv'), format=self.vcodec)
        time.sleep(self.n)
        self.camera.stop_recording()

    def capraw(self):
        #stream = io.BytesIO()
        camera.capture('{timestamp:%H-%M-%S-%f}.jpg', format='jpeg', bayer=True)

    def capcontinuous(self):
        stream = io.BytesIO()
        camera.capture()


if __name__=='__main__':

    #command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--stack", help="capture image stack, takes no input", action='store_true')
    ap.add_argument("-v", "--video", help="capture video, takes no input", action='store_true')
    ap.add_argument("-i", "--image", help="capture single image, takes no input", action='store_true')
    ap.add_argument("-r","--resolution", help="image resolution, default: 1920x1080")
    ap.add_argument("-e","--exposure", help="exposure mode, default: 'sports'")
    ap.add_argument("-r", "--framerate", help="video framerate, default: 30")
    ap.add_argument("-f", "--format", help="pass image file format")
    ap.add_argument("-vc", "--codec", help="pass the video codec to be used")
    ap.add_argument("-n", "--number", help="pass number of output objects or the length of video file in seconds")
    ap.add_argument("-o", "--output", help="output file name")
    args = vars(ap.parse_args())

    # defaults
    if args["resolution"]:
        resx, resy = args["resolution"].split("x")
        resolution = (int(resx), int(resy))
    else:
        resolution = (1920, 1080)
    if args["exposure"]:
        exposure = args["exposure"]
    else:
        exposure = 'sports'
    if args["framerate"]:
        rate = int(args["framerate"])
    else:
        rate = 30
    if args["format"]:
        imformat=str(args["format"])
    else:
        imformat='png'
    if args["codec"]:
        videocodec = str(args["codec"])
    else:
        videocodec = 'h264'
    if args["number"]:
        num = args["number"]
    else:
        num = 1
    if args["output"]:
        out = str(args["codec"])
    else:
        out = 'output%s' % str(time.asctime(time.localtime(time.time())))

    # initiate camera
    kamera = App(imformat, videocodec, resolution, exposure, rate, num, out)

    # captures
    if args["image"]:
        if args["format"]=='RAW':
            kamera.capRAW()
        else:
            kamera.capimage()
    if args["video"]:
        kamera.capvideo()
    if args["stack"]:
        kamera.capimagestack()


