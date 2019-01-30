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


Metadata = namedtuple("Metadata", ["author", "title"])
Passage = namedtuple("Passage", ["author", "title", "passage"])

UnrecognizedDataInCsv = []
Registrar = {
    "urn:cts:greekLit:tlg0527.tlg048": Metadata("Vulgate", "Isaiah")
}
# Treat CSV
with open("Authors-Abbreviation-Editions - Latin Authors.csv") as csv_file:
    reader = csv.DictReader(csv_file)
    Nones = ["NONE", "", "N.A.", "NOE", "ONE"]

    for row in reader:
        stoa, phi, other_identifier = row["STOA#"].strip(), row["PHI#"].strip(), row["Other identifier"].strip()
        if phi.upper() not in Nones and "." in phi:
            identifier = "urn:cts:latinLit:phi{0:0>4}.phi{1:0>3}".format(*tuple(phi.split(".")))
        elif "-" in stoa:
            if stoa == "stoa0045-stoa0024":
                stoa = "stoa0045-stoa024"
            identifier = "urn:cts:latinLit:{0}.{1}".format(*tuple(stoa.split("-")))

        elif other_identifier not in Nones:
            identifier = other_identifier
        else:
            UnrecognizedDataInCsv.append(row)
            pass
        Registrar[identifier] = Metadata(
            author=row["LC NAME/TITLE or VIAF AUTHOR NAME"].strip().split(" ca.")[0],
            title=row["WORK TITLE"].strip()
        )

# Treat XML
data = {}
for filepath in sorted(glob.glob("data/*.xml"), key= lambda x: int(os.path.basename(x).replace(".xml", ""))):
    with open(filepath) as open_file:
        xml = ET.parse(open_file).getroot()

    source = xml.xpath("//quote/@source[1]")[0]
    try:
        urn = URN(source)
        metadata = Passage(*Registrar[str(urn.upTo(URN.WORK))], urn.reference)
    except Exception as E:
        if source == "AnthLati:382.2":
            metadata = Passage(None, "Anthologie Latine", "382.2")
        elif source == "Hist Apoll Try 34":
            metadata = Passage(None, "Hist Apoll Try", "34")
        elif source == "Mulomedicina Chironis 681":
            metadata = Passage(None, "Mulomedicina Chironis", "681")
        elif source == "Mul. Chir. 177":
            metadata = Passage(None, "Mulomedicina Chironis", "177")
        elif source == "Mulomedicina Chironis 731":
            metadata = Passage(None, "Mulomedicina Chironis", "731")
        elif source == "Mulomedicina Chironis 681":
            metadata = Passage(None, "Mulomedicina Chironis", "681")
        else:
            print(" ".join(xml.xpath("//w/text()")))
            raise E
    bibl = ET.Element("bibl")
    if metadata.author:
        author = ET.Element("author")
        author.text = metadata.author
        bibl.append(author)

    title = ET.Element("title")
    title.text = metadata.title
    bibl.append(title)

    citedRange = ET.Element("citedRange")
    citedRange.text = str(metadata.passage)
    bibl.append(citedRange)

    xml.insert(0, bibl)

    NewDocument.xpath("//body")[0].append(xml)

data = ET.tostring(NewDocument, encoding=str).replace("<TEI>", '<TEI xmlns="http://www.tei-c.org/ns/1.0">')
with open("output.xml", "w") as output:
    output.write(data)
