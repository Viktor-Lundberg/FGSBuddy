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

#fileFolder = cwd

class FgsMaker:
    def __init__(self):
        self.filedict = {}
        self.arkivbildare = ''
        self.arkivbildarkod = ''
        self.pathToFiles = ''

    def inputValues (self, debug = False):
        if debug:
            self.arkivbildare = 'TESTARKIVBILDAREN'
            self.arkivbildarkod = '12323213123'
            self.pathToFiles = cwd
            self.organisation = 'TESTORGANISATIONEN'
            self.subfolders = False
            self.diarienummer = '123456789'
        else:
            self.arkivbildare = input('Ange vilken Arkivbildare FGS-paketet avser\n> ')
            self.organisation = input('Ange vilken organisation/myndighet som levererar FGS-paketet\n> ')

            loopChecker = True
            while loopChecker:
                idChecker = input('1. Generera diarienummer för leveransen\n2. Ange ett diarienummer för leveransen\n3. Avsluta\n> ')
                if idChecker == '1':
                    self.diarienummer = str(uuid.uuid4())
                    loopChecker = False
                elif idChecker == '2':
                    self.diarienummer = input('Skriv in diarienummer\n> ')
                    loopChecker = False
                elif idChecker == '3':
                    return 'No Values!'
                else:
                    'Felaktig inmatning' 
         
            loopChecker = True
            while loopChecker:
                idChecker = input('1. Generera arkivbildarkod\n2. Skriv in arkivbildarkoden\n3. Avsluta\n ')
                if idChecker == '1':
                    self.arkivbildarkod = str(uuid.uuid4())
                    loopChecker = False
                elif idChecker == '2':
                    self.arkivbildarkod = input('Skriv in arkivbildarkoden\n> ')
                    loopChecker = False
                elif idChecker == '3':
                    return 'No Values!'
                else:
                    'Felaktig inmatning' 
            
            loopChecker = True
            while loopChecker:
                print('Från vilken mapp ska man genera ett FGS-paket?')
                pathChecker = input('1. Samma katalog som skriptet\n2. Annan katalog\n3. Avsluta\n ')
                if pathChecker == '1':
                    self.pathToFiles = cwd
                    loopChecker = False
                elif pathChecker == '2':
                    self.pathToFiles = input('Skriv in sökväg till katalogen\n>')
                    print(self.pathToFiles)
                    self.pathToFiles.strip()
                    print(self.pathToFiles)
                    if os.path.exists(self.pathToFiles):
                        print(self.pathToFiles)
                        loopChecker = False
                    else:
                        print('Felaktig sökväg')
                elif pathChecker == '3':
                    return 'No Values!'
                else:
                    'Felaktig inmatning'
            
            loopChecker = True
            subfolders = input('Ska även underkataloger inkluderas i FGS-paketet?\n 1. Nej 2. Ja\n>')
            while loopChecker:
                if subfolders == '1':
                    self.subfolders = False
                    loopChecker = False
                elif subfolders == '2':
                    self.subfolders = True
                    loopChecker = False
                else:
                    continue    
            loopChecker = True

 
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
        namelement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'name'))).text = self.arkivbildare
        identitetselement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'note'))).text = self.arkivbildarkod
        
        agentLevererandeSystem = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeSystem.set('ROLE', "ARCHIVIST")
        agentLevererandeSystem.set('TYPE', "OTHER")
        agentLevererandeSystem.set('OTHERTYPE', "SOFTWARE")
        namelement = etree.SubElement(agentLevererandeSystem, str(QName(ns.get('mets'), 'name'))).text = 'Filer på disk' 

        agentLevererandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeOrganisation.set('ROLE', "CREATOR")
        agentLevererandeOrganisation.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentLevererandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.organisation

        # Skapar altrecordID
        altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
        altRecordID.set('TYPE', 'SUBMISSIONAGREEMENT')
        altRecordID.text = self.diarienummer
        
        # Skapar dmdSec
        #dmdSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'dmdSec')))

        #Filgrupper
        fileSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'fileSec')))
        fileGrp = etree.SubElement(fileSec, str(QName(ns.get('mets'), 'fileGrp')))
        
        #Filer använder värden i filedict som populerats via funktionen "collectFiles"
        for k, v in track(filedict.items(), 'Skapar Sip.xml'):
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
                time.sleep(0.05)

        # Skapar structMap
        structMap = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'structMap')))
        structMap.set('LABEL', 'No structMap defined in this information package')
        divelement = etree.SubElement(structMap, str(QName(ns.get('mets'), 'div'))) 
                     
        # Skriver xml till sip.xml
        xmlFile.write(f'Sip.xml', xml_declaration=True, encoding='utf-8', pretty_print=True)
    
    def collectFiles(self, directory, subdirectorys=False):
        filedict = self.filedict
        # Kontrollerar att sökvägen är ok.
        if not os.path.exists(directory):
            print("Path doesn't exist")
            return 'Wrong path'
        
        # Skapar en dict med alla filnamn och deras sökväg
        for root, dirs, files in os.walk(directory):
            # Om endast huvudkatalogen ska ingå i paketet
            if subdirectorys == False:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[f] = filedict.get(f,{'path':filePath})
                break
            
            # Om subdirectorys ska ingå i paketet
            if subdirectorys == True:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[f] = filedict.get(f,{'path':filePath})

        # Samlar metadata om filerna och lägger till i dicten. (Track används för att skapa "Progressbar")
        for  k, v in track(filedict.items(), description=f"Genererar metadata för filer"):
            # Samlar metadata
            #print(f'Genererar metadata för {k}')
            filePathFromDict = filedict[k]['path']
            fileSize = str(os.stat(filePathFromDict).st_size)
            # Lägg på en timme + 1
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(filePathFromDict).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(filePathFromDict)
            mimeType = mimetypes.guess_type(filePathFromDict)[0]
            originalFileName = k
            fgsFileName = str(originalFileName).lower().replace('å', 'a').replace('ä','a').replace('ö','o')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            relativeFilePath = filePathFromDict.replace(directory,'').replace(k,'').replace('\\','/')
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
            time.sleep(0.05)
        
            
            
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
        
        # Lägger paketets filer i contentmappen (track används för att skapa "progressbar")
        filedict = self.filedict
        for k, v in track(filedict.items(), description="Preparerar FGS-paketet"):
            if k == os.path.basename(sys.argv[0]):
                #print(f'Hoppar över {sys.argv[0]}')
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
                newPath = os.path.join(relativePackagePath, k)
                fgsPath = os.path.join(relativePackagePath, filedict[k]['fgsfilename'])
                try:
                   os.rename(newPath, fgsPath)
                except Exception as e:
                   print(e)
                time.sleep(0.05)
        # Skapar zippen
        with Progress() as progress:
            task = progress.add_task('Skapar FGS-paket', total=4)
            progress.update(task, advance=10)
            time.sleep(0.1)
            packageTime = datetime.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
            progress.update(task, advance=15)
            shutil.make_archive(f'FGS_Package_{packageTime}','zip', parentDir)
            progress.update(task, advance=25)
            time.sleep(0.1)
            # Tar bort katalogen FGSpackage efter att den zippats.
            shutil.rmtree(parentDir)
            progress.update(task, advance=50)
            time.sleep(1)
        print(f'Paketet FGS_Package_{packageTime}.zip genererades i katalogen {cwd}')     

# Startar Skriptet
fgsPackage = FgsMaker()
fgsPackage.inputValues(True)
fgsPackage.collectFiles(fgsPackage.pathToFiles, fgsPackage.subfolders)
fgsPackage.createSip()
fgsPackage.createFgsPackage(cwd)

