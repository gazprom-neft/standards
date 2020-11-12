# Docker container with Python 3 environment and GPU support for data science


# Checking NVIDIA driver
Visit [NVIDIA CUDA compatibility matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/index.html) and install the latest driver as shown in `utils/install_nvidia_430_18.04.sh`.

Check whether the driver is properly installed and its version:
```
nvidia-smi
```

# Installing Docker Engine
To install Docker and NVIDIA-docker2 execute `utils/install_docker.sh`.

If the installation succeeds, the list of GPUs available within a docker container will be shown.


# Running the container
Set a password for Jupyter in `run/config/jupyter_notebook_config.py`.

See [run/README.md](run/README.md) or just execute:
```
cd run
./run.sh
```

# Auto-building the image

Specify `FULL_IMAGE_NAME` in [action](.github/workflows/build-push.yml).
Set `DOCKER_HUB_TOKEN` and `DOCKER_HUB_USER` secrets to allow pushing the image to Docker Hub.
