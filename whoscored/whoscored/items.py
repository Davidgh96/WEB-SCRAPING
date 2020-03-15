# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WhoscoredItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    EquipoLocal= scrapy.Field()
    EquipoVisitante= scrapy.Field()
    Resultado= scrapy.Field()
    Comienzo= scrapy.Field()
    Fecha= scrapy.Field()
    Cronologia=scrapy.Field()
    EventoLocal=scrapy.Field()
    EventoVisitante=scrapy.Field()
    Minuto=scrapy.Field()
    EntrenadorLocal=scrapy.Field()
    EntrenadorVisitante=scrapy.Field()
    GoleadoresLocal=scrapy.Field()
    GoleadoresVisitante=scrapy.Field()
    FormacionLocal=scrapy.Field()
    FormacionVisitante=scrapy.Field()
    Estadio=scrapy.Field()
    Asistencia=scrapy.Field()
    Tiempo=scrapy.Field()
    Arbitro=scrapy.Field()
    PuntuacionLocal=scrapy.Field()
    PuntuacionVisitante=scrapy.Field()   
    JugadoresTitularesLocal=scrapy.Field()
    NumeroLocal=scrapy.Field()
    NombreLocal=scrapy.Field()
    PuntuacionJugadorLocal=scrapy.Field()
    NumeroVisitante=scrapy.Field()
    NombreVisitante=scrapy.Field()
    PuntuacionJugadorVisitante=scrapy.Field()
    JugadoresTitularesVisitante=scrapy.Field()
    SuplentesLocal=scrapy.Field()
    SuplentesVisitante=scrapy.Field()
    NumeroLocalSuplente=scrapy.Field()
    NombreLocalSuplente=scrapy.Field()
    PuntuacionJugadorLocalSuplente=scrapy.Field()
    NumeroVisitanteSuplente=scrapy.Field()
    NombreVisitanteSuplente=scrapy.Field()
    PuntuacionJugadorVisitanteSuplente=scrapy.Field()

    
