import cv2
import numpy as np
from retinavision.retina import Retina
from retinavision.cortex import Cortex
from retinavision import datadir, utils
from os.path import join
import os
from matplotlib import pyplot as plt

class CorticalMapping:
    def __init__(self):
        self.R = None
        self.C = None
        self.fixation = None

    def setup_cortex(self, retina_name):
        #Create and prepare cortex
        self.C = Cortex()
        lp = join(datadir, "cortices", "{0}_Lloc_final.pkl".format(retina_name))
        rp = join(datadir, "cortices", "{0}_Rloc_final.pkl".format(retina_name))
        self.C.loadLocs(lp, rp)
        self.C.loadCoeffs(join(datadir, "cortices", "{0}_Lcoeff.pkl".format(retina_name)), join(datadir, "cortices", "{0}_Rcoeff.pkl".format(retina_name)))

    def setup_retina(self, retina_name, fix_x, fix_y):
        #Create and load retina
        self.R = Retina()
        self.R.info()
        self.R.loadLoc(join(datadir, "retinas", "{0}_loc.pkl".format(retina_name)))
        self.R.loadCoeff(join(datadir, "retinas", "{0}_coeff.pkl".format(retina_name)))

        #Prepare retina
        # x = img.shape[1]/2
        # y = img.shape[0]/2
        # print("X: ", x)
        # print("Y: ", y)
        # print("Retina shape: ", img.shape)
        x = 120.0
        y = 112.0
        self.fixation = (y*fix_y,x*fix_x)
        self.R.prepare((224, 240, 3), self.fixation)


    def cortical_transform(self, im_array):
        V = self.R.sample(im_array, self.fixation)
        cimg = self.C.cort_img(V)
        # print("Cimg type: ", type(cimg))
        return cimg

    def backproject_transform(self, im_array):
        V = self.R.sample(im_array, self.fixation)
        tight = self.R.backproject_tight_last()
        # print("Cimg type: ", type(cimg))
        return tight

    def arr_to_img(self, img_arr, index):
        cv2.imwrite("{}/test_images/test_image_{}.jpg".format(os.getcwd(), index), img_arr)

        # cv2.imwrite("{}/examples/mario_backprojection.png".format(os.getcwd()), tight)
    # cv2.namedWindow("inverted", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("inverted", tight) 
            
    # cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("input", img) 
            
    # cv2.namedWindow("cortical", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("cortical", cimg)
            
    # key = cv2.waitKey(10)

