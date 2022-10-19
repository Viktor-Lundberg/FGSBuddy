import os
from pydoc import visiblename
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc

cwd = os.getcwd()
sg.theme('LightGreen2')

# GUI ELEMENT
paketinformation = [
    [sg.Text('Övergripande paketinformation', font='Consolas 12', background_color='gray')], 
    [sg.Text('Status*'), sg.Combo(['NEW', 'SUPPLEMENT', 'REPLACEMENT','TEST','VERSION', 'OTHER'], default_value='NEW', key='recordstatus') ],
    [sg.Text('Beskrivning', tooltip='<mets>?'),sg.Input(key='beskrivning', tooltip='''?''')],
    [sg.Text('Leveransöverenskommelse*'), sg.Input('Submissionagremmentnernrenre',key='submissionagreement')],
    [sg.Text('Tidigare leveransöverenskommelse'),sg.Input(key='formersubmissionagreement')],
]

parter = [
    [sg.Text('Arkivbildare', font='Consolas 12', background_color='gray', size=25)],    
    [sg.Text('Arkivbildare - Namn*', tooltip='<mets><metsHdr><agent ROLE=”ARCHIVIST” TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Arkivbildaren',key='arkivbildare', tooltip='''Namn på arkivbildaren. 
Arkivbildaren är den organisation som har skapat arkivmaterialet''',)],
    [sg.Text('Arkivbildare - Identitetskod*')],
    [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyp'),sg.Input('koden', key='IDkod')],
    [sg.Text('Levererande organisation - Namn*', tooltip='<mets><metsHdr><agent ROLE="Creator" TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Organisationen',key='levererandeorganisation', tooltip='''Namn på den organisation som levererat SIP:en till e-arkivet. 
Denna organisation är ofta identisk med den som anges som arkivbildare. Det skiljer sig i de fall där en myndighet övertagit en annan myndighets arkiv''')],
    [sg.Text('Levererande organisation - Identitetskod')],
    [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyplevererandeorganisation'),sg.Input('koden', key='IDkodlevererandeorganisation')],
    
    ]

system = [
    [sg.Text('Källsystem', font='Consolas 12', background_color='gray', size=25)], 
    [sg.Text('Systemnamn*')],
    [sg.Input(default_text ='SYSTEMET', key='system')],
    [sg.Text('Systemversion')],
    [sg.Input(key='systemversion')],
    [sg.Text('Systemtyp')],
    [sg.Input(key='systemtyp')],

    ]

innehall = [  
    [sg.Text('Innehåll', font='Consolas 12', background_color='gray', size=25)],
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
    [sg.Text('Information', font='Consolas 12', background_color='gray', size=25)],
    [sg.Text('Informationstyp*'), sg.Combo(['ERMS','Personnel','Medical record','Economics','Databases','Webpages', 'GIS', 'No specification', 'AIC', 'Archival information','Unstructured', 'Single records', 'Publication'], default_value='ERMS', key='informationstyp')],
    [sg.Text('Informationstypsspecifikation'),sg.Input(key='informationstypsspecifikation')],
    [sg.Text('Tidsomfång'), sg.CalendarButton('Startdatum', target='startdatum', format='%Y-%m-%d',no_titlebar=False), sg.Input(key='startdatum', size=(10,1)), sg.Text('-'), sg.Input(key='slutdatum', size=(10,1)),sg.CalendarButton('Slutdatum', target='slutdatum', format='%Y-%m-%d',no_titlebar=False)],
    [sg.Text('Informationsklass'), sg.Input(key='Informationsklass')],
    [sg.Text('Sekretess'), sg.Combo(['Secrecy', 'PuL', 'Secrecy and PuL','GDPR','Ej angett'], default_value='Ej angett', key='sekretess')],
    [ sg.Text('Gallring'),sg.Combo(['Yes', 'No'], default_value='No', key='Gallring') ],
]

# Work in progress == Ej obligatoriska värden
overforing = [
    [sg.Text('Överföring', font='Consolas 12', background_color='gray', size=25)],
    [(sg.Text('Överföring')), sg.Text('Ordningsnummer inom överföring')],
    [sg.Input(key='overforing'), sg.Input(key='overforingNR')]
    ]

ovrigt = [
    [sg.Text('Övrig information', font='Consolas 12', background_color='gray', size=25)],
    [(sg.Text('Arkivets namn')), sg.Input(key='arkivetsnamn')],
    [(sg.Text('Arkivets referenskod')), sg.Input(key='arkivetsreferenskod')],
    [(sg.Text('Tidigare referenskod')),sg.Input(key='tidigarereferenskod')],
    [(sg.Text('Producerande organisation - Namn')), sg.Input(key='prodorgnamn')],
    [(sg.Text('Producerande organisation - Identitetskod')), sg.Input(key='prodorgidkod')],
    [(sg.Text('Avsändande organisation - Namn')), sg.Input(key='avsandandeorgnamn')],
    [(sg.Text('Avsändande organisation - Identitetskod')), sg.Input(key='avsandarekod')],
    [(sg.Text('Informationsägande organisation - Namn')), sg.Input(key='infoagarenamn')],
    [(sg.Text('Informationsägande organisation - Identitetskod')), sg.Input(key='infoagarekod')],
]

ovrigt2 = [
    [sg.Text('', font='Consolas 12', size=25)],
    [(sg.Text('Levererande system - Namn')), sg.Input(key='levererandesystemnamn')],
    [(sg.Text('Levererande system - Version')), sg.Input(key='levererandesystemversion')],
    [(sg.Text('Konsult - Namn')), sg.Input(key='konsultnamn')],
    [(sg.Text('Konsult - Identitetskod')), sg.Input(key='konsultidkod')],
    [(sg.Text('Mottagare - Namn')), sg.Input(key='mottagarenamn')],
    [(sg.Text('Mottagare - Identitetskod')), sg.Input(key='mottagareidkod')],
    [(sg.Text('Kontaktperson - Namn')), sg.Input(key='kontaktpersonnamn')],
    [(sg.Text('Kontatperson - Kontaktuppgifter')), sg.Input(key='kontaktuppgifter')],







]


# GUI layout
layout = [
    [sg.Column(paketinformation, vertical_alignment='top'), sg.Column(information)],
    [sg.Column(parter, vertical_alignment='top'), sg.Column(system, vertical_alignment='top'), sg.Column(innehall, vertical_alignment='top')],
    [sg.pin(sg.Column(overforing, vertical_alignment='top', key='non', visible=False))],
    [sg.pin(sg.Column(ovrigt, key='non2', visible=False)), sg.Column(ovrigt2, key='non3', visible=False)],
    [sg.Submit('Skapa paket', key='createSIP'), sg.Button('Visa/Dölj fält', key='fields')],
    [sg.Output(size=(100,7))]
    ]

window = sg.Window('FGS-Buddy v 0.8.1 - Viktor Lundberg', layout, font='Consolas 10')

forcedvaluesdict = {}
allvalues = False

# Program-Loop
while True:
    event, values = window.read()
    match event:
        case sg.WIN_CLOSED:
            break
        case 'createSIP':
            metadatafile = False
            schemafile = False
            subfolders = False

            # Kontrollerar alla obligatoriska värden!
            if values['submissionagreement'] == '' or values['system'] == '' or values['arkivbildare'] == '' or values['IDkod'] == '' or values['levererandeorganisation'] == '':
                forcedvaluesdict['System'] = values['system']
                forcedvaluesdict['Leveransöverenskommelse'] = values['submissionagreement']
                forcedvaluesdict['Arkivbildare'] = values['arkivbildare']
                forcedvaluesdict['Identitetskod'] = values['IDkod']
                forcedvaluesdict['Levererande organisation'] = values['levererandeorganisation']
                print('Du måste fylla i alla obligatoriska värden.')
                for k, v in forcedvaluesdict.items():
                    if v == '':
                        print(f'Fältet {k} saknar värde.')
                
            # OM ALLT ÄR OK KÖR PAKETET
            else:
                fgsPackage = FGSfunc.FgsMaker()
                fgsPackage.inputValues(values, False)
                if values['folder']== '':
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
        case 'fields':
            if allvalues == False:
                window['non'].Update(visible=True)
                window['non2'].Update(visible=True)
                window['non3'].Update(visible=True)
                allvalues = True
            else:
                window['non'].Update(visible=False)
                window['non2'].Update(visible=False)
                window['non3'].Update(visible=False)
                allvalues = False

            
            
            

            

    

'''
col1=[
[sg.Button('Skapa SIP', tooltip="TESTING")],
[sg.Input(tooltip="AAA"), sg.FolderBrowse('Välj katalog',key="-Fil-", ), sg.Submit('Submit')], 
[sg.pin(sg.Button('1', key = '_1_', visible=False))]
    ]

col2 = [
[sg.OptionMenu(values=['SIP', 'DIP'], default_value='SIP', key="-OAIS-"), sg.Button('Button', tooltip="TESTING")],
[sg.Combo(['Körv', 'Dricka'], default_value='Körv')],
[sg.Text('Arkivbildare fssssssssssssss'),sg.pin(sg.InputText(key='Arkivbildare')), sg.Text('SFSFSF')]]

layout = [[sg.Column(col1, background_color='Blue'), sg.Column(col2)]]

#[sg.Output(size=(125, 100), key=('_output_'), font='Consolas 10')]


windowchanger = 0
window = sg.Window('FGS-Buddy v 0.1 - Viktor Lundberg (c) 2022', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Start':
        print('Start')
        fgsPackage = FGSfunc.FgsMaker()
        fgsPackage.inputValues(True)
        fgsPackage.collectFiles(fgsPackage.pathToFiles, fgsPackage.subfolders)
        fgsPackage.createSip()
        fgsPackage.createFgsPackage(cwd)
    elif event == "Button":
        print(values['-OAIS-'])
    elif event == "Submit":
        print(values['-OAIS-'])
        for k, v in values.items():
            print(k,v)
        if windowchanger == 0:
            window['_1_'].Update(visible=True)
            windowchanger = 1
        else:
            window['_1_'].Update(visible=False)
            windowchanger = 0
'''
        
