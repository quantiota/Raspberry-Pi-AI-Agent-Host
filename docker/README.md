# Docker

You will find all the Docker services set up in this folder.

## Services

### VSCode

:link: [docker image](https://hub.docker.com/r/codercom/code-server)
:link: [github repository](https://github.com/coder/code-server)

Access VSCode through [localhost:8080](http://localhost:8080).

:lock:
The password to access VSCode is `yourpassword` it can be set it in the [docker-compose.yaml file](docker-compose.yaml).

:wrench: To configure VSCode, follow [this documentation](./vscode/README.md).

### QuestDB

:link: [docker image](https://hub.docker.com/r/questdb/questdb)
:link: [github repository](https://github.com/questdb/questdb)
:link: [questdb Docker documentation](https://questdb.io/docs/get-started/docker/)

Access QuestDB GUI through [localhost:9000](http://localhost:9000).
Access the database using [localhost:8812](http://localhost:8812).

:lock:
The user/password are the default one: `admin:quest` ([see the documentation](https://questdb.io/docs/reference/configuration/#postgres-wire-protocol)) and the database name is `qdb`.

### Grafana

:link: [docker image](https://hub.docker.com/r/grafana/grafana)
:link: [github repository](https://github.com/grafana/grafana)

Access Grafana through [localhost:3000](http://localhost:3000).

:lock:
The user/password are the default one: `admin:admin`.
You can add set the password adding the environment variable `GF_SECURITY_ADMIN_PASSWORD`.

:wrench: To configure Grafana, follow [this documentation](./grafana/README.md).



## Understanding and Managing Docker Permissions in a Docker Stack

### 1 Docker Volumes Permissions 

The Docker Compose configuration mounts the local directory **../notebooks** to **/home/coder/project** inside the **vscode** service using Docker volumes. This is specified in the **volumes** section of the **vscode** service:

``````
volumes:
  # volume used to access the `notebooks` folder
  - ../notebooks:/home/coder/project
``````

However, this configuration doesn't specify any permission settings for the **../notebooks** directory. Therefore, the permissions inside the container for the mounted directory will be the same as the permissions on the host for **../notebooks.**

In other words, the permissions are determined by the file system of the host machine where the Docker Compose file is run, not by the Docker Compose configuration itself. You can check these permissions using the **ls -l** command in your host system's terminal.

If you want to change the permissions, you would have to do this at the operating system level, outside of Docker. For example, in a Unix-like system, you might use the **chmod** command to change the permissions of the **../notebooks** directory.

Please note that if the **coder** user in your Docker container needs specific permissions (e.g., to write to the **/home/coder/project** directory), you will need to ensure that the host-level permissions for **../notebooks** allow for this. Otherwise, you may run into permission errors.

If you wish to enforce specific permissions within the container regardless of host permissions, you would likely need to handle this in the Dockerfile used to build your image, for example by adding **RUN chmod** commands to change the permissions after the volume is mounted. But keep in mind that it might not always work depending on the volume's nature, and the Dockerfile does not have direct access to the volumes at build time.

Another option would be to use an entrypoint script in your Dockerfile that modifies the permissions of the directory when the container starts, but again, be cautious about potential security implications of changing permissions in this way.


### 2 Setting Default File and Directory Permissions for Git Clone Operations

The permissions for files and directories created by **git clone** are determined by your system's settings, not by Git itself. The most important of these settings is the **umask**, a value that determines the default permissions for newly created files and directories.

When you run **git clone**, Git creates a new directory for the repository, and the permissions for this directory are determined by subtracting the umask from **777** (for directories) or **666** (for files). The resulting permissions apply to the cloned directory and all files within.

If you want to change the default permissions for **git clone**, you can temporarily change the umask before running the command. For example, if you want the cloned directory to have permissions of **755** (rwxr-xr-x), you could set the umask to **022** like so:

```
umask 022
git clone https://github.com/quantiota/Raspberry-Pi-AI-Agent-Host.git
```

This will only affect the current shell session. If you want to change the umask permanently, you can add the **umask 022** command to your shell's initialization file (like **~/.bashrc** or **~/.bash_profile** for the Bash shell).

Keep in mind that this will affect all file and directory creation operations in your system, not just **git clone**, so be careful when changing the umask.

Remember that you can always change the permissions of a directory or file after it's created using the **chmod** command. For example:

```
chmod 755 /path/to/directory
```

This command will change the permissions of the specified directory to **755**, regardless of the umask or the directory's initial permissions.