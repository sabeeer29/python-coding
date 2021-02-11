import ftplib
from ctypes import *
import os
import time
import shutil 
from os.path import basename
from pathlib import Path
from tkinter import *
from urllib.parse import urlparse, urljoin
from urllib.request import urlretrieve
import serial
from zipfile import ZipFile
#import requests


def switch_P5():
    serialPort = serial.Serial(port = "COM1", baudrate=9600,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)


    serialPort.write(str.encode('C'))
    serialPort.close()

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def format(disk_f,type_f,name_f):
    fm = windll.LoadLibrary('fmifs.dll')

    def myFmtCallback(command, modifier, arg):
        #print (command)
        return 1  # TRUE
                        
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_HARDDISK = 0x0C
    fm.FormatEx(c_wchar_p(disk_f), FMIFS_HARDDISK, c_wchar_p(type_f),
                c_wchar_p(name_f), True, c_int(0), FMT_CB_FUNC(myFmtCallback))
    

def files_in_folder(disk_name):
    file_count = sum(len(files) for _, _, files in os.walk(disk_name))
    return file_count



class Interface(Frame):
    
    
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=20000, height=20000, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        v=os.path.isfile('D:\\automatiser_mise_a_jour\\update.zip')
        
        if v is True :

            # Création de nos widgets
            self.message = Label(self, text="Bonjour Mise a jour disponible.").pack()

            self.bouton_quitter = Button(self, text="Quitter",padx=100,pady=25, command=self.quit, fg='red').pack(side="left")


            self.bouton_cliquer = Button(self, text="Update", fg="blue",padx=100,pady=25,command=self.cliquer).pack(side="right")
        
        
        
        else :
            self.message = Label(self, text="Bonjour pas de mise a jour disponible.").pack()

            self.bouton_quitter = Button(self, text="Quitter",padx=100,pady=25, command=self.quit, fg='red').pack(side="bottom")

    def cliquer(self, ftp_dirname=None):
        
        
        switch_P5()
        
        time.sleep(8)
        
        self.message = Label(self, text="Mise a jour ..",padx=100).pack()

        cmd = 'wmic logicaldisk where drivetype=3 get deviceid,size >Disk1.txt'
        os.system(cmd)
        cmd = 'wmic logicaldisk where drivetype=2 get deviceid,size >Disk2.txt'
        os.system(cmd)
        
        """
        with ZipFile(r'D:\\automatiser_mise_a_jour\\update.zip', 'r') as zip_ref:
            zip_ref.extractall('D:\\automatiser_mise_a_jour\\')
        os.system('echo %date% %time% >D:\\automatiser_mise_a_jour\\last_update.txt')
        """
        
        
        
        
        with open('Disk1.txt', 'r', encoding='utf-16') as f :
                contents = f.readlines()
                for line in contents[1:]:
                    line = line.replace(' ', '')
                    line = line.split(':')

                    DeviceID = line[0] + ':'

                    Size = int(line[1])
                    print(DeviceID,Size)
                    
                    if DeviceID=='G:':
                        
                        format('G:\\','NTFS','M1')                        
                        
                        print('*****************copy to G:********************')
                        
                        
                        copytree('D:\M1', 'G:')
                        print('end of copying to F:')
                        
                        if (files_in_folder('G:')>=files_in_folder('D:\M1')):
                            self.message = Label(self, text="mise a jour de M1(2) terminée ").pack()
                        else:
                            self.message = Label(self, text="mise a jour de M1(2) échouée ").pack()    
                        
                    
                    if DeviceID=='F:':
                        
                        format('F:\\','NTFS','M1')
                        
                        print('*****************copy to F:********************')
                        
                        copytree('D:\M1', 'F:')
                        
                        print('end of copying to F:')

                        if (files_in_folder('F:')>=files_in_folder('D:\M1')):
                            self.message = Label(self, text="mise a jour de M1(1) terminée ").pack()
                        else:
                            self.message = Label(self, text="mise a jour de M1(1) échouée ").pack()
        
        
        with open('Disk2.txt', 'r', encoding='utf-16') as f:
            contents = f.readlines()
            
            for line in contents[1:]:
                line = line.replace(' ', '')
                line = line.split(':')
                DeviceID = line[0] + ':'
                Size = int(line[1])
                
                print(DeviceID, Size)
                
                if DeviceID=='H:':
                    
                    fm = windll.LoadLibrary('fmifs.dll')

                    def myFmtCallback(command, modifier, arg):
                        #print(command)
                        return 1  # TRUE

                    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
                    FMIFS_HARDDISK = 0
                    fm.FormatEx(c_wchar_p('H:\\'), FMIFS_HARDDISK, c_wchar_p('FAT32'),
                                c_wchar_p('P5'), True, c_int(0), FMT_CB_FUNC(myFmtCallback))
                    
                    print('*****************copy to H:********************')
                    
                    copytree('D:\P5','H:')
                    
                    print('end of copying to H:')
                    
                    if (files_in_folder('H:')>=files_in_folder('D:\P5')):
                        self.message = Label(self, text="mise a jour de P5 terminée ").pack()
                    else:
                        self.message = Label(self, text="mise a jour de P5 échouée ").pack()

fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
interface.destroy()