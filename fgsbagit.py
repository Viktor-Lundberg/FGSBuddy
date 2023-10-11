# Test för att skapa BAGIT
import bagit
import os 
import shutil
import datetime

def buddybagit(inputfolder: str, destinationfolder: str, metadata: dict, zipBag = True):
    

    # Skapar sökvägar för platsen att bygga BagIT-paketet
    cwd = os.getcwd()
    directoryName = os.path.join(cwd,'BagIT')

    # Flyttar filerna för att kunna skapa Bagen
    try:
        shutil.copytree(inputfolder, directoryName)
    except Exception as error:
        print(error)
    
    # Skapar Bag
    packageTime = datetime.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
    try:
        bag = bagit.make_bag(directoryName, metadata)
    except Exception as error:
        print(error)
    # Genererar zip-fil om Bagen ska komprimeras och tar bort BagIT-mappen.
    if zipBag:    
        try:
            output = os.path.join(destinationfolder, f'Bag_{packageTime}')
            shutil.make_archive(output,'zip', directoryName)
            shutil.rmtree(directoryName)
            print(f'BagIT-paketet Bag_{packageTime} skapades i katalogen {destinationfolder}')
        except Exception as error:
            print(error)
    
        
# Om skriptet körs direkt för testning...
if __name__ == "__main__":
    print('testar BagIT')
    metadata = {'Contact-Name': 'Ed Summers', 'Körv': 'makaroner', 'Hallå' : 'ffff'}
    cwd = os.getcwd()
    destinationfolder = os.path.join(cwd, 'test22')
    inputfolder = os.path.join('C:\Viktor\korv')
    buddybagit(inputfolder, destinationfolder, metadata, True)