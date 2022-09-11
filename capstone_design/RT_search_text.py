import requests as req 
import tensorflow
from bs4 import BeautifulSoup as bfu

signal_RT_search = 'https://signal.bz/'
address = req.get(signal_RT_search) #브릭 대학원생 채용정보사이트
address.raise_for_status()
soup = bfu(address.text, 'html.parser')