import os
import time
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc
import json


# Current working directory
cwd = os.getcwd()

# Laddar tooltipsfil
tooltipsfile = open('tooltips.json', encoding='utf-8')
tt = json.load(tooltipsfile)
# Fixar jsonformateringen i tooltips \\\n --> \n
for k, v in tt.items():
    tt[k] = v.replace('\\', '')


# Sätter färgtema
sg.theme('greenMono') #LightGreen2 DarkBlue3 #reddit greenMono

# Listor med element som utgör olika delar av layouten. 
paketinformation = [
    [sg.Text('Övergripande paketinformation', font='Arial 12 bold',size=30)], 
    [sg.Text('Status*', size=32, tooltip=tt['StatusT']), sg.Combo(['NEW', 'SUPPLEMENT', 'REPLACEMENT','TEST','VERSION', 'OTHER'], default_value='NEW', key='recordstatus', tooltip=tt['Status']) ],
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
    [sg.Input(default_text=cwd,tooltip="Välj katalog"), sg.FolderBrowse('Välj katalog',key="folder", initial_folder=os.path.join(cwd))],
    [sg.Text('Inkludera undermappar')],
    [sg.Radio('Ja', 'subfolders', default=False, key='subfolderstrue'), sg.Radio('Nej', 'subfolders', default=True, key='subfoldersfalse')],
    [sg.Text('Sökväg till metadatafil')],
    [sg.Input(tooltip="Välj metadatafil"), sg.FileBrowse('Välj fil',key="metadatafile", initial_folder=os.path.join(cwd))],
    [sg.Text('Sökväg till schemafil')],
    [sg.Input(tooltip="Välj schemafil"), sg.FileBrowse('Välj fil', key="schemafile", initial_folder=os.path.join(cwd))],

    ]

information = [
    [sg.Text('Information', font='Arial 12 bold', size=30)],
    [sg.Text('Informationstyp*', size=32, tooltip=tt['InformationstypT']), sg.Combo(['ERMS','Personnel','Medical record','Economics','Databases','Webpages', 'GIS', 'No specification', 'AIC', 'Archival information','Unstructured', 'Single records', 'Publication'], default_value='ERMS', key='informationstyp', tooltip=tt['Informationstyp'])],
    [sg.Text('Informationstypsspecifikation', size=32, tooltip=tt['InformationstypsspecifikationT']),sg.Input(key='informationstypsspecifikation', tooltip=tt['Informationstypsspecifikation'])],
    [sg.Text('Tidsomfång', size=32), sg.CalendarButton('Startdatum', target='startdatum', format='%Y-%m-%d',no_titlebar=False, tooltip=tt['StartdatumT']), sg.Input(key='startdatum', size=(10,1), tooltip=tt['Startdatum']), sg.Text('-'), sg.Input(key='slutdatum', size=(10,1), tooltip=tt['Slutdatum']),sg.CalendarButton('Slutdatum', target='slutdatum', format='%Y-%m-%d',no_titlebar=False, tooltip=tt['SlutdatumT'])],
    [sg.Text('Informationsklass', size=32, tooltip=tt['InformationsklassT']), sg.Input(key='informationsklass', tooltip=tt['Informationsklass'])],
    [sg.Text('Sekretess', size=32, tooltip=tt['SekretessT']), sg.Combo(['Secrecy', 'PuL', 'Secrecy and PuL','GDPR','Ej angett'], default_value='Ej angett', key='sekretess', tooltip=tt['Sekretess'])],
    [sg.Text('Gallring', size=32, tooltip=tt['GallringT']),sg.Combo(['Yes', 'No'], default_value='No', key='gallring', tooltip=tt['Gallring']) ],
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
    [(sg.Text('Informationsägande org. - IDkod',size=32, tooltip=tt['InfoagareIDkodT'])),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='InfoagareIDkod'),sg.Input('', key='infoagareIDkod',size=35)],
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
]


# GUI layout
layout = [
    [sg.Column(paketinformation, vertical_alignment='top'), sg.Column(information)],
    [sg.Column(space)],
    [sg.Column(parter, vertical_alignment='top'), sg.Column(system, vertical_alignment='top'), sg.Column(innehall, vertical_alignment='top')],
    [sg.pin(sg.Column(ovrigt, key='non2', visible=False)), sg.Column(ovrigt2, key='non3', visible=False, vertical_alignment='top')],
    [sg.Submit('Skapa paket', key='createSIP', size=15), sg.Button('Visa alla fält', key='fields', size=15)],
    [sg.Output(size=(165,5), key='output', pad=0)]
    ]

# Skapar "menyfönstret"
window = sg.Window('FGS-Buddy v 1.0 - Viktor Lundberg', layout, font='Consolas 10', icon="Buddy.ico")

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
            window.FindElement('output').Update('')
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
                if values['subfolderstrue']:
                    subfolders = True
                if values['metadatafile'] != '':
                    metadatafile = values['metadatafile']
                if values['schemafile'] != '':
                    schemafile = values['schemafile']
                fgsPackage.collectFiles(folder, subfolders, metadatafile, schemafile)
                fgsPackage.createSip()
                fgsPackage.createFgsPackage(cwd)
                time.sleep(0.3)
                window.FindElement('output').update('')
                window.refresh()
                print(fgsPackage.output)
        
        # Visar eller döljer layout om användaren trycker på knappen
        case 'fields':
            if allvalues == False:
                window['non2'].Update(visible=True)
                window['non3'].Update(visible=True)
                window.refresh()
                window['fields'].Update('Dölj fält')
                allvalues = True
            else:
                window['non2'].Update(visible=False)
                window['non3'].Update(visible=False)
                window.refresh()
                window['fields'].Update('Visa alla fält')
                allvalues = False

            