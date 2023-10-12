import os
from lxml import etree
from xml.etree.ElementTree import QName


class EarkMaker:
    def __init__(self) -> None:
        print('Holy moly!')

    
    def createMets(self):
        ns = {
        'xsi' :"http://www.w3.org/2001/XMLSchema-instance",
        'xlink': "http://www.w3.org/1999/xlink",
        'ext' : "ExtensionMETS",
        'sip': "https://DILCIS.eu/XML/METS/SIPExtensionMETS",
        'csip':"https://DILCIS.eu/XML/METS/CSIPExtensionMETS"
        }

        schemaLocation = str(QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"))

        rotelement = etree.Element('mets',attrib={'xmlns':'http://www.loc.gov/METS/'}, nsmap=ns)
        xmlFile = etree.ElementTree(rotelement)
        
        xmlFile.write(f'mets.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
        #return xmlFile
    
    def collectFiles(self):
        pass

    def createEarkPackage(self, xmlFile):
        directoryName = 'IP_x/IP_x'
        cwd = os.getcwd()
        ipPath = os.path.join(cwd, directoryName)
        os.makedirs(ipPath, exist_ok=True)

        # Sökväg för doumentation
        documentationDir = 'documentation'
        documentationDirPath = os.path.join(ipPath, documentationDir)
        os.makedirs(documentationDirPath, exist_ok=True)

        # Sökväg för metadata/ 1. descriptive 2. other 3. preservation
        descriptiveMetadataDir = 'metadata/descriptive'
        otherMetadataDir = 'metadata/other'
        preservationMetadataDir = 'metadata/preservation'

        descriptiveMetadataPath = os.path.join(ipPath, descriptiveMetadataDir)
        otherMetadataPath = os.path.join(ipPath, otherMetadataDir)
        preservationMetadataPath = os.path.join(ipPath, preservationMetadataDir)

        os.makedirs(descriptiveMetadataPath, exist_ok=True)
        os.makedirs(otherMetadataPath, exist_ok=True)
        os.makedirs(preservationMetadataPath, exist_ok=True)

        # Sökväg representations/rep_1/data
        dataDir = 'representations/rep_1/data'
        dataDirPath = os.path.join(ipPath, dataDir)
        os.makedirs(dataDirPath, exist_ok=True)

        # sökväg schemas
        schemasDir = 'schemas'
        schemasDirPath = os.path.join(ipPath, schemasDir)
        os.makedirs(schemasDirPath, exist_ok=True)
        
        #xmlFile.write(f'{ipPath}/mets.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
        








if __name__ == '__main__':
    earkPackage = EarkMaker()
    metsfile = earkPackage.createMets()
    #earkPackage.createEarkPackage(metsfile)