from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter.filedialog import *
from os import path
import tkinter as tk

root = tk.Tk(className= "Vcard Splitter") # Creation of the window
root.geometry("500x180") # set the dimension of the window


def openfile(): #function for find the Vcard file
    char = Entry1.get()
    file = askopenfilename(filetypes=[("Vcard files", ".vcf")])
    Entry1.delete(0,len(char))
    Entry1.insert(0,file)    
    
def openfolder(): #function for find the folder where the Vcard file will be create
    char = Entry2.get()
    folder = askdirectory()
    Entry2.delete(0,len(char))
    Entry2.insert(0,folder)

def annuler(): #function close the window
    root.destroy()
    
def error(): # function with all the error
    error = False # set error to false
    if Entry1.get() != "":
        try:
            open(Entry1.get(),"a") # try to open the Vcard file
        except : 
            messagebox.showerror("ERREUR DE CHEMIN", "Le chemin renseignée du fichier à séparer n'est pas connu !") # test the file s path and send a message of error if the path is incorrect
            error = True # if the path is incorrect set error to true
        if Entry1.get().endswith('.vcf') == False : # look if the extension of the file is .vcf
            messagebox.showerror("ERREUR DE FICHIER", "L'extension du fichier n'est pas le bon.") 
            error = True
        else : # if is a Vcard file check the file if is corrupt 
            file1 = open(Entry1.get(),"r",encoding='utf8') # open the file with a encoding for emoji and others special character
            text1 = file1.readlines()
            end = 0
            begin = 0
            for i in text1:
                if i.find('VERSION:') == 0 : 
                    version = i[8:-1]
                    if float(version) < 3.0:
                        messagebox.showerror("FIHCHIER NON A JOUR", "Le fichier n'est pas à jour, merci de prendre un fichier a jour")
                        error = True
                    elif float(version) > 3.0 :
                        messagebox.showerror("PROGRAMME NON A JOUR", "Le programme n'est pas à jour,\nmerci de contacter LARROCHE MAXIMILIEN \nAdresse-mail : larroche.maximilien@gmail.com pour mettre à jour le programme.")
                        error = True
                if i == 'END:VCARD\n' or i == 'END:VCARD': # count the number of END VCARD
                    end = end + 1
                elif i == 'BEGIN:VCARD\n' or i == 'BEGIN:VCARD' : # count the number of BEGIN VCARD
                    begin = begin + 1
                if begin == end +2 or begin == end - 2: # if the number is two more than the other the file is corrupt
                    error = True
                    messagebox.showerror("FICHIER CORROMPU", "Le fichier est corrompu, \n Merci de vérifier le fichier.")
                    break


    if Entry1.get() == "" : error = True and messagebox.showinfo("Manque de donnée", "Merci de renseigné le chemin du fichier à séparer.") # check if the input is empty
    try:
        path.exists(Entry2.get()) # try the path for the install folder
    except : 
        messagebox.showerror("ERREUR DE CHEMIN", "Le chemin renseignée du dossier n'est pas connu !")  
        error = True
    if Entry2.get() == "" : error = True and messagebox.showinfo("Manque de donnée", "Merci de renseigné le chemin du dossier où les fichiers Vcards seront installés.")



    if error : return error

def split():
    # For copy the path of the file without using askopenfile we have to replace the quotation marks from the input
    pathfile = Entry1.get()
    pathfile = pathfile.replace('"',"")
    pathfolder = Entry2.get()
    pathfolder = pathfolder.replace('"',"")
    Entry1.delete(0,len(pathfile))
    Entry2.delete(0,len(pathfolder))
    Entry1.insert(0,pathfile)
    Entry2.insert(0,pathfolder)

    if error() == True : return # test the error if there is an error stop the split

    file = open(Entry1.get(), "r", encoding='utf8')
    count = 0

    while True: # set the loop
        lines = file.readline()
        while lines == '\n': # if there is an empty line between the tag
            lines = file.readline() # read the next line
        if lines == '': #if the line is empty is the end of the file
            break #stop the function
        else:
            begin = lines #put in variable the three first line to recover the name of the contact
            lines = file.readline()
            l2 = lines
            lines = file.readline()[3:-1] # take just the name
            nom = lines
            chemin = Entry2.get() + "/"+ nom + ".vcf" # create the file for the contact
            flux = open(chemin, "a", encoding='utf8') # open the new file
            flux.write(begin + l2 + "FN:" + nom + "\n") # write the three first line
            lines = file.readline() # read the next line
            count += 1
            while lines != 'END:VCARD\n' : # loop to write all the information into the new file
                flux.write(lines)
                lines = file.readline()
            flux.write(lines) #write the END VCARD
    file.close() # close the file
    messagebox.showinfo("Validation", "La séparation du fichier est un succès !\nNombre de contact séparer " + str(count)) # send a message for the end of the process
    annuler() # close the window

b1 = Button(root, text="...", command = openfile,width=3) # creation of the button with the function associate
b2 = Button(root, text="...", command = openfolder,width=3)
b3 = Button(root, text="Valider", command = split,width=12)
b4 = Button(root, text="Annuler", command = annuler ,width=12)
Entry1 = Entry(root, width= 50, font=("",11)) # create the input
Entry2 = Entry(root, width= 50,font=("",11))
label1 = Label(root, text="Chemin du fichier Vcard", font=("",12),bg="#D3D3D3") # create the label info
label2 = Label(root, text="Chemin du dossier des Vcards séparés",font=("",12),bg="#D3D3D3")
b1.place(x=450,y=30) # coordinate of all UI object
b2.place(x=450,y=90)
b3.place(x=250,y=150)
b4.place(x=150,y=150)
Entry1.place(x=10,y=30)
Entry2.place(x=10,y=90)
label1.place(x=10,y=5)
label2.place(x=10,y=65)
root.resizable(False,False) # the user can t change the size of the window
root.configure(bg="#D3D3D3")  # set a color background
root.tk.call('wm', 'iconphoto', root._w,
    PhotoImage(file = "icon\\splitter.png") # set a icon
)
root.mainloop() # launch the program
