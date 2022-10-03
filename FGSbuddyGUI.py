import os
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc

cwd = os.getcwd()
sg.theme('LightGreen2')

column1 = [
    [sg.Text('Arkivbildare - Namn*', tooltip='<mets><metsHdr><agent ROLE=”ARCHIVIST” TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Arkivbildaren',key='arkivbildare', tooltip='''Namn på arkivbildaren. 
Arkivbildaren är den organisation som har skapat arkivmaterialet''',)],
    [sg.Text('Identitetskod*')],
    [sg.Combo(['VAT', 'DUNS', 'ORG','HSA','Local', 'URI'], default_value='ORG', key='IDkodtyp'),sg.Input('koden', key='IDkod')],
    [sg.Text('Levererande organisation - Namn*', tooltip='<mets><metsHdr><agent ROLE="Creator" TYPE=”ORGANIZATION”><name>[Arkivbildare Namn]') ],
    [sg.Input('Organisationen',key='levererandeorganisation', tooltip='''Namn på den organisation som levererat SIP:en till e-arkivet. 
Denna organisation är ofta identisk med den som anges som arkivbildare. Det skiljer sig i de fall där en myndighet övertagit en annan myndighets arkiv''')],
    [sg.Button('Byt färg', key='tema')]
    ]

column2 = [
    [sg.Text('System*')],
    [sg.Input(default_text ='SYSTEMET', key='system')],
    [sg.Text('Informationstyp*')],
    [sg.Combo(['ERMS','Personnel','Medical record','Economics','Databases','Webpages', 'GIS', 'No specification', 'AIC', 'Archival information','Unstructured', 'Single records', 'Publication'], default_value='ERMS', key='informationstyp')],
    [sg.Text('Status*')],
    [sg.Combo(['NEW', 'SUPPLEMENT', 'REPLACEMENT','TEST','VERSION', 'OTHER'], default_value='NEW', key='recordstatus')],
    [sg.Text('Leveransöverenskommelse*')],
    [sg.Input('Submissionagremmentnernrenre',key='submissionagreement')],
    [sg.Text('Sökväg till filer*')],
    [sg.Input(default_text=cwd,tooltip="Välj katalog"), sg.FolderBrowse('Välj katalog',key="folder", initial_folder=os.path.join(cwd))],
    [sg.Text('Inkludera undermappar')],
    [sg.Radio('Ja', 'subfolders', default=False, key='subfolderstrue'), sg.Radio('Nej', 'subfolders', default=True, key='subfoldersfalse')],
    [sg.Text('Sökväg till metadatafilen*')],
    [sg.Input(tooltip="Välj katalog"), sg.FileBrowse('Välj fil',key="metadatafile", initial_folder=os.path.join(cwd))],
    [sg.Text('Sökväg till schemafil*')],
    [sg.Input(tooltip="Välj katalog"), sg.FileBrowse('Välj fil',key="schemafile", initial_folder=os.path.join(cwd))],

    ]

layout = [[sg.Column(column1, vertical_alignment='top'), sg.Column(column2)], [sg.Submit('Skapa paket', key='createSIP')]]

window = sg.Window('FGS-Buddy v 0.6 - Viktor Lundberg', layout, font='Consolas 10')


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
            #SKAPA KONTROLL PÅ OBLIGATORISKA VÄRDEN
            if values['submissionagreement'] == '' or values['system'] == '':
                print('tttt')
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
        case 'tema':
            print(f"{values['schemafile']}")
            
            

            

    

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
        
