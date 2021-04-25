# CORTARIO

Cortario is a project combinging a Software Retina with a PPO Reinforcement Learning agent playing Super Mario Bros.

## Installation

This project utilises Anaconda environments. To install the required packages run the command:

```
conda env create -f cortario-env.yml
```

This will create a conda environment `cortario`.

Additionally Python 3.5 is required.

## Usage

This project can be run in different configurations.

First activate the conda environment:

```
conda activate cortario
```

To run the baseline agent:

```
python PPO/train.py --no-retina --saved_path my_saved_path --num_processes 8
```

To run with the default retina:

```
python PPO/train.py --retina --saved_path my_saved_path --num_processes 8
```

To run with a different retina:

```
python PPO/train.py --retina --retina_name retina_folder_name --saved_path my_saved_path --num_processes 8
```

In the above command, `retina_folder_name` is a folder that contains pickled retina and cortices files.

To run with the default retina fixated at a different location:

```
python PPO/train.py --retina --saved_path my_saved_path --num_processes 8 --fix_x 1.2 --fix_y 1.4
```

`fix_x` and `fix_y` are scalar values. (1.0,1.0) is the centre of the environment, and (2.0, 2.0) is the top right corner of the environment.

To run with the foveated images:

```
python PPO/train.py --foveation --saved_path my_saved_path --num_processes 8
```

## Openshift Cluster

The project can be run using Docker on the SoCS Kubernetes cluster. The user must copy all required files on to the cluster before running the project (using scp or alternatives). The below assumes the source is copied to a folder called `Cortario`. An example job configuration is below:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: cortario-experiment
  namespace: 2162979kproject # YOUR_PROJECT_HERE
spec:
  backoffLimit: 0
  template:
    metadata:
      name: cortario-experiment
    spec:
      containers:
      - name: cortario-experiment-container
        # uncomment below if fresh pull of the image needed
        # imagePullPolicy: Always 
        image: haradra/cortario:latest
        # cd into the folder and run the PPO training
        # /nfs/ is equivalent of 2252756jvol1claim/
        command: ["/bin/bash","-c","cd /nfs/Cortario && python PPO/train.py --saved_path cortario_experiment --retina --num_processes 8"]
        resources:
          # start container only if requests are met
          requests:
            # 1 physical CPU core = 1000m
            cpu: "1000m" 
            memory: "2Gi"
            nvidia.com/gpu: 1 
          # kill container if goes beyond the limits
          limits:
            cpu: "4000m" 
            memory: "8Gi"
            nvidia.com/gpu: 1 
        # mount the external volume 'nfs-access' at the location /nfs inside this container
        volumeMounts:
        - mountPath: /nfs
          name: nfs-access
      volumes:
      - name: nfs-access
        persistentVolumeClaim: 
          claimName: 2162979kvol1claim
      # request specific GPU ("gpu2080ti" or "gputitan")
      nodeSelector:
        node-role.ida/gpu2080ti: "true"
      restartPolicy: Never
```

