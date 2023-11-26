import os
import uuid
import datetime
import hashlib
import mimetypes
from lxml import etree
from xml.etree.ElementTree import QName



class EarkMaker:
    def __init__(self) -> None:
        print('Holy moly!')

    
    def createMets(self):
        allvalues = True
        # Skapar namespaces
        ns = {
        'xsi' :"http://www.w3.org/2001/XMLSchema-instance",
        'xlink': "http://www.w3.org/1999/xlink",
        'ext' : "ExtensionMETS",
        'sip': "https://DILCIS.eu/XML/METS/SIPExtensionMETS",
        'csip':"https://DILCIS.eu/XML/METS/CSIPExtensionMETS"
        }

        schemaLocation = str(QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"))

        # Skapar rotelementet
        rotelement = etree.Element('mets',attrib={'xmlns':'http://www.loc.gov/METS/'}, nsmap=ns)
        xmlFile = etree.ElementTree(rotelement)
        objID = f'IP_{str(uuid.uuid4())}'
        rotelement.set('OBJID', objID)
        if allvalues:
            rotelement.set('LABEL', 'VÄRDE')
        rotelement.set('TYPE', 'VÄRDELISTA')
        if allvalues:
            #Används vid othertype
            rotelement.set(str(QName(ns.get('csip'),'OTHERTYPE')),'ALTERNATIV INNEHÅLLSKATEGORI')
        rotelement.set('PROFILE', 'https://earksip.dilcis.eu/profile/E-ARK-SIP.xml')
        
        if allvalues:
            rotelement.set(str(QName(ns.get('csip'),'CONTENTINFORMATIONTYPE')),'INFORMATIONSTYPSSPECIFIKATION värdelista')
            rotelement.set(str(QName(ns.get('csip'),'OTHERCONTENTINFORMATIONTYPE')),'OM OTHER')

        
        # metsHdr
        metsHdr = etree.SubElement(rotelement, 'metsHdr')
        metsHdr.set('CREATEDATE', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        metsHdr.set('RECORDSTATUS', 'VÄRDELISTA')
        metsHdr.set(str(QName(ns.get('csip'),'OAISPACKAGETYPE')), 'SIP')

        #altRecordID Submissionagreement
        altRecordID = etree.SubElement(metsHdr, 'altrecordID')
        altRecordID.set('TYPE', 'SUBMISSIONAGREEMENT')
        altRecordID.text = 'LEVERANSÖVERENSKOMMELSEN'
        
        # altRecordID Previous submission agreement
        altRecordID = etree.SubElement(metsHdr, 'altrecordID')
        altRecordID.set('TYPE', 'PREVIOUSSUBMISSIONAGREEMENT')
        altRecordID.text = 'TIDIGARE'

        # altRecordID Previous submission agreement
        altRecordID = etree.SubElement(metsHdr, 'altrecordID')
        altRecordID.set('TYPE', 'REFERENCECODE')
        altRecordID.text = 'TIDIGARE arkivreferenskod'

         # altRecordID Previous submission agreement
        altRecordID = etree.SubElement(metsHdr, 'altrecordID')
        altRecordID.set('TYPE', 'PREVIOUSREFERENCECODE')
        altRecordID.text = 'TIDIGARE Refkod'

        # Agent Software som skapat paketet
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'CREATOR')
        agent.set('TYPE', 'OTHER')
        agent.set('OTHERTYPE', 'SOFTWARE')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'FGS Buddy'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'SOFTWARE VERSION')
        agentNote.text = 'VERSION'
        
        # Agent Arkivbildare 
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'ARCHIVIST')
        agent.set('TYPE', 'ORGANIZATION')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'ARKIVBILDAREN'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'IDENTIFICATIONCODE')
        agentNote.text = 'ORG:XXXXXX'

        # Leverantör - Den som skapat och står som leverantör för paketet
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'CREATOR')
        agent.set('TYPE', 'ORGANIZATION')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'LEVERERANDE ORGANISATION'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'IDENTIFICATIONCODE')
        agentNote.text = 'ORG:242424'

        # Kontaktperson
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'CREATOR')
        agent.set('TYPE', 'INDIVIDUAL')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'NAMNET'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.text = 'KONTAKTUPPGIFTER'

        # Mottagare 
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'PRESERVATION')
        agent.set('TYPE', 'ORGANIZATION')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'NAMN PÅ MOTTAGARE'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'IDENTIFICATIONCODE')
        agentNote.text = 'IDKOD'

        # Konsult
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'EDITOR')
        agent.set('TYPE', 'ORGANIZATION')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'KONSULTBOLAG'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'IDENTIFICATIONCODE')
        agentNote.text = 'IDKOD'

        # Ursprungssystem
        agent = etree.SubElement(metsHdr, 'agent')
        agent.set('ROLE', 'OTHER')
        agent.set('OTHERROLE', 'PRODUCER')
        agent.set('TYPE', 'OTHER')
        agent.set('OTHERTYPE', 'SOFTWARE')
        agentName = etree.SubElement(agent, 'name')
        agentName.text = 'SYSTEMNAMNET'
        agentNote = etree.SubElement(agent, 'Note')
        agentNote.set(str(QName(ns.get('csip'),'NOTETYPE')),'SOFTWARE VERSION')
        agentNote.text = 'VERSIONSNUMMER'

        # dmdSec Beskrivande metadata --> arkivredovisningsinformation etc
        # amdSec Administrativ metadata --> Bevarandemetadata etc
        # amdSec --> rightsMD rättigheter!

        # FILEGRP OCH FILESEC
        # fileSec
        fileSec = etree.SubElement(rotelement, 'fileSec')
        fileSec.set('ID', f'uuid-{str(uuid.uuid4())}')
        
        # filegroup --> Documentation
        fileGrp = etree.SubElement(fileSec, 'fileGrp')
        documentationUUID = str(uuid.uuid4())
        fileGrp.set('ID', f'uuid-{documentationUUID}')
        fileGrp.set('USE', 'Documentation')
        # FILER 
        
        ''' Additional package info
        if additionalpackageinfo:
            pass 
        '''
        # filegroup --> Scheman
        fileGrp = etree.SubElement(fileSec, 'fileGrp')
        fileGrp.set('ID', f'uuid-{str(uuid.uuid4())}')
        fileGrp.set('USE', 'Schemas')

        # filegroup --> Representations (DATA)
        fileGrp = etree.SubElement(fileSec, 'fileGrp')
        fileGrp.set('ID', f'uuid-{str(uuid.uuid4())}')
        fileGrp.set('USE', 'Representations')

        # StructMap
        structMap = etree.SubElement(rotelement, 'StructMap')
        structMap.set('TYPE', 'PHYSICAL')
        structMap.set('LABEL', 'CSIP')

        # DIV
        div = etree.SubElement(structMap, 'div')
        div.set('ID', f'uuid-{str(uuid.uuid4())}')

        # Underdivs





            

        xmlFile.write(f'METS.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
        #return xmlFile , objID
    
    def collectFiles(self, directory, category = 'representation', subdirectorys = True):
        filedict = {}
        if not os.path.exists(directory):
            print(f"Path doesn't exist {directory}")
            return 'Wrong path'
        
        # Skapar en dict med alla filnamn och deras sökväg
        for root, dirs, files in os.walk(directory):
            # Om endast huvudkatalogen ska ingå i paketet
            
            if subdirectorys == False:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[filePath] = filedict.get(f,{'path':filePath})
                    filedict[filePath]['fileName'] = f
                    filedict[filePath]['directory'] = directory
                    filedict[filePath]['category'] = category
                break
            
            # Om subdirectorys ska ingå i paketet
            if subdirectorys == True:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[filePath] = filedict.get(f,{'path':filePath})
                    filedict[filePath]['fileName'] = f
                    filedict[filePath]['directory'] = directory
                    filedict[filePath]['category'] = category      
        return filedict
    
    
    def collectMetadata(self, files):
        filedict = files
        for  k, v in filedict.items():
            # Samlar metadata
            filePathFromDict = filedict[k]['path']
            fileSize = str(os.stat(filePathFromDict).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(filePathFromDict).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(filePathFromDict)
            mimeType = mimetypes.guess_type(filePathFromDict)[0]
            originalFileName = filedict[k]['fileName']
            fgsFileName = str(originalFileName).replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_').replace('Å','A').replace('Ä','A').replace('Ö','O')
            fileuuid = f'uuid-{str(uuid.uuid4())}'
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            relativeFilePath = filePathFromDict.replace(filedict[k]['directory'],'').replace(originalFileName,'').replace('\\','/')
            fileLink = f'file:///Content{relativeFilePath}{fgsFileName}'
            

            # Lägger i dict           
            filedict[k]['filesize'] = fileSize
            filedict[k]['hashvalue'] = hashValue
            filedict[k]['createdate'] = createdDate
            filedict[k]['mimetype'] = mimeType
            filedict[k]['filelink'] = fileLink
            filedict[k]['originalfilename'] = originalFileName
            filedict[k]['fgsfilename'] = fgsFileName
            filedict[k]['relativefilepath'] = relativeFilePath
            #filedict[k]['category'] = 'content'
            filedict[k]['uuid'] = fileuuid
            print(filedict[k]['uuid'])

        
        return filedict
    
    # Code slightly modified from https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    def hashfunction(self, file):
        with open(file, "rb") as f:
            fileHash = hashlib.sha256()
            while bits := f.read(8192):
                fileHash.update(bits)
        hashValue = fileHash.hexdigest()
        f.close
        return hashValue

    
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
        
        #print(xmlFile[0])
        #xmlFile[0].write(f'{ipPath}/mets.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
        








if __name__ == '__main__':
    earkPackage = EarkMaker()
    metsfile = earkPackage.createMets()
    earkPackage.createEarkPackage(metsfile)
    dicten = earkPackage.collectFiles('C:\Viktor\Viktor_testar', 'schemas')
    #print(dicten)
    metadata = earkPackage.collectMetadata(dicten)
    print(metadata)