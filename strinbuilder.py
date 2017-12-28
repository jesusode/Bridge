#------------------------------------------------------------------------------
#Clase que envuelve un StringBuffer
#El contenido del buffer se obtiene con una llamada al mismo sin argumentos
#Para poner strings en el buffer se pude usar el operador +
# que admite un string o bien otro StringBuffer,
#o un llamada con tantos argumentos como se quieran meter en el buffer
#------------------------------------------------------------------------------ 
import cStringIO

class StringBuffer:
    def __init__(self,*vals):
        self._sb= cStringIO.StringIO()
        if vals!=(): 
            for item in vals:
                if type(item)==str:
                    self._sb.write(item)
                elif isinstance(item,StringBuffer):
                    self._sb.write(item._collect())
                else:
                    self._sb.write(str(item))
        self.__canCollect=True

    def _canCollect(self):
        return self.__canCollect

    def __add__(self,astr):
        if self._canCollect():
            if type(astr)==str:
                self._sb.write(astr)
            elif isinstance(astr,StringBuffer):
                self._sb.write(astr._collect())
            else:
                self._sb.write(str(astr))

    def __call__(self,*args):
        if args!=():
            for item in args:
                if type(item)==str:
                    self._sb.write(item)
                elif isinstance(item,StringBuffer):
                    self._sb.write(item._collect())
                else:
                    self._sb.write(str(item))
            return ""
        else:
            return self._collect()

    def _collect(self):
        if self._canCollect():
            self.__canCollect=False
            return self._sb.getvalue()
        else:
            raise Exception("Error: This StringBuffer has been collected yet!")

#---------------------------------------------------------------------------------------------------


if __name__=="__main__":
    sb= StringBuffer("abrimos con la ","linea uno")
    sb + "\nponme a la cola!"
    sb("\notra","\ny otra", StringBuffer("\ny otra mas ","por aqui\n"))
    sb(*["\cuatro "," cinco ","seis ","y siete\n"])
    for i in range(40):
        (sb + i) + "\n"
    print sb()