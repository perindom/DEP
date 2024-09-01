docker build -t dep .
docker run --rm -it \
    -p 8888:8888 \
    --user=root \
    --env="DISPLAY" \
    --workdir=/main \
    --volume="$PWD":/main \
    dep /bin/bash
