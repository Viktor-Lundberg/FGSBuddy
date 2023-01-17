import datetime
import hashlib
import mimetypes
import os
import shutil
import sys
import time
import uuid
from xml.etree.ElementTree import QName
from lxml import etree

cwd = os.getcwd()


class FgsMaker:
    def __init__(self, values):
        self.filedict = {}
        self.GUIvalues = dict(values)

       
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
        rotelement.set('TYPE', self.GUIvalues['informationstyp'])
        rotelement.set('PROFILE', 'http://xml.ra.se/e-arkiv/METS/CommonSpecificationSwedenPackageProfile.xml')
        if self.GUIvalues['beskrivning'] != '':
            rotelement.set('LABEL', self.GUIvalues['beskrivning'])
        if self.GUIvalues['informationstypsspecifikation'] != '':
            rotelement.set(str(QName(ns.get('ext'),'CONTENTTYPESPECIFICATION')),self.GUIvalues['informationstypsspecifikation'])
        if self.GUIvalues['systemtyp'] != '':
            rotelement.set(str(QName(ns.get('ext'),'SYSTEMTYPE')),self.GUIvalues['systemtyp'])
        if self.GUIvalues['overforing'] != '':
            rotelement.set(str(QName(ns.get('ext'),'DATASUBMISSIONSESSION')),self.GUIvalues['overforing'])
        if self.GUIvalues['overforingNR'] != '':
            rotelement.set(str(QName(ns.get('ext'),'PACKAGENUMBER')),self.GUIvalues['overforingNR'])
        if self.GUIvalues['arkivetsnamn'] != '':
            rotelement.set(str(QName(ns.get('ext'),'ARCHIVALNAME')),self.GUIvalues['arkivetsnamn'])
        rotelement.set(str(QName(ns.get('ext'),'APPRAISAL')),self.GUIvalues['gallring'])
        if self.GUIvalues['sekretess'] != 'Not specified':
            rotelement.set(str(QName(ns.get('ext'),'ACCESSRESTRICT')),self.GUIvalues['sekretess'])
        if self.GUIvalues['startdatum'] != '':
            rotelement.set(str(QName(ns.get('ext'),'STARTDATE')),self.GUIvalues['startdatum'])
        if self.GUIvalues['slutdatum'] != '':
            rotelement.set(str(QName(ns.get('ext'),'ENDDATE')),self.GUIvalues['slutdatum'])
        if self.GUIvalues['informationsklass'] != '':
            rotelement.set(str(QName(ns.get('ext'),'INFORMATIONCLASS')),self.GUIvalues['informationsklass'])
        
        # Skapar metsHdr
        metsHdr = etree.SubElement(rotelement, str(QName(ns.get('mets'),'metsHdr')))
        metsHdr.set('CREATEDATE', datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        metsHdr.set(str(QName(ns.get('ext'),'OAISSTATUS')),'SIP')
        metsHdr.set('RECORDSTATUS', self.GUIvalues['recordstatus'])
        metsHdr.set(str(QName(ns.get('ext'),'AGREEMENTFORM')), self.GUIvalues['avtalsform'])                                                     
        
        # Skapar agents
        # Arkivbildare
        agentArkivbildare = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentArkivbildare.set('ROLE', "ARCHIVIST")
        agentArkivbildare.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['arkivbildare']
        identitetselement = etree.SubElement(agentArkivbildare, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["IDkodtyp"]}:{self.GUIvalues["IDkod"]}'
        
        # System
        agentSystem = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentSystem.set('ROLE', "ARCHIVIST")
        agentSystem.set('TYPE', "OTHER")
        agentSystem.set('OTHERTYPE', "SOFTWARE")
        namelement = etree.SubElement(agentSystem, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['system']
        if self.GUIvalues['systemversion'] != '':
            noteelement = etree.SubElement(agentSystem, str(QName(ns.get('mets'), 'note'))).text = self.GUIvalues['systemversion'] 

        # Levererande organisation
        agentLevererandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
        agentLevererandeOrganisation.set('ROLE', "CREATOR")
        agentLevererandeOrganisation.set('TYPE', "ORGANIZATION")
        namelement = etree.SubElement(agentLevererandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['levererandeorganisation']
        if self.GUIvalues['IDkodlevererandeorganisation'] != '':
            identitetselement = etree.SubElement(agentLevererandeOrganisation, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["IDkodtyplevererandeorganisation"]}:{self.GUIvalues["IDkodlevererandeorganisation"]}'

        # Producerande organisation
        if self.GUIvalues['prodorgnamn'] !='':
            agentProducerandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentProducerandeOrganisation.set('ROLE', "OTHER")
            agentProducerandeOrganisation.set('OTHERROLE', "PRODUCER")
            agentProducerandeOrganisation.set('TYPE', "ORGANIZATION")
            namelement = etree.SubElement(agentProducerandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['prodorgnamn']
            if self.GUIvalues['prodorgIDkod'] !='':
                identitetselement = etree.SubElement(agentProducerandeOrganisation, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["prodorgIDkodtyp"]}:{self.GUIvalues["prodorgIDkod"]}'

        # Avsändande organisation
        if self.GUIvalues['avsandandeorgnamn'] !='':
            agentAvsandandeOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentAvsandandeOrganisation.set('ROLE', "OTHER")
            agentAvsandandeOrganisation.set('OTHERROLE', "SUBMITTER")
            agentAvsandandeOrganisation.set('TYPE', "ORGANIZATION")
            namelement = etree.SubElement(agentAvsandandeOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['avsandandeorgnamn']
            if self.GUIvalues['avsandandeorgIDkod'] !='':
                identitetselement = etree.SubElement(agentAvsandandeOrganisation, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["avsandandeorgIDkodtyp"]}:{self.GUIvalues["avsandandeorgIDkod"]}'

        # Informationsägande organisation
        if self.GUIvalues['infoagarenamn'] !='':
            agentIpownerOrganisation = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentIpownerOrganisation.set('ROLE', "IPOWNER")
            agentIpownerOrganisation.set('TYPE', "ORGANIZATION")
            namelement = etree.SubElement(agentIpownerOrganisation, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['infoagarenamn']
            if self.GUIvalues['infoagareIDkod'] !='':
                identitetselement = etree.SubElement(agentIpownerOrganisation, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["infoagareIDkodtyp"]}:{self.GUIvalues["infoagareIDkod"]}'

        #  Konsult
        if self.GUIvalues['konsultnamn'] !='':
            konsult = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            konsult.set('ROLE', "EDITOR")
            konsult.set('TYPE', "ORGANIZATION")
            namelement = etree.SubElement(konsult, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['konsultnamn']
            if self.GUIvalues['konsultIDkod'] !='':
                identitetselement = etree.SubElement(konsult, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["konsultIDkodtyp"]}:{self.GUIvalues["konsultIDkod"]}'

        #  Levererande system
        if self.GUIvalues['levererandesystemnamn'] !='':
            agentLevererandeSystem = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentLevererandeSystem.set('ROLE', "CREATOR")
            agentLevererandeSystem.set('TYPE', "OTHER")
            agentLevererandeSystem.set('OTHERTYPE', "SOFTWARE")
            namelement = etree.SubElement(agentLevererandeSystem, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['levererandesystemnamn']
            if self.GUIvalues['levererandesystemversion'] !='':
                noteelement = etree.SubElement(agentLevererandeSystem, str(QName(ns.get('mets'), 'note'))).text = self.GUIvalues['levererandesystemversion']

        #  Kontaktperson
        if self.GUIvalues['kontaktpersonnamn'] !='':
            agentKontaktperson = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentKontaktperson.set('ROLE', "CREATOR")
            agentKontaktperson.set('TYPE', "INDIVIDUAL")
            namelement = etree.SubElement(agentKontaktperson, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['kontaktpersonnamn']
            if self.GUIvalues['kontaktuppgifter'] !='':
                noteelement = etree.SubElement(agentKontaktperson, str(QName(ns.get('mets'), 'note'))).text = self.GUIvalues['kontaktuppgifter']

        # Mottagare
        if self.GUIvalues['mottagarenamn'] !='':
            agentMottagare = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'agent')))
            agentMottagare.set('ROLE', "PRESERVATION")
            agentMottagare.set('TYPE', "ORGANIZATION")
            namelement = etree.SubElement(agentMottagare, str(QName(ns.get('mets'), 'name'))).text = self.GUIvalues['mottagarenamn']
            if self.GUIvalues['mottagareIDkod'] !='':
                identitetselement = etree.SubElement(agentMottagare, str(QName(ns.get('mets'), 'note'))).text = f'{self.GUIvalues["mottagareIDkodtyp"]}:{self.GUIvalues["mottagareIDkod"]}'

        # Skapar altrecordID
        altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
        altRecordID.set('TYPE', 'SUBMISSIONAGREEMENT')
        altRecordID.text = self.GUIvalues['submissionagreement']
        if self.GUIvalues['formersubmissionagreement'] != '':
            altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
            altRecordID.set('TYPE', 'PREVIOUSSUBMISSIONAGREEMENT')
            altRecordID.text = self.GUIvalues['formersubmissionagreement']
        if self.GUIvalues['arkivetsreferenskod'] != '':
            altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
            altRecordID.text = self.GUIvalues['arkivetsreferenskod']
            altRecordID.set('TYPE', 'REFERENCECODE')
        if self.GUIvalues['tidigarereferenskod'] != '':
            altRecordID = etree.SubElement(metsHdr, str(QName(ns.get('mets'),'altRecordID')))
            altRecordID.text = self.GUIvalues['tidigarereferenskod']
            altRecordID.set('TYPE', 'PREVIOUSREFERENCECODE')

        # Skapar dmdSec
        #dmdSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'dmdSec')))

        #Filgrupper
        fileSec = etree.SubElement(rotelement, str(QName(ns.get('mets'), 'fileSec')))
        fileGrp = etree.SubElement(fileSec, str(QName(ns.get('mets'), 'fileGrp')))
        
        #Filer använder värden i filedict som populerats via funktionen "collectFiles"
        for k, v in filedict.items():
            # Hoppar över filen om det är samma som filen som körs.
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
    
    def collectFiles(self, directory, subdirectorys=False, metadatafile=False, schemafile=False):
        filedict = self.filedict
        # Kontrollerar att sökvägen är ok.
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
                break
            
            # Om subdirectorys ska ingå i paketet
            if subdirectorys == True:
                for f in files:
                    filePath = os.path.join(root,f)
                    filedict[filePath] = filedict.get(f,{'path':filePath})
                    filedict[filePath]['fileName'] = f
                    

        # Samlar metadata om filerna och lägger till i dicten.
        for  k, v in filedict.items():
            # Samlar metadata
            filePathFromDict = filedict[k]['path']
            fileSize = str(os.stat(filePathFromDict).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(filePathFromDict).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(filePathFromDict)
            mimeType = mimetypes.guess_type(filePathFromDict)[0]
            originalFileName = filedict[k]['fileName']
            fgsFileName = str(originalFileName).replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_').replace('Å','A').replace('Ä','A').replace('Ö','O')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            relativeFilePath = filePathFromDict.replace(directory,'').replace(originalFileName,'').replace('\\','/')
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
            filedict[k]['category'] = 'content'
            

        # METADATAFILE
        if metadatafile:
            metadatafilepath = os.path.join(metadatafile)
            print(metadatafilepath)
            fileSize = str(os.stat(metadatafilepath).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(metadatafilepath).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(metadatafilepath)
            mimeType = mimetypes.guess_type(metadatafilepath)[0]
            originalFileName = os.path.basename(metadatafilepath)
            fgsFileName = str(originalFileName).replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_').replace('Å','A').replace('Ä','A').replace('Ö','O')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            relativeFilePath = '/'
            
            fileLink = f'file:///Metadata/{fgsFileName}'

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
            filedict[metadatafilepath]['category'] = 'metadata'
        
        # Schemafile
        if schemafile:
            metadatafilepath = os.path.join(schemafile)
            fileSize = str(os.stat(metadatafilepath).st_size)
            createdDate = datetime.datetime.utcfromtimestamp(os.stat(metadatafilepath).st_mtime).strftime('%Y-%m-%dT%H:%M:%S')
            hashValue = self.hashfunction(metadatafilepath)
            mimeType = mimetypes.guess_type(metadatafilepath)[0]
            originalFileName = os.path.basename(metadatafilepath)
            fgsFileName = str(originalFileName).replace('å', 'a').replace('ä','a').replace('ö','o').replace(' ','_').replace('Å','A').replace('Ä','A').replace('Ö','O')
            
            # Tar fram den relativa sökvägen genom att ta hela filsökvägen - {directory} för att använda till att skapa fileLink.
            # C:\mappen\undermapp1\undermapp2\Engöttigfil.txt --> undermapp1/undermapp2
            # file:///Content/undermapp1/undermapp2/engottigfil.txt'
            relativeFilePath = '/'
            
            fileLink = f'file:///System/{fgsFileName}'

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
            filedict[metadatafilepath]['category'] = 'schema'
            
            
    # Code slightly modified from https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    def hashfunction(self, file):
        with open(file, "rb") as f:
            fileHash = hashlib.sha256()
            while bits := f.read(8192):
                fileHash.update(bits)
        hashValue = fileHash.hexdigest()
        f.close
        return hashValue
    
    def createFgsPackage(self, directory, outputfolder):
        # Skapar paths och mappar för att kunna bygga FGS-paketet.
        directoryName = 'FGSpackage'
        parentDir = os.path.join(directory, directoryName)
        childDir = 'Content'
        path = os.path.join(parentDir, childDir)
        os.makedirs(path, exist_ok=True)
        # kopierar sip.xml till paketet.
        sipPath = os.path.join(directory,'sip.xml')
        shutil.copy2(sipPath, parentDir)

        # Sökvägar för metadatafilen
        metadataDir = 'Metadata'
        metadataPath = os.path.join(parentDir,metadataDir)
        os.mkdir(metadataPath)

        # Sökvägar för schemafilen
        schemaDir = 'System'
        schemaPath = os.path.join(parentDir,schemaDir)
        os.mkdir(schemaPath)

        
        # Lägger paketets filer i contentmappen
        filedict = self.filedict
        i = 0
        for k, v in filedict.items():
            if filedict[k]['category'] == 'metadata':
                shutil.copy2(filedict[k]['path'], metadataPath)
            elif filedict[k]['category'] == 'schema':
                shutil.copy2(filedict[k]['path'], schemaPath)       
            else:
                # Tar fram den relativa sökvägen till filen genom att lägga ihop cwd + relativ path. Skapar katalog i FGSpackage om den inte finns.
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
        packageTime = datetime.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
        destinationFolder = os.path.join(outputfolder, f'{self.GUIvalues["arkivbildare"]}_{self.GUIvalues["system"]}_{packageTime}')
        FGSName = f'{self.GUIvalues["arkivbildare"]}_{self.GUIvalues["system"]}_{packageTime}'
        try:
            shutil.make_archive(destinationFolder,'zip', parentDir)
        except:
            shutil.make_archive(FGSName,'zip', parentDir)
            outputfolder = cwd
       
        # Tar bort katalogen FGSpackage efter att den zippats.
        shutil.rmtree(parentDir)
        self.output = ''
        self.output = f'FGS-paketet "{self.GUIvalues["arkivbildare"]}_{self.GUIvalues["system"]}_{packageTime}.zip" genererades i katalogen {outputfolder}'     
             
