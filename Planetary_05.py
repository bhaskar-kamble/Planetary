# this file is based on my_models_GUI_4.py.

# The "side" arguments for rb_fr.pack, screen_fr.pack and b.pack should be TOP,TOP,LEFT or LEFT,LEFT,TOP respectively
from Tkinter import *
import tkMessageBox
import planetary_orbit
#import ScrolledText as tkst

root = Tk( )

root.title("Planetary Motion")

class notebook(object):
    def __init__(self,master):
        self.active_fr = None
        self.count  = 0
        self.choice = IntVar()
        self.rb_fr = Frame(master,borderwidth=2, relief=GROOVE)# this contains the "Time plot" and "Phase plot" buttons
        self.rb_fr.pack(side=TOP) # as of now side=TOP makes no difference
        self.screen_fr = Frame(master, borderwidth=2, relief=FLAT) #has "Calculating angle...initial conditions": similar label for phase plot
        self.screen_fr.pack(side=TOP)

    def __call__(self): 
        return self.screen_fr

    def add_screen(self,fr,title):
        b = Radiobutton(self.rb_fr , text=title, indicatoron=0, variable=self.choice, value=self.count, command=lambda: self.display(fr)) 
        b.pack(side=LEFT) # this ensures that the radiobuttons "Time plot" and "Phase plot" are side-by-side and not on top of each other
	if not self.active_fr:   # this if not block seems superfluous...
	    fr.pack()#(fill=BOTH, expand=1) 
	self.active_fr = fr
        self.count += 1

    def display(self, fr): 
        self.active_fr.forget( ) #if you comment this out then all the menus of DFT, STFT etc. will be exhibited.
	fr.pack(fill=BOTH, expand=1) 
	self.active_fr = fr




class Start_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Welcome to Planetary!\n\nYou can make interactive animations of planetary orbits with parameters of your choice!"

        Label(self.parent,text=choose_label,wraplength=300,width=50,height=30,relief=SUNKEN,justify=LEFT,bg="tan1").grid()
        ######################################################################################################
        #pend_pic = PhotoImage(file="./Pendulum.gif") #http://www.python-course.eu/tkinter_labels.php
        #Label(self.parent,text=choose_label,wraplength=300,width=50,height=30,relief=SUNKEN,justify=LEFT,image=pend_pic).grid()
        ######################################################################################################

        ######################################################################################################
        #tkst.ScrolledText(self.parent, text=choose_label,wraplength=400,width=50,relief=SUNKEN).grid()
        ######################################################################################################



class Orbit_frame:
    def __init__(self,parent):
        self.parent = parent
        self.initUI()
    def initUI(self):
        choose_label = "Plotting the orbit."
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))
        choose_label = "Give initial conditions and time"
        Label(self.parent, text=choose_label).grid()#row=0, column=0, sticky=W, padx=5, pady=(10,2))

        choose_label = "x(0)"
        Label(self.parent, text=choose_label).grid()
        self.x0 = Entry(self.parent)
        self.x0.grid()
        self.x0.delete(0,END)   # warum? i guess just in case there is some other text already, which is being removed thru this command
        self.x0.insert(0,"1.0") # putting in a default value

        choose_label = "xdot(0)"
        Label(self.parent, text=choose_label).grid()
        self.xdot0 = Entry(self.parent)
        self.xdot0.grid()
        self.xdot0.delete(0,END)
        self.xdot0.insert(0,"0.0")
        
        choose_label = "y(0)"
        Label(self.parent, text=choose_label).grid()
        self.y0 = Entry(self.parent)
        self.y0.grid()
        self.y0.delete(0,END)   # warum? i guess just in case there is some other text already, which is being removed thru this command
        self.y0.insert(0,"0.1") # putting in a default value

        choose_label = "ydot(0)"
        Label(self.parent, text=choose_label).grid()
        self.ydot0 = Entry(self.parent)
        self.ydot0.grid()
        self.ydot0.delete(0,END)
        self.ydot0.insert(0,"1.0")

        choose_label = "time"
        Label(self.parent, text=choose_label).grid()
        self.time = Entry(self.parent)
        self.time.grid()
        self.time.delete(0,END)
        self.time.insert(0,"30.0")

        # Button to compute the orbit
        self.compute = Button(self.parent,text="Compute",command=lambda:self.compute_orbit())
        self.compute.grid()

    def compute_orbit(self):
        try:
            ini_x = float(self.x0.get())
            ini_xdot = float(self.xdot0.get())
            ini_y = float(self.y0.get())
            ini_ydot = float(self.ydot0.get())
            zeit          = float(self.time.get())

            #tkMessageBox.showinfo(message="We will now calculate theta and omega")

            planetary_orbit.solution(ini_x,ini_xdot,ini_y,ini_ydot,zeit)

        except ValueError as errorMessage:
	    tkMessageBox.showerror("Input values error",errorMessage)











nb = notebook(root) # an instance of "notebook" class created



f0 = Frame(nb())
nb.add_screen(f0,"Start")
anfang = Start_frame(f0)



f1 = Frame(nb()) 
nb.add_screen(f1, "Time plot") 
kreisbahn = Orbit_frame(f1)  

nb.display(f0)

root.geometry('+0+0')
root.mainloop( )
