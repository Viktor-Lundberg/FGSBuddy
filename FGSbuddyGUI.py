import os
import time
from turtle import update
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc

# Current working directory
cwd = os.getcwd()

# Sätter färgtema
sg.theme('greenMono') #LightGreen2 DarkBlue3 #reddit greenMono

# Listor med element som utgör olika delar av layouten. 
paketinformation = [
    [sg.Text('Övergripande paketinformation', font='Arial 12 bold',size=30)], 
    [sg.Text('Status*', size=32), sg.Combo(['NEW', 'SUPPLEMENT', 'REPLACEMENT','TEST','VERSION', 'OTHER'], default_value='NEW', key='recordstatus') ],
    [sg.Text('Beskrivning', tooltip='<mets>?', size=32),sg.Input(key='beskrivning', tooltip='''?''')],
    [sg.Text('Leveransöverenskommelse*', size=32), sg.Input('Submissionagremmentnernrenre',key='submissionagreement')],
    [sg.Text('Tidigare leveransöverenskommelse', size=32),sg.Input(key='formersubmissionagreement')],
    [(sg.Text('Överföring', size=32)), sg.Input(key='overforing')],
    [sg.Text('Ordningsnummer inom överföring', size=32), sg.Input(key='overforingNR')]

]

parter = [
    [sg.Text('Arkivbildare', font='Arial 12 bold', size=25)],    
    [sg.Text('Arkivbildare - Namn*', tooltip='<mets><metsHdr><agent ROLE=”ARCHIVIST” TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Arkivbildaren',key='arkivbildare', tooltip='''Namn på arkivbildaren. 
Arkivbildaren är den organisation som har skapat arkivmaterialet''',)],
    [sg.Text('Arkivbildare - Identitetskod*')],
    [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyp'),sg.Input('koden', key='IDkod',size=35)],
    [sg.Text('Levererande organisation - Namn*', tooltip='<mets><metsHdr><agent ROLE="Creator" TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Organisationen',key='levererandeorganisation', tooltip='''Namn på den organisation som levererat SIP:en till e-arkivet. 
Denna organisation är ofta identisk med den som anges som arkivbildare. Det skiljer sig i de fall där en myndighet övertagit en annan myndighets arkiv''')],
    [sg.Text('Levererande organisation - Identitetskod')],
    [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyplevererandeorganisation'),sg.Input('koden', key='IDkodlevererandeorganisation',size=35)],
    
    ]

system = [
    [sg.Text('Källsystem', font='Arial 12 bold', size=30)], 
    [sg.Text('Systemnamn*')],
    [sg.Input(default_text ='SYSTEMET', key='system')],
    [sg.Text('Systemversion')],
    [sg.Input(key='systemversion')],
    [sg.Text('Systemtyp')],
    [sg.Input(key='systemtyp')],

    ]

innehall = [  
    [sg.Text('Innehåll', font='Arial 12 bold', size=30)],
    [sg.Text('Sökväg till filer*')],
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
    [sg.Text('Informationstyp*', size=32), sg.Combo(['ERMS','Personnel','Medical record','Economics','Databases','Webpages', 'GIS', 'No specification', 'AIC', 'Archival information','Unstructured', 'Single records', 'Publication'], default_value='ERMS', key='informationstyp')],
    [sg.Text('Informationstypsspecifikation', size=32),sg.Input(key='informationstypsspecifikation')],
    [sg.Text('Tidsomfång', size=32), sg.CalendarButton('Startdatum', target='startdatum', format='%Y-%m-%d',no_titlebar=False), sg.Input(key='startdatum', size=(10,1)), sg.Text('-'), sg.Input(key='slutdatum', size=(10,1)),sg.CalendarButton('Slutdatum', target='slutdatum', format='%Y-%m-%d',no_titlebar=False)],
    [sg.Text('Informationsklass', size=32), sg.Input(key='informationsklass')],
    [sg.Text('Sekretess', size=32), sg.Combo(['Secrecy', 'PuL', 'Secrecy and PuL','GDPR','Ej angett'], default_value='Ej angett', key='sekretess')],
    [sg.Text('Gallring', size=32),sg.Combo(['Yes', 'No'], default_value='No', key='gallring') ],
]

space = [
    [sg.Text('', font='Arial 8 bold', size=30)],
    ]

ovrigt = [
    [sg.Text('Övrig information', font='Arial 12 bold', size=30)],
    [(sg.Text('Arkivets namn',size=32)), sg.Input(key='arkivetsnamn')],
    [(sg.Text('Arkivets referenskod',size=32)), sg.Input(key='arkivetsreferenskod')],
    [(sg.Text('Tidigare referenskod',size=32)),sg.Input(key='tidigarereferenskod')],
    [(sg.Text('Producerande organisation - Namn',size=32)), sg.Input(key='prodorgnamn')],
    [(sg.Text('Producerande organisation- IDkod',size=32)),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='prodorgIDkodtyp'),sg.Input('', key='prodorgIDkod',size=35)],
    [(sg.Text('Avsändande organisation - Namn',size=32)), sg.Input(key='avsandandeorgnamn')],
    [(sg.Text('Avsändande organisation - IDkod',size=32)),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='avsandandeorgIDkodtyp'),sg.Input('', key='avsandandeorgIDkod',size=35)],
    [(sg.Text('Informationsägande org. - Namn',size=32)), sg.Input(key='infoagarenamn')],
    [(sg.Text('Informationsägande org. - IDkod',size=32)),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='infoagareIDkodtyp'),sg.Input('', key='infoagareIDkod',size=35)],
]

ovrigt2 = [
    [sg.Text('', font='Consolas 12', size=30)],
    [(sg.Text('Levererande system - Namn',size=32)), sg.Input(key='levererandesystemnamn')],
    [(sg.Text('Levererande system - Version',size=32)), sg.Input(key='levererandesystemversion')],
    [(sg.Text('Konsult - Namn',size=32)), sg.Input(key='konsultnamn')],
    [(sg.Text('Konsult - Identitetskod',size=32)),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='konsultIDkodtyp'),sg.Input('', key='konsultIDkod',size=35)],
    [(sg.Text('Mottagare - Namn',size=32)), sg.Input(key='mottagarenamn')],
    [(sg.Text('Mottagare - Identitetskod',size=32)),sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='mottagareIDkodtyp'),sg.Input('', key='mottagareIDkod',size=35)],
    [(sg.Text('Kontaktperson - Namn',size=32)), sg.Input(key='kontaktpersonnamn')],
    [(sg.Text('Kontaktperson - Kontaktuppgifter',size=32)), sg.Input(key='kontaktuppgifter')],
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
window = sg.Window('FGS-Buddy v 0.9.1 - Viktor Lundberg', layout, font='Consolas 10')

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
                        print(f'Fältet {k} saknar värde.')
                
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

            