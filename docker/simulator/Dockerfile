FROM osrf/ros2:bouncy-ros-base

ENV DEBIAN_FRONTEND noninteractive

# install package managers
RUN apt-get update && apt-get install -y \
      python3-pip \
      tshark \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip3 install \
      argparse \
      docker \
      pathlib
