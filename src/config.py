# Configuration for the Emol Graph Project

# Words to ignore during entity extraction (noise reduction)
BLACKLIST = {
    "Emol",
    "Twitter",
    "X",
    "Facebook",
    "Instagram",
    "TikTok",
    "WhatsApp",
    "AFP",
    "AP",
    "EFE",
    "S.A.",
    "Inc.",
    "TV",
    "TVN",
    "Mega",
    "Canal 13",
    "CHV",
    "CNN",
    "BBC",
    "Radio",
    "BioBio",
    "Cooperativa",
    "ADN",
    "Lunes",
    "Martes",
    "Miércoles",
    "Jueves",
    "Viernes",
    "Sábado",
    "Domingo",
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
    "Foto",
    "Video",
    "Clic",
    "Aquí",
    "Fuente",
    "Agencia",
    "Pesos",
    "Dólares",
}


# Entity Resolution: Map variations to a canonical name
ENTITY_MAPPING = {
    "Presidente Boric": "Gabriel Boric",
    "Boric": "Gabriel Boric",
    "Mandatario": "Gabriel Boric",
    "Jefe de Estado": "Gabriel Boric",
    "Camila Vallejo": "Camila Vallejo",
    "Ministra Vallejo": "Camila Vallejo",
    "Republicanos": "Partido Republicano",
    "La U": "Universidad de Chile",
    "Colo Colo": "Colo-Colo",
}

# File paths
RAW_DATA_PATH = "../data/example_raw_news.csv"
PROCESSED_DATA_PATH = "../data/example_graph_edges.csv"
