## VSCode configuration

### Dockerfile

 The fact that the coder user only exists inside the Docker container presents a unique situation. You essentially want to grant permissions from the Docker host to a user inside a container.

 Here are the steps you can follow:

1. **On the Docker Host**:

Find out the group ID (**gid**) of the **/dev/i2c-1** device on the host.

```
ls -ln /dev/i2c-1
```

This will give you an output like:

```
crw-rw---- 1 0 123 89, 1 Aug 17 18:27 /dev/i2c-1
```

The number **123** in the example above is the group ID of the device.

2. **In the Dockerfile**:

As the coder user is already a part of the image (like it seems to be in the codercom/code-server image), then you can create a new group inside the Docker container with the gid you found in the previous step and add the coder user to that group.

Add these commands to the Dockerfile:


```
# Replace 955 with the gid you found
RUN groupadd -g 995 i2cgroup
RUN usermod -aG i2cgroup code

```
