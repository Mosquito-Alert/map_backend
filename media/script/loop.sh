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
zoom=5
gadmX=gadm3
for x in {0..31}
do
    for y in {0..31}
    do
    filename=/home/toni/git/mosquito2_backend/media/cache/$gadmX/$zoom/$x/$y.pbf
    if [ ! -f "$filename" ]; then
        mkdir E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom
        mkdir E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom/$x
    	wget "localhost:8000/api/tiles/$gadmX/$zoom/$x/$y" -O E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom/$x/$y.pbf
    fi
    done
done
