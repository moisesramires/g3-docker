
# export FLASK_APP=flapp.py 
# flask run

# 127.0.0.1:5000/info?freg=São José de São Lázaro&rua=Avenida da Liberdade
import os.path
from os import path
from flask import Flask
from flask import request as req
import requests
import re
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
import overpy
from overpy import Result
import time
import sys
from flask import render_template



api = overpy.Overpass()

app = Flask(__name__ ,template_folder='.')




@app.route('/info')
def street_info():
	rua = req.args.get('rua').strip()
	freguesia = req.args.get('freg').strip()
		
	print(rua)
	print(freguesia)

	name=freguesia + rua + ".html"

	mapper = open("map.txt", "r")
	template = open("template.html", "r").read();


	if(path.exists(name)):
		return render_template("./"+name)

	else:

		#Códgio para Freguesia
		fl = 0
		for m in mapper:
			m = m.split("|",1)
			if (m[0].strip() == freguesia or freguesia in m[0].strip()):
				URL=m[1].strip()
				fl=1
				break

		if (fl == 0):
			print("no data on that one")


		else:
			hist=""
			page = requests.get(URL)
			soup = BeautifulSoup(page.content, 'html.parser')		

			title = soup.find('title').getText().replace("– Wikipédia, a enciclopédia livre","").replace("Abrantes","").replace("Baião","").replace("Arraiolos","").replace("Arcos de Valdevez","").replace("Angra do Heroísmo","").replace("Amares","").replace("Alandroal","").replace("Amarante","").replace("Alcácer do Sal","").replace("Alenquer","").replace("(","").replace(")","")
			
			b=False
			e=True
			w=0
			for i in soup.find_all(["p","h2","li"]):
				s=str(i.getText(strip=True))
				if( ("Toponímia" in s) ):
					if(w < 1):
						w+=1
					else:
						e=False	
				
				if(s == "Referências" or   ( "Gastronomia"in s ) or   ( "Criada pela Lei" in s ) or   ( "Geografia" in s ) or ( "Portal de Portugal"in s ) or   ( "Praça dos Combatentes" in s )   or ("Notas e referências" in s) ):
					e=False
				

				if(len(i.getText()) >3 and (not ( str(i.getText()).startswith("!") ) ) and b and e and (not (i.getText()[0].isdigit())) and (i.getText()!="Índice") and ("População" not in i.getText()) and ("Demografia" not in i.getText()) and ("Média do País" not in i.getText()) and ("Política" not in i.getText()) and ("Facebook" not in i.getText()) and "Ligações externas" not in i.getText()  and "Toponímia" not in i.getText() and "(Fonte: INE)" not in i.getText()) :
					hist= hist +re.sub("\[\d\]","",i.getText().replace("[editar | editar código-fonte]","")).replace("[Eleições autárquicas portuguesas de 2017|Eleições de 2017]","").replace(";\n","").replace("\n","<br>").replace("História","História<br>")
					print(re.sub("\[\d\]","",i.getText().replace("[editar | editar código-fonte]","")).replace("[Eleições autárquicas portuguesas de 2017|Eleições de 2017]","").replace(";\n",""))
				if(i.getText() == "Ver histórico"):
					b=True
			
		print(hist)
		template=template.replace("INFOFREGUESIA",hist);

		
		
			
		#Código para Hostel
		s ="area[name=\""+ freguesia + "\"];node(area)[name][tourism=hostel][\"addr:street\"=\"" + rua + "\"];out;"
		result: Result = api.query(s)
		hostel=""
		for way in result.nodes:
			if( way.tags.get("name", "n/a") not in hostel):
				hostel=hostel +  (way.tags.get("name", "n/a")) + "<br>"
				hostel=hostel +("  email: %s" % way.tags.get("email", "n/a")) + "<br>" 
				hostel=hostel +("  website: %s" % way.tags.get("website", "n/a")) + "<br>"
				hostel=hostel +("  phone: %s" % way.tags.get("phone", "n/a")) + "<br>"+ "<br>"+ "<br>"



		
		
		if hostel=="":
			hostel="Sem hostels na área"
		template=template.replace("ALOJAMENTOLOCAL",hostel);
		print(hostel)




		template=template.replace("NOMEDAFREGUESIA",freguesia);
		template=template.replace("NOMEDARUA",rua);

		open(name, "w").write(template);
		final = " <h1><b>Alojamento Local</b></h1>"
		final += "<p>" + hostel + "</p>"
		final += " <h1><b>Freguesia</b></h1>"
		final += "<p>" + hist + "</p>"

		return final		

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port='9595')
