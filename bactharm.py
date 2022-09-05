import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import filedialog as fd
import os
from Bio.Blast import NCBIXML
from tkinter import *
from tkinter import font
import subprocess





customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

#stores the location of the file provided.
seq_file_loc = ''

class App(customtkinter.CTk):

    WIDTH = 1200
    HEIGHT = 750

    def __init__(self):
        super().__init__()

        self.title("Bacteria Virulence Finder")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (1x2)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        

        self.frame_up = customtkinter.CTkFrame(master=self)
        self.frame_up.grid(row=0, column=0, sticky="we", padx=20, pady=20)

        
        self.frame_down = customtkinter.CTkFrame(master=self, height=500, corner_radius=2 , padx=20, pady=20)
        self.frame_down.grid(row=1, column=0, sticky="we")

        # ============ frame_up ============

        # configure grid layout (3*1)
        self.frame_up.grid_columnconfigure((0,1,2), weight=1)
        self.frame_up.grid_rowconfigure((0,1,2), weight=1)

        
        # ============ frame_down ============

        # configure grid layout (2*1)
        self.frame_down.grid_rowconfigure(0,weight=1)
        self.label = customtkinter.CTkLabel(master=self.frame_down, text="Label")
        self.label.grid(row=0 , column=0 , pady=25 , padx=25)
            

        self.button_1 = customtkinter.CTkButton(master=self.frame_up, text="Upload SEQ", text_font=(tkinter.font.NORMAL,20), width=200 , height = 100, command=self.select_file)
        self.button_1.grid(row=1, column=0, pady=10, padx=10)

        
        self.button_2 = customtkinter.CTkButton(master=self.frame_up, text="Analyze SEQ", text_font=(tkinter.font.NORMAL,20),  width=200 , height = 100, command=self.analyze)
        self.button_2.grid(row=1, column=1, pady=10, padx=10) 

        self.button_3 = customtkinter.CTkButton(master=self.frame_up, text="Show Result", text_font=(tkinter.font.NORMAL,20),  width=200 , height = 100, command= self.ChangeLabelText)
        self.button_3.grid(row=1, column=2, pady=10, padx=10) 

        
        self.button_4 = customtkinter.CTkButton(master=self.frame_up, text="Update VFDB", text_font=(tkinter.font.NORMAL,20),  width=200 , height = 100, command=self.update_db)
        self.button_4.grid(row=1, column=3, pady=10, padx=10) 




        
        # ============ frame_down ============

    def on_closing(self, event=0):
        self.destroy()


    def select_file(self):
        filetypes = (
              ('All files', '*.*'),
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/mnt/d/fifth_sem/biohackathon',
            filetypes=filetypes)
            
        global seq_file_loc
        seq_file_loc = filename

        tkinter.messagebox.showinfo(
            title='Selected File',
            message=filename
         )
        
    def analyze(self):
        print(seq_file_loc)
        
        err = os.system('blastn -query '+  seq_file_loc + ' -db ./databases/VFDB_core_nt -dust no -soft_masking false -out ' +seq_file_loc+'.xml' )
        

    def ChangeLabelText(self):
        # os.system("sed -i '/Sequence/,$!d'" + seq_file_loc)
        # file1 = open(seq_file_loc, 'r')
        # Lines = file1.readlines()
        # fd = open('output_table.txt','w')
        # for line in Lines[19:27]:
        #      fd.write(line)
        # blastout = open('./output_table.txt' , 'r')
        # datatable = blastout.read()
        # self.label.configure(text=datatable)
        global seq_file_loc
        subprocess.call([r"gedit", seq_file_loc+'.xml'])

        



    def update_db(self):
        top = Toplevel()
        top.title('Updating the database')
        Message(top, text='This will take some time. We will update the entire virulent database. Please make sure you have a strong netwrok connection.', padx=20, pady=20 , width=500).pack()
        top.after(2000, top.destroy)

        err = 0
        err = os.system('wget http://www.mgc.ac.cn/VFs/Down/VFDB_setA_nt.fas.gz -O ./databases/core_nt.fas.gz')
        err = os.system('wget http://www.mgc.ac.cn/VFs/Down/VFDB_setA_pro.fas.gz -O ./databases/core_pro.fas.gz')
        err = os.system('gzip -d ./databases/core_nt.fas.gz')
        err = os.system('gzip -d ./databases/core_pro.fas.gz')
        err = os.system('makeblastdb -in ./databases/core_nt.fas -parse_seqids -title "VFDB_core_nt" -dbtype nucl -out ./databases/VFDB_core_nt')
        err = os.system('makeblastdb -in ./databases/core_pro.fas -parse_seqids -title "VFDB_core_pro" -dbtype nucl -out ./databases/VFDB_core_pro')

        if(err == 0):
            tkinter.messagebox.showinfo(
                title='Updated Sucessfully',
                message='all databases have been updated sucessfully')
        else:
            tkinter.messagebox.showinfo(
                title='Update Failed',
                message='Please Try again later')

        
        

        
if __name__ == "__main__":
    app = App()
    app.mainloop()