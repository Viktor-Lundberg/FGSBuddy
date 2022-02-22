from dataclasses import replace
import os
from re import sub
from xml.etree.ElementTree import QName
from lxml import etree
import uuid
import datetime
import hashlib
import mimetypes
import shutil
import sys


cwd = os.getcwd()

fileFolder = cwd

class FgsMaker:
    def __init__(self):
        self.filedict = {}

    def createSip(self):
        filedict = self.filedict
        ns = {'mets' : 'http://www.loc.gov/METS/',
        'xsi' :"http://www.w3.org/2001/XMLSchema-instance",
        'xlink': "http://www.w3.org/1999/xlink",
        'ext' : "ExtensionMETS"}
        
        schemaLocation = str(QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation"))

        # Skapar rotelementet 'mets'
        rotelement = etree.Element(str(QName(ns.get('mets'),'mets')), nsmap=ns)
        xmlFile = etree.ElementTree(rotelement)
        rotelement.set(schemaLocation, 'http://www.loc.gov/METS/ http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd ExtensionMETS http://xml.ra.se/e-arkiv/METS/CSPackageExtensionMETS.xsd')
        rotelement.set('OBJID', str(uuid.uuid4()))
        rotelement.set('TYPE', 'Unstructured')
        rotelement.set('PROFILE', 'http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xml')
        
        # Skapar metsHdr
        metsHdr = etree.SubElement(rotelement, str(QName(ns.get('mets'),'metsHdr')))
        metsHdr.set('CREATEDATE', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        
        # Skapar agents
        agentArkivbildare = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentArkivbildare.set('ROLE', "ARCHIVIST")
        agentArkivbildare.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'name'))).text = 'INPUT! TESTARKIVBILDAREN' 
        identitetselement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'note'))).text = 'INPUT! UNIK KOD FÖR AB' 
        
        agentLevererandeSystem = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeSystem.set('ROLE', "ARCHIVIST")
        agentLevererandeSystem.set('TYPE', "OTHER")
        agentLevererandeSystem.set('OTHERTYPE', "SOFTWARE")
        namelement = etree.SubElement(agentLevererandeSystem, str(QName(ns.get('mets'), 'name'))).text = 'Filer på disk' 

        agentLevererandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeOrganisation.set('ROLE', "CREATOR")
        agentLevererandeOrganisation.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentLevererandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = 'INPUT LEVERERANDE ORG' 

        # Skapar altrecordID
        altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
        altRecordID.set('TYPE', 'SUBMISSIONAGREEMENT')
        altRecordID.text = 'INPUT! NÅGOT BRA DIARIENUMMER'
        
        # Skapar dmdSec
        #dmdSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'dmdSec')))

        #Filgrupper
        fileSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'fileSec')))
        fileGrp = etree.SubElement(fileSec, str(QName(ns.get('mets'), 'fileGrp')))
        
        #Filer använder värden i filedict som populerats via funktionen "collectFiles"
        for k, v in filedict.items():
            # Hoppar över filen om det är samma som pythonfilen som körs.
            if k == os.path.basename(sys.argv[0]):
                continue
            else:
                fileelement = etree.SubElement(fileGrp, str(QName(ns.get('mets'), 'file')))
                fileelement.set('ID', f'ID{str(uuid.uuid4())}')
                fileelement.set('MIMETYPE', filedict[k]['mimetype'])
                fileelement.set('SIZE', filedict[k]['filesize'])
                fileelement.set('CHECKSUM', filedict[k]['hashvalue'])
                fileelement.set('CREATED', filedict[k]['createdate'])
                fileelement.set('CHECKSUMTYPE', 'SHA-256')
                fileelement.set(str(QName(ns.get('ext'), 'ORIGINALFILENAME')),filedict[k]['originalfilename'])
                fLocat = etree.SubElement(fileelement, str(QName(ns.get('mets'), 'FLocat')))
                fLocat.set('LOCTYPE', 'URL')
                fLocat.set(str(QName(ns.get('xlink'),'type')),'simple')
                fLocat.set(str(QName(ns.get('xlink'),'href')),filedict[k]['filelink'])

        # Skapar structMap
        structMap = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'structMap')))
        structMap.set('LABEL', 'No structMap defined in this information package')
        divelement = etree.SubElement(structMap, str(QName(ns.get('mets'), 'div'))) 
                     
        # Skriver xml till sip.xml
        xmlFile.write(f'Sip.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
    
    def collectFiles(self, directory, subdirectorys=False):
        filedict = self.filedict
        
        # Skapar en dict med alla filnamn och deras sökväg
        for root, dirs, files in os.walk(directory):
            # Om 
            if subdirectorys == False:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[f] = filedict.get(f,{'path':filePath})
                    #print(filedict)
                break
        # OBS! LÄGG TILL KOD OM MAN VILL INKLUDERA SUBDIR
        
        # Samlar metadata om filerna och lägger till i dicten.
        for  k, v in filedict.items():
            # Samlar metadata
            filePathFromDict = filedict[k]['path']
            fileSize = str(os.stat(filePathFromDict).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(filePath).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(filePathFromDict)
            mimeType = mimetypes.guess_type(filePathFromDict)[0]
            originalFileName = k
            fgsFileName = str(originalFileName).lower().replace('å', 'a').replace('ä','a').replace('ö','o')
            fileLink = f'file:///Content/{fgsFileName}'

            
            # Lägger i dict           
            filedict[k]['filesize'] = fileSize
            filedict[k]['hashvalue'] = hashValue
            filedict[k]['createdate'] = createdDate
            filedict[k]['mimetype'] = mimeType
            filedict[k]['filelink'] = fileLink
            filedict[k]['originalfilename'] = originalFileName
            filedict[k]['fgsfilename'] = fgsFileName
            
            
            
    
    # Code slightly modified from https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    def hashfunction(self, file):
        with open(file, "rb") as f:
            fileHash = hashlib.sha256()
            while bits := f.read(8192):
                fileHash.update(bits)
        hashValue = fileHash.hexdigest()
        f.close
        return hashValue
    
    def createFgsPackage(self, directory):
        # Skapar paths och mappar för att kunna bygga FGS-paketet.
        directoryName = 'FGSpackage'
        parentDir = os.path.join(directory, directoryName)
        childDir = 'content'
        path = os.path.join(parentDir, childDir)
        os.makedirs(path, exist_ok=True)
        # kopierar sip.xml till paketet.
        sipPath = os.path.join(directory,'sip.xml')
        shutil.copy2(sipPath, parentDir)
        
        # Lägger paketets filer i contentmappen.
        filedict = self.filedict
        for k, v in filedict.items():
            if k == os.path.basename(sys.argv[0]):
                continue
            else:
                # Flyttar filen till contentkatalogen
                shutil.copy2(filedict[k]['path'], path)
                # Path till den flyttade filen
                newPath = os.path.join(path, k)
                # Fgs-namnet på filen (utan åäö + lower)
                fgsFileName = filedict[k]['fgsfilename']
                # skapar path för att kunna byta namn till fgsnamnet
                changePathName = os.path.join(path,fgsFileName)
                # Byter namn.
                try:
                    os.rename(newPath, changePathName)
                except:
                    print('!')
        shutil.make_archive('fgs','zip', parentDir)     

# Startar Skriptet
fgsPackage = FgsMaker()
fgsPackage.collectFiles(cwd)
fgsPackage.createSip()
fgsPackage.createFgsPackage(cwd)


#print(sys.argv[0])
#print(os.path.basename(sys.argv[0]))