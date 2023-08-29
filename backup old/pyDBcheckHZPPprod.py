import pyodbc
##import mailSend8hours as alert8
##import mailSend16hours as alert16
##import mailSend24hours as alert24


from datetime import datetime

print(datetime.now(), " - Vrijeme početka")
cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=10.215.100.16;"
                      "Database=ISPRO_ODS;"
                      "uid=ispro_monitor;"
                      "pwd=1$p4oM0n1t04123!")

def get_difference(date1, date2):
    delta=date2-date1
    hours=((delta.total_seconds())/3600)
    return hours

def provjera_sati(sati, kanal): 
    satiPrvaRazina=8
    satiDrugaRazina=16
    satiTrecaRazina=24
    razina=0
    if sati >= satiPrvaRazina and sati <= satiDrugaRazina:
        print(kanal, "smjene nisu učitane dulje od 8 sati! Posljednja učitana - (", sati, ")")
        razina=1
    elif sati >= satiDrugaRazina and sati <= satiTrecaRazina:
        print(kanal, "smjene nisu učitane dulje od 16 sati!!! Posljednja učitana - (", sati, ")")
        razina=2
    elif sati >= satiTrecaRazina:
        print(kanal, "smjene nisu učitane dulje od 24 sata!!!!!!!!!! Posljednja učitana - (", sati, ")")
        razina=3
    elif sati < 0:
        print(kanal, "ima smjene u budućnosti!!! - (", sati, ")")
        razina=99
    else:
        print(kanal, "smjene su OK. Posljednja učitana - (", sati, ")")
    return razina




def select_Kanal(kanal):
    cursorGeneral=cnxn.cursor()
    
    ##cursorGeneral.execute("SELECT * FROM Monitoring.Smjene_POC WHERE Kanal=?", kanal)
    cursorGeneral.execute("SELECT * FROM Monitoring.vw_LastShiftBySalesChannel WHERE SalesChannel=?", kanal)
    for row in cursorGeneral:
        print(row)
        varijablaGeneral=row
    return varijablaGeneral


##varijablaZebra3=select_Kanal("PID Zebra ZXP series 3")
varijablaWEB=select_Kanal("WEB application")
varijablaIntegration=select_Kanal("INTEGRATION")  
varijablaSmartPhone=select_Kanal("Smart phone")
##varijablaZebra7=select_Kanal("PID Zebra ZXP series 7")
varijablaPOS=select_Kanal("POS") 
varijablaHandheld=select_Kanal("Handheld")
##varijablaPortal=select_Kanal("Portal")






today=datetime.now()
##zadnjaSmjenaZebra3=varijablaZebra3[1]
zadnjaSmjenaWEB=varijablaWEB[1]
zadnjaSmjenaIntegration=varijablaIntegration[1]
zadnjaSmjenaSmartPhone=varijablaSmartPhone[1]
##zadnjaSmjenaZebra7=varijablaZebra7[1]
zadnjaSmjenaPOS=varijablaPOS[1]
zadnjaSmjenaHandheld=varijablaHandheld[1]
##zadnjaSmjenaPortal=varijablaPortal[1]






##hoursZebra3=get_difference(zadnjaSmjenaZebra3, today)
hoursWEB=get_difference(zadnjaSmjenaWEB, today)
hoursIntegration=get_difference(zadnjaSmjenaIntegration, today)
hoursSmartPhone=get_difference(zadnjaSmjenaSmartPhone, today)
##hoursZebra7=get_difference(zadnjaSmjenaZebra7, today)
hoursPOS=get_difference(zadnjaSmjenaPOS, today)
hoursHandheld=get_difference(zadnjaSmjenaHandheld, today)
##hoursPortal=get_difference(zadnjaSmjenaPortal, today)






flag_ALL=0



print("!!!!!\n\n!!!!!!\n\n!!!!!")


##levelZebra3=provjera_sati(hoursZebra3, "PID Zebra ZXP series 3")
levelWEB=provjera_sati(hoursWEB, "WEB")
levelIntegration=provjera_sati(hoursIntegration, "Integration")
levelSmartphone=provjera_sati(hoursSmartPhone, "SmartPhone")
##levelZebra7=provjera_sati(hoursZebra7, "PID Zebra ZXP series 7")
levelPOS=provjera_sati(hoursPOS, "POS")
levelHandheld=provjera_sati(hoursHandheld, "Handheld")
##levelPortal=provjera_sati(hoursPortal, "Portal")






##if levelWEB >= 1 and levelIntegration >= 1 and levelSmartphone >= 1  and levelHandheld >= 1 and levelPOS >= 1 and levelZebra3 >= 1 and levelZebra7 >= 1: flag_ALL=1
    
##if levelWEB >= 2 and levelIntegration >= 2 and levelSmartphone >= 2  and levelHandheld >= 2 and levelPOS >= 2 and levelZebra3 >= 2 and levelZebra7 >= 2: flag_ALL=2

##if levelWEB >= 3 and levelIntegration >= 3 and levelSmartphone >= 3  and levelHandheld >= 3 and levelPOS >= 3 and levelZebra3 >= 3 and levelZebra7 >= 4: flag_ALL=3

##if levelWEB == 99 or levelIntegration == 99 or levelSmartphone == 99 or levelHandheld == 99 or levelPOS == 99 and levelZebra3 == 99 and levelZebra7 == 99: flag_ALL=99


if levelWEB >= 1 and levelSmartphone >= 1 and levelIntegration >= 1 and levelHandheld >= 1 and levelPOS >= 1 : flag_ALL=1
    
if levelWEB >= 2 and levelSmartphone >= 1 and levelIntegration >= 2 and levelHandheld >= 2 and levelPOS >= 2 : flag_ALL=2

if levelWEB >= 3 and levelSmartphone >= 1 and levelIntegration >= 3 and levelHandheld >= 3 and levelPOS >= 3 : flag_ALL=3

if levelWEB == 99 or levelSmartphone == 99 or levelIntegration == 99 or levelHandheld == 99 or levelPOS == 99 : flag_ALL=99


print("!!!\n!!!\n!!!\n!!!")


if flag_ALL == 1:
    import mailSend8hours as alert8
elif flag_ALL == 2 :
    import mailSend16hours as alert16
elif flag_ALL == 3 :
    import mailSend24hours as alert24
elif flag_ALL == 99 :
    import mailSendFutureShift as alertF
elif hoursWEB > 2 or hoursSmartPhone > 2 or hoursHandheld > 16 or hoursPOS > 16:
    if hoursWEB > 2 or hoursSmartPhone > 2 : import mailSend2hoursWEB
    if hoursHandheld > 16 or hoursPOS > 16: import mailSend16hoursPOSHHT as alertPOSHHT16h

    

cnxn.close()
print(datetime.now(), " - Vrijeme kraja")

