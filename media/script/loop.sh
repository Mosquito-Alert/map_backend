# Script per solicitar al backend tots els vector tiles existents per a un nivell de zoom determinat.
# zooms de cada nivel gadmX
# gadm1, zoom 1 i 2
# gadm2, zoom 3 i 4
# gadm3, zoom 5 i 6
# gadm4, zoom 7, 8 i 9

# Aquests són el número de iteracions corresponen a cada nivell de zoom
# zoom = 1, Numero iteracions 2
# zoom = 2, Numero iteracions 4
# zoom = 3, Numero iteracions 8
# zoom = 4, Numero iteracions 32
# zoom = 5, Numero iteracions 32
# zoom = 7, Numero iteracions 128

nIteracions = 31
zoom=5
gadmX=gadm3

for x in {0..$nIteracions}
do
    for y in {0..$nIteracions}
    do
    filename=/home/toni/git/mosquito2_backend/media/cache/$gadmX/$zoom/$x/$y.pbf
    if [ ! -f "$filename" ]; then
        mkdir E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom
        mkdir E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom/$x
    	wget "localhost:8000/api/tiles/$gadmX/$zoom/$x/$y" -O E:/toni/sigte/projectes/mosquito2_backend/media/cache/$gadmX/$zoom/$x/$y.pbf
    fi
    done
done
