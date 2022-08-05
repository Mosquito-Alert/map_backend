for x in {0..3}
do
    for y in {0..3}
    do
    wget "localhost:8000/api/tiles/gadm1/2/$x/$y" -O /dev/null
    done
done
