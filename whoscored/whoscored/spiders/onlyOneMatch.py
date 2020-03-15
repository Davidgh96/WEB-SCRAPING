# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import logging

import time
import scrapy
from scrapy.spiders import CrawlSpider
from whoscored.items import WhoscoredItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
#Aqui se coloca el path a chromedriver
driver = webdriver.Chrome(path)
class OnlyOneMatch(CrawlSpider):
	
	name = 'OnlyOneMatch'
	allowed_domains = ['es.whoscored.com']
	start_urls = ["https://es.whoscored.com/Matches/1316778/Live/Espa%C3%B1a-La-Liga-2018-2019-Leganes-Levante"]
	def parse(self, response):
		
		driver.get(response.url)

		yield scrapy.Request(url = "https://es.whoscored.com/Matches/1316778/Live/Espa%C3%B1a-La-Liga-2018-2019-Leganes-Levante", callback = self.parse_item)
			
	
	def parse_item(self, response):
	
		
		driver.get(response.url)
		items=WhoscoredItem()
		try:			
			items['EquipoLocal']= driver.find_element_by_xpath('//*[@id="match-header"]//td[@class="team"][1]').text
		except StaleElementReferenceException:
			items['EquipoLocal']= driver.find_element_by_xpath('//*[@id="match-header"]//td[@class="team"][1]').text

		items['EquipoVisitante']= driver.find_element_by_xpath('//*[@id="match-header"]//td[@class="team"][2]').text
		items['Resultado']= driver.find_element_by_xpath('//*[@id="match-header"]//td[@class="result"]').text
		items['Comienzo']= driver.find_element_by_xpath('//*[@id="match-header"]//div[@class="info-block cleared"][3]//dd[1]').text
		items['Fecha']= driver.find_element_by_xpath('//*[@id="match-header"]//div[@class="info-block cleared"][3]//dd[2]').text

		
		element = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="live-incidents"]//tr')))

		items['EntrenadorLocal']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="home"]//span[@class="manager-name"]').text
		items['EntrenadorVisitante']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="away"]//span[@class="manager-name"]').text
		items['GoleadoresLocal']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="home"]//ul').text
		items['GoleadoresVisitante']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="away"]//ul').text
		items['FormacionLocal']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="home"]//div[@class="formation"]').text
		items['FormacionVisitante']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="away"]//div[@class="formation"]').text
		items['Estadio']=driver.find_element_by_xpath('//div[@id="match-centre"]//div[@id="stadium"]//div[@class="match-info"]//span[@class="venue"]//span[@class="value"]').text
		items['Asistencia']=driver.find_element_by_xpath('//div[@id="match-centre"]//div[@id="stadium"]//div[@class="match-info"]//span[@class="attendance"]//span[@class="value"]').text
		items['Tiempo']=driver.find_element_by_xpath('//div[@id="match-centre"]//div[@id="stadium"]//div[@class="match-info"]//span[@class="weather"]//span[@class="value"]').text
		items['Arbitro']=driver.find_element_by_xpath('//div[@id="match-centre"]//div[@id="stadium"]//div[@class="match-info"]//span[@class="referee"]//span[@class="value"]').text
		items['PuntuacionLocal']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="home"]//div[@class="team-rating"]').text
		items['PuntuacionVisitante']=driver.find_element_by_xpath('//div[@id="match-centre-header"]//div[@data-field="away"]//div[@class="team-rating"]').text

		JugadoresLocal=driver.find_elements_by_xpath('//div[@id="match-centre"]//div[@class="pitch"]//div[@data-field="home"]//div[@class="player" or @class="player is-man-of-the-match"]')
		items['JugadoresTitularesLocal']=[]
		x=0
		for i in JugadoresLocal:
			#logging.critical(i)
			items['JugadoresTitularesLocal'].append(dict())
			
			numero=i.find_element_by_xpath('.//span[@class="shirt-number"]').text
			items['JugadoresTitularesLocal'][x]["NumeroLocal"]=numero
			nombre=i.find_element_by_xpath('.//div[@class="player-name-wrapper"]')
			items['JugadoresTitularesLocal'][x]["NombreLocal"]=nombre.get_attribute("title")
			puntuacion=i.find_element_by_xpath('.//span[@class="player-stat-value"]').text
			items['JugadoresTitularesLocal'][x]["PuntuacionJugadorLocal"]=puntuacion
			x+=1
		
		JugadoresVisitante=driver.find_elements_by_xpath('//div[@id="match-centre"]//div[@class="pitch"]//div[@data-field="away"]//div[@class="player" or @class="player is-man-of-the-match"]')
		items['JugadoresTitularesVisitante']=[]
		x=0
		for i in JugadoresVisitante:
			#logging.critical(i)
			items['JugadoresTitularesVisitante'].append(dict())
			
			numero=i.find_element_by_xpath('.//span[@class="shirt-number"]').text
			items['JugadoresTitularesVisitante'][x]["NumeroVisitante"]=numero
			nombre=i.find_element_by_xpath('.//div[@class="player-name-wrapper"]')
			items['JugadoresTitularesVisitante'][x]["NombreVisitante"]=nombre.get_attribute("title")
			puntuacion=i.find_element_by_xpath('.//span[@class="player-stat-value"]').text
			items['JugadoresTitularesVisitante'][x]["PuntuacionJugadorVisitante"]=puntuacion
			x+=1	

		JugadoresLocalSuplente=driver.find_elements_by_xpath('//div[@id="match-centre"]//div[@class="substitutes" and @data-field="home"]//div[@class="player" or @class="player is-man-of-the-match"]')
		items['SuplentesLocal']=[]
		x=0
		for i in JugadoresLocalSuplente:
			#logging.critical(i)
			items['SuplentesLocal'].append(dict())
			
			numero=i.find_element_by_xpath('.//span[@class="shirt-number"]').text
			items['SuplentesLocal'][x]["NumeroLocalSuplente"]=numero
			nombre=i.find_element_by_xpath('.//div[@class="player-name-wrapper"]')
			items['SuplentesLocal'][x]["NombreLocalSuplente"]=nombre.get_attribute("title")
			puntuacion=i.find_element_by_xpath('.//span[@class="player-stat-value"]').text
			items['SuplentesLocal'][x]["PuntuacionJugadorLocalSuplente"]=puntuacion
			x+=1
		
		JugadoresVisitanteSuplente=driver.find_elements_by_xpath('//div[@id="match-centre"]//div[@class="substitutes" and @data-field="away"]//div[@class="player" or @class="player is-man-of-the-match"]')
		items['SuplentesVisitante']=[]
		x=0
		for i in JugadoresVisitanteSuplente:
			#logging.critical(i)
			items['SuplentesVisitante'].append(dict())
			
			numero=i.find_element_by_xpath('.//span[@class="shirt-number"]').text
			items['SuplentesVisitante'][x]["NumeroVisitanteSuplente"]=numero
			nombre=i.find_element_by_xpath('.//div[@class="player-name-wrapper"]')
			items['SuplentesVisitante'][x]["NombreVisitanteSuplente"]=nombre.get_attribute("title")
			puntuacion=i.find_element_by_xpath('.//span[@class="player-stat-value"]').text
			items['SuplentesVisitante'][x]["PuntuacionJugadorVisitanteSuplente"]=puntuacion
			x+=1	

		tr=driver.find_elements_by_xpath('//*[@id="live-incidents"]//tr')
		
		items['Cronologia']=[]
		x=0
		for i in tr:
			logging.critical(i)
			items['Cronologia'].append(dict())
			try:
				local=i.find_elements_by_xpath('.//td[@data-field="home"]//div[@class!="clear"]')
				items['Cronologia'][x]["EventoLocal"]=""
				for j in local:
					items['Cronologia'][x]["EventoLocal"]+=j.get_attribute("title")+" "
				items['Cronologia'][x]["EventoLocal"]=items['Cronologia'][x]["EventoLocal"].rstrip()
			except NoSuchElementException:
				pass

			items['Cronologia'][x]["Minuto"]=(i.find_element_by_xpath('.//span[contains(@class,"minute")]')).text

			try:
				visitante=i.find_elements_by_xpath('.//td[@data-field="away"]//div[@class!="clear"]')
				items['Cronologia'][x]["EventoVisitante"]=""
				for j in visitante:
					items['Cronologia'][x]["EventoVisitante"]+=j.get_attribute("title")+" "
				items['Cronologia'][x]["EventoVisitante"]=items['Cronologia'][x]["EventoVisitante"].rstrip()	
			except NoSuchElementException:
				pass
			for j in minuto:
				if (j.text in i.text):
					logging.debug("Minuto" + j.text)
					items['Cronologia'][x]["Minuto"]+= j.text
					break
				logging.debug("MinutoFuera" + j.text)
			for j in eventosLocal:
				if (j.text!="" and j.text in i.text and items['Cronologia'][x]["Minuto"] in i[x].text):
					logging.debug("eventoLocal" + j.get_attribute('title'))
					items['Cronologia'][x]["EventoLocal"]+=" "+ j.get_attribute('title')
				logging.debug("local" + j.get_attribute('title'))

			for j in eventosVisitante:
				if (j.text!="" and j.text in i.text and items['Cronologia'][x]["Minuto"] in i[x].text):
					logging.debug("EventoVisitante" + j.get_attribute('title'))
					items['Cronologia'][x]["EventoVisitante"]+=" "+ j.get_attribute('title')
				logging.debug("visitante" + j.get_attribute('title'))	
			logging.info("Final")
			x+=1	


		
		driver.quit()
		yield items	
#scrapy crawl OnlyOneMatch -o datos.json 
