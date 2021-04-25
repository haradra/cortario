FROM pytorch/pytorch:1.8.0-cuda11.1-cudnn8-runtime
WORKDIR /tmp

# install packages by updating base env in conda
COPY docker-env.yml /tmp
COPY . /tmp
RUN conda env update -f docker-env.yml
RUN conda install pytorch torchvision cudatoolkit=11 -c pytorch-nightly

# solution to cv2 shared lib issue
RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'gcc'\ 
    'libxext6'  -y

CMD ["/bin/bash"]