# Software i estratègia de dades

## Anàlisi d'alternatives

L'objectiu d'aquesta anàlisi és decidir quin framework de mapes farem servir (Leaflet o OpenLayers) i quina estratègia de càrrega de dades farem servir.

### Objecte de l'anàlisi

Les proves les hem fet sobre els components del mapa, pensant especialment en les capes que necessitarem inicialment al mapa públic per a l'apartat d'observacions. Aquestes capes es poden dividir en:

1. **Capes de punts**: observacions (de presència de mosquit, llocs de cria, ...).

    > Hem fet proves carregant aproximadament uns 20.000 punts. Al mapa públic oficial de MA ara hi tenen un total de 15.000 punts.

1. **Capes de polígons**: només hi ha una capa d'aquest estil: l'esforç de mostreig (antiga distribució de participants).

    > Hem fet proves carregant el mateix conjunt de dades (uns 20.000 punt) i mostrant-los com a cercles (polígons).

A l'apartat (pestanya) de models, la previsió és que les capes siguin totes (o gairebé totes) del segon tipus i farem servir la mateixa estratègia.

### Mètriques de les proves

Per la part del mapa hem fet proves amb diferent software i estratègies. A l'hora de fer les proves hem prioritzat:

- **La velocitat**. Hem mesurat el temps que es triga a veure i poder interactuar amb les dades del mapa.

- **La "integrabilitat"**, és a dir, com de fàcil és integrar aquell software amb la resta de software de l'stack, especialment amb Vue3.

- **La legibilitat**, és a dir, com de fàcil és de mantenir el codi necessari per fer servir aquell software o estratègia.

- **La flexibilitat**, és a dir, com de fàcil és definir les funcionalitats que hem de fer servir (clustering, click al marcador, efecte hover,...).

### Subjecte de l'Anàlisi

#### Frameworks de mapes

Hem fet proves amb els dos frameworks amb els que hem treballat més habitualment: Leaflet i OpenLayers.

#### Estratègies de càrrega i descàrrega

Per cada un dels frameworks anteriors, hem fet proves amb diferents mètodes de descàrrega i representació de les dades.

**Mètodes de descàrrega**

1. Descàrrega de tot el conjunt de dades de cop.

    Hem fet proves descarregant totes les dades de cop. Això té coses bones i dolentes. Per una banda, el fitxer inicial a descarregar és més gran i per tant inicialment requereix més temps.

    Per una altra banda, si l'usuari s'acaba descarregant totes les dades, en conjunt serà més ràpid perquè amb una sola crida ja ho tens tot, mentre que fent múltiples crides t'acabes baixant el mateix volum de dades i, a més a més, acumules les latències de cada crida.

    Un altre avantatge de la descàrrega sencera és que no cal tornar a fer cap més crida al servidor durant tota la sessió.

1. Segmentació de la descàrrega en base al territori (tiles).

    Les avantatges i inconvenients són les mateixes que al punt anterior però a la inversa. Quan el volum de dades és molt i molt gran, aquesta estratègia sovint és millor.

    En la descàrrega per tiles, però, a cada zoom i pan cal fer noves crides. Això genera un efecte de pampallugues que no és desitjable i, tot i que, la descàrrega inicial pot ser més ràpida, la fluïdesa de l'aplicació després de la primera càrrega no necessàriament ho és.

1. Segmentació de la descàrrega en base al temps.

    Aquesta és una variant de la primera opció. Consistiria en descarregar totes les dades de tot el món, però només per una finestra de temps determinada. Aquesta finestra de temps podria ser configurable, de manera que es podria configurar per a que mostrés totes les dades de tots els temps, o bé només les dades de l'últim any.

    Aquesta estratègia pot ser bona si, inicialment, al mapa només hi carreguem les dades de l'últim any (per exemple). Només en cas que l'usuari vulgui consultar dades més antigues caldria fer una nova crida al servidor per obtenir tot l'històric.

    Aquesta opció també permet segmentar les dades. La diferència principal amb l'anterior, és que en el cas anterior el criteri de segmentació (la vista) canvia molt i molt ràpidament (a cada pan i cada zoom). En aquest cas, en canvi, és previsible que la majoria de les consultes es limitin al conjunt de dades descarregat inicialment. Només quan un usuari vulgui veure dades de l'any anterior caldria tornar a fer una crida al servidor.

**Mètodes de càrrega (renderització al mapa)**

Hem estudiat:

1. Càrrega tradicional en format vector (amb una capa de tipus GeoJSON).

1. Càrrega de vector tiles emprant geojson-vt o descarregant les dades directament en fitxers protobuf.

### Anàlisi de les capes de punts (observacions)

#### Velocitat

De les proves que hem fet, tant amb OpenLayers com amb Leaflet, la solució més ràpida ha resultat la que descarrega totes les dades de cop i les mostra en el format tradicional vectorial (capa GeoJSON).

> Aquesta versió podria limitar-se, com s'explica més amunt, a les dades només d'aquest any i encara seria més ràpid, però ja ho és molt (com veureu més avall).

Això ha estat així gràcies a l'ús d'un complement de JavaScript pensat per fer clustering de punts geolocalitzats: [Supercluster](https://github.com/mapbox/supercluster).

Aquest complement és independent de qualsevol framework i es pot fer servir tant amb Leaflet com amb OpenLayers (ho hem provat). El comportament és similar en tots dos casos.

> A diferència d'altres llibreries de clustering (com MarkerCluster de Leaflet o el propi clustering d'OpenLayers), el supercluster no carrega tots els punts al mapa, sinó que els manté en memòria en un web worker. En fer zoom i pan es fa una petició al web worker per a que torni només els punts (ja clusteritzats) de la vista actual.

La resta d'opcions presenten comportaments més o menys correctes, però cap és comparable a aquesta opció.

Amb l'analítica del complement Lighthouse de Chrome, cada una de les diferents proves mostra els següents temps i comportament:

|                                                             | Performance | primeres dades | càrrega completa | Temps bloquejat |
|-------------------------------------------------------------|-------------|----------------|------------------|-----------------|
| Opció 1. MVT en servidor i client                           | 53%         | 1.7s           | 3.2s             | 1s              |
| Opció 2. GeoJSON sencer en servidor, MVT en client          | 46%         | 0.7s           | 3.9s             | 2.5s            |
| Opció 3. GeoJSON tiles en servidor, Geojson tiles en client | 42%         | 1.7s           | 9.8s             | 5s              |
| Opció 4. GeoJSON sencer en servidor, Geojson en client      | 100%        | 0.5s           | 0.5s             | 0s              |

Al directori [proves](proves) hi podeu veure l'exemple de càrrega de cada un d'aquestes proves.

També podeu veure aquestes proves desplegant la branca `leaflet` del repositori https://bitbucket.org/sigte/mosquito_proves/.

#### Facilitat d'integració

Aquí el punt més conflictiu era poder integrar l'alternativa triada (Leaflet, OpenLayers, MarkerCluster/Supercluster,...) amb el framework web principal que pensem fer amb Vue3.

Hi ha complements de Vue3 tant per Leaflet (https://github.com/vue-leaflet/vue-leaflet) com per OpenLayers (https://github.com/MelihAltintas/vue3-openlayers).

Hem fet una prova d'integració de Leaflet amb Supercluster i Vue3 sense problemes inicials. Amb OpenLayers no hem fet cap prova però la documentació sembla molt completa i fiable, de manera que no hi preveiem més dificultats que les que implica treballar amb un framework nou.

#### Legibilitat del codi

Per a les tasques més bàsiques i habituals, Leaflet genera un codi més simple i més fàcil de llegir i, per tant, de mantenir. OpenLayers, en canvi, té més flexibilitat però això va en detriment d'un codi més extens i, a vegades, més difícil de llegir i, per tant, de mantenir.

En tasques molt poc habituals, en canvi, OpenLayers pot requerir un codi més senzill.

Pel que fa a les estratègies de càrrega, la que empra Supercluster (la més ràpida) genera un codi molt net i fàcilment modulable.

#### Flexibilitat del framework

Leaflet és un framework de mínims, a l'estil Flask de Python, perquè busca ser una opció de poc pes i per a "tots els públics". Per això, el framework en sí porta menys funcionalitats que OpenLayers i cada cosa addicional que volem fer, sovint, cal fer-la amb un plugin addicional (ex: Draw, Clusters,...).

Algunes d'aquestes funcionalitats són molt habituals i estan ben testejades i, en general, ben resoltes amb complements que, en ocasions, han estat desenvolupats pels mateixos que han fet Leaflet. Si hi ha alguna funcionalitat que no és habitual el més probable és que porti més feina fer-la amb Leaflet que amb OpenLayers, però tampoc hi ha garantia que sigui així.

OpenLayers, en canvi, és un framework a l'estil Django: amb piles incloses. La seva filosofia és oferir un producte que ja ho pugui fer tot (o gairebé) sense necessitat d'instal·lar coses addicionals. Per tant, el core de OpenLayers és més potent que el de Leaflet i més flexible sense necessitat de desenvolupar molt codi propi. Per exemple, les funcionalitats de Draw i Cluster es poden afegir al mapa sense haver de carregar nous plugins o components addicionals.

### Anàlisi de les capes de polígons (esforç de mostreig)

En el cas dels polígons, el complement Supercluster no aplica i per tant, la solució més eficient serà la que empra Mapbox Vector Tiles (opcions 1 o 2).

Caldrà acabar de definir alguns detalls en aquest cas (descarreguem totes les dades? o descarreguem per tiles?), però que no afecten al framework de mapes triat ni a l'estratègia principal, perquè ja estem més limitats.

## Conclusions

### Estratègia de càrrega

Farem servir dues estratègies diferents per les capes de punts i les de polígons.

#### Capes de punts

Carregarem els punts en un mapa d'OpenLayers utilitzant Supercluster i Vue.

Hem d'acabar d'acordar si és millor descarregar totes les dades de cop (això, a priori no sembla un problema important) o si les segmentarem per data, però a nivell de comportament, aquest enfoc és molt millor que qualsevol dels altres que hem provat.

Això ens donarà una velocitat força més elevada, tant de la càrrega inicial com de la navegació pel mapa. A més, com que no cal fer noves crides al servidor l'efecte "pampallugues" serà gairebé imperceptible.

A més a més, la implementació és molt simple i el codi (aquesta part del codi) hauria de ser de més fàcil desenvolupament i manteniment. I com que les dades es carreguen com a objectes del DOM, la interactivitat és molt elevada.

#### Capes de polígons

Carregarem els punts en un mapa d'OpenLayers utilitzant geojson-vt per tilejar les dades en client i renderitzar-les més ràpidament.

La descàrrega pot anar lligada a com fem la descàrrega de les observacions. Si d'aquestes en descarreguem només el darrer any pot tenir sentit que a l'esforç de mostreig també es descarregui només les dades del darrer any.

Si no, l'esforç de mostreig segurament també el descarregarem sencer.

### Software

- **Framework web**: Vue3
- **Framework de mapes**: OpenLayers
- **Clustering**: Supercluster
- **Tilejat en client**: geojson-vt
- **Altres**: Peces de software que pensem fer servir però que no són rellevants per al comportament més important del mapa (l'ús de capes i la navegació del mapa):
    - **eCharts**: Aquest complement el van proposar des de Mosquito i hi ha un complement per Vue3. Caldrà acabar de fer proves amb això en el seu moment per acabar de decidir si fem servir aquest software o un altre. https://www.npmjs.com/package/vue3-echarts
