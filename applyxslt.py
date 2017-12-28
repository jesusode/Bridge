#Aplica una transformacion XSLT a un documento XML

import lxml.etree as ET

def applyXSLT(xml,xsl):
	dom = ET.parse(xml_filename)
	xslt = ET.parse(xsl_filename)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)
	return ET.tostring(newdom, pretty_print=True)