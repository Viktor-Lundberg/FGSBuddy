import datetime
import hashlib
import mimetypes
import os
import shutil
import sys
import time
import uuid
from xml.etree.ElementTree import QName
from rich.progress import track
from rich.progress import Progress
from lxml import etree

cwd = os.getcwd()
print(cwd)
testfolder = os.path.join(cwd, 'Testis')
#fileFolder = cwd
print(testfolder)

class FgsMaker:
    def __init__(self):
        self.filedict = {}
        self.arkivbildare = ''
        self.arkivbildarkod = ''
        self.pathToFiles = ''

    def inputValues (self, values=False, debug = False):
        if debug:
            self.arkivbildare = 'TESTARKIVBILDAREN'
            self.arkivbildarkod = '12323213123'
            self.pathToFiles = testfolder
            self.organisation = 'TESTORGANISATIONEN'
            self.subfolders = True
            self.submissionagreement = '123456789'
            self.informationstyp = 'ERMS'
            self.system = 'Systemet'
        
        if not debug:
            self.arkivbildare = values['arkivbildare']
            self.arkivbildarkod = f'{values["IDkodtyp"]}:{values["IDkod"]}'
            self.submissionagreement =  values['submissionagreement']
            self.pathToFiles = values['folder']
            self.organisation = values['levererandeorganisation']
            self.recordstatus =values['recordstatus']
            self.informationstyp = values['informationstyp']
            self.system = values['system']



       
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
        rotelement.set('TYPE', self.informationstyp)
        rotelement.set('PROFILE', 'http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xml')
        
        # Skapar metsHdr
        metsHdr = etree.SubElement(rotelement, str(QName(ns.get('mets'),'metsHdr')))
        metsHdr.set('CREATEDATE', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        metsHdr.set(str(QName(ns.get('ext'),'OAISSTATUS')),'SIP')                                                     
        
        # Skapar agents
        agentArkivbildare = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentArkivbildare.set('ROLE', "ARCHIVIST")
        agentArkivbildare.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'name'))).text = self.arkivbildare
        identitetselement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'note'))).text = self.arkivbildarkod
        
        agentLevererandeSystem = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeSystem.set('ROLE', "ARCHIVIST")
        agentLevererandeSystem.set('TYPE', "OTHER")
        agentLevererandeSystem.set('OTHERTYPE', "SOFTWARE")
        namelement = etree.SubElement(agentLevererandeSystem, str(QName(ns.get('mets'), 'name'))).text = self.system 

        agentLevererandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeOrganisation.set('ROLE', "CREATOR")
        agentLevererandeOrganisation.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentLevererandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.organisation

        # Skapar altrecordID
        altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
        altRecordID.set('TYPE', 'SUBMISSIONAGREEMENT')
        altRecordID.text = self.submissionagreement
        
        # Skapar dmdSec
        #dmdSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'dmdSec')))

        #Filgrupper
        fileSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'fileSec')))
        fileGrp = etree.SubElement(fileSec, str(QName(ns.get('mets'), 'fileGrp')))
        
        #Filer använder värden i filedict som populerats via funktionen "collectFiles"
        for k, v in track(filedict.items(), 'Skapar Sip.xml'):
            # Hoppar över filen om det är samma som pythonfilen som körs samt ignorerar andra pythonfiler
            if k == os.path.basename(sys.argv[0]):
                continue
            else:
                fileelement = etree.SubElement(fileGrp, str(QName(ns.get('mets'), 'file')))
                fileelement.set('ID', f'ID{str(uuid.uuid4())}')
                 # Fångar upp fel på MIMETYPE
                try:
                    fileelement.set('MIMETYPE', filedict[k]['mimetype'])
                except:
                    fileelement.set('MIMETYPE', 'unknown mimetype')
                    
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
        xmlFile.write(f'sip.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
    
    def collectFiles(self, directory, subdirectorys=False, metadatafile=False):
        filedict = self.filedict
        # Kontrollerar att sökvägen är ok.
        if not os.path.exists(directory):
            print(f"Path doesn't existnnn {directory}")
            return 'Wrong path'
        
        # Skapar en dict med alla filnamn och deras sökväg
        for root, dirs, files in os.walk(directory):
            # Om endast huvudkatalogen ska ingå i paketet
            
            if subdirectorys == False:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[filePath] = filedict.get(f,{'path':filePath})
                    filedict[filePath]['fileName'] = f
                break
            
            # Om subdirectorys ska ingå i paketet
            if subdirectorys == True:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[filePath] = filedict.get(f,{'path':filePath})
                    filedict[filePath]['fileName'] = f
                    

        # Samlar metadata om filerna och lägger till i dicten. (Track används för att skapa "Progressbar")
        for  k, v in track(filedict.items(), description=f"Genererar metadata för filer"):
            # Samlar metadata
            #print(f'Genererar metadata för {k}')
            filePathFromDict = filedict[k]['path']
            fileSize = str(os.stat(filePathFromDict).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(filePathFromDict).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(filePathFromDict)
            mimeType = mimetypes.guess_type(filePathFromDict)[0]
            originalFileName = filedict[k]['fileName']
            fgsFileName = str(originalFileName).lower().replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            #relativeFilePath = filePathFromDict.replace(directory,'').replace(k,'').replace('\\','/')
            relativeFilePath = filePathFromDict.replace(directory,'').replace(originalFileName,'').replace('\\','/')
            print(filePathFromDict)
            print(f'detta är {relativeFilePath}')
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
            

        # METADATAFILE
        if metadatafile:
            metadatafilepath = os.path.join(metadatafile)
            print(metadatafilepath)
            fileSize = str(os.stat(metadatafilepath).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(metadatafilepath).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(metadatafilepath)
            mimeType = mimetypes.guess_type(metadatafilepath)[0]
            originalFileName = os.path.basename(metadatafilepath)
            #Ta bort lower om man vill att det ska fungera med filer som heter samma sak fast med stora/respektive små bokstäver......
            fgsFileName = str(originalFileName).lower().replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            print(f'Detta är directory {directory}')
            #relativeFilePath = metadatafilepath.replace(directory,'').replace(originalFileName,'').replace('\\','/')
            relativeFilePath = '/'
            
            fileLink = f'file:///{fgsFileName}'

            filedict[metadatafilepath] = filedict.get(metadatafilepath,{'path':metadatafilepath})

            
            # Lägger i dict           
            filedict[metadatafilepath]['filesize'] = fileSize
            filedict[metadatafilepath]['hashvalue'] = hashValue
            filedict[metadatafilepath]['createdate'] = createdDate
            filedict[metadatafilepath]['mimetype'] = mimeType
            filedict[metadatafilepath]['filelink'] = fileLink
            filedict[metadatafilepath]['originalfilename'] = originalFileName
            filedict[metadatafilepath]['fgsfilename'] = fgsFileName
            filedict[metadatafilepath]['relativefilepath'] = relativeFilePath
            filedict[metadatafilepath]['fileName'] = originalFileName
        for k, v in filedict.items():
            print(k, v)
            print(f'\n')    
            
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
        childDir = 'Content'
        path = os.path.join(parentDir, childDir)
        os.makedirs(path, exist_ok=True)
        # kopierar sip.xml till paketet.
        sipPath = os.path.join(directory,'sip.xml')
        shutil.copy2(sipPath, parentDir)
        
        # Lägger paketets filer i contentmappen (track används för att skapa "progressbar")
        filedict = self.filedict
        i = 0
        for k, v in track(filedict.items(), description="Preparerar FGS-paketet"):
            print(i)
            if k == os.path.basename(sys.argv[0]):
                continue
            else:
                # Tar fram den relativa sökvägen till filen genom att lägga ihop cwd + relativ path. Skapar katalog i FGSpackage om den inte finns.
                #print(f'Lägger till {k} i FGS-paketet')
                relativePackagePath = path + filedict[k]['relativefilepath']
                relativePackagePath = os.path.join(relativePackagePath)
                os.makedirs(os.path.dirname(relativePackagePath), exist_ok=True)
                # Kopierar från path till relativepackagePath
                shutil.copy2(filedict[k]['path'], relativePackagePath)
                # Ger filerna fgs-namn.
                newPath = os.path.join(relativePackagePath, filedict[k]['fileName'])
                fgsPath = os.path.join(relativePackagePath, filedict[k]['fgsfilename'])
                i+=1
                try:
                   os.rename(newPath, fgsPath)
                except Exception as e:
                   print(e)
                

        # Skapar zippen
        with Progress() as progress:
            task = progress.add_task('Skapar FGS-paket', total=4)
            progress.update(task, advance=10)
            packageTime = datetime.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
            progress.update(task, advance=15)
            shutil.make_archive(f'FGS_Package_{packageTime}','zip', parentDir)
            progress.update(task, advance=25)
            # Tar bort katalogen FGSpackage efter att den zippats.
            shutil.rmtree(parentDir)
            progress.update(task, advance=50)
        print(f'Paketet FGS_Package_{packageTime}.zip genererades i katalogen {cwd}')     

'''
# Startar Skriptet
fgsPackage = FgsMaker()
fgsPackage.inputValues(debug=True)
fgsPackage.collectFiles(fgsPackage.pathToFiles, fgsPackage.subfolders, False)
fgsPackage.createSip()
fgsPackage.createFgsPackage(cwd)
'''