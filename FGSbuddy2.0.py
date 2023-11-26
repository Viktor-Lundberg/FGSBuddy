import os
import time
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc
import json
import webbrowser
import fgsbagit as FGSbag


# Nuvarande version
version = '1.5.0'
# Current working directory
cwd = os.getcwd()
# Tema för layout
#sg.theme('greenMono')
sg.theme('TealMono')


def menyrad() -> list:
    """Skapar innehållet i menyraden genom att returnera en lista med värden som ska ingå i menyn"""
    meny = [ ['FGS-dokumentation', ['FGS-Paketstruktur v 1.2','FGS-Paketstruktur v 1.2 - tillägg','Schema v 1.2']],['Hjälp', ['Om FGS-Buddy']]]
    return meny

def mainmenu():
    """Funktion för att skapa huvudmenyn och program-loop"""
    # FIX Fönster som stänger---

    mainmenulayout = [
    [sg.MenuBar(menyrad(), background_color='Pink')],
    [sg.Text('', font='Arial 12 bold', size=1)],
    [sg.Image('Buddy.PNG')],
    #[sg.Text(f'Version: {version}\nSkapad av: Viktor Lundberg\nLicens: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)', font='Consolas 10')],
    #[sg.Text('Välj format', font='Arial 10 bold', size=30)],
    [sg.Text('', font='Arial 12 bold', size=1)],
    [sg.Button('FGS 1.2', key='fgs', size=(20,3), font='Arial 10 bold'), 
     sg.Button('BagIT', key='bagit', font='Arial 10 bold', size=(20,3)), 
     sg.Button('FGS 2.0', key='fgs_2.0', font='Arial 10 bold', size=(20,3))],
    [sg.Text(f'Version: {version}\nSkapad av: Viktor Lundberg\nLicens: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)', font='Consolas 10')],

]
   
    layout = [[sg.Column(mainmenulayout, element_justification='center')],
                       ]
    
    mainmenuwindow = sg.Window(f'FGS-Buddy {version}', layout, icon="Buddy.ico")
    
    # Programloop för "huvudmenyn"
    while True:
        event, values = mainmenuwindow.read()
        match event:
            case sg.WIN_CLOSED:
                break
            case "Exit":
                mainmenuwindow.close()
                break
            case 'githublink':
                webbrowser.open('https://github.com/Viktor-Lundberg/FGSBuddy')
            case 'fgs':
                fgswindow()
            case 'FGS-Paketstruktur v 1.2':
                    webbrowser.open('https://riksarkivet.se/Media/pdf-filer/doi-t/FGS_Paketstruktur_RAFGS1V1_2.pdf')
            case 'FGS-Paketstruktur v 1.2 - tillägg':
                    webbrowser.open('https://riksarkivet.se/Media/pdf-filer/doi-t/FGS_Paketstruktur_Tillagg_RAFGS1V1_2A20171025.pdf')
            case 'Schema v 1.2':
                    webbrowser.open('http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd')
            case 'Om FGS-Buddy':
                buddywindow()
            case 'bagit':
                bagitwindow()


def clearinput(inputdict: dict):
    """Funktion för att rensa alla input-fält för FGS 1.2-fönstret"""

    saveinput = ['folderinput', 'outputfolderinput']
    # Går igenom key_dict och kontrollerar vad det är för sg objekt
    for k, v in inputdict.items():
        # Om fältet är ett inputfält och keyn inte finns med i listan över värden som inte ska ändras --> Rensa 
        if isinstance(v, sg.Input) and k not in saveinput:
            v.update('')
        # Sätter alla combofält till defaultvärdet
        elif isinstance(v, sg.Combo):
            v.update(v.DefaultValue)
        # Ändrar till defaultvärdet i radioknapparna kring om paketet ska innehålla "undermappar"
        elif isinstance(v, sg.Radio) and k == 'subfoldersfalse':
            v.update(True)
        else:
            continue


def buddywindow():
    """Funktion för att skapa popup-fönstret 'Om FGS-Buddy'"""

    # Hämtar alla releasenotes från txt-fil och lägger i variabeln releasenotes
    with open('releasenotes.txt', encoding='utf-8') as releasenotesdoc:
        releasenotes = releasenotesdoc.read()

    # Layout för fönstret
    aboutlayout = [
        [sg.Text('FGS-Buddy', font='Arial 12 bold', size=30)],
        [sg.Text(f'Version: {version}\nSkapad av: Viktor Lundberg\nLicens: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)', font='Consolas 10')],
        [sg.Text('FGS-Buddy på github',font='Consolas 10 underline', text_color='blue', enable_events=True, key='githublink')],
        [sg.Text('', font='Arial 12 bold', size=30)],
        [sg.Text('Release notes', font='Arial 10 bold', size=30)],
        [sg.Text(releasenotes, font='Consolas 8')],
        [sg.Button('Ok', key='Exit', size=7)]
    ]

    # Skapar nya fönstret
    about = sg.Window('Om FGS-Buddy', aboutlayout, icon="Buddy.ico")
    
    # Programloop för "Om FGS-Buddy"-fönstret.
    while True:
        event, values = about.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            about.close()
            releasenotesdoc.close()
            break
        if event == 'githublink':
            webbrowser.open('https://github.com/Viktor-Lundberg/FGSBuddy')

 
def fgswindow():
    """Skapar GUI-fönster för FGS 1.2"""

    # Laddar tooltipsfil
    tooltipsfile = open('tooltips.json', encoding='utf-8')
    tt = json.load(tooltipsfile)
    # Fixar jsonformateringen i tooltips \\\n --> \n
    for k, v in tt.items():
        tt[k] = v.replace('\\', '')


    # Sätter färgtema
    #sg.theme('greenMono') #LightGreen2 DarkBlue3 #reddit greenMono

    # Listor med element som utgör olika delar av layouten. 

    paketinformation = [
        [sg.Text('Övergripande paketinformation', font='Arial 12 bold',size=30)], 
        [sg.Text('Status*', size=32, tooltip=tt['StatusT']), sg.Combo(['NEW', 'SUPPLEMENT', 'REPLACEMENT','TEST','VERSION', 'OTHER'], default_value='NEW', key='recordstatus', tooltip=tt['Status'], size=43) ],
        [sg.Text('Beskrivning', tooltip=tt['BeskrivningT'], size=32),sg.Input(key='beskrivning', tooltip=tt['Beskrivning'])],
        [sg.Text('Leveransöverenskommelse*', size=32, tooltip=tt['LeveransoverenskommelseT']), sg.Input(key='submissionagreement',tooltip=tt['Leveransoverenskommelse'])],
        [sg.Text('Tidigare leveransöverenskommelse', size=32, tooltip=tt['TidigareLeveransoverenskommelseT']),sg.Input(key='formersubmissionagreement', tooltip=tt['TidigareLeveransoverenskommelse'])],
        [(sg.Text('Överföring', size=32, tooltip=tt['OverforingT'])), sg.Input(key='overforing', tooltip=tt['Overforing'])],
        [sg.Text('Ordningsnummer inom överföring', size=32, tooltip=tt['OrdningsnummerT']), sg.Input(key='overforingNR',tooltip=tt['Ordningsnummer'])]

    ]

    parter = [
        [sg.Text('Arkivbildare', font='Arial 12 bold', size=25)],    
        [sg.Text('Arkivbildare - Namn*', tooltip=tt['ArkivbildarenamnT']) ],
        [sg.Input(key='arkivbildare', tooltip=tt['Arkivbildarenamn'])],
        [sg.Text('Arkivbildare - Identitetskod*', tooltip=tt['ArkivbildareIDkodT'])],
        [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyp'),sg.Input(key='IDkod',size=35, tooltip=tt['ArkivbildareIDkod'])],
        [sg.Text('Levererande organisation - Namn*', tooltip=tt['LevererandeorganisationnamnT']) ],
        [sg.Input(key='levererandeorganisation', tooltip=tt['Levererandeorganisationnamn'])],
        [sg.Text('Levererande organisation - Identitetskod', tooltip=tt['LevererandeorganisationIDkodT'])],
        [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyplevererandeorganisation'),sg.Input(key='IDkodlevererandeorganisation',size=35, tooltip=tt['LevererandeorganisationIDkod'])],
        
        ]

    system = [
        [sg.Text('Källsystem', font='Arial 12 bold', size=30)], 
        [sg.Text('Systemnamn*', tooltip=tt['SystemnamnT'])],
        [sg.Input(key='system', tooltip=tt['Systemnamn'])],
        [sg.Text('Systemversion',tooltip=tt['SystemversionT'])],
        [sg.Input(key='systemversion', tooltip=tt['Systemversion'])],
        [sg.Text('Systemtyp', tooltip=tt['SystemtypT'])],
        [sg.Input(key='systemtyp', tooltip=tt['Systemtyp'])],

        ]

    innehall = [  
        [sg.Text('Innehåll', font='Arial 12 bold', size=30)],
        [sg.Text('Sökväg till filer som ska ingå i paketet')],
        [sg.Input(default_text=cwd,tooltip="Välj katalog", key='folderinput'), sg.FolderBrowse('Välj katalog',key="folder", initial_folder=os.path.join(cwd))],
        [sg.Text('Inkludera undermappar')],
        [sg.Radio('Ja', 'subfolders', default=False, key='subfolderstrue'), sg.Radio('Nej', 'subfolders', default=True, key='subfoldersfalse')],
        [sg.Text('Sökväg till metadatafil')],
        [sg.Input(tooltip="Välj metadatafil", key='metadatafile'), sg.FileBrowse('Välj fil',key="metadatafileB", initial_folder=os.path.join(cwd))],
        [sg.Text('Sökväg till schemafil')],
        [sg.Input(tooltip="Välj schemafil", key='schemafile'), sg.FileBrowse('Välj fil', key="schemafileB", initial_folder=os.path.join(cwd) )],

        ]

    information = [
        [sg.Text('Information', font='Arial 12 bold', size=30)],
        [sg.Text('Informationstyp*', size=32, tooltip=tt['InformationstypT']), sg.Combo(['ERMS','Personnel','Medical record','Economics','Databases','Webpages', 'GIS', 'No specification', 'AIC', 'Archival information','Unstructured', 'Single records', 'Publication'], default_value='ERMS', key='informationstyp', tooltip=tt['Informationstyp'], size=43)],
        [sg.Text('Informationstypsspecifikation', size=32, tooltip=tt['InformationstypsspecifikationT']),sg.Input(key='informationstypsspecifikation', tooltip=tt['Informationstypsspecifikation'])],
        [sg.Text('Tidsomfång', size=32), sg.CalendarButton('Startdatum', target='startdatum', format='%Y-%m-%d', tooltip=tt['StartdatumT']), sg.Input(key='startdatum', size=(10,1), tooltip=tt['Startdatum']), sg.Text('-'), sg.Input(key='slutdatum', size=(10,1), tooltip=tt['Slutdatum']),sg.CalendarButton('Slutdatum', target='slutdatum', format='%Y-%m-%d', tooltip=tt['SlutdatumT'])],
        [sg.Text('Informationsklass', size=32, tooltip=tt['InformationsklassT']), sg.Input(key='informationsklass', tooltip=tt['Informationsklass'])],
        [sg.Text('Sekretess', size=32, tooltip=tt['SekretessT']), sg.Combo(['Secrecy', 'PuL', 'Secrecy and PuL','GDPR','Not specified'], default_value='Not specified', key='sekretess', tooltip=tt['Sekretess'], size=43)],
        [sg.Text('Gallring', size=32, tooltip=tt['GallringT']),sg.Combo(['Yes', 'No'], default_value='No', key='gallring', tooltip=tt['Gallring'], size=43) ],
    ]

    space = [
        [sg.Text('', font='Arial 8 bold', size=30)],
        ]

    ovrigt = [
        [sg.Text('Övrig information', font='Arial 12 bold', size=30)],
        [(sg.Text('Arkivets namn',size=32, tooltip=tt['ArkivetsnamnT'])), sg.Input(key='arkivetsnamn', tooltip=tt['Arkivetsnamn'])],
        [(sg.Text('Arkivets referenskod',size=32, tooltip=tt['ArkivetsreferenskodT'])), sg.Input(key='arkivetsreferenskod',tooltip=tt['Arkivetsreferenskod'])],
        [(sg.Text('Tidigare referenskod',size=32, tooltip=tt['TidigareReferenskodT'])),sg.Input(key='tidigarereferenskod', tooltip=tt["TidigareReferenskod"])],
        [(sg.Text('Producerande organisation - Namn',size=32, tooltip=tt['ProducerandeorganisationnamnT'])), sg.Input(key='prodorgnamn', tooltip=tt['Producerandeorganisationnamn'])],
        [(sg.Text('Producerande organisation- IDkod',size=32, tooltip=tt['ProducerandeorganisationIDkodT'])),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='prodorgIDkodtyp'),sg.Input('', key='prodorgIDkod',size=35, tooltip=tt['ProducerandeorganisationIDkod'])],
        [(sg.Text('Avsändande organisation - Namn',size=32, tooltip=tt['AvsandandeorganisationnamnT'])), sg.Input(key='avsandandeorgnamn', tooltip=tt['Avsandandeorganisationnamn'])],
        [(sg.Text('Avsändande organisation - IDkod',size=32, tooltip=tt['AvsandandeorganisationIDkodT'])),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='avsandandeorgIDkodtyp'),sg.Input('', key='avsandandeorgIDkod',size=35, tooltip=tt['AvsandandeorganisationIDkod'])],
        [(sg.Text('Informationsägande org. - Namn',size=32, tooltip=tt['InfoagarenamnT'])), sg.Input(key='infoagarenamn', tooltip=tt['Infoagarenamn'])],
        [(sg.Text('Informationsägande org. - IDkod',size=32, tooltip=tt['InfoagareIDkodT'])),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='infoagareIDkodtyp'),sg.Input('', key='infoagareIDkod',size=35)],
    ]

    ovrigt2 = [
        [sg.Text('', font='Consolas 12', size=30)],
        [(sg.Text('Levererande system - Namn',size=32, tooltip=tt['LevererandesystemnamnT'])), sg.Input(key='levererandesystemnamn', tooltip=tt['Levererandesystemnamn'])],
        [(sg.Text('Levererande system - Version',size=32, tooltip=tt['LevererandesystemversionT'])), sg.Input(key='levererandesystemversion', tooltip=tt['Levererandesystemversion'])],
        [(sg.Text('Konsult - Namn',size=32, tooltip=tt['KonsultnamnT'])), sg.Input(key='konsultnamn', tooltip=tt['Konsultnamn'])],
        [(sg.Text('Konsult - Identitetskod',size=32,tooltip=tt['KonsultIDkodT'] )),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='konsultIDkodtyp'),sg.Input('', key='konsultIDkod',size=35, tooltip=tt['KonsultIDkod'])],
        [(sg.Text('Mottagare - Namn',size=32, tooltip=tt['MottagarenamnT'])), sg.Input(key='mottagarenamn', tooltip=tt['Mottagarenamn'])],
        [(sg.Text('Mottagare - Identitetskod',size=32, tooltip=tt['MottagareIDkodT'])),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='mottagareIDkodtyp'),sg.Input('', key='mottagareIDkod',size=35, tooltip=tt['MottagareIDkod'])],
        [(sg.Text('Kontaktperson - Namn',size=32, tooltip=tt['KontaktpersonnamnT'])), sg.Input(key='kontaktpersonnamn', tooltip=tt['Kontaktpersonnamn'])],
        [(sg.Text('Kontaktperson - Kontaktuppgifter',size=32, tooltip=tt['KontaktuppgifterT'])), sg.Input(key='kontaktuppgifter', tooltip=tt['Kontaktuppgifter'])],
        [sg.Text('Avtalsform', size=32, tooltip=tt['AvtalsformT']), sg.Combo(['AGREEMENT', 'DEPOSIT', 'GIFT','Not specified'], default_value='Not specified', key='avtalsform', tooltip=tt['Avtalsform'], size=43)],

    ]


    # GUI layout
    layout = [
        # OBS! Pysimplegui har problem med custom menubar (om det används syns inte applikationen i verktygsfältet, använd classic tills fix...)
        #[sg.Titlebar('FGS-Buddy v 1.1 - Viktor Lundberg', font='Consolas 10', background_color='Black')],
        #[sg.MenubarCustom(meny, bar_background_color='Pink', bar_text_color='Black')],
        
        [sg.MenuBar(menyrad(), background_color='Pink')],
        [sg.Column(paketinformation, vertical_alignment='top'), sg.Column(information)],
        [sg.Column(space)],
        [sg.Column(parter, vertical_alignment='top'), sg.Column(system, vertical_alignment='top'), sg.Column(innehall, vertical_alignment='top')],
        [sg.pin(sg.Column(ovrigt, key='invisible', visible=False)), sg.Column(ovrigt2, key='invisible2', visible=False, vertical_alignment='top')],
        [sg.Text('')],
        [sg.Output(size=(165,5), key='output', pad=5, background_color=	'pink', echo_stdout_stderr=True)],
        [sg.Text('Outputkatalog'),sg.Input(default_text=cwd, tooltip="Välj katalog", size=65, key='outputfolderinput'), sg.FolderBrowse('Välj katalog',key="outputfolder", initial_folder=os.path.join(cwd)),sg.Submit('Skapa paket', key='createSIP', size=15,button_color='black on pink'),sg.Text('', size=15), sg.Button('Rensa', key='clear', size=15),sg.Button('Visa alla fält', key='fields', size=15)],
        ]



    # Skapar "FGS 1.2-fönstet"
    window = sg.Window(f'FGS-Buddy {version}',layout, font='Consolas 10', icon="Buddy.ico", resizable=True, titlebar_background_color='green') 


    # Variabler för att kontrollera obligatoriska värden samt trigger för att visa/dölja alla element i layouten.
    forcedvaluesdict = {}
    allvalues = False


    # Program-Loop
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                break

            # Startar processen för att skapa FGS-paket om användaren trycker på "skapa paket"-knappen
            case 'createSIP':
                window.find_element('output').Update('')
                window.refresh()
                metadatafile = False
                schemafile = False
                subfolders = False

                # Kontrollerar att alla obligatoriska värden har information!
                if values['submissionagreement'] == '' or values['system'] == '' or values['arkivbildare'] == '' or values['IDkod'] == '' or values['levererandeorganisation'] == '':
                    # Lägger till värden i dicten för att kunna visa användaren vilka värden som saknas
                    forcedvaluesdict['System'] = values['system']
                    forcedvaluesdict['Leveransöverenskommelse'] = values['submissionagreement']
                    forcedvaluesdict['Arkivbildare'] = values['arkivbildare']
                    forcedvaluesdict['Identitetskod'] = values['IDkod']
                    forcedvaluesdict['Levererande organisation'] = values['levererandeorganisation']
                    # Loopar igenom dicten
                    for k, v in forcedvaluesdict.items():
                        # Returnerar de värden som saknas till användaren.
                        if v == '':
                            print(f'Fältet "{k}" saknar värde.')
                    
                # Om allt är ok skapa paketet med inkommande parametrar.
                else:
                    print(f'Skapar FGS-paketet...')
                    window.refresh()
                    fgsPackage = FGSfunc.FgsMaker(values)
                    if values['folder'] == '':
                        folder = os.path.join(cwd)
                    else:
                        folder = os.path.join(values['folder'])
                    if values['outputfolder'] == '':
                        outputfolder = os.path.join(cwd)
                    else:
                        outputfolder = os.path.join(values['outputfolder'])
                    if values['subfolderstrue']:
                        subfolders = True
                    if values['metadatafile'] != '':
                        metadatafile = values['metadatafile']
                    if values['schemafile'] != '':
                        schemafile = values['schemafile']
                    fgsPackage.collectFiles(folder, subfolders, metadatafile, schemafile)
                    fgsPackage.createSip()
                    fgsPackage.createFgsPackage(cwd,outputfolder)
                    time.sleep(0.3)
                    window.find_element('output').update('')
                    window.refresh()
                    print(fgsPackage.output)
            
            # Visar eller döljer layout om användaren trycker på knappen
            case 'fields':
                if allvalues == False:
                    window['invisible'].Update(visible=True)
                    window['invisible2'].Update(visible=True)
                    window.refresh()
                    window['fields'].Update('Dölj fält')
                    allvalues = True
                else:
                    window['invisible'].Update(visible=False)
                    window['invisible2'].Update(visible=False)
                    window.refresh()
                    window['fields'].Update('Visa alla fält')
                    allvalues = False
            
            case 'clear':
                clearinput(window.key_dict)
                #print(window.key_dict)
                window.refresh()
            
            # Meny - FGS-dokumentation
            case 'FGS-Paketstruktur v 1.2':
                webbrowser.open('https://riksarkivet.se/Media/pdf-filer/doi-t/FGS_Paketstruktur_RAFGS1V1_2.pdf')
            case 'FGS-Paketstruktur v 1.2 - tillägg':
                webbrowser.open('https://riksarkivet.se/Media/pdf-filer/doi-t/FGS_Paketstruktur_Tillagg_RAFGS1V1_2A20171025.pdf')
            case 'Schema v 1.2':
                webbrowser.open('http://xml.ra.se/e-arkiv/METS/CSPackageMETS.xsd')
            
            # Meny - Hjälp
            case 'Om FGS-Buddy':
                sg.Window.disappear(window)
                buddywindow()
                sg.Window.reappear(window)



def bagitwindow():
    metadata = {'Creator':'FGS-Buddy'}
    defaultvalues = []
    for k, v in metadata.items():
        newvalue = f'{k}:{v}'
        defaultvalues.append(newvalue)

    layout = [
        [sg.Text('Innehåll', font='Arial 12 bold', size=30)],
        [sg.Text('Sökväg till katalog som ska paketeras')],
        [sg.Input(default_text=cwd, tooltip="Välj katalog"), sg.FolderBrowse('Välj katalog', key="inputfolder", initial_folder=os.path.join(cwd))],
        [sg.Text('Metadata', font='Arial 12 bold', size=30)],    
        [sg.Text('Beskrivning:', size=13), sg.InputText(key='key')],
        [sg.Text('Värde:', size=13), sg.InputText(key='value')],
        [sg.Text('', size=48),sg.Button('Lägg till')],
        [sg.Text('Innehåll i "bag-info.txt" (metadata om paket och innehåll):')],
        [sg.Listbox(values=defaultvalues, size=(58, 5), key='output')],
        [sg.Text('', size=42),sg.Button('Ta bort'), sg.Button('Rensa')],
        
        [sg.Text('Outputkatalog', font='Arial 12 bold', size=30)],
        [[sg.Input(default_text=cwd,tooltip="Välj katalog"), sg.FolderBrowse('Välj katalog',key="destinationfolder", initial_folder=os.path.join(cwd))]],
        
        [sg.Output(key='output2', size=(58, 3), background_color='pink')],
        [sg.Button('Huvudmeny'), sg.Text('') ,sg.Button('Skapa Bag')]
    ]

    bagwindow = sg.Window(f'FGS-Buddy {version}', layout, font='Consolas 10', icon="Buddy.ico")
    
    while True:
        event, values = bagwindow.read()
        bagwindow.refresh()
        match event:
            case sg.WIN_CLOSED:
                break
            case 'Lägg till':
                key = values['key']
                value = values['value']
                if key and value:
                    metadata[key] = value
                    bagwindow['output'].update(values=[f"{k}: {v}" for k, v in metadata.items()])
                    bagwindow['key'].update('')
                    bagwindow['value'].update('')
            case 'Ta bort':
                selected_item = values['output']
                if selected_item:
                    try:
                        selected_key = selected_item[0].split(":")[0].strip()
                        del metadata[selected_key]
                        bagwindow['output'].update(values=[f"{k}: {v}" for k, v in metadata.items()])
                    except Exception as error:
                        print(error)
            case 'Huvudmeny':
                bagwindow.close()
                mainmenu()
                break
            case 'Skapa Bag':

                if values['destinationfolder'] == '':
                    destinationfolder = os.path.join(cwd)
                else:
                    destinationfolder = os.path.join(values['destinationfolder'])
                
                inputfolder = values['inputfolder']
                if inputfolder == '':
                    inputfolder = os.path.join(cwd)
                
                if inputfolder == cwd:
                    print(f'Kan inte skapa Bag av Katalogen {inputfolder}!')
                else:
                    FGSbag.buddybagit(inputfolder, destinationfolder, metadata, True)
            case 'Rensa':
                metadata = {}
                bagwindow['output'].update('')
                bagwindow.refresh() 
                
                


if __name__ == "__main__":
    mainmenu()
    #bagitwindow()
    #fgswindow()