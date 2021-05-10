import glob
import os.path
from MyCapytain.common.reference import URN
import lxml.etree as ET
from collections import namedtuple, Counter
import csv


BASE = """<TEI>
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title>Title</title>
         </titleStmt>
         <publicationStmt>
            <p>Publication Information</p>
         </publicationStmt>
         <sourceDesc>
            <p>Information about the source</p>
         </sourceDesc>
      </fileDesc>
  </teiHeader>
  <text>
      <body>
      </body>
  </text>
</TEI>"""
NewDocument = ET.fromstring(BASE)

# Treat XML
data = {}
body = NewDocument.xpath("//body")[0]

for filepath in sorted(glob.glob("data/*.xml"), key= lambda x: int(os.path.basename(x).replace(".xml", ""))):
    with open(filepath) as open_file:
        xml = ET.parse(open_file).getroot()

    body.append(xml)

data = ET.tostring(NewDocument, encoding=str).replace("<TEI>", '<TEI xmlns="http://www.tei-c.org/ns/1.0">')
with open("output.xml", "w") as output:
    output.write(data)
