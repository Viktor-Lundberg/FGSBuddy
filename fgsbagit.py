# Test för att skapa BAGIT
import bagit
import os 
import shutil
import datetime

def buddybagit(inputfolder, destinationfolder, metadata, zipBag = True):
    
    # Hämtar sökväg till filerna som ska ingå i Bagen.
    try:
        for root, dirs, files in os.walk(inputfolder):
            for file in files:
                filepath = os.path.join(root,file)
                print(filepath)
    except Exception as error:
        print(error)
    
    # Flyttar filerna för att kunna skapa Bagen
    try:
        shutil.copytree(inputfolder,destinationfolder)
    except Exception as error:
        print(error)
    
    # Skapar Bag
    packageTime = datetime.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
    bag = bagit.make_bag(destinationfolder, metadata)
    # Genererar zip-fil om Bagen ska komprimeras
    if zipBag:    
        try:
            shutil.make_archive(f'BagIT_{packageTime}','zip', destinationfolder)
        except Exception as error:
            print(error)


# Om skriptet körs direkt för testning...
if __name__ == "__main__":
    print('testar BagIT')
    metadata = {'Contact-Name': 'Ed Summers', 'Körv': 'makaroner', 'Hallå' : 'ffff'}
    cwd = os.getcwd()
    destinationfolder = os.path.join(cwd, 'test22')
    inputfolder = os.path.join('C:\Viktor\korv')
    buddybagit(inputfolder, destinationfolder, metadata)