from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import WebDriverException
import pandas as pd
from datetime import date
import time

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

home_link = "https://listado.mercadolibre.com.ar/"
search_kw = "iphone xs".replace(" ", "+")

driver.get(home_link + search_kw + "#D[A:" + search_kw + "]")

telefono_titulo = []
telefono_precio = []
telefono_envio = []
telefono_link = []
telefono_estado = []
telefono_calificacion = []

cantidad_pagina = 2

page = BeautifulSoup(driver.page_source, 'html.parser')

try:
    time.sleep(5)
    boton_entendido = driver.find_element(By.CLASS_NAME, "cookie-consent-banner-opt-out__action--key-accept")
    boton_entendido.click()
    # Cerrar aviso de cookies
    time.sleep(2)
except:
    pass

for i in range(0, cantidad_pagina):
    # moverse por las paginas
    for telefono in page.findAll('li', class_='ui-search-layout__item shops__layout-item'):
        titulo = telefono.find('h2', class_="ui-search-item__title shops__item-title")
        if titulo:
            telefono_titulo.append(titulo.text)
        else:
            telefono_titulo.append('Sin titulo')

        precio = telefono.find('span', class_="price-tag-fraction")
        if precio:
            telefono_precio.append('$' + precio.text)
        else:
            telefono_precio.append('Sin precio')

        envio = telefono.find('p', class_="ui-search-item__shipping ui-search-item__shipping--free"
                                          " shops__item-shipping-free")
        if envio:
            telefono_envio.append(envio.text)
        else:
            telefono_envio.append('Sin envio gratuito')

        link = telefono.find('a', class_="ui-search-item__group__element shops__items-group-details ui-search-link")
        if link:
            telefono_link.append(link['href'])
        else:
            telefono_link.append('Sin link')

        estado = telefono.find('span',
                            class_="ui-search-item__group__element ui-search-item__details shops__items-group-details")
        if estado:
            telefono_estado.append(estado.text)
        else:
            telefono_estado.append('Nuevo')

        calificacion = telefono.find('div',
                                     class_="ui-search-item__group ui-search-item__group--reviews shops__items-group")
        if calificacion:
            telefono_calificacion.append(calificacion.text)
        else:
            telefono_calificacion.append('')

    try:
        siguiente_btn = driver.find_element(By.CLASS_NAME, "andes-pagination__button--next")
        siguiente_btn.click()
        time.sleep(2)
    except:
        pass

lista_producto = pd.DataFrame({
    'TITULO': telefono_titulo,
    'PRECIO': telefono_precio,
    'ENVIO': telefono_envio,
    'ESTADO': telefono_estado,
    'CALIFICACION': telefono_calificacion,
    'LINK': telefono_link
})

lista_producto = lista_producto.sort_values(by=['PRECIO', 'ESTADO'], ascending=[True, False])

lista_producto.to_csv(r'D:/Facultad/El-Tomas-Del-Precio/listas/lista_' + search_kw + '.csv', index=None,
                      header=True, encoding='utf-8-sig', sep=';')
