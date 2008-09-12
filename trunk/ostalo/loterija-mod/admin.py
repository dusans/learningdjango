import re, urllib, time, sqlite3, random 
from mod_python import Session 
def index(req):
	sess = Session.Session(req) 
	txt = sess.get('uporId', '-')
	req.content_type="text/html"
	return txt

def login(req):
	#==== VARIABLE ====
	sess = Session.Session(req) 
	upoImeLogin = req.form.get("upoImeLogin", "")
	gesloLogin = req.form.get("gesloLogin", "")
	
	#==== BAZA ====	
	conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db")
	c = conn.cursor()
	c.execute("SELECT * FROM uporabniki WHERE uporIme = '"+upoImeLogin+"' and geslo = '"+gesloLogin+"';")
	d = c.fetchone()
	c.close()
	conn.close()
	#==== SEJA ====
	req.content_type="text/html"
	if d != None:
		sess['uporId'] = d[0]
		sess['uporIme'] = d[1]
		sess['datumR'] = d[5]
		sess.set_timeout(1200)
		sess.save()
		#getData()
		
		script = '<script> function move() {window.location = "../prvi.psp"}</script>'
		return script+'<html><body onload="timer=setTimeout(''move()'',4000)"><b>Prijava uspesna</b><br></body></html>'
	else:
		return "<html><b>Napaka</b><br></html>"

def register(req):
	#==== VARIABLE ====
	
	upoIme = req.form.get("upoIme", "")
	ime = req.form.get("ime", "")
	priimek = req.form.get("priimek", "")
	mail = req.form.get("mail", "")
	datum = req.form.get("datum", "")
	geslo = req.form.get("geslo", "")

	#==== BAZA ====
	try:
		conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db")
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS uporabniki (id INTEGER PRIMARY KEY, uporIme TEXT, ime TEXT, priimek TEXT, mail TEXT, datum TEXT, geslo TEXT );") 
		c.execute("INSERT INTO uporabniki VALUES (NULL, '"+upoIme+"', '"+ime+"', '"+priimek+"', '"+mail+"', '"+datum+"', '"+geslo+"') ;")
		conn.commit()
		
	except Exception, inst:
		conn.rollback()
		req.write(str(type(inst)) + " " + str(inst.args) + " " + str(inst))     # the exception instance
		req.write("Prislo je do napake :(")
	finally:
		c.close()
		del c
		conn.close()

	req.content_type="text/html"
	script = '<script> function move() {window.location = "../login.html"}</script>'
	return script+'<html><body onload="timer=setTimeout(''move()'',4000)"><b>Done</b></body></html>'

def srecna(req):
	#podanaStevilke = "False"
	aliSrecne = req.form.get("srecne", "")
	podaneStevilke = req.form.get("podaneStevilke", "False")
	#==== RANDOM ====
	if podaneStevilke == "False": #ce je uporabnik sam podal kombinacijo
		datumR = req.form.get("datumR", "")
		datumR = datumR.split(".")

		if len(datumR) == 3:	
			d = int(datumR[0])
			m = int(datumR[1])
			l = int(datumR[2])
		else:
			d = random.randint(1,31) 
			m = random.randint(1,12)
			l = random.randint(1,2007)
			
		srecne = []
		srecne = dodaj( (  (d+m+l) *  random.randint(1,m+1) /23%39  ) , srecne)
		srecne = dodaj( (  (l/d*m) * random.randint(1,d+1) /23%39  ) , srecne)
		srecne = dodaj( (  (l/d/m) * random.randint(1,m+d) /23%39  )  , srecne)
		srecne = dodaj( (  (l/d/m) * random.randint(1,m+d) /23%39  ) , srecne)
		srecne = dodaj( (  abs(l-d-m) * random.randint(1,l) /23%39  ), srecne)
		srecne = dodaj( (  abs(m-d-l) * random.randint(1,m) /23%39  ) , srecne)
		srecne = dodaj( (  abs(d-l) * random.randint(1,d) /23%39  ), srecne)

		while(len(srecne) < 7):
			srecne = dodaj( random.randint(1,39), srecne)

		srecne.sort()
	else:
		srecne = podaneStevilke

	#==== VARIABLE ====
	uporId = ""
	sess = Session.Session(req) 
	if not sess.is_new():
		sess.load()
		uporId = str(sess.get('uporId', '-'))
	
	#==== BAZA ====
	max = -1
	if uporId != "":
		try:
			conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db")
			c = conn.cursor()
			c.execute("CREATE TABLE IF NOT EXISTS srecne (id INTEGER PRIMARY KEY, idUpor INTEGER, stevilke TEXT);") 
			c.execute("INSERT INTO srecne VALUES (NULL, '"+uporId+"', '"+str(srecne)+"') ;")
			conn.commit()
			c.execute("SELECT MAX(id) FROM srecne WHERE idUpor = '"+uporId+"'")
			max = (c.fetchone())[0]
		except Exception, inst:
			conn.rollback()
			req.write(str(type(inst)) + " " + str(inst.args) + " " + str(inst))     # the exception instance
			req.write("Prislo je do napake :(")
		finally:
			c.close()
			del c
			conn.close()

	vrni = str(srecne)
	
	#==== ZAHTEVA s SRECNA  strani ====
	if aliSrecne == "True" and max != -1:
		vrni = str(max) + ":" + str(srecne) #v obliki slovarja

	req.content_type="text/html"

	return vrni

def dodaj(kaj, komu):
	if kaj > 0 and not kaj in komu:
		komu.append(kaj)
	return komu

def stUpo(req):
	conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db")
	c = conn.cursor()
	c.execute("SELECT id, uporIme, ime, priimek, mail, datum FROM uporabniki")
	d = ""
	for i in c:
		d += str(i) +"<br>"
	req.content_type="text/html"
	return d

def getData():
	#req.content_type="text/html"
	#time.sleep(5)
	try:
		#==== Povezi se da DB ====
		conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db",timeout=5.0)
		c = conn.cursor()
		#==== Vse daj v zgodovino ====
		c.execute("UPDATE loto SET staro='1'")

		#TODO updati samo je to potrebno

		# ==== ZMANJSANJE BAZE
		c.execute("SELECT COUNT(*) FROM loto")
		if c.fetchone()[0] > 100000:
			c.execute("SELECT MIN(id) FROM loto")
			od = c.fetchone()[0]
			c.execute("DELETE FROM loto WHERE id<"+str(od+10000))
			
		#c.execute("CREATE TABLE IF NOT EXISTS loto (id INTEGER PRIMARY KEY, datum TEXT, krog INTEGER, stevilke TEXT, dodatna INTEGER, sedmica INTEGER, vrednost INTEGER, kraj TEXT, staro INTEGER );") #IF NOT EXISTS

		#==== Dobi linke za VSA LETA ====
		lotoLeta = urllib.urlopen("http://www.loterija.si/igre/loto/statistike/").read()
		leta = re.search('(<DIV class="content-aux"> <div class="box-title">Loto statistike</div><div class="box-body"><UL>)(?P<temp>(.|[\n\r])*?)(<\/UL>)',lotoLeta)
		linki = (re.sub(r"(<LI><A HREF=\"../../../)|\">.{4}</A></LI>","",leta.group("temp"))).split("\n")
		#print "Linki: ", linki
		a = b = zac = time.asctime()

		foo = open("/var/www/ora/ora_mod_python/ora31/procent.txt", "w")
		max = len(linki); counter = 1
		
		#==== Za vsako leto pojdi po podatke ====
		for leto in linki:
			#==== AJAX file ====
			foo.seek(0); foo.truncate() #zbrisi vsebino vmesne datoteke
			foo.write(str(counter*100/max)) #nastavi procent
			foo.flush()
			#==== Odpri URL ====
			loto = urllib.urlopen("http://www.loterija.si/" + leto).read()
			tabela = re.search('(<TABLE cellspacing="0" cellpadding="3" class="stable-border" >)(?P<temp>(.|[\n\r])*?)(<\/TABLE>)',loto) #Najdi tabelo
			if tabela != None:
				a = time.time()
				vrstice = re.split(r"<TR>|<\/TR>", tabela.group("temp").upper()) #rezultat razdeli v VRSTICE
				vrstice = vrstice[1:] #brez GLAVE

				#odstrani <td...> argumente in prazne vrstice
				HTMLtabela = [i for i in vrstice if re.search(r"^\0|^\s$|^\n$|^\r$|^(\r\n)$", i) == None and i != ""]
				for i in reversed(HTMLtabela):
					#NA STOLPCE
					polja = re.split(r"<TD>|<TD[^>]*>|<\/TD>|<NOBR>|<\/NOBR>|<BR\/>|<BR>", i) 
					l = [i for i in polja if re.search(r"^\0|^\s$|^\n$|^\r$|^(\r\n)$", i) == None and i != ""]
					l = [i.replace("&NBSP;","") for i in l] #grdo

					if len(l) >= 9:	#grdo
						l = l[0:8]
					if len(l) > 4: #grdo
						c.execute("INSERT INTO loto VALUES (NULL, '"+l[0]+"', '"+l[1]+"', '"+l[2]+"', '"+l[3]+"', '"+l[4]+"', '"+l[-2]+"', '', '0') ;") #"+l[-1]+"
					#print l
				b = time.time()
				#print polja
				#print len(vrstice)
			#print leto, "Cas:", b-a
		conn.commit()
	except Exception, inst:
		conn.rollback()
		req.write(str(type(inst)))     	# the exception instance
		req.write(str(inst.args))     	# arguments stored in .args
		req.write(str(inst))        	# __str__ allows args to printed directly
		req.write("Prislo je do napake :(")
	finally:
		#if foo != None:
			#foo.close() 
		c.close()
		del c
		conn.close()
def removeVseSrecne(req):
	
	dodaj = uporId = ""
	#==== VARIABLE ====
	id = req.form.get("id", -1)
	if id != -1:
		dodaj = " AND id='"+id+"'"

	sess = Session.Session(req) 
	if not sess.is_new():
		sess.load()
		uporId = str(sess.get('uporId', '-'))
	
	#==== BAZA ====
	if uporId != "":
		try:
			conn = sqlite3.connect("/var/www/ora/ora_mod_python/ora31/semi.db")
			c = conn.cursor()
			c.execute("DELETE FROM srecne WHERE idUpor = '"+uporId+"' " + dodaj)
			conn.commit()
		except Exception, inst:
			conn.rollback()
			req.write(str(type(inst)) + " " + str(inst.args) + " " + str(inst))     # the exception instance
			req.write("Prislo je do napake :(")
		finally:
			c.close()
			del c
			conn.close()
	
	req.content_type="text/html"
	if id == -1:
		script = '<script> function move() {window.location = "../srecne.psp"}</script>'
		return script+'<html><body onload="timer=setTimeout(''move()'',4000)"><b>Done</b></body></html>'

	return id