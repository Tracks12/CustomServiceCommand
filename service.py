#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	----------------------
	 Autor   : Anarchy
	 Date    : 05/02/2019
	 Name    : service.py
	 Version : 0.0.6-a
	----------------------
"""

import os, platform, sys, time
try: from Tkinter import *
except: from tkinter import *

python = "Python {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
button, label, date = [], [], ['10 avr 2017', '5 fev 2019']
dev, name, tor, version = 'Anarchy', 'service.py', False, "v_0.0.6-a"

class color:
	BOLD	= '\033[1m'
	ITALIC	= '\033[3m'
	
	RED	= '\033[31m'
	GREEN	= '\033[32m'
	YELLOW	= '\033[33m'
	PURPLE	= '\033[35m'
	WHITE	= '\033[37m'
	
	END	= '\033[0m'

def madeButton(panel, act, r):
	global button
	button.append([])
	
	for i, txt in enumerate(['START', 'RESTART', 'CONFIG']):
		button[r].append(Button(panel, text=txt, font=['Ubuntu', 9], command=act[i], width=8, state=NORMAL))
		button[r][i].grid(row=i+1, column=0, padx=6, pady=4, sticky=W)

def madeLabel(panel, labels, _font):
	for i, txt in enumerate(labels):
		Label(panel, text=txt, font=_font).grid(row=i+1, column=0, pady=1, sticky=W)

def madePanel(panel, panelName, r, act):
	subpanel = LabelFrame(panel, bd=1, relief=GROOVE, text=panelName, font=['Ubuntu Light', 12])
	subpanel.grid(row=1, column=r, padx=8, pady=8)
	
	label.append(Label(subpanel, text="STOPPED", bg="#AA0000", fg="#000000", height=2, width=10))
	label[r].grid(row=0, column=0, padx=6, pady=4)
	madeButton(subpanel, act, r)

def edit(serv):	
	def save():
		file = open("/etc/{}".format(msg[1]), "w")
		file.write(area.get("1.0", END))
		file.close()
		
		check('Modification de {}'.format(msg[1]))
		config.destroy()
	
	if(serv == 'apache'): msg = ['Apache2', 'apache2/apache2.conf']
	elif(serv == 'mysql'): msg = ['MySQL', 'mysql/my.cnf']
	elif(serv == 'tor'): msg = ['Tor', 'tor/torsocks.conf']
	
	print("{}> {}Editing {} Configuration File{}_".format(name, color.YELLOW, msg[0], color.END))
	
	config = Tk()
	config.title("Edition Configuration {}".format(msg[0]))
	config.resizable(width=FALSE, height=FALSE)
	
	file = open("/etc/{}".format(msg[1]), "r")
	content = file.read()
	file.close()
	
	area = Text(config, font=["Monospace", 9], height=40, width=81, wrap=WORD)
	area.insert(END, content)
	area.grid(row=0, column=0)
	
	Button(config, text="Modifier", font=["Ubuntu", 10], command=lambda:save()).grid(row=1, column=0, sticky=E)
	Button(config, text="Annuler", font=["Ubuntu", 10], command=config.destroy).grid(row=1, column=0, sticky=W)
	
	config.mainloop()
	config.quit()

def viewLog(serv, log):
	if(serv == 'apache'): path = 'apache2/'
	elif(serv == 'tor'): path = 'tor/'
	
	os.system("cat /var/log/{}{}".format(path, log))

def serv(s, x):
	global button
	
	if(s == 'apache'): msg = ['Serveur Apache', 'apache2', 0]
	elif(s == 'mysql'): msg = ['Base de données MySQL', 'mysql', 1]
	elif(s == 'tor'): msg = ['Service Tor', 'tor', 2]
	
	if(x == 1):
		line = ['start', '{} lancer'.format(msg[0])]
		label[msg[2]].config(text='LAUNCHED', bg="#00AA00")
		button[msg[2]][0].config(text='STOP', command=lambda:serv(s, 0))
	
	elif(x == 2):
		line = ['restart', '{} relancer'.format(msg[0])]
		label[msg[2]].config(text='LAUNCHED', bg="#00AA00")
	elif(x == 0):
		line = ['stop', '{} arrêter'.format(msg[0])]
		label[msg[2]].config(text='STOPPED', bg="#AA0000")
		button[msg[2]][0].config(text='START', command=lambda:serv(s, 1))
	
	os.system("sudo /etc/init.d/{} {}".format(msg[1], line[0]))
	check(line[1])

def servAll(x):
	serv('apache', x)
	serv('mysql', x)
	if(tor): serv('tor', x)

def check(act):
	global step
	step.set(act)
	print(" [ {}{}FINISHED{} ]".format(color.BOLD, color.GREEN, color.END))

def listProject():
	info = ["/var/www/html", ""]
	
	print("{}> {}Listing Project in {}{}{}{}\n".format(name, color.YELLOW, color.END, color.ITALIC, info[0], color.END))
	for txt in os.listdir(info[0]):
		typeMsg = ["" ,""]
		
		if("." in txt): typeMsg[0] += color.PURPLE;
		else: typeMsg = [color.BOLD+color.GREEN, "/"]
		
		if(txt in ["index.php", "index.html"]): typeMsg = [color.BOLD+color.PURPLE, " <- Index File"]
		elif(txt == ".htaccess"): typeMsg = [color.BOLD+color.YELLOW, " <- Apache Configuration File"]
		
		info[1] += "\t./{}{}{}{}\n".format(typeMsg[0], txt, color.END, typeMsg[1])
	
	print(info[1])

def verify():
	checked, DIR, services, stop = [], os.listdir('/etc/init.d/'), ['apache2', 'mysql', 'tor'], False
	
	time.sleep(.5)
	print("{}> {}Checking installed services{}_".format(name, color.YELLOW, color.END))
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
		"\n{}{}     ____               O             ___".format(color.BOLD, color.YELLOW),
		"    | ___|----.---,-.--.-.----.----. | _ \_ __",
		"    |___ | -__| .-| |  | |  __| -__| | ,_/\` /",
		"    |____|____|_| |___/|_|____|____|.|_|  / /\t{}{}".format(color.RED, version),
		"             {}Take a easier control       {}{}/_/\t{}By {}{}\n".format(color.BOLD + color.WHITE, color.BOLD, color.YELLOW, color.PURPLE, dev, color.END)
	]
	
	for txt in screen:
		print(txt)
		time.sleep(.1)
	
	time.sleep(.5)

def about():
	print("{}> {}Show more info{}_".format(name, color.YELLOW, color.END))
	aboutus = Tk()
	aboutus.title('A Propos')
	aboutus.resizable(width=FALSE, height=FALSE)
	
	content = Frame(aboutus, bd=0)
	content.grid(row=0, column=0, padx=25, pady=30)
	Label(content, text=name.capitalize(), font=['Ubuntu', 20]).grid(row=0, pady=20, sticky=W)
	madeLabel(content, [
		"Ecrit le\t\t: {}".format(date[0]),
		"Mis à Jour le\t: {}".format(date[1]),
		"Version\t\t: {}".format(version),
		"\nCe programme a été écrit en python",
		"https://tracks12.github.io/service.py/"
	], ['Ubuntu', 11])
	Label(aboutus, text=dev, font=['Ubuntu', 9]).grid(row=1, pady=5)
	
	aboutus.mainloop()
	aboutus.quit()

def helper():
	print("{}> {}Show helper{}_".format(name, color.YELLOW, color.END))
	helper = Tk()
	helper.title('Aide')
	
	Label(helper, text="Aide aux fonctionnalités", font=['Ubuntu', 20]).grid(row=0, pady=20)
	
	article = [Frame(helper), Frame(helper)]
	
	article[0].grid(row=1, padx=20, pady=10, sticky=W)
	Label(article[0], text="Commande :", font=['Ubuntu', 14]).grid(row=0, pady=10, sticky=W)
	madeLabel(article[0], [
		"START\t : Démarre le service concerné",
		"STOP\t : Arrête le service concerné",
		"RESTART\t : Redémarre le service concerné",
		"CONFIG\t : Modifie le fichier de configuration du service concerné avec l'éditeur de texte local"
	], ['Ubuntu light', 10])
	
	article[1].grid(row=2, padx=20, pady=10, sticky=W)
	Label(article[1], text="Lancement :", font=['Ubuntu', 14]).grid(row=0, pady=10, sticky=W)
	madeLabel(article[1], helpArg, ['Monospace', 9])
	
	helper.mainloop()
	helper.quit()

def main():
	global name, step, tor, version
	print("{}> {}Initializing IHM{}_".format(name, color.GREEN, color.END))
	
	window = Tk()
	window.title(name.capitalize())
	window.resizable(width=FALSE, height=FALSE)
	
	step = StringVar()
	
	""" Menu """
	menubar = Menu(window, bd=0)
	
	menuContent = [
		[ # Menu Principale
			'Fichier', Menu(menubar, tearoff=0),
			['Quitter'],
			[window.quit]
		],
		[ # Menu Apache2
			'Serveur', Menu(menubar, tearoff=0),
			['Démarrer Apache2', 'Redémarrer Apache2', 'Arrêter Apache2', 'Configurer Apache2', 'Voir Access.log', 'Voir Error.log', 'Lister les Projets'],
			[lambda:serv('apache', 1), lambda:serv('apache', 2), lambda:serv('apache', 0), lambda:edit('apache'), lambda:viewLog('apache', 'access.log'), lambda:viewLog('apache', 'error.log'), listProject]
		],
		[ # Menu MySQL
			'Base de Données', Menu(menubar, tearoff=0),
			['Démarrer MySQL', 'Redémarrer MySQL', 'Arrêter MySQL', 'Configurer MySQL'],
			[lambda:serv('mysql', 1), lambda:serv('mysql', 2), lambda:serv('mysql', 0), lambda:edit('mysql')]
		],
		[ # Menu d'Information
			'Plus', Menu(menubar, tearoff=0),
			['Aide', 'A propos du soft'],
			[helper, about]
		]
	]
	
	if(tor):
		menuContent.append([])
		menuContent[len(menuContent)-1] = menuContent[len(menuContent)-2]
		menuContent[len(menuContent)-2] = [ # Menu Tor
			'Tor', Menu(menubar, tearoff=0),
			['Démarrer Tor', 'Redémarrer Tor', 'Arrêter Tor', 'Configurer Tor', 'Voir Tor.log'],
			[lambda:serv('tor', 1), lambda:serv('tor', 2), lambda:serv('tor', 0), lambda:edit('tor'), lambda:viewLog('tor', 'log')]
		]
	
	for i in range(0, len(menuContent)):
		for j, txt in enumerate(menuContent[i][2]):
			menuContent[i][1].add_command(label=txt, font=['Ubuntu Light', 10], command=menuContent[i][3][j])
			if(True in [(i == 1) and (j in [2, 3, 5]), (i == 2) and (j == 2), tor and (i == 3) and (j in [2, 3])]):
				menuContent[i][1].add_separator()
		
		menubar.add_cascade(label=menuContent[i][0], font=['Ubuntu Light', 10], menu=menuContent[i][1])
	""" ---------------------------------------------------------------------------------- """
	
	Label(window, text=name.capitalize(), font=['Ubuntu', 20]).grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky=W)
	
	panel = [
		LabelFrame(window, bd=1, relief=GROOVE, text="General", font=['Ubuntu Light', 12]),
		Frame(window, bd=1, relief=GROOVE)
	]
	
	""" General Control COMMAND """
	panel[0].grid(row=1, column=0, padx=8, pady=8)
	Button(panel[0], text='START', font=['Ubuntu', 9], command=lambda:servAll(1), width=8).grid(row=0, column=0, padx=6, pady=4, sticky=W)
	Button(panel[0], text='STOP', font=['Ubuntu', 9], command=lambda:servAll(0), width=8).grid(row=1, column=0, padx=6, pady=4, sticky=W)
	Button(panel[0], text='RESTART', font=['Ubuntu', 9], command=lambda:servAll(2), width=8).grid(row=2, column=0, padx=6, pady=4, sticky=W)
	""" ---------------------------------------------------------------------------------- """
	
	""" Main Panel """
	panel[1].grid(row=1, column=1, padx=8, pady=8)
	
	# Apache2 Service COMMAND
	madePanel(panel[1], "Apache2", 0, [lambda:serv('apache', 1), lambda:serv('apache', 2), lambda:edit('apache')])
	
	# MySQL Service COMMAND
	madePanel(panel[1], "MySQL", 1, [lambda:serv('mysql', 1), lambda:serv('mysql', 2), lambda:edit('mysql')])
	
	# Tor Service COMMAND
	if(tor): madePanel(panel[1], "Tor", 2, [lambda:serv('tor', 1), lambda:serv('tor', 2), lambda:edit('tor')])
	""" ---------------------------------------------------------------------------------- """
	
	Button(window, text="Lister les Projets", font=['Ubuntu', 10], command=listProject).grid(row=2, column=0, padx=8, pady=8)
	Button(window, text="Quitter", font=['Ubuntu', 10], command=window.quit).grid(row=2, column=1, padx=8, pady=8, sticky=E)
	Label(window, textvariable=step, font=['Monospace', 8]).grid(row=3, column=0, columnspan=2, padx=5, sticky=W)
	
	servAll(1)
	step.set("Lancement avec {} Prêt".format(python))
	
	window.config(menu=menubar)
	window.mainloop()
	window.quit()
	
	print("{}> {}Quitting{}_".format(name, color.RED, color.END))

arg, helpArg, aboutUs = [
	["-h" in sys.argv, "-?" in sys.argv, "--help" in sys.argv],
	["-l" in sys.argv, "--list" in sys.argv],
	["-t" in sys.argv, "--tor" in sys.argv],
	["-v" in sys.argv, "--version" in sys.argv],
	["-a" in sys.argv, "--about" in sys.argv],
	["-c" in sys.argv, "--check" in sys.argv]
], [
	" python {}\n".format(name),
	" Option         Option longue GNU       Description",
	" -a             --about                 A propos du soft",
	" -c             --check                 Vérifie l'existance des services Web",
	" -h, -?         --help                  Affiche ce message",
	" -l             --list                  Liste tous le repertoire du serveur",
	" -t             --tor                   Lancement en mod Tor",
	" -v             --version               Affiche la version du soft\n"
], [
	" {}{}{}{}".format(color.BOLD, color.YELLOW, name.capitalize(), color.END),
	" Running with {}".format(python),
	"\n Writed\t\t: {}".format(date[0]),
	" Last Update\t: {}".format(date[1]),
	" Version\t: {}{}{}{}".format(color.BOLD, color.RED, version, color.END),
	"\n This program was writed in python",
	" {}https://tracks12.github.io/service.py/{}".format(color.YELLOW, color.END),
	"\n {}\n".format(dev)
]

if(True in arg[0]):
	for txt in helpArg: print(txt)

elif(True in arg[1]): listProject()
elif(True in arg[3]): print(" {}{}{}{}\n".format(color.BOLD, color.RED, version, color.END))
elif(True in arg[4]):
	for txt in aboutUs: print(txt)

elif(True in arg[5]): verify()
else:
	if((platform.system() == "Linux") and (os.environ["USER"] == "root")):
		print("Launching with {}".format(python))
		splash()
		if(verify()):
			if(True in arg[2]):
				tor = True
				print("{}> {}Tor mod enabled{}_".format(name, color.YELLOW, color.END))
			main()
		print("Bye :)\n")
	
	elif(os.environ["USER"] != "root"): os.system("sudo python service.py {}".format(sys.argv[1]))
	elif(platform.system() != "Linux"): print(" [ {}{}ERROR{} ] - Operating System wasn't support\n".format(color.BOLD, color.RED, color.END))

# -----
#  END
# -----
