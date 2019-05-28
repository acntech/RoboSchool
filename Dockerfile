# In the repo root, run
# docker build -f Dockerfile -t docker_image_name .
# to build this image

# After successful build, it can be started with
# docker run --rm --detach docker_image_name

# You can also check the image by
# docker run --rm -it --entrypoint /bin/bash docker_image_name
# to enter the container and observe

FROM python:3-onbuild

CMD ["python", "-m", "project_code"]
