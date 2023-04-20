from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.utils import translation
from api.decorators import deny_empty_origin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

# from django.shortcuts import render
# from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework import status


a = ("Open", "Layers")

def translations(request, lang):
    if not request.session or not request.session.session_key:
        request.session.save()

    authorized = request.user.is_authenticated

    translation.activate(lang)

    response = JsonResponse({
        # User
        "registered-user": authorized,
        # General
        "Shown points": _("Shown points"),
        "Open": _("Open"),
        "Close": _("Close"),
        "Select": _("Select"),
        "Mosquitos": _("Mosquitos"),
        "Bites": _("Bites"),
        "Breeding sites": _("Breeding sites"),
        "Sampling effort": _("Sampling effort"),
        "Placeholder location": _("Placeholder location"),
        "Placeholder hashtag": _("Placeholder hashtag"),
        'Reports': _("Reports"),        
        'Estimates': _("Estimates"),        
        "Filter": _("Filter"),
        "Continue": _("Continue"),

        # observation categories
        "Mosquito_tiger_probable": _("Mosquito tiger probable"),
        "Breeding_site_not_yet_filtered": _("Breeding site not yet filtered"),
        "Conflict": _("Conflict"),
        "Mosquito_tiger_confirmed": _("Mosquito tiger confirmed"),
        "Unidentified": _("Unidentified"),
        "Yellow_fever_confirmed": _("Yellow fever confirmed"),
        "Storm_drain_water": _("Storm drain water"),
        "Breeding_site_other": _("Breeding site other"),
        "Other_species": _("Other species"),
        "Storm_drain_dry": _("Storm drain dry"),
        "Not_yet_validated": _("Not yet validated"),
        "Yellow_fever_probable": _("Yellow fever probable"),
        "Trash_layer": _("Trash layer"),

        # Mosquito types
        "Tiger mosquito": _("Tiger mosquito"),
        "Tiger mosquito confirmed": _("Tiger mosquito confirmed"),
        "Tiger mosquito possible": _("Tiger mosquito possible"),
        "Tiger": _("Tiger mosquito"),

        "Yellow fever mosquito": _("Yellow fever mosquito"),
        "Yellow fever mosquito confirmed": _("Yellow fever mosquito confirmed"),
        "Yellow fever mosquito possible": _("Yellow fever mosquito possible"),
        "Yellow": _("Yellow fever mosquito"),

        "Japonicus mosquito": _("Japonicus mosquito"),
        "Japonicus mosquito confirmed": _("Japonicus mosquito confirmed"),
        "Japonicus mosquito possible": _("Japonicus mosquito possible"),
        "Japonicus": _("Japonicus mosquito"),

        "Mosquito japonicus/koreicus": _("Mosquito japonicus/koreicus"),
        "Mosquito albopictus/cretinus": _("Mosquito albopictus/cretinus"),
        "Koreicus mosquito": _("Koreicus mosquito"),
        "Koreicus mosquito confirmed": _("Koreicus mosquito confirmed"),
        "Koreicus mosquito possible": _("Koreicus mosquito possible"),
        "Koreicus": _("Koreicus mosquito"),

        "Culex mosquito": _("Culex mosquito"),
        "Culex mosquito confirmed": _("Culex mosquito confirmed"),
        "Culex mosquito possible": _("Culex mosquito possible"),
        "Culex": _("Culex mosquito"),

        "Unidentified mosquito": _("Unidentified mosquito"),
        "Unidentified": _("Unidentified mosquito"),
        "Others_mosquito": _("Others_mosquito"),

        # breeding sites
        "Stormdrain with water": _("Storm drain with water"),
        "Stormdrain without water": _("Storm drain without water"),
        "Storm_drain_dry": _("Storm_drain_dry"),
        "Breeding site other": _("Breeding site other"),
        
        # other observations
        "Other species": _("Other species"),
        
        # Left drawer, Toolbar
        "Layers": _("Layers"),
        "Models": _("Models"),
        "Lang": _("Lang"),
        "Share": _("Share"),
        "Help": _("Help"),
        "Log in": _("Log in"),
        "Log out": _("Log out"),
        
        # Timeseries
        "Time series": _("Time series"),
        "Pick a date range": _("Pick a date range"),
        "Delete calendar": _("Delete calendar"),
        "Select all": _("Select all"),
        "Apply calendar": _("Apply calendar"),
        "All years and all months": _("All years and all months"),
        "Reset zoom graph": _("Reset zoom graph"),
        "reloading graph": _("reloading graph"),
        "Loading...": _("Loading..."),

        # Map, Popup
        'Anonymous': _("Anonymous"),
        'How many bites': _("How many bites"),
        'Body part': _("Body part"),
        'Bite location': _("Bite location"),   
        'Bite time': _("Bite time"),   

        "Date": _("Date"),
        "Expert note": _("Expert note"),
        "Citizen note": _("Citizen note"),
        "Confirmed": _("Confirmed"),
        "Probable": _("Probable"),
        "Expert validation": _("Expert validation"),
        "AI validation": _("AI validation"),

        'Unknown': _("_Unknown"),
        'Outdoors': _("Outdoors"),
        'Inside building': _("Inside building"),
        'inside vehicle': _("Inside vehicle"),
        'At sunrise': _("At sunrise"),
        'At noon': _("At noon"),
        'At sunset': _("At sunset"),
        'At night': _("At night"),
        'Not really sure': _("Not really sure"),
    
        'Head':  _("Head"),
        'Left arm': _("Left arm"),
        'Right arm': _("Right arm"),
        'Chest': _("Chest"),
        'Left leg': _("Left leg"),
        'Right leg': _("Right leg"),
    
        'Breeding site with water': _("Breeding site with water"),
        'Breeding site without water': _("Breeding site without water"),
        'Breeding site with larva': _("Breeding site with larva"),
        'No': _("No"),
        'Yes': _("Yes"),

        'Not available':_("Not available"),
        'No results found': _("No results found"),

        # Download
        'Download': _("Download"),
        'Download geopackage': _("Download geopackage"),
        'Download excel': _("Download excel"),
        'No features to download': _("No features to download"),
        'Only data displayed in the current map view will be downloaded. Verify your current active layers, temporal filters and zoom.': _("Only data displayed in the current map view will be downloaded. Verify your current active layers, temporal filters and zoom."),
        'Once verified, press the download button.': _("Once verified, press the download button."),
        'For the Mosquito Alert complete dataset, with advanced options, go to Mosquito Alert portal:': _("For the Mosquito Alert complete dataset, with advanced options, go to Mosquito Alert portal:"),   
        'Mosquito portal URL': _("Mosquito portal URL"),   
    
        # Share view
        'This is the new view url': _("This is the new view url"),
        'This view does not exist': _("This view does not exist"),
        'Share modal title': _("Share modal title"),
        'Share this map view': _("Share this map view"),
        'Url has been copied': _("Url has been copied"),
        'Copy url to clipboard': _("Copy url to clipboard"),
        'Share view': _("Share view"),

        # Reports / modal
        'Observation code': _("Observation code"),
        'Coordinates (latitud, longitud)': _("Coordinates (latitud, longitud)"),
        'List of observations': _("List of observations"),
        'Reports limit exceeded': _("Reports limit exceeded"),
        'List of observations':_("List of observations"),       
        'Selected observations': _("Selected observations"),
        'Filters applied': _("Filters applied"),
        'Reports modal title': _("Reports modal title"),
        'Report with the observations displayed in the current map view (maximum: 300 observations)': _("Report with the observations displayed in the current map view (maximum: 300 observations)"),
        'Verify this by looking at the map point counter': _("Verify this by looking at the map point counter (on the down left map corner)."),

        # Info modal

        'Check the': _("Check the"),
        'data on mosquitoes, breeding places and bites': _("data on mosquitoes, breeding places and bites"),
        'sent by citizens, through the Mosquito Alert app.': _(" sent by citizens, through the Mosquito Alert app."),
        'Part of this data has been validated by entomology professionals or by Artificial Intelligence (AI) algorithms. You will also find data modeled from the original data.': _("Part of this data has been validated by entomology professionals or by Artificial Intelligence (AI) algorithms. You will also find data modeled from the original data."),
        'You can ': _("You can "),
        'view, filter and download data': _("view, filter and download data"),
        'among other functions': _("among other functions"),
        'Use the Help': _("Use the Help"),
        'and Info': _("and Info"), 
        'for more information.': _("for more information."), 
        'If you want the complete Mosquito Alert data set, with advanced documentation and download options, go to the Mosquito Alert Data Portal:': _("If you want the complete Mosquito Alert data set, with advanced documentation and download options, go to the Mosquito Alert Data Portal:"), 
        'You can also consult the Mosquito Alert website: ': _("You can also consult the Mosquito Alert website: "), 
        'MODELED DATA': _('MODELED DATA'),
        'Model maps show the probability of encountering a specific mosquito species or of receiving a mosquito bite. Probabilities are based on data submitted by citizens to Mosquito Alert. The first estimates for a month are based on observations received for that month in previous years, estimates that are updated weekly with data for the current year to readjust the values in real time.': _("Model maps show the probability of encountering a specific mosquito species or of receiving a mosquito bite. Probabilities are based on data submitted by citizens to Mosquito Alert. The first estimates for a month are based on observations received for that month in previous years, estimates that are updated weekly with data for the current year to readjust the values in real time."),
        'Models show the probability of encountering each of the target species: the tiger mosquito, the yellow fever mosquito, the Asian bush mosquito, the Korean mosquito, and the common house mosquito. Another model shows the probability of receiving a mosquito bite, which does not correspond to any specific mosquito species, but to all the reports of bites received, reflecting the human-mosquito interaction in the area.': _("Models show the probability of encountering each of the target species: the tiger mosquito, the yellow fever mosquito, the Asian bush mosquito, the Korean mosquito, and the common house mosquito. Another model shows the probability of receiving a mosquito bite, which does not correspond to any specific mosquito species, but to all the reports of bites received, reflecting the human-mosquito interaction in the area."),
        'Estimates are displayed at different world’s administrative areas or boundaries depending on the zoom and the map view. Administrative areas in the database are countries and lower lever subdivisions such as provinces. At high resolution, estimates are displayed in grids of approximately 2x2 kilometers (grid of 0.05 degrees latitude by 0.05 degrees longitude). In addition to the probability of encountering a mosquito or receiving a bite, each administrative area also shows its uncertainty value.': _("Estimates are displayed at different world’s administrative areas or boundaries depending on the zoom and the map view. Administrative areas in the database are countries and lower lever subdivisions such as provinces. At high resolution, estimates are displayed in grids of approximately 2x2 kilometers (grid of 0.05 degrees latitude by 0.05 degrees longitude). In addition to the probability of encountering a mosquito or receiving a bite, each administrative area also shows its uncertainty value."),
        'This calculation considers the sampling effort, considering the number of participants with the active app in each grid or area in the defined time. The probability of mosquitoes or of receiving a mosquito bite is higher in a grid in which 10 observations have been received and there are 5 participants, than in another with 10 observations and 10 participants. Modeling observations and active participants determines the value of the probability shown on the map.': _("This calculation considers the sampling effort, considering the number of participants with the active app in each grid or area in the defined time. The probability of mosquitoes or of receiving a mosquito bite is higher in a grid in which 10 observations have been received and there are 5 participants, than in another with 10 observations and 10 participants. Modeling observations and active participants determines the value of the probability shown on the map."),
        'This probability has been observed to correspond to the observations of the tiger mosquito obtained by traditional surveillance methods (ovitraps), thus demonstrating that it is a good way of estimating the presence and abundance of a species.': _("This probability has been observed to correspond to the observations of the tiger mosquito obtained by traditional surveillance methods (ovitraps), thus demonstrating that it is a good way of estimating the presence and abundance of a species."),

        # Cookies comply
        'Cookies policy': _("Cookies policy"),
        'Manage cookies': _("Manage cookies"),
        'Cookies comply title': _("Cookies comply title"),
        'We use cookies and similar technologies to help personalize content and offer a better experience. You can opt to customize them by clicking the preferences button': _("We use cookies and similar technologies to help personalize content and offer a better experience. You can opt to customize them by clicking the preferences button"),
        'Tecnical cookies': _("Tecnical cookies"),
        'Tecnical cookies description': _("Tecnical cookies description"),
        'Analytics title': _("Analytics title"),
        'Analytics tooltip': _("Analytics tooltip"),
        'Analytics cookie title': _("Analytics cookie title"),
        'Analytics cookie description': _("Analytics cookie description"),
        'La web de Mosquito Alert utiliza cookies propias y de terceros con finalidades técnicas y analíticas. Para administrarlas utilice el gestor. Si desea más información acceda a la Política de cookies': _("La web de Mosquito Alert utiliza cookies propias y de terceros con finalidades técnicas y analíticas. Para administrarlas utilice el gestor. Si desea más información acceda a la Política de cookies"),
        'Save and close': _("Save and close"),
        'Accept all': _("Accept all"),
        'Is required': _("Is required"),
        'La web de Mosquito Alert utiliza': _("La web de Mosquito Alert utiliza"),
        'Escoge qué tipos de galletas aceptas que Mosquito Alert pueda guardar en tu navegador.': _("Escoge qué tipos de galletas aceptas que Mosquito Alert pueda guardar en tu navegador."),
        'Las galletas o cookies son pequeños archivos de texto que se instalan en los equipos desde los cuales se accede a nuestro sitio web. Entre otras finalidades, las cookies registran las preferencias y los hábitos de navegación de un usuario.': _("Las galletas o cookies son pequeños archivos de texto que se instalan en los equipos desde los cuales se accede a nuestro sitio web. Entre otras finalidades, las cookies registran las preferencias y los hábitos de navegación de un usuario."),
        'Se asocian al usuario y a su equipo, pero no proporcionan datos directamente identificativos. Algunas cookies, por ejemplo las que permiten elaborar estadísticas o anuncios, necesitan el consentimiento del usuario de nuestro sitio web. En cambio otras cookies, las de carácter técnico o las necesarias para ofrecer un servicio solicitado por el usuario, son imprescindibles para el funcionamiento del sitio.': _("Se asocian al usuario y a su equipo, pero no proporcionan datos directamente identificativos. Algunas cookies, por ejemplo las que permiten elaborar estadísticas o anuncios, necesitan el consentimiento del usuario de nuestro sitio web. En cambio otras cookies, las de carácter técnico o las necesarias para ofrecer un servicio solicitado por el usuario, son imprescindibles para el funcionamiento del sitio."),
        'Las cookies se pueden clasificar según su vigencia, quien las gestiona o su finalidad.': _("Las cookies se pueden clasificar según su vigencia, quien las gestiona o su finalidad."),
        'Según la vigencia': _("Según la vigencia"),
        'De sesión: son temporales y quedan en el archivo de galletas de vuestro navegador hasta el momento que abandonáis el sitio web': _("De sesión: son temporales y quedan en el archivo de galletas de vuestro navegador hasta el momento que abandonáis el sitio web"),
        'Persistentes: quedan almacenadas y el sitio web les lee cada vez que hacéis una visita': _("Persistentes: quedan almacenadas y el sitio web les lee cada vez que hacéis una visita"),
        'Según quién las gestione': _("Según quién las gestione"),
        'Propias: son las propias del titular del sitio web desde lo que se prestan los servicios al usuario': _("Propias: son las propias del titular del sitio web desde lo que se prestan los servicios al usuario"),
        'De terceros: se envían al usuario por parte de uno tercero, diferente al titular del lugar': _("De terceros: se envían al usuario por parte de uno tercero, diferente al titular del lugar"),
        'Según la finalidad': _("Según la finalidad"),
        'Necesarias: las imprescindibles para facilitar vuestra conexión. No hay opción de inhabilitarlas, dado que son las necesarias por el funcionamiento del sitio web': _("Necesarias: las imprescindibles para facilitar vuestra conexión. No hay opción de inhabilitarlas, dado que son las necesarias por el funcionamiento del sitio web"),
        'Técnicas: las que permiten controlar el tráfico y comunicación de datos, identificar la sesión y acceder a páginas de acceso restringido, entre otros': _("Técnicas: las que permiten controlar el tráfico y comunicación de datos, identificar la sesión y acceder a páginas de acceso restringido, entre otros"),
        'Analíticas: proporcionan información estadística y permiten mejorar los servicios': _("Analíticas: proporcionan información estadística y permiten mejorar los servicios"),
        'Listado de cookies utilizadas': _("Listado de cookies utilizadas"),
        'En la web de Mosquito Alert utilizamos una única cookie de tipo técnico y las cookies de Google Analytics': _("En la web de Mosquito Alert utilizamos una única cookie de tipo técnico y las cookies de Google Analytics"),
        'Las cookies de Google Analytics, permiten analizar estadísticamente la información a que acceden los usuarios de nuestro lugar. Los datos recopilados pueden incluir la actividad del navegador del usuario cuando nos visita, la ruta que siguen los usuarios en nuestro lugar, información del proveedor de servicios de Internet del visitante, el número a veces que los usuarios acceden al lugar y el comportamiento de los usuarios en nuestro lugar (páginas que ha visitado, formularios que se han completado y similares)': _("Las cookies de Google Analytics, permiten analizar estadísticamente la información a que acceden los usuarios de nuestro lugar. Los datos recopilados pueden incluir la actividad del navegador del usuario cuando nos visita, la ruta que siguen los usuarios en nuestro lugar, información del proveedor de servicios de Internet del visitante, el número a veces que los usuarios acceden al lugar y el comportamiento de los usuarios en nuestro lugar (páginas que ha visitado, formularios que se han completado y similares)"),
        'Puedes obtener más información sobre Google Analytics a': _("Puedes obtener más información sobre Google Analytics a"),
        'Para controlar la recopilación de datos con finalidades analíticas por parte de Google Analytics, puedes ir a': _("Para controlar la recopilación de datos con finalidades analíticas por parte de Google Analytics, puedes ir a"),
        'A continuación mostramos una tabla con las cookies utilizadas. Para cada cookie incluimos los siguientes atributos: finalidad, proveedor, nombre de la cookie, gestión, vigencia y función': _("A continuación mostramos una tabla con las cookies utilizadas. Para cada cookie incluimos los siguientes atributos: finalidad, proveedor, nombre de la cookie, gestión, vigencia y función"),
        'A continuación mostramos una tabla con las cookies utilizadas. Para cada cookie incluimos los siguientes atributos: finalidad, proveedor, nombre de la cookie, gestión, vigencia y función': _("A continuación mostramos una tabla con las cookies utilizadas. Para cada cookie incluimos los siguientes atributos: finalidad, proveedor, nombre de la cookie, gestión, vigencia y función"),
        'Permite recordar el idioma seleccionado con anterioridad': _("Permite recordar el idioma seleccionado con anterioridad"),
        'Permite recordar las cookies aceptadas con anterioridad': _("Permite recordar las cookies aceptadas con anterioridad"),
        'Finalidad': _("Finalidad"),
        'Proveedor': _("Proveedor"),
        'Nombre de la cookie': _("Nombre de la cookie"),
        'Gestión': _("Gestión"),
        'Vigencia': _("Vigencia"),
        'Función': _("Función"),
        'Necesarias': _("Necesarias"),
        'MOSQQUITO ALERT': _("MOSQQUITO ALERT"),
        'Propia': _("Propia"),
        'Persistente': _("Persistente"),
        'Mostrar la ventana informativa solo en la primera visita': _("Mostrar la ventana informativa solo en la primera visita"),
        'Analíticas': _("Analíticas"),
        'terceros': _("terceros"),
        '2 años': _("2 años"),
        'Registra una identificación única que se utiliza para generar datos estadísticos sobre cómo se utiliza el visitante el sitio web': _("Registra una identificación única que se utiliza para generar datos estadísticos sobre cómo se utiliza el visitante el sitio web"),
        '1 año': _("1 año"),
        'Necesarias': _("Necesarias"),
        'las imprescindibles para facilitar vuestra conexión. No hay opción de inhabilitarlas, dado que son las necesarias por el funcionamiento del sitio web': _("las imprescindibles para facilitar vuestra conexión. No hay opción de inhabilitarlas, dado que son las necesarias por el funcionamiento del sitio web"),
        'Técnicas': _("Técnicas"),
        'las que permiten controlar el tráfico y comunicación de datos, identificar la sesión y acceder a páginas de acceso restringido, entre otros': _("las que permiten controlar el tráfico y comunicación de datos, identificar la sesión y acceder a páginas de acceso restringido, entre otros"),
        'Analíticas':_("Analíticas"),
        'proporcionan información estadística y permiten mejorar los servicios':_("proporcionan información estadística y permiten mejorar los servicios"),
        'Cookie de sesión': _("Cookie de sesión"),

        # HELP
        'Layers selector help': _("Layers selector help"),
        'Filters help': _("Filters help"),
        'Download and reports help': _("Download and reports help"),
        'Graph help': _("Graph help"),
        'Shareview help': _("Shareview help"),
        'Información de los datos': _("Información de los datos"),
        'El mapa contiene información de 5 especies de mosquitos vectores de enfermedades:': _("El mapa contiene información de 5 especies de mosquitos vectores de enfermedades:"),
        'el mosquito tigre': _("el mosquito tigre"),
        'el mosquito de la fiebre amarilla': _("el mosquito de la fiebre amarilla"),
        'el mosquito del Japón': _("el mosquito del Japón"),
        'el mosquito de Corea': _("el mosquito de Corea"),
        'y el mosquito común': _("y el mosquito común"),
        'Además, puedes visualizar posibles lugares de cría de estos insectos en la vía pública. Esta información se complementa con modelos de probabilidad, elaborados a partir de los datos ciudadanos y con el esfuerzo de muestreo o distribución de participantes.': _("Además, puedes visualizar posibles lugares de cría de estos insectos en la vía pública. Esta información se complementa con modelos de probabilidad, elaborados a partir de los datos ciudadanos y con el esfuerzo de muestreo o distribución de participantes."),
        'DATOS NO MODELADOS': _("DATOS NO MODELADOS"),
        'según los expertos o los algoritmos de  Inteligencia Artificial (IA), las fotos de esta observación podrían ser de mosquito tigre': _("según los expertos o los algoritmos de  Inteligencia Artificial (IA), las fotos de esta observación podrían ser de mosquito tigre"),
        'o de': _("o de"),
        'en estos casos, no es posible determinar con seguridad de qué especie se trata.': _("en estos casos, no es posible determinar con seguridad de qué especie se trata."),

        ': según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito de la fiebre amarilla': _(": según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito de la fiebre amarilla"),
        'Mosquito del Japón': _("Mosquito del Japón"),

        ': según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito del Japón': _(": según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito del Japón"),
        
        'También incluye observaciones que podrían ser o de': _("También incluye observaciones que podrían ser o de"),
        'Mosquito del Japón': _("Mosquito del Japón"),
        'Mosquito del Corea': _("Mosquito del Corea"),
        'según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito de Corea': _("según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito de Corea"),
        'Mosquito Común': _("Mosquito Común"),
        ': según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito común': _(": según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser del mosquito común"),
        'Otras categorías. Mosquito no identificable:': _("Otras categorías. Mosquito no identificable:"),
        'según los expertos o los algoritmos de IA, estas observaciones y sus fotos no permiten determinar ninguna especie de mosquito en concreto. También incluye observaciones enviadas como “mosquito” que no han sido evaluadas al no contener imágenes asociadas.': _("según los expertos o los algoritmos de IA, estas observaciones y sus fotos no permiten determinar ninguna especie de mosquito en concreto. También incluye observaciones enviadas como “mosquito” que no han sido evaluadas al no contener imágenes asociadas."),
        ' Observaciones ciudadanas de picaduras de mosquito, de cualquier especie y sin ningún tipo de validación por parte de expertos o de algoritmos de IA.': _(" Observaciones ciudadanas de picaduras de mosquito, de cualquier especie y sin ningún tipo de validación por parte de expertos o de algoritmos de IA."),
        ': observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como imbornales con agua) en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA.': _(": observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como imbornales con agua) en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA."),        
        ': observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “imbornales con agua”) en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA.': _(": observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “imbornales con agua”) en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA."),
        'observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “imbornales sin agua”), en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA.': _("observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “imbornales sin agua”), en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA."),
        ': observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “otros tipos de lugares de cría”), en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA.': _(": observaciones ciudadanas de posibles lugares de cría de mosquitos (identificadas por la ciudadanía como “otros tipos de lugares de cría”), en su mayoría, sin ningún tipo de validación por parte de expertos o de algoritmos de IA."),
        'Según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser de otras especies de mosquito': _("Según los expertos o los algoritmos de IA, las fotos de esta observación podrían ser de otras especies de mosquito"),
        'La capa muestra la distribución de los participantes, donde las cuadrículas más oscuras indican un mayor número de dispositivos con la app instalada o que han estado mucho tiempo en la zona. Este dato es esencial para poder elaborar modelos: sin esta información no se podría saber si hay muchos mosquitos en un área o si lo que hay es mucha participación. En ecología esta información se conoce como esfuerzo de muestreo, permitiendo corregir las observaciones para hacerlas comparables entre áreas.': _("La capa muestra la distribución de los participantes, donde las cuadrículas más oscuras indican un mayor número de dispositivos con la app instalada o que han estado mucho tiempo en la zona. Este dato es esencial para poder elaborar modelos: sin esta información no se podría saber si hay muchos mosquitos en un área o si lo que hay es mucha participación. En ecología esta información se conoce como esfuerzo de muestreo, permitiendo corregir las observaciones para hacerlas comparables entre áreas."),
        'Selecciona las capas de información que te interese visualizar: observaciones de mosquito, picaduras, lugares de cría, otras especies y esfuerzo de muestreo.': _("Selecciona las capas de información que te interese visualizar: observaciones de mosquito, picaduras, lugares de cría, otras especies y esfuerzo de muestreo."),
        'Filtra tu selección de distintas maneras:': _("Filtra tu selección de distintas maneras:"),
        'POR LOCALIZACIÓN': _("POR LOCALIZACIÓN"),
        'Escribe y selecciona del desplegable tu lugar de interés': _("Escribe y selecciona del desplegable tu lugar de interés"),
        'POR HASHTAG': _("POR HASHTAG"),
        'puedes usar más de una etiqueta. Se mostrarán las observaciones que contengan como mínimo una de las etiquetas utilizadas.': _("puedes usar más de una etiqueta. Se mostrarán las observaciones que contengan como mínimo una de las etiquetas utilizadas."),
        'POR IDENTIFICADOR': _("POR IDENTIFICADOR"),
        ': escribe el identificador corto de un informe en el buscador de hashtag precedido por el símbolo :': _(": escribe el identificador corto de un informe en el buscador de hashtag precedido por el símbolo :"),
        'Ejemplo > :6RUID. Puedes usar más de un identificador. Se mostrarán las observaciones que contengan como mínimo uno de los identificadores utilizados.': _("Ejemplo > :6RUID. Puedes usar más de un identificador. Se mostrarán las observaciones que contengan como mínimo uno de los identificadores utilizados."),
        'POR FECHA O RANGO DE FECHAS': _("POR FECHA O RANGO DE FECHAS"),
        'Los filtros aplican a todas las capas de información de las observaciones (mosquitos, lugares de cría, picaduras, otras especies). La capa “esfuerzo de muestreo” sólo puede filtrarse por fecha o rango de fecha.': _("Los filtros aplican a todas las capas de información de las observaciones (mosquitos, lugares de cría, picaduras, otras especies). La capa \"esfuerzo de muestreo\" sólo puede filtrarse por fecha o rango de fecha."),
        'Los filtros son acumulativos, es decir, que actúan sobre el rango de datos previamente seleccionados. Por ejemplo, si filtramos mosquitos de la ciudad de Barcelona, y posteriormente buscamos un hashtag, el mapa nos devolverá solamente aquellas observaciones de la ciudad de Barcelona que tengan dicho hashtag.': _("Los filtros son acumulativos, es decir, que actúan sobre el rango de datos previamente seleccionados. Por ejemplo, si filtramos mosquitos de la ciudad de Barcelona, y posteriormente buscamos un hashtag, el mapa nos devolverá solamente aquellas observaciones de la ciudad de Barcelona que tengan dicho hashtag."),
        'Descarga los datos seleccionados en la vista de tu mapa y genera informes html con los datos seleccionados en la vista de tu mapa.': _("Descarga los datos seleccionados en la vista de tu mapa y genera informes html con los datos seleccionados en la vista de tu mapa."),
        'Consulta la información de la vista del mapa en formato de gráfico temporal': _("Consulta la información de la vista del mapa en formato de gráfico temporal"),
        'Comparte la vista del mapa, consulta la ayuda y la información del mapa y cambia el idioma del mapa': _("Comparte la vista del mapa, consulta la ayuda y la información del mapa y cambia el idioma del mapa"),
        'Estimates help': _("Estimates help"),
        'Consulta el grado de probabilidad e incertidumbre de encontrar una especie de mosquito concreta. Selecciona la especie que quieras consultar y el rango temporal': _("Consulta el grado de probabilidad e incertidumbre de encontrar una especie de mosquito concreta. Selecciona la especie que quieras consultar y el rango temporal"),
        
        # MODELS
        'Month / Year': _("Month / Year"),
        'Very low': _("Very low"),
        'Low': _("Low"),
        'Medium': _("Medium"),
        'High': _("High"),
        'Select model date': _("Select model date"),
        'Click on year and month': _("Click on year and month"),
        'Apply': _("Apply"),
        'Probability': _("Probability"),
        'Uncertainty': _("Uncertainty"),
        'Transparency': _("Transparency"),
        'Select species': _("Select species"),

        # LOGIN 
        'Field required': _("Field required"),
        'Username *': _("Username *"),
        'Password *': _("Password *"),
        'Confirm Logout Title': _("Confirm Logout Title"),
        'Confirm Logout Message': _("Confirm Logout Message"),
        'Confirm Logout': _("Confirm Logout"),

        # MODALS ERRORS
        'Model not found on Server': _("Model not found on Server"),
        'This map view does not exist': _("This map view does not exist"),
        'This report does not exist': _("This report does not exist"),
        'If you are using Safari, please Check that your pop-up windows block is not blocking the list of observations': _("If you are using Safari, please Check that your pop-up windows block is not blocking the list of observations"),

        # LOGOS
        'This interactive map has been funded by': _("This interactive map has been funded by"),
        'Coordinators': _("Coordinators"),
        'Mosquito Alert está coordinado por': _("Mosquito Alert está coordinado por"),
        'Con el apoyo de': _("Con el apoyo de"),
        'About us': _("About us")
    })

<<<<<<< HEAD
    # response.set_cookie(key='referrer', value='mosquitoalert')
=======
>>>>>>> master-gtm
    return response
