#!/usr/bin/env python
# coding: utf-8


from pyvirtualdisplay import Display
from selenium import webdriver
from datetime import datetime
from datetime import date
import time
from prettytable import PrettyTable
import smtplib
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)


username = "YOUR USERNAME HERE"
password = "YOUR PASSWORD HERE"
empresa = "YOUR BUSINESS HERE"
empresa2 = "YOUR SECOND BUSINESS HERE"
profissional_empresa_1 = "YOUR PROFESSIONAL NUMBER HERE"
profissional_empresa_2 = "YOUR PROFESSIONAL NUMBER HERE"

def replacing(string_para_salvar):
    st = string_para_salvar.replace("é", "e")
    st = st.replace("É", "E")
    st = st.replace("é", "e")
    st = st.replace("Ã", "A")
    st = st.replace("Â", "A")
    st = st.replace("â", "a")
    st = st.replace("Á", "A")
    st = st.replace("á", "a")
    st = st.replace("ã", "a")
    st = st.replace("Õ", "O")
    st = st.replace("Ô", "O")
    st = st.replace("Ó", "O")
    st = st.replace("õ", "o")
    st = st.replace("ô", "o")
    st = st.replace("ó", "o")
    st = st.replace("ê", "e")
    st = st.replace("Ê", "E")
    st = st.replace("Í", "I")
    st = st.replace("í", "i")
    st = st.replace("ç", "c")
    st = st.replace("Ç", "C")
    return st

def pagina(profissional):
    dia = datetime.now().strftime("%d")
    dia = int(dia)
    dia = dia + 1
    dia = str(dia)
    mes = datetime.now().strftime("%m")
    mes = str(mes)
    ano = datetime.now().strftime("%Y")
    ano = str(ano)
    url_part_1 = "http://popserver.com.br/easy/agendamento.php?mes="
    url_part_2 = str("%s&ano=%s&dia="%(mes, ano))
    url_part_3 = str("%s&profissional=%s&paciente=&acao=montar"%(dia, profissional))
    url = str(url_part_1+url_part_2+url_part_3)
    print(url)
    return url

def login(username, password, empresa):
    find_user = wd.find_element_by_xpath('//*[@id="username"]')
    find_user.send_keys(username)
    find_password = wd.find_element_by_id("psw")
    find_password.send_keys(password)
    find_empresa = wd.find_element_by_id("empresa")
    find_empresa.send_keys(empresa)
    wd.find_element_by_xpath('//*[@id="myModal"]/div/div/div[2]/form/button').click()

def horario(n):
    xp = str("/html/body/div[3]/font[%d]"%(n))
    try:
        xp_hora = wd.find_element_by_xpath(xp)
        txt_xp_hora = xp_hora.text
    except Exception:
        txt_xp_hora = "vazio"
    return txt_xp_hora

def sendmail(strpttable):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('YOUR EMAIL HERE', 'YOUR PASSWORD HERE')
    dia = datetime.now().strftime("%d")
    dia = int(dia)
    dia = dia + 1
    dia = str(dia)
    mes = datetime.now().strftime("%m")
    mes = str(mes)
    ano = datetime.now().strftime("%Y")
    ano = str(ano)
    data = str(dia+"."+mes+"."+ano)
    subject = str("Agenda do dia %s"%(data))
    body = strpttable
    msg = str(subject+"\n\n\n"+body)
    server.sendmail(
        'SENDER MAIL',
        'RECEIVER MAIL',
        msg
    )
    print("email enviado")
    server.quit()

def dia_da_semana():
    dia = datetime.now().strftime("%d")
    dia = int(dia)
    mes = datetime.now().strftime("%m")
    mes = int(mes)
    ano = datetime.now().strftime("%Y")
    ano = int(ano)
    data = date(year=ano, month=mes, day=dia)
    week_day = data.isoweekday()
    return week_day

week_day = dia_da_semana()

if week_day == 4 :
    try:
        pagina = pagina(profissional_empresa_1)
        wd.get("https://popserver.com.br/easy")
        time.sleep(5)
        login(username, password, empresa)
        time.sleep(6)
        wd.get(pagina)

        time.sleep(5)
        ####### NOVO ENVIO #######
        try:
            x = PrettyTable()
            html = wd.page_source
            time.sleep(5)

            soup = BeautifulSoup(html, "lxml")


            #strhtm = soup.prettify()
            strhtm = str(soup)

            hrs = soup.find_all('font')
            pacientes = soup.find_all('a', class_='btn btn-info btn-xs')

            hrlist = []

            for hr in hrs:
                hrstr = str(hr.text)
                hrlist.append(hrstr)
            if "\n" in hrlist[0]:
                del hrlist[0]

            x.field_names = ["HORARIO", "PACIENTES"]

            n = 0

            for hr in hrlist:
                hrstr = str(hr)

                if "tervalo" in hrstr:
                    linha = [hrstr, "  "]
                    x.add_row(linha)

                else:
                    hrinit= strhtm.find(hrstr) + 30
                    hrfin = strhtm.find(hrstr) + 41
                    teste_vacancia = strhtm[hrinit:hrfin]
                    if "su" in teste_vacancia:
                        linha = [hrstr, "Horario Fechado"]
                        n = n+0
                        x.add_row(linha)
                    else:
                        try:
                            caso = str(pacientes[n].text)
                            paciente = replacing(caso)
                            linha = [hrstr, paciente]
                            x.add_row(linha)
                        except:
                            linha = [hrstr, "  "]
                            x.add_row(linha)
                        n=n+1

            print(x)
            strpttable = str(x)
            sendmail(strpttable)

        except:

            print("novo método não funcionou")

            ########### ENVIO CONVENCIONAL######

            agenda = ([horario(1)],
                      [horario(2)],
                      [horario(3)],
                      [horario(4)],
                      [horario(5)],
                      [horario(6)],
                      [horario(7)],
                      [horario(8)],
                      [horario(9)],
                      [horario(10)],
                      [horario(11)],
                      [horario(12)],
                      [horario(13)],
                      [horario(14)]
                      )

            pttable = PrettyTable()
            pttable.add_row(agenda[0])
            pttable.add_row(agenda[1])
            pttable.add_row(agenda[2])
            pttable.add_row(agenda[3])
            pttable.add_row(agenda[4])
            pttable.add_row(agenda[5])
            pttable.add_row(agenda[6])
            pttable.add_row(agenda[7])
            pttable.add_row(agenda[8])
            pttable.add_row(agenda[9])
            pttable.add_row(agenda[10])
            pttable.add_row(agenda[11])
            pttable.add_row(agenda[12])
            pttable.add_row(agenda[13])

            strpttable = str(pttable)
            sendmail(strpttable)

    except Exception as err:
        err = str(err)
        sendmail(err)

if week_day == 2 :
    try:
        pagina = pagina(profissional_empresa_2)
        wd.get("https://popserver.com.br/easy")
        time.sleep(5)
        login(username, password, empresa2)
        time.sleep(6)
        wd.get(pagina)
        time.sleep(5)
        ####### NOVO ENVIO #######
        try:
            x = PrettyTable()
            html = wd.page_source
            time.sleep(5)

            soup = BeautifulSoup(html, "lxml")


            #strhtm = soup.prettify()
            strhtm = str(soup)

            hrs = soup.find_all('font')
            pacientes = soup.find_all('a', class_='btn btn-info btn-xs')

            hrlist = []

            for hr in hrs:
                hrstr = str(hr.text)
                hrlist.append(hrstr)
            if "\n" in hrlist[0]:
                del hrlist[0]

            x.field_names = ["HORARIO", "PACIENTES"]

            n = 0

            for hr in hrlist:
                hrstr = str(hr)

                if "tervalo" in hrstr:
                    linha = [hrstr, "  "]
                    x.add_row(linha)

                else:
                    hrinit= strhtm.find(hrstr) + 30
                    hrfin = strhtm.find(hrstr) + 41
                    teste_vacancia = strhtm[hrinit:hrfin]
                    if "su" in teste_vacancia:
                        linha = [hrstr, "Horario Fechado"]
                        n = n+0
                        x.add_row(linha)
                    else:
                        try:
                            caso = str(pacientes[n].text)
                            paciente = replacing(caso)
                            linha = [hrstr, paciente]
                            x.add_row(linha)
                        except:
                            linha = [hrstr, "  "]
                            x.add_row(linha)
                        n=n+1

            print(x)
            strpttable = str(x)
            sendmail(strpttable)

        except:

            print("novo método não funcionou")

            ########### ENVIO CONVENCIONAL######

            agenda = ([horario(1)],
                      [horario(2)],
                      [horario(3)],
                      [horario(4)],
                      [horario(5)],
                      [horario(6)],
                      [horario(7)],
                      [horario(8)],
                      [horario(9)],
                      [horario(10)],
                      [horario(11)],
                      [horario(12)],
                      [horario(13)],
                      [horario(14)],
                      [horario(15)],
                      [horario(16)],
                      [horario(17)],
                      [horario(18)],
                      [horario(19)],
                      [horario(20)],
                      [horario(21)],
                      [horario(22)],
                      [horario(23)],
                      [horario(24)],
                      [horario(25)],
                      [horario(26)],
                      [horario(27)],
                      [horario(28)],
                      [horario(29)],
                      [horario(30)]
                      )

            pttable = PrettyTable()
            pttable.add_row(agenda[0])
            pttable.add_row(agenda[1])
            pttable.add_row(agenda[2])
            pttable.add_row(agenda[3])
            pttable.add_row(agenda[4])
            pttable.add_row(agenda[5])
            pttable.add_row(agenda[6])
            pttable.add_row(agenda[7])
            pttable.add_row(agenda[8])
            pttable.add_row(agenda[9])
            pttable.add_row(agenda[10])
            pttable.add_row(agenda[11])
            pttable.add_row(agenda[12])
            pttable.add_row(agenda[13])
            pttable.add_row(agenda[14])
            pttable.add_row(agenda[15])
            pttable.add_row(agenda[16])
            pttable.add_row(agenda[17])
            pttable.add_row(agenda[18])
            pttable.add_row(agenda[19])
            pttable.add_row(agenda[20])
            pttable.add_row(agenda[21])
            pttable.add_row(agenda[22])
            pttable.add_row(agenda[23])
            pttable.add_row(agenda[24])
            pttable.add_row(agenda[25])
            pttable.add_row(agenda[26])
            pttable.add_row(agenda[27])
            pttable.add_row(agenda[28])
            pttable.add_row(agenda[29])

            strpttable = str(pttable)
            sendmail(strpttable)

    except Exception as err:
        err = str(err)
        sendmail(err)

wd.quit()
quit()