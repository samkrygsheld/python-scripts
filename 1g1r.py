#!/usr/bin/python3

import re
import sys
from lxml import etree

def stringify_children(node):
    """Given a LXML tag, return contents as a string

       >>> html = "<p><strong>Sample sentence</strong> with tags.</p>"
       >>> node = lxml.html.fragment_fromstring(html)
       >>> extract_html_content(node)
       "<strong>Sample sentence</strong> with tags."
    """
    if node is None or (len(node) == 0 and not getattr(node, 'text', None)):
        return ""
    node.attrib.clear()
    opening_tag = len(node.tag) + 2
    closing_tag = -(len(node.tag) + 3)
    return etree.tostring(node)[opening_tag:closing_tag]

def load_database(dbpath):
    tree = etree.parse(dbpath)
    root = tree.getroot()

    # extract some useful information
#    games = root.findall('game')
#    clones = root.findall('game[@cloneof]')

    for clones in tree.xpath('game[@cloneof]'):
        if "USA" in stringify_children(clones).decode('utf-8'):
#            print (etree.tostring(clones.getparent().xpath('game[@cloneof]')))
            print (etree.tostring(clones).decode('utf-8'))
            pass
        else:
            clones.getparent().remove(clones)
    
    tree.write('output.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")

if __name__ == '__main__':
    load_database("test.dat")

