import os
import PySimpleGUI as sg
import psutil
import xml.etree.ElementTree as ET
import pyperclip
import requests


def serverpath(path):                                   # Узнать путь до папки Server
    servpath = path[:path.rfind('bin')]
    servpath = servpath[:servpath.rfind('Tomcat')]
    servpath = servpath.replace('"', '')
    return servpath


iiko_array = [['Нажмите Поиск']]
slist = list(psutil.win_service_iter())
islist = list()

headings = ['Имя', 'Версия', 'Порт', 'Период', 'Имя службы', 'Описание', 'Статус', 'Статус iiko']
right_click_menu = [''], ['Папка Server', 'Конфигуратор Tomcat', 'Лицензии', ['Все лицензии', ' '], 'Служба', ['Запустить', 'Остановить'], 'Логи', ['Все логи', 'Startup', 'Error']]

layout = [
    [sg.Button('Поиск', key='_localsearch_'), sg.Text(key='_ptext_'), sg.Text(expand_x=True), sg.Button('Статус iiko', key='_iikostatus_')],
    [sg.Table(values=iiko_array,
              headings=headings,
              auto_size_columns=True,
              justification='center',
              enable_events=True,
              expand_x=True,
              expand_y=True,
              key='_table_',
              enable_click_events=True,
              right_click_menu=right_click_menu,
              right_click_selects=True)],
    [sg.Text(expand_x=True), sg.Button('Отмена',)]
]

window = sg.Window('iiko Service Warden', layout, size=(1200, 600), resizable=True, return_keyboard_events=True)

while True:
    event, values = window.read()

    if event in (None, 'Exit', 'Отмена'):
        break

    elif event == 'c:67':                                           # Ctrl + c
        items = values['_table_']                                   # Indexes for selection
        lst = list(map(lambda x: ' '.join(iiko_array[x]), items))   # Get data list for selection
        text = "\n".join(lst)                                       # Each line for one selected row in table
        pyperclip.copy(text)

    elif event == 'Папка Server':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        os.system('explorer.exe ' + serverpath(islist[selrownum[0]].get('binpath')))

    elif event == 'Конфигуратор Tomcat':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        tompth = islist[selrownum[0]].get('binpath')
        tompth = tompth[:tompth.rfind('.exe')] + 'w.exe" //ES//' + islist[selrownum[0]].get('name')
        os.system(tompth)

    elif event == 'Все лицензии':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        licpth = serverpath(islist[selrownum[0]].get('binpath')) + 'data\\LicenseText.txt'
        lic_layout = [[sg.Text(expand_x=True), sg.Button('Обновить', key='_lic_refresh_')],
                          [sg.Multiline(key='_lic_', expand_x=True, expand_y=True, autoscroll=True,
                                        enable_events=True, reroute_stdout=True)]]
        lic_window = sg.Window('Лицензии', lic_layout, size=(850, 500), resizable=True, modal=True)
        ref = True
        while True:
            event, values = lic_window.read(100, '_f_lic_refresh_')
            if event in (None, 'Exit'):
                break
            if event == '_f_lic_refresh_' and ref:
                f = open(licpth, encoding='utf8')
                print(f.read())
                f.close()
                ref = False
            if event == '_lic_refresh_':
                f = open(licpth, encoding='utf8')
                lic_window['_lic_'].update('')
                print(f.read())
                f.close()
        lic_window.close()

    elif event == 'Все логи':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        os.system('explorer.exe ' + serverpath(islist[selrownum[0]].get('binpath')) + 'logs\\')

    elif event == 'Startup':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        lstup = serverpath(islist[selrownum[0]].get('binpath')) + 'logs\\'
        startup_layout = [[sg.Text(expand_x=True), sg.Button('Обновить', key='_startup_refresh_')],
                          [sg.Multiline(key='_startup_', expand_x=True, expand_y=True, autoscroll=True, enable_events=True, reroute_stdout=True)]]
        startup_window = sg.Window('Startup', startup_layout, size=(850, 500), resizable=True, modal=True)
        ref = True
        while True:
            event, values = startup_window.read(100, '_f_startup_refresh_')
            if event in (None, 'Exit'):
                break
            if event == '_f_startup_refresh_' and ref:
                f = open(lstup + 'startup.log', encoding='utf8')
                print(f.read())
                f.close()
                ref = False
            if event == '_startup_refresh_':
                f = open(lstup + 'startup.log', encoding='utf8')
                startup_window['_startup_'].update('')
                print(f.read())
                f.close()
        startup_window.close()

    elif event == 'Error':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        lerr = serverpath(islist[selrownum[0]].get('binpath')) + 'logs\\'
        startup_layout = [[sg.Text(expand_x=True), sg.Button('Обновить', key='_err_refresh_')],
                          [sg.Multiline(key='_error_', expand_x=True, expand_y=True, autoscroll=True,
                                        enable_events=True, reroute_stdout=True)]]
        startup_window = sg.Window('Error', startup_layout, size=(850, 500), resizable=True, modal=True)
        ref = True
        while True:
            event, values = startup_window.read(100, '_f_error_refresh_')
            if event in (None, 'Exit'):
                break
            if event == '_f_error_refresh_' and ref:
                f = open(lerr + 'error.log', encoding='utf8')
                print(f.read())
                f.close()
                ref = False
            if event == '_err_refresh_':
                f = open(lerr + 'error.log', encoding='utf8')
                startup_window['_error_'].update('')
                print(f.read())
                f.close()
        startup_window.close()

    elif event == 'Запустить':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        selsname = islist[selrownum[0]].get('name')
        os.system('net start ' + selsname)

    elif event == 'Остановить':
        selrownum = values['_table_']
        if selrownum == [] or iiko_array[0] == ['Нажмите Поиск']:
            window['_ptext_'].update('Выберите строку')
            continue
        selsname = islist[selrownum[0]].get('name')
        os.system('net stop ' + selsname)

    elif event == '_localsearch_':
        window['_ptext_'].update('Поиск...')
        window.refresh()
        iiko_array = [['Нажмите Поиск']]
        islist = list()
        for i in range(len(slist)):                                                 # Составляется список служб
            pth = slist[i].as_dict().get('binpath')
            p = pth.find('Tomcat')
            if p != -1:
                islist.append(slist[i].as_dict())
        if len(islist) == 0:
            iiko_array = [['Не найдено']]

        for i in range(len(islist)):
            pth = serverpath(islist[i].get('binpath'))

            licpth = pth + 'data\\'                                                 # Узнать имя
            lic = open(licpth + 'LicenseText.txt', encoding='utf8')
            sname = lic.readlines()[1]
            sname = sname[(sname.find(':') + 2):]
            sname = sname[:(sname.find('\n'))]

            expth = pth + 'exploded\\update\\'                                      # Узнать версию
            upd = open(expth + 'updates.ini', encoding='utf8')
            version = upd.readlines()[2]
            version = version[8:]
            version = version[:(version.find('\n'))]

            tcpth = islist[i].get('binpath')[:islist[i].get('binpath').rfind('bin')] + 'conf\\'  # Узнать порт
            tcpth = tcpth.replace('"', '')
            tree = ET.parse(tcpth + 'server.xml')
            root = tree.getroot()
            for elem in root:
                for subelem in elem.findall('Connector'):
                    try:
                        port = subelem.get('port')
                    except Exception:
                        port = 'Не найдено'

            confpth = pth + 'config\\resto.properties'                              # Узнать период
            f = open(confpth)
            period = '~60'
            for line in f:
                if line.find('db-period-length-days') != -1:
                    period = line[line.rfind('=')+1:]
            f.close()

            if iiko_array[0] == ['Нажмите Поиск']:                                  # Вывод на окно всего, кроме статуса iiko
                iiko_array = [[sname, version, port, period, islist[i].get('display_name'), islist[i].get('description'), islist[i].get('status'), '']]
            else:
                iiko_array.append([sname, version, port, period, islist[i].get('display_name'), islist[i].get('description'), islist[i].get('status'), ''])

            window['_table_'].update(iiko_array)
            window.refresh()

        window['_ptext_'].update('Готово')

    elif event == '_iikostatus_':                                                   # Узнать статус iiko
        if iiko_array != [['Нажмите Поиск']]:
            for i in range(len(islist)):
                url = 'http://localhost:' + iiko_array[i][2] + '/resto/getServerMonitoringInfo.jsp'
                try:
                    req = requests.get(url)
                    sstate = req.json().get('serverState')
                except:
                    sstate = 'Неизвестно'
                iiko_array[i][7] = sstate                                           # Вывод на окно статуса iiko
                window['_table_'].update(iiko_array)
                window.refresh()


window.close()
