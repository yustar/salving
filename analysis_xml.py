#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
parse xml document
"""

from xml.etree import ElementTree

class XmlParse:
    
    _elem = None
    
    def __init__(self, file):
        self._elem = ElementTree.parse(file)
        
    def parse(self):
		"""parse xml document"""
		return None
                                    
                        
def Xml(file):
    xml = XmlParse(file)
    res = xml.parse()
    return res
