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
# zoom = 4, Numero iteracions 16
# zoom = 5, Numero iteracions 32
# zoom = 7, Numero iteracions 128


path='/home/toni/git/mosquito2_backend'
zoom=5
gadmX=gadm3
nIteracions=31


for x in $(seq 0 $nIteracions)
do
    for y in $(seq 0 $nIteracions)
    do
    filename=$path/media/tiles/$gadmX/$zoom/$x/$y.pbf
    echo $filename
    if [ ! -f "$filename" ]; then
        mkdir $path/media/tiles/$gadmX/$zoom
        mkdir $path/media/tiles/$gadmX/$zoom/$x
        echo localhost:8000/api/tiles/$gadmX/$zoom/$x/$y.pbf
        wget localhost:8000/api/tiles/$gadmX/$zoom/$x/$y.pbf -O $path/media/tiles/$gadmX/$zoom/$x/$y.pbf
    fi
    done
done
