# Non working version!!!
import os
import PySimpleGUI as sg
import fgsbuddyfunctions as FGSfunc

cwd = os.getcwd()
sg.theme('LightGreen2')

layout = [[sg.Button('Start', tooltip="TESTING"), ],[sg.Input(tooltip="AAA"), sg.FileBrowse('Välj fil',key="-Fil-"), sg.Submit('Submit')],[sg.Output(size=(125, 100), key=('_output_'), font='Consolas 10')]]


window = sg.Window('FGS-Buddy v 0.1 - Viktor Lundberg (c) 2022', layout, size=(700, 600), element_justification='c')

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