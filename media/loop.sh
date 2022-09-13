# for x in {0..7}
# do
#     for y in {0..7}
#     do
#     filename=/home/toni/git/mosquito2_backend/media/cache/gadm1/3/$x/$y.pbf
#     if [ ! -f "$filename" ]; then
#         mkdir /home/toni/git/mosquito2_backend/media/cache/gadm1/3/$x
#     	wget "localhost:8000/api/tiles/gadm1/3/$x/$y" -O /home/toni/git/mosquito2_backend/media/cache/gadm1/3/$x/$y.pbf
#     fi
#     done
# done

for x in {0..63}
do
    for y in {0..63}
    do
    filename=/home/toni/git/mosquito2_backend/media/cache/gadm2/6/$x/$y.pbf
    if [ ! -f "$filename" ]; then
        mkdir /home/toni/git/mosquito2_backend/media/cache/gadm2/6/$x
    	wget "localhost:8000/api/tiles/gadm2/6/$x/$y" -O /home/toni/git/mosquito2_backend/media/cache/gadm2/6/$x/$y.pbf
    fi
    done
done
