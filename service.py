#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	----------------------
	 Autor   : Anarchy
	 Date    : 16/02/2019
	 Name    : service.py
	 Version : 0.0.8-a
	----------------------
"""

import inspect, json, os, platform, sys, time
try: from Tkinter import *
except: from tkinter import *

class color:
	BOLD	= '\033[1m'
	ITALIC	= '\033[3m'
	
	RED	= '\033[31m'
	GREEN	= '\033[32m'
	BLUE	= '\033[34m'
	YELLOW	= '\033[33m'
	PURPLE	= '\033[35m'
	WHITE	= '\033[37m'
	
	END	= '\033[0m'

def madeLabel(panel, labels, _font):
	for i, txt in enumerate(labels):
		Label(panel, text=txt, font=_font).grid(row=i+1, column=0, pady=1, sticky=W)

def madePanel(panel, panelName, r, act):
	def madeButton(panel, act, r):
		global button, label, subpanel
		button.append([])
		
		for i, txt in enumerate(['START', 'RESTART', 'CONFIG']):
			button[r].append(Button(panel, text=txt, font=['Ubuntu', 9], command=act[i], width=8, state=NORMAL))
			button[r][i].grid(row=i+1, column=0, padx=6, pady=4, sticky=W)
	
	subpanel.append(LabelFrame(panel, bd=1, relief=GROOVE, text=panelName, font=['Ubuntu Light', 12]))
	subpanel[len(subpanel)-1].grid(row=1, column=r, padx=8, pady=8)
	
	label.append(Label(subpanel[len(subpanel)-1], text='ARRÊTER', font=["Ubuntu", 10], bg="#AA0000", fg="#000000", height=2, width=10))
	label[r].grid(row=0, column=0, padx=6, pady=4)
	madeButton(subpanel[len(subpanel)-1], act, r)

def serv(s, x):
	global button, label
	
	if(s == 'apache2'): msg = ['Serveur Apache', 0]
	elif(s == 'mysql'): msg = ['Base de données MySQL', 1]
	elif(s == 'tor'): msg = ['Service Tor', 2]
	
	if(x in [1, 2]):
		if(x == 1): line = ['start', '{} lancer'.format(msg[0])]
		elif(x == 2): line = ['restart', '{} relancer'.format(msg[0])]
		label[msg[1]].config(text='LANCER', bg="#00AA00")
		button[msg[1]][0].config(text='STOP', command=lambda:serv(s, 0))
	elif(x == 0):
		line = ['stop', '{} arrêter'.format(msg[0])]
		label[msg[1]].config(text='ARRÊTER', bg="#AA0000")
		button[msg[1]][0].config(text='START', command=lambda:serv(s, 1))
	
	os.system("/etc/init.d/{} {}".format(s, line[0]))
	check(line[1])

def servAll(x):
	serv('apache2', x)
	serv('mysql', x)
	if(tor): serv('tor', x)

def check(act):
	global step
	step.set(act)
	print(" [ {}FINISHED{} ]".format(color.BOLD+color.GREEN, color.END))

def verify():
	checked, DIR, stop = [], os.listdir('/etc/init.d/'), False
	
	time.sleep(.5)
	print("{}> {}Checking installed services{}_".format(info[2], color.YELLOW, color.END))
	for txt in services:
		if(txt in DIR): checked.append([txt, True])
		elif(not txt in DIR): checked.append([txt, False])
	
	for i, txt in enumerate(checked):
		time.sleep(.1)
		if(False in checked[i]):
			stop = True
			print(" [ {}NOT FOUND{} ] - {}".format(color.RED, color.END, checked[i][0]))
	
	if(stop): return False
	else: print(" [ {}OK{} ] - No missing services\n".format(color.GREEN, color.END))
	return True

def splash():
	time.sleep(.5)
	screen = [
		"\n{}     ____               O             ___".format(color.BOLD+color.YELLOW),
		"    | ___|----.---,-.--.-.----.----. | _ \_ __",
		"    |___ | -__| .-| |  | |  __| -__| | ,_/\` /",
		"    |____|____|_| |___/|_|____|____|.|_|  / /\t{}".format(color.RED+info[3]),
		"             {}Take a easier control       {}/_/\t{}By {}\n".format(color.BOLD+color.WHITE, color.BOLD+color.YELLOW, color.PURPLE, info[1]+color.END)
	]
	
	for txt in screen:
		print(txt)
		time.sleep(.1)

def listProject():
	def sort(content):
		for j, raw in enumerate(content):
			stick = W
			if(not j): stick = ""
			Label(panel[0], text=raw, font=["monospace", 8]).grid(row=i, column=j, padx=5, sticky=stick)
	
	global step
	prop = [
		"/var/www/html",
		['o', 'ko', 'Mo', 'Go', 'To']
	]
	
	print("{}> {}Listing Project in{} {}_".format(info[2], color.YELLOW, color.END, color.ITALIC+prop[0]+color.END))
	try: step.set("Analyse du répertoire de projets {}".format(prop[0]))
	except: """ """
	
	window = Tk()
	window.title("Liste des Projets")
	window.resizable(height=False, width=False)
	
	Label(window, text="{}/".format(prop[0]), font=["Ubuntu", 18]).grid(row=0, padx=15, pady=10, sticky=W)
	
	panel = [Frame(window)]
	panel[0].grid(row=1, column=0, pady=10)
	
	for i, txt in enumerate(['*', 'Name', 'Size', 'Type', 'Dernière MàJ']):
		Label(panel[0], text=txt, font=["Ubuntu", 10]).grid(row=0, column=i, padx=15)
	
	for i, txt in enumerate(os.listdir(prop[0])):
		path = "{}/{}".format(prop[0], txt)
		i += 1
		
		try:
			with open(path, "r") as content:
				ba = [0, len(content.read()), ""]
				content.close()
				
				while(ba[1] > 1000): ba = [ba[0] + 1, ba[1] / 1000.0, ""]
				if(txt in ['.htaccess', 'index.php', 'index.html']): ba[2] = "*"
				
				sort([ba[2], txt, "{} {}".format(ba[1], prop[1][ba[0]]), ".{}".format(txt.split('.')[1]), time.ctime(os.path.getctime(path))])
		except:
			ba = len(os.listdir(path))
			sort(["", "{}/".format(txt), "{} elements".format(ba), "folder", time.ctime(os.path.getctime(path))])
	
	scroll = Scrollbar(panel[0])
	scroll.grid(row=1, column=5, rowspan=i, sticky=NS)
	
	Label(window, text="{} Elements Trouvés".format(i), font=["Ubuntu Light", 8]).grid(row=2, column=0, padx=5, pady=2, sticky=E)
	print(" [ {}INFO{} ] - {} Elements found !\n".format(color.BLUE, color.END, i))
	Button(window, text="Fermer", font=["Ubuntu", 10], command=window.destroy).grid(row=2, column=0)
	
	window.mainloop()
	window.quit()

def edit(serv):
	def save():
		with open(path, "w") as config:
			config.write(area.get("1.0", END))
		
		check('Modification de {}'.format(msg[1]))
		window.destroy()
	
	if(serv == 'apache2'): msg = ['Apache2', 'apache2.conf']
	elif(serv == 'mysql'): msg = ['MySQL', 'my.cnf']
	elif(serv == 'tor'): msg = ['Tor', 'torsocks.conf']
	
	path = "/etc/{}/{}".format(serv, msg[1])
	print("{}> {}Editing {} configuration file{}_".format(info[2], color.YELLOW, msg[0], color.END))
	with open(path, "r") as content:
		content = content.read()
	
	window = Tk()
	window.title("Edition Configuration {}".format(msg[0]))
	window.resizable(height=FALSE, width=FALSE)
	
	panel = [Frame(window)]
	panel[0].grid(row=0, column=0)
	
	scroll = Scrollbar(panel[0])
	scroll.grid(row=0, column=1, pady=1, sticky=N+S)
	area = Text(panel[0], font=["Monospace", 9], height=40, width=81, wrap=WORD)
	area.insert(END, content)
	area.grid(row=0, column=0)
	area.config(yscrollcommand=scroll.set)
	scroll.config(command=area.yview)
	
	Button(window, text="Enregistrer", font=["Ubuntu", 10], command=lambda:save()).grid(row=1, column=0, sticky=E)
	Button(window, text="Fermer", font=["Ubuntu", 10], command=window.destroy).grid(row=1, column=0, sticky=W)
	
	window.mainloop()
	window.quit()

def viewLog(serv, log):
	global step
	
	print("{}> {}Show {} {} file{}_".format(info[2], color.YELLOW, serv, log, color.END))
	step.set("Affichage du fichier {} {}".format(serv, log))
	with open("/var/log/{}/{}".format(serv, log), "r") as content:
		content = content.read()
	
	window = Tk()
	window.title("Logs de {}".format(log))
	window.resizable(height=False, width=False)
	
	panel = [Frame(window)]
	panel[0].grid(row=0, column=0)
	
	scroll = Scrollbar(panel[0])
	scroll.grid(row=0, column=1, pady=1, sticky=N+S)
	area = Text(panel[0], font=["Monospace", 9], height=30, width=81, wrap=WORD)
	area.insert(END, content)
	area.grid(row=0, column=0)
	area.config(yscrollcommand=scroll.set)
	scroll.config(command=area.yview)
	
	Button(window, text="Fermer", font=["Ubuntu", 10], command=window.destroy).grid(row=1, column=0)
	
	window.mainloop()
	window.quit()

def shell():
	global step
	print("{}> {}Opening shell{}_".format(info[2], color.YELLOW, color.END))
	step.set("Ouverture du shell")
	
	window = Tk()
	window.title("{} Shell".format(info[2].capitalize()))
	window.resizable(height=False, width=False)
	
	panel = [Frame(window, height=330, width=560)]
	panel[0].grid(sticky="news")
	os.system("xterm -into {} -geometry 90x25 -sb &".format(panel[0].winfo_id()))
	
	window.mainloop()
	window.quit()

def about():
	print("{}> {}Show more info{}_".format(info[2], color.YELLOW, color.END))
	window = Tk()
	window.title("A propos de {}".format(info[2].capitalize()))
	window.resizable(width=FALSE, height=FALSE)
	
	panel = [Frame(window, bd=0)]
	panel[0].grid(row=0, column=0, padx=25, pady=30)
	Label(panel[0], text=info[2].capitalize(), font=['Ubuntu', 20]).grid(row=0, pady=20, sticky=W)
	madeLabel(panel[0], [
		"Ecrit le\t\t: {}".format(info[0][0]),
		"Mis à Jour le\t: {}".format(info[0][1]),
		"Version\t\t: {}".format(info[3]),
		"\nCe programme a été écrit en python",
		info[4]
	], ['Ubuntu', 11])
	Label(window, text="By {}".format(info[1]), font=['Ubuntu', 9]).grid(row=1, pady=5)
	
	window.mainloop()
	window.quit()

def helper():
	print("{}> {}Show helper{}_".format(info[2], color.YELLOW, color.END))
	window = Tk()
	window.title("{} Aide".format(info[2].capitalize()))
	Grid.rowconfigure(window, 0, weight=1)
	Grid.columnconfigure(window, 0, weight=1)
	
	Label(window, text="Aide aux fonctionnalités", font=['Ubuntu', 20]).grid(row=0, pady=20)
	
	article = [Frame(window), Frame(window)]
	
	article[0].grid(row=1, padx=20, pady=10, sticky=E+W)
	Label(article[0], text="Commande :", font=['Ubuntu', 14]).grid(row=0, pady=10, sticky=W)
	madeLabel(article[0], [
		"START\t : Démarre le service concerné",
		"STOP\t : Arrête le service concerné",
		"RESTART\t : Redémarre le service concerné\n",
		"CONFIG\t : Modifie le fichier de configuration du service concerné avec l'éditeur de texte local"
	], ['Ubuntu light', 10])
	
	article[1].grid(row=2, padx=20, pady=10, sticky=E+W)
	Label(article[1], text="Lancement :", font=['Ubuntu', 14]).grid(row=0, pady=10, sticky=W)
	madeLabel(article[1], helpArg, ['Monospace', 9])
	
	window.mainloop()
	window.quit()

def main():
	def theme():
		global skin
		
		if(not skin):
			skin = True
			ground = [dColor[0], dColor[1], dColor[2]]
		else:
			skin = False
			ground = ["#333333", "#CCCCCC", "#444444", "#CCCCCC"]
		
		window.config(bg=ground[0])
		menubar.config(bg=ground[0], fg=ground[1], activebackground=ground[2], activeforeground=ground[1])
		for i in range(0, len(menuContent)): menuContent[i][1].config(bg=ground[0], fg=ground[1], activebackground=ground[2], activeforeground=ground[1])
		for i in range(0, len(panel)):
			if(not i): panel[i].config(bg=ground[0], fg=ground[1])
			else: panel[i].config(bg=ground[0])
		for i in range(0, len(subpanel)): subpanel[i].config(bg=ground[0], fg=ground[1])
		for i in range(0, len(lbl)): lbl[i].config(bg=ground[0], fg=ground[1])
		for i in range(0, len(btn)): btn[i].config(bg=ground[0], fg=ground[1], activebackground=ground[2], activeforeground=ground[1])
		for i in range(0, len(button)):
			for j in range(0, len(button[i])):
				button[i][j].config(bg=ground[0], fg=ground[1], activebackground=ground[2], activeforeground=ground[1])
	
	global button, btn, label, lbl, step
	print("{}> {}Initializing IHM{}_".format(info[2], color.GREEN, color.END))
	
	window = Tk()
	window.title(info[2].capitalize())
	window.resizable(width=FALSE, height=FALSE)
	
	step = StringVar()
	
	""" Menu """
	menubar = Menu(window, bd=0)
	
	menuContent = [ # Contenu des Menus
		[ # Menu Principale
			'Fichier', Menu(menubar, tearoff=0),
			['Terminal', 'Quitter'],
			[lambda:shell(), window.quit]
		],
		[ # Menu Apache2
			'Serveur', Menu(menubar, tearoff=0),
			['Démarrer Apache2', 'Redémarrer Apache2', 'Arrêter Apache2', 'Configurer Apache2', 'Voir Access.log', 'Voir Error.log', 'Lister les Projets'],
			[lambda:serv('apache2', 1), lambda:serv('apache2', 2), lambda:serv('apache2', 0), lambda:edit('apache2'), lambda:viewLog('apache2', 'access.log'), lambda:viewLog('apache2', 'error.log'), listProject]
		],
		[ # Menu MySQL
			'Base de Données', Menu(menubar, tearoff=0),
			['Démarrer MySQL', 'Redémarrer MySQL', 'Arrêter MySQL', 'Configurer MySQL'],
			[lambda:serv('mysql', 1), lambda:serv('mysql', 2), lambda:serv('mysql', 0), lambda:edit('mysql')]
		],
		[ # Menu d'Information
			'Plus', Menu(menubar, tearoff=0),
			['Aide', 'A propos'],
			[helper, about]
		]
	]
	
	if(tor):
		menuContent.append(menuContent[len(menuContent)-1])
		menuContent[len(menuContent)-2] = [ # Menu Tor
			'Tor', Menu(menubar, tearoff=0),
			['Démarrer Tor', 'Redémarrer Tor', 'Arrêter Tor', 'Configurer Tor', 'Voir Tor.log'],
			[lambda:serv('tor', 1), lambda:serv('tor', 2), lambda:serv('tor', 0), lambda:edit('tor'), lambda:viewLog('tor', 'log')]
		]
	
	for i in range(0, len(menuContent)):
		for j, txt in enumerate(menuContent[i][2]):
			menuContent[i][1].add_command(label=txt, font=['Ubuntu Light', 10], command=menuContent[i][3][j])
			sep = [ # Contrôleur des séparateurs du menu
				(not i) and (not j),                                         # Fichier
				(i == 1) and (j in [2, 3, 5]),                               # Serveur
				(i == 2) and (j == 2),                                       # Base de Données
				tor and (i == 3) and (j in [2, 3]),                          # Tor
				(((not tor) and (i == 3)) or (tor and (i == 4))) and (not j) # Plus
			]
			if(True in sep): menuContent[i][1].add_separator()
		
		menubar.add_cascade(label=menuContent[i][0], font=['Ubuntu Light', 10], menu=menuContent[i][1])
	""" ---------------------------------------------------------------------------------- """
	
	logo = PhotoImage(file="{}/assets/python.png".format(info[6]))
	logo = logo.subsample(35)
	btn.append(Button(window, image=logo, command=theme))
	btn[len(btn)-1].grid(row=0, column=0, ipadx=4, ipady=4, padx=(7, 0), pady=8, sticky=W)
	lbl.append(Label(window, text=info[2].capitalize(), font=['Ubuntu', 20]))
	lbl[len(lbl)-1].grid(row=0, column=0, columnspan=2, padx=(60, 0), pady=8, sticky=W)
	
	panel = [
		LabelFrame(window, bd=1, relief=GROOVE, text=" General ", font=['Ubuntu Light', 12]),
		Frame(window, bd=1, relief=GROOVE),
		Frame(window)
	]
	
	""" General Control COMMAND """
	panel[0].grid(row=1, column=0, padx=8, pady=0, sticky=N)
	panelBtn = [lambda:servAll(1), lambda:servAll(0), lambda:servAll(2)]
	
	for i, txt in enumerate(['START', 'STOP', 'RESTART']):
		btn.append(Button(panel[0], text=txt, font=['Ubuntu', 9], command=panelBtn[i], width=8))
		btn[len(btn)-1].grid(row=i, column=0, padx=6, pady=4)
	""" ---------------------------------------------------------------------------------- """
	
	""" Main Panel """
	panel[1].grid(row=1, column=1, padx=8, pady=10)
	
	panelCtnt = [
		[" Apache2 ", " MySQL "],
		[
			[lambda:serv('apache2', 1), lambda:serv('apache2', 2), lambda:edit('apache2')],
			[lambda:serv('mysql', 1), lambda:serv('mysql', 2), lambda:edit('mysql')]
		]
	]
	
	if(tor):
		panelCtnt[0].append(' Tor ')
		panelCtnt[1].append([lambda:serv('tor', 1), lambda:serv('tor', 2), lambda:edit('tor')])
	
	for i, txt in enumerate(panelCtnt[0]):
		madePanel(panel[1], txt, i, panelCtnt[1][i])
	""" ---------------------------------------------------------------------------------- """
	
	""" Anex Panel """
	panel[2].grid(row=2, column=0, columnspan=2, padx=(3, 0), pady=6, sticky=W+E)
	
	btn.append(Button(panel[2], text="Terminal", font=['Ubuntu', 10], command=lambda:shell()))
	btn[len(btn)-1].grid(row=0, column=0, padx=4)
	btn.append(Button(panel[2], text="Lister les Projets", font=['Ubuntu', 10], command=listProject))
	btn[len(btn)-1].grid(row=0, column=1, padx=4)
	""" ---------------------------------------------------------------------------------- """
	btn.append(Button(window, text="Quitter", font=['Ubuntu', 10], command=window.quit))
	btn[len(btn)-1].grid(row=2, column=1, padx=(0, 7), sticky=E)
	
	lbl.append(Label(window, textvariable=step, font=['Monospace', 8]))
	lbl[len(lbl)-1].grid(row=3, column=0, columnspan=2, padx=2, sticky=W)
	
	print("{}> {}Checking of services launched{}_".format(info[2], color.YELLOW, color.END))
	funct = [lambda:serv(services[0], 0), lambda:serv(services[1], 0), lambda:serv(services[2], 0)]
	for i, txt in enumerate(services):
		if(not os.system("/etc/init.d/{} status".format(txt))):
			label[i].config(text='LANCER', bg="#00AA00")
			button[i][0].config(text='STOP', command=funct[i])
	
	dColor = [btn[0].cget('bg'), btn[0].cget('fg'), btn[0].cget('activebackground')]
	theme()
	
	step.set("Prêt")
	if(tor): step.set("[ Mode Tor ]")
	
	window.config(menu=menubar)
	window.mainloop()
	window.quit()
	
	print("{}> {}Quitting{}_".format(info[2], color.RED, color.END))

button, label, subpanel, btn, lbl = [], [], [], [], []
info = [
	['10 avr 2017', '16 fev 2019'],
	"Anarchy", "service.py", "v_0.0.8-a",
	"https://tracks12.github.io/service.py/",
	"Python {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]),
	os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
]

arg, helpArg, aboutUs = [
	["-h" in sys.argv, "-?" in sys.argv, "--help" in sys.argv],
	["-l" in sys.argv, "--list" in sys.argv],
	["-t" in sys.argv, "--tor" in sys.argv],
	["-v" in sys.argv, "--version" in sys.argv],
	["-a" in sys.argv, "--about" in sys.argv],
	["-c" in sys.argv, "--check" in sys.argv]
], [
	"python {}\n".format(info[2]),
	"Option         Option longue GNU       Description",
	"-a             --about                 A propos du soft",
	"-c             --check                 Vérifie l'existance des services Web",
	"-h, -?         --help                  Affiche ce message",
	"-l             --list                  Liste tous le repertoire du serveur",
	"-t             --tor                   Lancement en mod Tor",
	"-v             --version               Affiche la version du soft\n"
], [
	"{}".format(color.BOLD+color.YELLOW+info[2].capitalize()+color.END),
	"Running with {}\n".format(info[5]),
	"Writed\t\t: {}".format(info[0][0]),
	"Last Update\t: {}".format(info[0][1]),
	"Version\t: {}\n".format(color.BOLD+color.RED+info[3]+color.END),
	"This program was writed in python",
	"{}\n".format(color.YELLOW+info[4]+color.END),
	"{}By {}\n".format(color.BOLD+color.PURPLE, info[1]+color.END)
]

if(True in arg[0]):
	for txt in helpArg: print(" {}".format(txt))
elif(True in arg[1]): listProject()
elif(True in arg[3]): print(" {}\n".format(color.BOLD+color.RED+info[3]+color.END))
elif(True in arg[4]):
	for txt in aboutUs: print(" {}".format(txt))
elif(True in arg[5]): verify()
else:
	if(platform.system() != "Linux"): print(" [ {}ERROR{} ] - Operating system wasn't support\n".format(color.BOLD+color.RED, color.END))
	elif(os.environ["USER"] != "root"):
		sys.argv.append("")
		if(sys.version_info[0] == 2): prog = "python2"
		elif(sys.version_info[0] == 3): prog = "python3"
		os.system("sudo {} {}/{} {}".format(prog, info[6], info[2], sys.argv[1]))
	else:
		print("Launching with {}".format(info[5]))
		splash()
		print("{}> {}Load configuration file{}_".format(info[2], color.YELLOW, color.END))
		with open("{}/conf.json".format(info[6]), "r") as conf:
			conf = json.load(conf)
			prog, services, skin, tor = conf["prog"], conf["services"], conf["skin"], conf["tor"]
		if(True in arg[2] or tor):
			tor = True
			services.append(u'tor')
			print("{}> {}Tor mod enabled{}_".format(info[2], color.YELLOW, color.END))
		
		if(verify()): main()
		time.sleep(1)
		print("Bye :)\n")

"""
	-----
	 END
	-----
"""
