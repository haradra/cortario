import cv2
import numpy as np
import argparse
from retinavision.retina import Retina
import matplotlib.pyplot as plt
from retinavision.cortex import Cortex
from retinavision import datadir, utils
from os.path import join
import os

def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of model described in the paper: Proximal Policy Optimization Algorithms for Super Mario Bros""")
    parser.add_argument("--retina_name", type=str, default="ret8k")
    parser.add_argument("--input_image_name", type=str)
    parser.add_argument("--output_image_name", type=str)
    parser.add_argument("--fix_x", type=float, default=1.0)
    parser.add_argument("--fix_y", type=float, default=1.0)
    args = parser.parse_args()
    return args

def transform(opt):
    #Create and load retina
    R = Retina()
    R.info()
    R.loadLoc(join("{}/PPO/data".format(os.getcwd()), "retinas", "{}_loc.pkl".format(opt.retina_name)))
    R.loadCoeff(join("{}/PPO/data".format(os.getcwd()), "retinas", "{}_coeff.pkl".format(opt.retina_name)))

    img = cv2.imread("{}/PPO/examples/{}.png".format(os.getcwd(), opt.input_image_name), cv2.COLOR_BGR2GRAY)
    # img = cv2.resize(img, (0,0), fx=5.0, fy=5.0)
        #cv2.COLOR_BGR2GRAY
        #IMREAD_GRAYSCALE
    print(type(img))

    #Prepare retina
    x = img.shape[1]/2
    y = img.shape[0]/2
    print(x)
    print(y)

    fixation = (y*opt.fix_y,x*opt.fix_x)
    print(x*opt.fix_x)
    print(y*opt.fix_y)
    R.prepare(img.shape, fixation)

    #Create and prepare cortex
    C = Cortex()
    lp = join("{}/PPO/data".format(os.getcwd()), "cortices", "{}_Lloc_final.pkl".format(opt.retina_name))
    rp = join("{}/PPO/data".format(os.getcwd()), "cortices", "{}_Rloc_final.pkl".format(opt.retina_name))
    C.loadLocs(lp, rp)
    C.loadCoeffs(join("{}/PPO/data".format(os.getcwd()), "cortices", "{}_Lcoeff.pkl".format(opt.retina_name)), join("{}/PPO/data".format(os.getcwd()), "cortices", "{}_Rcoeff.pkl".format(opt.retina_name)))

    V = R.sample(img, fixation)
    tight = R.backproject_tight_last()
    cimg = C.cort_img(V)
    cv2.imwrite("{}/PPO/examples/{}.png".format(os.getcwd(), opt.output_image_name), cimg)
    cv2.imwrite("{}/PPO/examples/{}_backprojection.png".format(os.getcwd(), opt.output_image_name), tight)
    # cv2.imwrite("{}/examples/mario_backprojection_1k.png".format(os.getcwd()), tight)
    # cv2.namedWindow("inverted", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("inverted", tight) 
            
    # cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("input", img) 
            
    # cv2.namedWindow("cortical", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("cortical", cimg)
            
    # key = cv2.waitKey(10)


if __name__ == "__main__":
    opt = get_args()
    transform(opt)