# Fooocus on Docker

The Docker image is based on NVIDIA CUDA 12.4 and PyTorch 2.1. For more details, refer to the [Dockerfile](Dockerfile) and [requirements_docker.txt](requirements_docker.txt).

## Requirements

- A computer with specifications sufficient to run Fooocus, along with proprietary Nvidia drivers.
- Docker, Docker Compose, or Podman.

## Quick Start

**For additional information, refer to the [notes](#notes).**

### Running with Docker Compose

1. Clone this repository.
2. Run the Docker container with `docker compose up`.

### Running with Docker

```sh
docker run -p 7865:7865 -v fooocus-data:/content/data -it \
--gpus all \
-e CMDARGS=--listen \
-e DATADIR=/content/data \
-e config_path=/content/data/config.txt \
-e config_example_path=/content/data/config_modification_tutorial.txt \
-e path_checkpoints=/content/data/models/checkpoints/ \
-e path_loras=/content/data/models/loras/ \
-e path_embeddings=/content/data/models/embeddings/ \
-e path_vae_approx=/content/data/models/vae_approx/ \
-e path_upscale_models=/content/data/models/upscale_models/ \
-e path_inpaint=/content/data/models/inpaint/ \
-e path_controlnet=/content/data/models/controlnet/ \
-e path_clip_vision=/content/data/models/clip_vision/ \
-e path_fooocus_expansion=/content/data/models/prompt_expansion/fooocus_expansion/ \
-e path_outputs=/content/app/outputs/ \
ghcr.io/lllyasviel/fooocus
```

### Running with Podman

```sh
podman run -p 7865:7865 -v fooocus-data:/content/data -it \
--security-opt=no-new-privileges --cap-drop=ALL --security-opt label=type:nvidia_container_t --device=nvidia.com/gpu=all \
-e CMDARGS=--listen \
-e DATADIR=/content/data \
-e config_path=/content/data/config.txt \
-e config_example_path=/content/data/config_modification_tutorial.txt \
-e path_checkpoints=/content/data/models/checkpoints/ \
-e path_loras=/content/data/models/loras/ \
-e path_embeddings=/content/data/models/embeddings/ \
-e path_vae_approx=/content/data/models/vae_approx/ \
-e path_upscale_models=/content/data/models/upscale_models/ \
-e path_inpaint=/content/data/models/inpaint/ \
-e path_controlnet=/content/data/models/controlnet/ \
-e path_clip_vision=/content/data/models/clip_vision/ \
-e path_fooocus_expansion=/content/data/models/prompt_expansion/fooocus_expansion/ \
-e path_outputs=/content/app/outputs/ \
ghcr.io/lllyasviel/fooocus
```

Once the message `Use the app with http://0.0.0.0:7865/` appears in the console, you can access the app via the browser.

Your models and outputs are stored in the `fooocus-data` volume, which, depending on your OS, is located at `/var/lib/docker/volumes/` (or `~/.local/share/containers/storage/volumes/` when using `podman`).

## Building the Container Locally

1. Clone the repository.
2. Open a terminal in the folder where you cloned the repository.
3. Build with `docker`:

```sh
docker build . -t fooocus
```

4. Build with `podman`:

```sh
podman build . -t fooocus
```

## Details

### Updating the Container Manually (`docker compose`)

When using `docker compose up` continuously, the container does not automatically update to the latest Fooocus version. Run `git pull` to fetch the latest updates before executing:

```sh
docker compose build --no-cache
```

Then, start the container with:

```sh
docker compose up
```

### Importing Models and Outputs

To import files from the models or outputs folder, add the following bind mounts to your [docker-compose.yml](docker-compose.yml) or your preferred method of running the container:

```yaml
#- ./models:/import/models   # Once you import files, you don't need to mount again.
#- ./outputs:/import/outputs  # Once you import files, you don't need to mount again.
```

After running the container, your files will be copied to `/content/data/models` and `/content/data/outputs`. Since `/content/data` is a persistent volume, your files will persist even when the container is restarted without these mounts.

### Paths Inside the Container

| Path                                | Details                                                                 |
|-------------------------------------|-------------------------------------------------------------------------|
| `/content/app`                      | The folder where the application is stored.                             |
| `/content/app/models.org`           | Original 'models' folder. Files are copied to `/content/app/models`, which is symlinked to `/content/data/models` every time the container boots. (Existing files will not be overwritten.) |
| `/content/data`                     | Persistent volume mount point.                                          |
| `/content/data/models`              | The folder symlinked to `/content/app/models`.                          |
| `/content/data/outputs`             | The folder symlinked to `/content/app/outputs`.                         |

### Environment Variables

You can change parameters in `config.txt` by using environment variables. **Environment variables take precedence over the values defined in `config.txt`, and changes will be saved to `config_modification_tutorial.txt`.**

Here are the Docker-specific environment variables used by the `entrypoint.sh` script:

| Environment Variable               | Details                                             |
|-------------------------------------|-----------------------------------------------------|
| `DATADIR`                          | Location of `/content/data`.                        |
| `CMDARGS`                          | Arguments for [entry_with_update.py](entry_with_update.py) called by [entrypoint.sh](entrypoint.sh). |
| `config_path`                      | Location of `config.txt`.                           |
| `config_example_path`              | Location of `config_modification_tutorial.txt`.     |
| `HF_MIRROR`                        | Hugging Face mirror site domain.                    |

You can also use the same JSON key names and values from `config_modification_tutorial.txt` as environment variables. See examples in the [docker-compose.yml](docker-compose.yml).

## Notes

- Keep `path_outputs` under `/content/app` to avoid errors when opening the history log.
- Docker on Mac/Windows may experience slow volume access when using "bind mount" volumes. Refer to [this article](https://docs.docker.com/storage/volumes/#use-a-volume-with-docker-compose) to avoid using "bind mount."
- The MPS backend (Metal Performance Shaders, for Apple Silicon M1/M2) is not yet supported in Docker. See [this issue](https://github.com/pytorch/pytorch/issues/81224).
- To start the container in detached mode, use `docker compose up -d`. To view logs, run `docker compose logs -f`. You can then close the terminal, and the container will continue running.
