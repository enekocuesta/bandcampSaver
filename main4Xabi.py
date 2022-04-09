# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import shutil
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import Button
#import win32api
import os
import pathlib
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
#Globals
thisPath = pathlib.Path().resolve()
lista_No_Descargados = []
download_path = "C:/Users/Eneko Cuesta/Downloads"

#Methods
def listaSinHacer(sinHacer):
    String = ''
    for song in sinHacer:
        String = String+'\n'+song
    return String


def cambiarNombreEnSuCarpeta(root, name, newName, i):
    try:
        os.rename(os.path.join(root, name), os.path.join(root, newName))
    except FileExistsError:
        cambiarNombreEnSuCarpeta(root,name,'('+str(i)+')_'+newName,i+1)
        #os.rename(os.path.join(root, name), os.path.join(root, newName+'_'+str(i)))


def guardarEspeciales(file,path, name): #Deprecated
    try:
        file.write(path+'/'+name+"\n")
    except UnicodeEncodeError:
        print("Ey yo' Un error raro de unicode, probablemente por intentar renombrar un zip tocho")
        print("Exactamente: \n UnicodeEncodeError: 'charmap' codec can't encode character '\u200b' in position 43: character maps to <undefined>")

def changeName(): #cambiar nombres
    try:

        i=1
        print("Iniciando cambiador de nombres...")
        path = askdirectory(
            title='Elige la carpeta grande en la que guardes todos los tunes que quieras renombrar')  # shows dialog box and return the path
        files = os.listdir(path)
        sinHacer = []
        #newRoot = path + '/Casos_Especiales'
        #if (not os.path.isdir(newRoot)):
        #    os.mkdir(newRoot)
        file = open(path + "/Casos_especiales.txt", "w")
        for root, directories, files in os.walk(path, topdown=False):
            for name in files:
                #newName = name.split(' - ')
                #Regex \s(\d\d)\s.+$

                x = re.search(r"\s(\d\d)\s.+$", name)
                if(x == None):
                    if ('.png' not in name and '.jpg' not in name and ".pdf" not in name and '.txt' not in name and '.JPG' not in name):
                        i=1
                        sinHacer.append(root+ '\\' + name)
                        print('\n---\nEl siguiente documento no se ha renombrado: ' + os.path.join(root, name)+"\n---\n")
                        #print('\nSe movera a: '+ os.path.join(newRoot, name)+"\n")
                        #os.replace(os.path.join(root, name), os.path.join(newRoot, name))
                        guardarEspeciales(file,root,name)
                else:
                    newName = x.group()
                    #print(newName)
                    cambiarNombreEnSuCarpeta(root,name,newName,i)
                    i=i+1


        file.close()
        if(len(sinHacer)>0):
            messagebox.showwarning(title='Casos excepcionales',
                                message="No se han cambiado los nombres de algunos archivos, se guardaran en un documento llamado: Casos_especiales.txt")
        # Press the green button in the gutter to run the script.
        messagebox.showinfo(title='Informacion adicional',
                            message="Realizado por: Eneko Cuesta\n" "Custom made para: @Xabi_Brutality")
    except FileNotFoundError:
        print("No se ha encontrado el directorio")
        messagebox.showerror(title="Errorazo selektah", message="No se ha encontrado el directorio")


def login(): #deprecated
    try:
        #path = askdirectory(
        #    title='Elije la carpeta en la que quieras descargar')  # shows dialog box and return the path
        #print("Va a descargar en " + path)

        #Aqui empieza selenium

        # Crear una sesión de Firefox
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.maximize_window()

        # Acceder a la aplicación web
        driver.get("https://bandcamp.com/login")

        # Localizar cuadro de texto
        Usuario = driver.find_element_by_id("username-field")
        Usuario.clear()

        # Indicar y confirmar término de búsqueda
        Usuario.send_keys("Usuario")
        Usuario.submit()

        # Localizar cuadro de texto
        Contraseña = driver.find_element_by_id("password-field")
        Contraseña.clear()
        driver.implicitly_wait(30)
        # Indicar y confirmar término de búsqueda
        Contraseña.send_keys("Contraseña")
        Contraseña.submit()

        # Obtener la lista de resultados de la búsqueda y mostrarla
        # mediante el método find_elements_by_class_name
        lists = driver.find_elements_by_class_name("_Rm")

        # Pasar por todos los elementos y reproducir el texto individual

        i = 0
        for listitem in lists:
            print(listitem.get_attribute("innerHTML"))
            i = i + 1
            if (i > 10):
                break

        # Cerrar la ventana del navegador
        driver.quit()





    except FileNotFoundError:
        print("Directorio no encontrado guey")
        messagebox.showerror(title="Errorazo selektah", message="No se ha encontrado el directorio")

def scroll(driver):
    # scrollear hasta el final
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def check_if_replayable(driver):
    try:
        driver.find_element_by_link_text("Click here") #para el caso de error click again
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        print("Ha sido un error de carga")
    except:
        pass


def not_avaiable(driver): #devuelve false si esta disponible
    try:
        driver.find_element_by_link_text("Download")
        #print("Puede descargar")
        return False
    except: #devuelbe true si NO esta disponible
        check_if_replayable(driver)
        return True

def getNumberSongs():
    with open('conf.txt') as f:
        lines = f.readlines()
        for line in lines:
            if (len(lines) > 2):
                number = int(lines[2].strip('\n'))
            else:
                number = 40
    f.close()
    return number

def setLastSong(currentSong):
    try:
        with open('conf.txt') as f:
            lines = f.readlines()
            f.close()
        os.remove('conf.txt')
        file = open('conf.txt', 'w')
        file.write(lines[0] + lines[1] + lines[2] + currentSong)
        file.close()
    except UnicodeEncodeError:
        file.write(lines[0] + lines[1] + lines[2])
        file.close()
        print("Encode error, calling again")
        setLastSong(currentSong.replace("\u200b", "_"))


def has_it_arrived(currentSong):
    #print("Has it arrived?")
    if(getLastSong() == ''):
        #print("Yes, esta vacio")
        return True
    else:
        #print("No esta vacio")
        if(currentSong == getLastSong()):
            print("Arrived  :-  "+currentSong +" == "+getLastSong())
            print("\n---    It has STARTED    ---\n")
            return True



def is_there_song(driver):
    try:
        time.sleep(0.5)
        song = driver.find_element_by_xpath("//div[@class ='free-download download']/div[@class='title']").get_attribute('innerHTML')  # recojer nombre de la cancion
        #print("there is: " + song)
        return True
    except NoSuchElementException:
        return False


def descargable(driver):
    try:
        # preparing = driver.find_element_by_link_text("Preparing")
        #preparing_el = driver.find_element_by_xpath("//span[@class='preparing']")
        #preparing_title_el = driver.find_element_by_xpath("//span[@class='preparing-title']")

        #preparing = preparing_el.is_displayed()
        #preparing_title = preparing_title_el.is_displayed()

        #checkear si el item-format button style="display: none;


        #print(str(preparing_title) + ": Prepared - visible")

        estilo = driver.find_element_by_xpath("//div[@class='item-format button']").get_attribute("style")
        #print("Style: " + estilo)
        #preparing_title or preparing or
        if (estilo != "display: none;"): # si es distinto a no tener estilo
            return True
        else:
            #return (not not_avaiable())
            href = driver.find_element_by_xpath("//a[@class='item-button']").get_attribute("href")
            driver.get(href)
            print("-- ESTE NO SE PUEDE DESCARGAR --")
            return False
    except:
        print("\nDescargable? exception")
        return False
        # print("prep: "+driver.find_element_by_link_text("Preparing"))
        # print("type: " + driver.find_element_by_xpath("//div[@class ='type']").get_attribute('innerHTML'))
        # print("\n")


def registrarNoDescargadas():
    try:
        if(len(lista_No_Descargados) > 0):
            file = open('No_Descargados.txt', 'w')
            for cancion in lista_No_Descargados:
                file.write(cancion+'\n')
            file.close()
    except:
        print("No ha podido printear la lista de las no descargadas")


def getCurrentSong(driver):
    try:
        return driver.find_element_by_xpath("//div[@class ='free-download download']/div[@class='title']").get_attribute('innerHTML')  # recojer nombre de la cancion
    except:
        print("Couldn't get name")
        return "No es valido"
        pass


def has_already(currentSong):
    try:
        found = False

        for root, directories, files in os.walk(download_path, topdown=False):
            for file in files:
                if(file.__contains__('.zip')):
                    if (file.__contains__(currentSong.split(' ...')[0])):
                        found=True
                    else:
                        print("file: "+file)
        fileShould = 'Concrete &amp; Steel (Gorgon Sound &amp;...'
        filename='Dubkasm - Concrete & Steel'
        fileShould_spl = fileShould.split("...",1)
        if(filename.__contains__(fileShould_spl[0])):
            print("eureka!")

        print(currentSong.split(' ...')[0])
        print("Found?: "+str(found))
        return found
    except:
        print("exception has_already")
        return False


def cambiarCalidad(driver):
    try:
        calidades = driver.find_elements_by_xpath("//li/span[@class ='description']")
        boton_seleccionador = driver.find_element_by_xpath("//div[@class='format-type']")
        boton_seleccionador.click()
        for calidad in calidades:
            #print(calidad.get_attribute('innerHTML'))
            if ((not calidad.is_selected()) and calidad.get_attribute('innerHTML') == 'WAV'):
                calidad.click()
        boton_seleccionador.click()
    except:
        pass


def download(): #para descargar
    try:
        #path = askdirectory(
        #    title='Elije la carpeta en la que quieras descargar')  # shows dialog box and return the path
        #print("Va a descargar en " + path)

        #Aqui empieza selenium

        #Profile load 'C:/Users/XABIER/AppData/Roaming/Mozilla/Firefox/Profiles/b6faao4y.default-release'
        #'C:/Users/Eneko Cuesta/AppData/Roaming/Mozilla/Firefox/Profiles/zrmc1nzx.default-release'
        fp = webdriver.FirefoxProfile('C:/Users/XABIER/AppData/Roaming/Mozilla/Firefox/Profiles/b6faao4y.default-release')
        #fp = webdriver.FirefoxProfile('C:/Users/Eneko Cuesta/AppData/Roaming/Mozilla/Firefox/Profiles/zrmc1nzx.default-release')
        #profile change
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/zip")
        # Crear una sesión de Firefox
        driver = webdriver.Firefox(firefox_profile=fp)
        driver.maximize_window()

        # Acceder a la aplicación web
        driver.get("https://bandcamp.com/xabirasta/purchases")


        #localizar show more
        driver.find_element_by_class_name("view-all-button").click()



        #scroll
        scroll(driver)
        time.sleep(3)
        #scroll
        scroll(driver)


        #getNumber songs
        number = getNumberSongs()
        print ("number: "+str(number))

        #get Last song
        lastSong = getLastSong()
        print("lastSong: "+lastSong)

        #localizar todos los botones de download
        descargadores = driver.find_elements_by_xpath("//div[@class='purchases-item-download']/a")

        # Store the ID of the original window
        original_window = driver.current_window_handle

        #cuantas va
        index = 0 # 0 al principio
        arrived=False
        for descarga in descargadores: #por cada boton de descarga (nueva pestaña)
            descarga.click() #hacer clik
            time.sleep(1) #esperar
            window_after = driver.window_handles[1] #siempre sera el uno #pasar a la nueva pestaña
            driver.switch_to.window(window_after) #pasar

            #currentSong
            thereIsSong = False
            auxCont = 30
            while(thereIsSong == False and auxCont != 0): #para que no se quede pillau
                thereIsSong = is_there_song(driver)
                auxCont = auxCont-1
            #setLastSong(currentSong)

            currentSong = getCurrentSong(driver)

            print("currentSong: "+currentSong)
            already = False

            if(arrived and currentSong != "No es valido"): #si ya ha llegado
                index = index+1
                i = 0
                esta = True
                cambiarCalidad(driver)

                while not_avaiable(driver):
                    time.sleep(0.5)
                    #i = i + 1

                    #check if has type

                    #childs = driver.find_element_by_xpath("//div[@class ='type']").get_attribute('innerHTML')
                    #dscargable = descargable(driver)

                    if (not descargable(driver)): #Si no cumple las condiciones para ser descargable
                        esta = False #para saltarlo
                        lista_No_Descargados.append(currentSong)
                        break #salir del buble

                if (esta):
                    down = driver.find_element_by_link_text("Download")
                    # down = driver.find_elements_by_class_name("item-button")[2]
                    down.get_attribute('innerHTML')
                    print(down.get_attribute('innerHTML'))
                    print(down.get_attribute('href'))

                    down.click()
                    time.sleep(2)
                    # Close the tab or window
                    driver.close()

                    # Switch back to the old tab or window
                    driver.switch_to.window(original_window)

                else:
                    # Close the tab or window
                    driver.close()

                    # Switch back to the old tab or window
                    driver.switch_to.window(original_window)
                    time.sleep(0.5)


                if (index == number):  # si ya ha descargado las ultimas, break y guardar la last song
                    setLastSong(currentSong)
                    break
                if(index % 50 == 0):
                    print("Va a esperar 2 minutitos, buen momento para etxar un txis")
                    time.sleep(120)
            else:
                #solo tiene que mirar si llego cuando no ha llegado
                if(currentSong != 'No es valido'):
                    arrived = has_it_arrived(currentSong)  # preguntar en cada iteracion si ha llegado o no

                time.sleep(1)

                # Close the tab or window
                driver.close()

                # Switch back to the old tab or window
                driver.switch_to.window(original_window)


        MsgBox = messagebox.askyesno(title='Han terminado las descargas?',message='Haz clik YES para cerrar SOLO si ya han terminado de descargarse')
        if(MsgBox == 'Yes'):
            driver.switch_to.window(original_window)
            driver.close()
        # Switch back to the old tab or window
        #driver.switch_to.window(original_window)
        #driver.close()
        messagebox.showinfo(title="Ha descargado bien", message="El numero de canciones ha sido: "+str(number)+". Y la ultima deberia de ser: "+getLastSong()+"\n Ademas ahora tienes un documento de texto con los nombres de las canciones que no se han descargado")
        messagebox.showinfo(title='Informacion adicional',
                            message="Realizado por: Eneko Cuesta\n" "Custom made para: @Xabi_Brutality")
        registrarNoDescargadas()
    except FileNotFoundError:
        print("Directorio no encontrado guey")
        messagebox.showerror(title="Errorazo selektah", message="No se ha encontrado el directorio")




















def fullMenuSetup():
    # cambiar menu
    set = tk.Tk()
    # size and position for window
    set.geometry("0x0+0+0")
    set.withdraw
    #Usuario = simpledialog.askstring(title="Usuario?",
    #                                  prompt="Introduce el usuario:")
    #Contraseña = simpledialog.askstring(title="Contraseña?",
    #                                  prompt="Introduce la contraseña:")
    nSongs = simpledialog.askstring(title="Numero de canciones que descargar cada vez?",
                                      prompt="Introduce el numero de canciones que quieres que se descarguen cada vez:")
    #set.withdraw
    return ['','',nSongs]

def getLastSong():
    try:
        with open('conf.txt') as f:
            lines = f.readlines()
            for line in lines:
                if (len(lines) == 4):
                    lastSong = lines[3]
                else:
                    lastSong = ""
        f.close()
        return lastSong
    except UnboundLocalError:
        return ""

def setup(): #para guardar la configuracion (de momento te pedira todo)

    try:
        #recuperar la ultima cancion
        lastSong = getLastSong()
        #conseguir los nuevos parametros
        listaConf = fullMenuSetup()

        print(type(listaConf[0]))
        print(type(listaConf[1]))
        print(type(int(listaConf[2])))
        #Volverlo string (Aqui daria el type Error)
        configuracion = listaConf[0] + "\n" + listaConf[1] + "\n" + listaConf[2] + "\n" + lastSong

        #fileSwapearlo
        file = open("conf.txt","w")
        file.write(configuracion)
        file.close()
    except TypeError:
        print("typeError")  # cuando entra en typeError se borra la configuracion
        messagebox.showwarning(title="Ups", message="Has cancelado la nueva configuracion, se mantendra como estaba. Si es la primera vez que configuras el numero de configuracion por defecto sera 40!!")
    except ValueError:
        messagebox.showwarning(title="Ups", message="El usuario y contraseña realmente dan igual, pero el numero de canciones parece ser importante. Seguro que has metido un numero?")
        setup()



def configExists(): #devuelve true or false si existe o no el fichero de configuracion
    found = False
    for root, directories, files in os.walk(thisPath, topdown=False):
        for name in files:
            if(name == 'conf.txt'):
                found = True
    return found

def menu():
    # creating window object
    top = tk.Tk()
    # size and position for window
    top.geometry("400x100+900+300")
    top.title(" --El SuperPrograma 3000-- ")
    B1 = Button(top, text="Descargar canciones",
                command=download)
    B2 = Button(top, text="Cambiar nombre",
                command=changeName)
    B3 = Button(top, text="Configurar",
                command=setup)
    B1.pack()
    B2.pack()
    B3.pack()
    top.mainloop()


if __name__ == '__main__':
    if(not configExists()):
        print("config not found")
        file = open("conf.txt", "w")
        file.close()
        setup()
        menu()


    else:
        print("config found")
        menu()
