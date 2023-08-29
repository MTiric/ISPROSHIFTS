import pyodbc
from datetime import datetime

print(datetime.now(), " - Vrijeme početka")

# this method connects to the database and returns desired channel shift data
def select_Kanal(kanal):
    try:
        cnxn = pyodbc.connect("Driver={SQL Server};"
                            "Server=10.215.100.16;"
                            "Database=ISPRO_ODS;"
                            "uid=ispro_monitor;"
                            "pwd=1$p4oM0n1t04123!")
    except:
        print("Couldn't connect to database ISPRO_ODS")
        import mailSendConnection
        print(datetime.now(), " - Vrijeme završetka")

    cursorGeneral=cnxn.cursor()
    cursorGeneral.execute("SELECT * FROM Monitoring.vw_LastShiftBySalesChannel WHERE SalesChannel=?", kanal)
    

    for row in cursorGeneral:
        print(row)
        varijablaGeneral=row
    cnxn.close()
    return varijablaGeneral


# this method gets the time from the last uploaded shift in database
def get_difference(date1, date2):
    delta=date2-date1
    hours=((delta.total_seconds())/3600)
    return hours


# this method is setting the "level" of the severity of missing shifts
def provjera_sati(sati, kanal):
    satiLVL =  [8, 16, 24]
    level=0

    if sati >= satiLVL[0] and sati < satiLVL[1]:
        print(kanal, "smjene nisu učitane dulje od 8 sati! Posljednja učitana - (", sati, ")")
        level=1
    elif sati >= satiLVL[1] and sati < satiLVL[2]:
        print(kanal, "smjene nisu učitane dulje od 16 sati!!! Posljednja učitana - (", sati, ")")
        level=2
    elif sati >= satiLVL[2]:
        print(kanal, "smjene nisu učitane dulje od 24 sata!!!!!!!!!! Posljednja učitana - (", sati, ")")
        level=3
    elif sati < 0:
        print(kanal, "ima smjene u budućnosti!!! - (", sati, ")")
        level=99
    else:
        print(kanal, "smjene su OK. Posljednja učitana - (", sati, ")")

    return level




flagDATA = True
try:
    hoursWEB=get_difference(select_Kanal("WEB application")[1], datetime.now())
except:
    print("There is no data for |WEB application|")
    flagDATA = None

try:
    hoursIntegration=get_difference(select_Kanal("INTEGRATION")[1], datetime.now())
except:
    print("There is no data for |INTEGRATION|")
    flagDATA = None    

try: 
    hoursSmartPhone=get_difference(select_Kanal("Smart phone")[1], datetime.now())
except:
    print("There is no data for |Smart phone|")
    flagDATA = None 

try:    
    hoursPOS=get_difference(select_Kanal("POS")[1], datetime.now())
except:
    print("There is no data for |POS|")
    flagDATA = None 

try:
    hoursHandheld=get_difference(select_Kanal("Handheld")[1], datetime.now())
except:
    print("There is no data for |Handheld|")
    flagDATA = None 

if flagDATA == None:
    import mailSendMissingContent

    
print("!!!!!\n\n!!!!!!\n\n!!!!!")


levelWEB=provjera_sati(hoursWEB, "WEB")
levelIntegration=provjera_sati(hoursIntegration, "Integration")
levelSmartphone=provjera_sati(hoursSmartPhone, "SmartPhone")
levelPOS=provjera_sati(hoursPOS, "POS")
levelHandheld=provjera_sati(hoursHandheld, "Handheld")


flag_ALL=0

if levelWEB >= 1 and levelSmartphone >= 1 and levelIntegration >= 1 and levelHandheld >= 1 and levelPOS >= 1 : flag_ALL=1  

elif levelWEB >= 2 and levelSmartphone >= 2 and levelIntegration >= 2 and levelHandheld >= 2 and levelPOS >= 2 : flag_ALL=2

elif levelWEB >= 3 and levelSmartphone >= 3 and levelIntegration >= 3 and levelHandheld >= 3 and levelPOS >= 3 : flag_ALL=3

elif levelWEB == 99 or levelSmartphone == 99 or levelIntegration == 99 or levelHandheld == 99 or levelPOS == 99 : flag_ALL=99


print("!!!\n!!!\n!!!\n!!!")


if flag_ALL == 1: 
    import mailSend8hours

elif flag_ALL == 2 : 
    import mailSend16hours

elif flag_ALL == 3 : 
    import mailSend24hours

elif flag_ALL == 99 :
    import mailSendFutureShift

elif hoursWEB > 2 or hoursSmartPhone > 2 or hoursHandheld > 16 or hoursPOS > 16:

    if hoursWEB > 2 or hoursSmartPhone > 2 : import mailSend2hoursWEB

    if hoursHandheld > 16 or hoursPOS > 16: import mailSend16hoursPOSHHT


print(datetime.now(), " - Vrijeme kraja")

