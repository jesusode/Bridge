#-----------------------------------------------------
#   GUI basica via Tk
#-----------------------------------------------------
import sys
#if 'win32' in sys.platform:
import os
#Basadas en EasyDialogs, easygui y hechas a medida---------------
import tkMessageBox
import tkColorChooser
import tkFileDialog
#from msgbox import *

import easygui_tuned as easygui
import threading
import idlelib
import tkFont
import Tkinter
import fontselect
#import Image as PILImage
#import ImageTk as PILImageTk    
#----------------------------------------------------------------    


def chooseDir(*args):
	if len(args)not in [1,2]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _chooseDir(title[,basedir])'''
		raise Exception(msg)
	basedir='/'
	if len(args)==2:
		basedir=args[1]
	root = Tkinter.Tk()
	root.withdraw()
	dirname = tkFileDialog.askdirectory(master=root,initialdir="/",title=args[0])
	root.destroy()
	return dirname

def fontDialog(*args):
	if len(args)!=0:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _fontDialog()'''
		raise Exception(msg)
	global fontpanel,font,root
	root = Tkinter.Tk()
	root.protocol('WM_DELETE_WINDOW', __denyWindowManagerClose )
	root.title('Font Dialog')
	root.minsize(400, 100)
	#Tuneado para poder poner un icono---------------------------
	if os.path.exists('icono.ico'):
		root.wm_iconbitmap('icono.ico')
	#------------------------------------------------------------    
	fontpanel=fontselect.FontSelect(root)
	fontpanel.pack()
	okFont  =  tkFont.Font (family="new century schoolbook", size="13" )
	okFont.configure ( weight=tkFont.BOLD )
	okButton  =  Tkinter.Button ( root,
		command=__fontdlgexit,
		font=okFont,
		text="OK" )
	okButton.pack()       
	root.mainloop()
	#Cambiar los False por 0
	if font:
		for key in font:
			if font[key]==False:
				font[key]=0
	return str(font)

def __fontdlgexit():
	global fontpanel,font,root
	font=fontpanel.get().actual()
	root.destroy()

def __denyWindowManagerClose():
	""" don't allow WindowManager close
	"""
	x = Tkinter.Tk()
	x.withdraw()
	x.destroy()    

def colorDialog(*args):
	if len(args)!=0:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _colorDialog()'''
		raise Exception(msg)
	root = Tkinter.Tk()
	root.withdraw()
	(rgb, hx) = tkColorChooser.askcolor()
	root.destroy()
	if not rgb:
		return ''
	else:
		return '#%02X%02X%02X'%(rgb[0],rgb[1],rgb[2])


	
def message(*args): #tkMessageBox
	'''
	Muestra un mensaje.
	Prototipo: message(mensaje,titulo[,icon])
	'''
	if len(args)not in [1,2,3]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _message(mensaje[,titulo,icono])'''
		raise Exception(msg)
	icons=['info','warning','error','question']
	msg=args[0]
	title='Minimal message'
	if len(args) >1:
		title=args[1]
	icon='info'
	type='ok'       
	if len(args)>2 and args[2] in icons:
		icon=args[2]
	return easygui.message(title,msg,type,icon)



	
def fileDialog(*args): #RECONSTRUIR
	if len(args) not in [3,4,5,6]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es:
		_fileDialog(mode,title,message,[,allowMultiple=0,type_list='All Files (*.*)|*.*',defaultPath='.'])'''
		raise Exception(msg)
	mode=args[0]
	title=args[1]
	message=args[2]
	allowMultiple=0
	if len(args)>=4 and int(args[3])==1: allowMultiple=1
	type_list='All Files (*.*)|*.*'
	defaultPath='.'
	
	files_selected=[]
	if allowMultiple==0:
		allowMultiple=None
	if message=='': message=None
	#----------------------------------------------------------------------------------

	#Cadena para _openFile: "All Files|*.*|Video Files(.avi)|.avi;.mpg".---------------------------------------------
	#Se parte por los pipes y debe tener un numero par de elementos.
	tlist=[]
	temp=type_list.split('|')
	#Colocar en tuplas de dos en dos los elementos
	numels=len(temp)/2
	cont=0
	for i in range(numels):
		tlist.append((temp[cont],temp[cont+1]))
		#Avanzar i 1 posicion
		cont+=2
	#------------------------------------------------------------------------------------------------------------------
	#print tlist
	
	if mode.lower() in ['open', 'o','op']: #Revisar opciones primero!!!!!
		files_selected=easygui.fileopenbox(title=title,msg=message,default=defaultPath)
		#Si se pulsa el boton cancel, files_selected es None-----------------------------------
		if files_selected==None:
			return ''
		else:
			return files_selected
	else: #No permitimos seleccion multiple para guardar un archivo!!
		ftype=('All Files (*.*)','*.*')
		if len(tlist)>=1:
			ftype=tlist[0]
		files_selected=easygui.fileopenbox(title=title,msg=message,default=defaultPath)
		#Si se pulsa el boton cancel, files_selected es None-----------------------------------
		if files_selected==None:
			return ''
		else:
			return files_selected
		 #--------------------------------------------------------------------------------------  



def guiButtonBox(*args):
	if len(args)not in [6,7,8]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiButtonBox(titulo,mensaje,list_options,codes_dicts,default_code,vert_align[,icon,image])'''
		raise Exception(msg)   
	options=args[2]
	code_dict=args[3]
	#Icono por defecto
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	image=None
	default=args[4]
	vert_align=int(args[5])
	if len(args)>=7:
		if args[6]: ico=args[6]
	if len(args)==8:
		image=args[7]
	return easygui.buttonbox(msg,title,options,image=image,icon=ico,vert=vert_align,code_opts=code_dict,noCode=0, default_code=default)

def guiMenuBox(*args):
	if len(args)not in [4,5,6]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiMenuBox(titulo,mensaje,list_options_name,vert_align[,icon,image])'''
		raise Exception(msg)
	options=args[2]
	#Icono por defecto
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	image=None
	vert_align=int(args[3])
	if len(args)>=5:
		if args[4]: ico=args[4]
	if len(args)==6:
		image=args[5]
	return easygui.buttonbox(msg,title,options,image=image,icon=ico,vert=vert_align,code_opts={},noCode=1)


def guiEnterBox(*args):
	if len(args)not in [4,5,6]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiEnterBox(titulo,mensaje,default,isPass[,icon,image])'''
		raise Exception(msg)
	default=args[2]
	if not default: default=''
	#Icono por defecto
	msg=args[1]
	title=args[0]
	if args[3]:
		ispass=1
	ico='icono.ico'
	image=None
	if len(args)>=5:
		if args[4]: ico=args[4]
	if len(args)==6:
		image=args[5]
	if args[3]!=1:
		return easygui.enterbox(msg,title,default,image=image,icon=ico)
	else:
		return easygui.passwordbox(msg,title,default,image=image,icon=ico)

def guiMultEnterBox(*args):
	if len(args)not in [4,5]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiEnterBox(titulo,mensaje,fields,values[,large_text])'''
		raise Exception(msg)
	#Icono por defecto
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	image=None
	large_text=0
	fields=args[2]
	values=args[3]
	if len(args)==5 and int(args[4])==1: large_text=1
	return easygui.multenterbox(msg,title,fields,values,icon=ico,large_text=large_text)


def guiYesNoBox(*args):
	if len(args)not in [2,3,4]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiYesNoBox(titulo,mensaje[,icon,image])'''
		raise Exception(msg)
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	image=None
	if len(args)>=3:
		if args[2]: ico=args[2]
	if len(args)==4:
		image=args[3]
	return easygui.ynbox(msg,title,image=image,icon=ico)

def guiCalendarBox(*args):
	if len(args)not in [4,5]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiCalendarBox(titulo,year,month,day[,ico])'''
		raise Exception(msg)
	title=args[0]
	ico='icono.ico'
	if len(args)>4:
		if args[4]: ico=args[4]
	return easygui.calendarbox(title,args[1],args[2],args[3],ico)


def guiListViewBox(*args):
	if len(args)not in [7,8]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiListViewBox(titulo,mensaje,cols_title_list,matrix,allow_multisel,allow_delete,allow_find[,icon])'''
		raise Exception(msg)       
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	titles=args[2]
	#print titles
	matrix=args[3]
	multi=int(args[4])
	delete=int(args[5])
	find=int(args[6])
	if len(args)==8:
		if args[7]: ico=args[7]
	return easygui.listview(msg,title,titles,matrix,multi,delete,find,icon=ico)


def guiImageBox(*args):
	if len(args)not in [3,4]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiImageBox(titulo,mensaje,image_list[,icon])'''
		raise Exception(msg)
	if type(args[2])==type([]) and not SYMTAB['__LISTS__'].has_key(args[2]):
		raise Exception('Excepcion: La lista %s no esta definida.' %args[2])
	msg=args[1]
	title=args[0]
	ico='icono.ico'
	images=SYMTAB['__LISTS__'][args[2]]
	if len(args)==4:
		if args[3]: ico=args[3]
	return easygui.imagebox(msg,title,images,icon=ico)



def guiGridViewBox(*args):
	if len(args)not in [3,4]:
		#gridview(title,colnames,rows_list,icon=None)
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiGridViewBox(titulo,cols_title_list,matrix_name,[,icon])'''
		raise Exception(msg)      
	title=args[0]
	ico='icono.ico'
	titles=args[1]
	matrix=args[2]
	if len(args)==4:
		if args[3]: ico=args[3]
	return easygui.gridview(title,titles,matrix,icon=ico)
	

def guiChoiceBox(*args):
	if len(args)not in [4,5,7]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiChoiceBox(titulo,mensaje,options_list,allow_multiple[,icon,width,height])'''
		raise Exception(msg)
	options=args[2]       
	msg=args[1]
	title=args[0]
	multiple=0
	width=300
	height=300
	if int(args[3])==1:
		multiple=1
	ico='icono.ico'
	ret=''
	if len(args)>=5:
		if args[4]: ico=args[4]
	if len(args)==7:
		width=args[5]
		height=args[6]
		if multiple:
			ret=easygui.multchoicebox(msg,title,options,icon=ico,width=width,height=height)
			if ret==None: return ''
			ret=','.join(ret)
			return ret
		else:
			ret=easygui.choicebox(msg,title,options,icon=ico,width=width,height=height)
			if ret==None: return ''
			return ret
	else:
		if multiple:
			ret=easygui.multchoicebox(msg,title,options,icon=ico,width=width,height=height)
			if ret==None: return ''
			ret=','.join(ret)            
			return ret
		else:
			ret=easygui.choicebox(msg,title,options,icon=ico)
			if ret==None: return ''
			return ret

def guiTextBox(*args):
	if len(args)not in [5,6,7,8,9,11]:
		msg='''Numero incorrecto de argumentos para la funcion.
		La sintaxis correcta es _guiTextBox(titulo,mensaje,texto,editable,showfiles[,font,color,bgcolor,icon,width,height_lines])'''
		raise Exception(msg)
	msg=args[1]
	title=args[0]
	text=args[2]
	editable=1
	if args[3]==0:
		editable=0
	ico='icono.ico'
	font=''
	color=None
	bgcolor=None
	width=None
	height=None
	show=int(args[4])
	if show!=0:
		show=1
	if len(args)>=6:
		#Puede ser una cadena o una lista(para fuentes que tengan un nombre con espacios)
		flist=args[5]
		for i in range(len(flist)):
			if type(flist[i]) in [type(1),type(1.0)]:
				flist[i]=int(flist[i])               
		font=tuple(flist)
	if len(args)>=7:
		color=args[6]
	if len(args)>=8:
		bgcolor=args[7]
	if len(args)>=9:
		ico=args[8]
	if len(args)==11:
		width=int(args[9])
		height=int(args[10])
	return easygui.textbox(msg,title,text,edit=editable,font=font,color=color,bgcolor=bgcolor,icon=ico,width=width,height=height,showfiles=show)    