# -*- coding: utf-8 -*-
import sys, os
import urllib 
from urllib import urlencode, quote, unquote_plus
from urlparse import parse_qsl
import json
import xbmcgui
import xbmcplugin
import xbmc, xbmcaddon
import urllib


ADDON_ID      	= 'plugin.audio.lohro'
SETTINGS 		= xbmcaddon.Addon(id=ADDON_ID)
ADDON_PATH    	= SETTINGS.getAddonInfo('path')	# Basis-Pfad Addon

ICON_BLANK = 'blank.png'
ICON_LOHRO = 'icon.png'

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'music')


sendungenurl = 'https://produktion.lohro.de/api/v1/broadcasts?format=json'
sendungenresponse = urllib.urlopen(sendungenurl)
sendungenendlich = json.loads(sendungenresponse.read())


#############################
def PLog(msg, loglevel=xbmc.LOGDEBUG):
#	if DEBUG == 'false':
#		return
	if isinstance(msg, str):		# entf. mit six
		msg = msg.encode('utf-8')
	loglevel = xbmc.LOGNOTICE
	# PLog('loglevel: ' + str(loglevel))
	if loglevel >= 2:
		xbmc.log("%s --> %s" % ('mattipunkt', msg), level=loglevel)


def R(fname, abs_path=False):	
	PLog('R(fname): %s' % fname); # PLog(abs_path)
	# PLog("ADDON_PATH: " + ADDON_PATH)
	if abs_path:
		try:
			# fname = '%s/resources/%s' % (PluginAbsPath, fname)
			path = os.path.join(ADDON_PATH,fname)
			return path
		except Exception as exception:
			PLog(str(exception))
	else:
		if fname.endswith('png'):	# Icons im Unterordner images
			fname = '%s/resources/images/%s' % (ADDON_PATH, fname)
			fname = os.path.abspath(fname)
			# PLog("fname: " + fname)
			return os.path.join(fname)
		else:
			fname = "%s/resources/%s" % (ADDON_NAME, fname)
			fname = os.path.abspath(fname)
			return fname 

	

	
#def build_url(query):														# s. Main												
#   return base_url + '?' + urllib.urlencode(query)

def Menu():
	PLog("Menu")
	bitrate =  SETTINGS.getSetting('livestreambitrate')
	li = xbmcgui.ListItem('Livestream (%s)' % bitrate, thumbnailImage=ICON_LOHRO)
	if bitrate ==  '72kbit/s AAC':
		liveurl = 'http://stream.lohro.de:8000/lohro.aac.m3u'
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveurl, listitem=li)
	if bitrate ==  '128kbit/s MP3':
		liveurl = 'http://stream.lohro.de:8000/lohro_low.mp3.m3u'
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveurl, listitem=li)
	if bitrate ==  '192kbit/s MP3':
		liveurl = 'http://stream.lohro.de:8000/lohro.mp3.m3u'
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveurl, listitem=li)
	if bitrate ==  '256kbit/s OGG Opus':
		liveurl = 'http://stream.lohro.de:8000/lohro_opus.ogg.m3u'
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=liveurl, listitem=li)
	
	
	
	fparams="&fparams={}"									
	url = base_url + '?mode=Sendungen'+"&dirID=Sendungen"+quote(fparams) # Kurzform addDir
	li = xbmcgui.ListItem('Sendungen', thumbnailImage=ICON_BLANK)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	fparams="&fparams={}"
	url = base_url + '?mode=neustebeitraege'+"&dirID=neustebeitraege"+quote(fparams)
	li = xbmcgui.ListItem('Neueste Beiträge', thumbnailImage=ICON_BLANK)
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

# Folgende Anweisungen sind für Mediales, das aussehen soll wie ein Ordner.
#	link = "https://media.tagesschau.de/video/2020/1115/TV-20201115-1405-2700.webml.h264.mp4"
#	fparams="&fparams={'link': '%s'}" % quote(link)
#	url = base_url + '?mode=show_video'+"&dirID=show_video"+quote(fparams)
#	li = xbmcgui.ListItem('Zeige Video', thumbnailImage=ICON_BLANK)
#	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)		

def Sendungen():
	PLog("function Sendungen")
	global sendung
	if SETTINGS.getSetting('debugnotify') == 'true':
		for sendung in sendungenendlich['results']:
			#xbmcgui.Dialog().notification('Funktion wird gestartet!',sendung['title'],R(ICON_LOHRO),3000)
			fparams="&fparams={}"									
			url = base_url + '?mode=Sendung'+"&dirID=Sendung"+quote(fparams) # Kurzform addDir
			li = xbmcgui.ListItem(sendung['title'], thumbnailImage=ICON_BLANK)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

		xbmcplugin.endOfDirectory(addon_handle)
	

def neustebeitraege():
	PLog("function neuste beitraege")
	xbmcgui.Dialog().notification('Funktion wird gestartet!','Neuste Beiträge',R(ICON_LOHRO),3000)
	return

def show_video(link):
	PLog("function show_video")
	xbmc.Player().play(link)
	return

def Sendung():
	PLog("Sendung Funktioniert!")
	for sendung in sendungenendlich['results']:
		xbmcgui.Dialog().notification('Das hat funktioniert.','Die Sendung heisst %s' % sendung['title'])
	return
	
#############################
PLog('Routing')
paramstring = unquote_plus(sys.argv[2])				
PLog(paramstring)
if paramstring:
	params = dict(parse_qsl(paramstring[1:]))	
	PLog("params" + str(params))
	newfunc = params['dirID']

	PLog('router mode: ' + params['mode']) 				# ungenutzt, optionale Verwendung
	PLog('router dirID: ' + params['dirID'])			# enthält den Funktionsnamen
	PLog('router fparams: ' + params['fparams'])		# Parameter für die Funktion
		
	func_pars = params['fparams']
	PLog("func_pars " + str(func_pars))
	mydict = {}
	if func_pars:
		func_pars = func_pars.replace("'", "\"")		# json.loads-kompatible string-Rahmen
		func_pars = func_pars.replace('\\', '\\\\')		# json.loads-kompatible Windows-Pfade
		mydict = json.loads(func_pars)
	PLog(mydict)

	function = getattr(sys.modules[__name__], newfunc)
	function(**mydict)	
else:
	Menu()
	
	 

	

