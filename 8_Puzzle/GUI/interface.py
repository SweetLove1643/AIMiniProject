from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
from tkinter import PhotoImage



import main

### Global Variables to store the solution analytics ###
algorithm = None
initialState = None
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []


class InterfaceApp:

    # =============================================================================================================== #
    ###     Build the GUI     ###

    def __init__(self, master=None):


        self._job = None
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=550, width=800)
        self.appFrame.pack(side="top")


        self.mainlabel = ttk.Label(self.appFrame)
        self.mainlabel.configure(
            anchor="center", font="{Forte} 36 {bold}", foreground="#003e3e", justify="center", text='8-Puzzle by Phan Quan')
        self.mainlabel.place(anchor="center", x=300, y=50)

        self.backbutton = ttk.Button(self.appFrame)
        self.img_backicon = tk.PhotoImage(file="back-icon.png")
        self.backbutton.configure(cursor="hand2", image=self.img_backicon)
        self.backbutton.place(anchor="center", height=80, width=80, x=250, y=500)
        self.backbutton.bind("<ButtonPress>", self.prevSequence)

        self.nextbutton = ttk.Button(self.appFrame)
        self.img_nexticon = tk.PhotoImage(file="next-icon.png")
        self.nextbutton.configure(cursor="hand2", image=self.img_nexticon)
        self.nextbutton.place(anchor="center", height=80, width=80, x=350, y=500)
        self.nextbutton.bind("<ButtonPress>", self.nextSequence)

        self.fastforwardbutton = ttk.Button(self.appFrame)
        self.img_fastforwardicon = tk.PhotoImage(file="fast-forward-icon.png")
        self.fastforwardbutton.configure(cursor="hand2", image=self.img_fastforwardicon)
        self.fastforwardbutton.place(anchor="center", height=80, width=80, x=450, y=500)
        self.fastforwardbutton.bind("<ButtonPress>", self.fastForward)

        self.fastbackwardbutton = ttk.Button(self.appFrame)
        self.img_fastbackwardicon = tk.PhotoImage(file="fast-backward-icon.png")
        self.fastbackwardbutton.configure(cursor="hand2", image=self.img_fastbackwardicon)
        self.fastbackwardbutton.place(anchor="center", height=80, width=80, x=150, y=500)
        self.fastbackwardbutton.bind("<ButtonPress>", self.fastBackward)

        self.stopbutton = ttk.Button(self.appFrame)
        self.img_stopicon = tk.PhotoImage(file="stop.png")
        self.stopbutton.configure(cursor="hand2", image=self.img_stopicon, state='disabled')
        self.stopbutton.place(anchor="center", height=80, width=80, x=550, y=500)
        self.stopbutton.bind("<ButtonPress>", self.stopFastForward)

        self.resetbutton = ttk.Button(self.appFrame)
        self.img_reseticon = tk.PhotoImage(file="reset-icon.png")
        self.resetbutton.configure(cursor="hand2", image=self.img_reseticon, state='disabled')
        self.resetbutton.place(anchor="center", height=80, width=80, x=50, y=500)
        self.resetbutton.bind("<ButtonPress>", self.resetStepCounter)

        self.stepCount = ttk.Label(self.appFrame)
        self.stepCount.configure(anchor="center", background="#d6d6d6",
                                 font="{@Malgun Gothic Semilight} 12 {}", justify="center", text='0 / 0')
        self.stepCount.place(anchor="center", width=200, x=300, y=440)
         
       

        self.solvebutton = ttk.Button(self.appFrame)
        self.img_solveicon = tk.PhotoImage(file="solve-icon.png")
        self.solvebutton.configure(cursor="hand2", text='Solve', image=self.img_solveicon, compound="top")
        self.solvebutton.place(anchor="s", height=150, width=150, x=700, y=200)
        self.solvebutton.bind("<ButtonPress>", self.solve)

        self.gif_loading = tk.Label(self.appFrame)

        self.algorithmbox = ttk.Combobox(self.appFrame)
        self.algorithmbox.configure(cursor="hand2", state="readonly",
                                    values=('BFS', 'UCS','HillClimbing', 'IDFS','DFS', 'Greedy', 'A*'))
        self.algorithmbox.place(anchor="center", height=30, width=150, x=700, y=230)
        self.algorithmbox.bind("<<ComboboxSelected>>", self.selectAlgorithm)

        self.algolabel = ttk.Label(self.appFrame)
        self.algolabel.configure(anchor="center", text='Search Algorithm:')
        self.algolabel.place(anchor="center", x=570, y=230)

        self.analysisbox = ttk.Label(self.appFrame)
        self.analysisbox.configure(anchor="center", text='', background="#d6d6d6", borderwidth=3, relief="sunken")
        self.analysisbox.place(anchor="center", width=150, height=210, x=700, y=400)

    
        self.cell0 = ttk.Label(self.appFrame)
        self.cell0.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text=' ')
        self.cell0.place(anchor="center", height=100, width=100, x=200, y=150)

        self.cell1 = ttk.Label(self.appFrame)
        self.cell1.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='1')
        self.cell1.place(anchor="center", height=100, width=100, x=300, y=150)

        self.cell2 = ttk.Label(self.appFrame)
        self.cell2.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='2')
        self.cell2.place(anchor="center", height=100, width=100, x=400, y=150)

        self.cell3 = ttk.Label(self.appFrame)
        self.cell3.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='3')
        self.cell3.place(anchor="center", height=100, width=100, x=200, y=250)

        self.cell4 = ttk.Label(self.appFrame)
        self.cell4.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='4')
        self.cell4.place(anchor="center", height=100, width=100, x=300, y=250)

        self.cell5 = ttk.Label(self.appFrame)
        self.cell5.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='5')
        self.cell5.place(anchor="center", height=100, width=100, x=400, y=250)

        self.cell6 = ttk.Label(self.appFrame)
        self.cell6.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='6')
        self.cell6.place(anchor="center", height=100, width=100, x=200, y=350)

        self.cell7 = ttk.Label(self.appFrame)
        self.cell7.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='7')
        self.cell7.place(anchor="center", height=100, width=100, x=300, y=350)

        self.cell8 = ttk.Label(self.appFrame)
        self.cell8.configure(anchor="center", background="#5aadad", borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='8')
        self.cell8.place(anchor="center", height=100, width=100, x=400, y=350)
   
        
        self.enterstatebutton = ttk.Button(self.appFrame)
        self.img_inputicon = tk.PhotoImage(file="input-icon.png")
        self.enterstatebutton.configure(
            cursor="hand2", text='Enter initial state', image=self.img_inputicon, compound="left")
        self.enterstatebutton.place(anchor="n", width=150, x=700, y=250)
        self.enterstatebutton.bind("<ButtonPress>", self.enterInitialState)

        self.mainwindow = self.appFrame

        self.gif = [tk.PhotoImage(file='loading.gif', format='gif -index %i' % i) for i in range(10)]

    def run(self):
        
        app.displayStateOnGrid('000000000')
        app.gif_loading.place_forget()
        self.refreshFrame()
        self.mainwindow.after(0, app.refreshGIF, 0)
        self.mainwindow.mainloop()

    # =============================================================================================================== #
    ###     Widget Methods     ###

    @staticmethod
    def refreshGIF(ind):
        
        frame = app.gif[ind]
        ind = (ind + 1) % 10
        app.gif_loading.configure(image=frame)
        app.appFrame.after(50, app.refreshGIF, ind)

    def prevSequence(self, event=None):
       
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer -= 1
            self.refreshFrame()

    def nextSequence(self, event=None):
       
        global statepointer
        if statepointer < len(path) - 1:
            self.stopFastForward()
            statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        
        global algorithm, initialState
        app.gif_loading.place(x=600, y=125, anchor="s")
        if self.readyToSolve():
            msg = 'Algorithm: ' + str(algorithm) + '\nInitial State = ' + str(initialState)
            messagebox.showinfo('Confirm', msg)
            self.resetGrid()
            self.solveState()
            if len(path) == 0:
                messagebox.showinfo('Unsolvable!', 'The state you entered is unsolvable')
                self.displaySearchAnalysis(True)
            else:
                self.refreshFrame()
        else:
            solvingerror = 'Cannot solve.\n' \
                           'Algorithm in use: ' + str(algorithm) + '\n' \
                                                                   'Initial State   : ' + str(initialState)
            messagebox.showerror('Cannot Solve', solvingerror)
        app.gif_loading.place_forget()

    def enterInitialState(self, event=None):
        
        global initialState, statepointer
        inputState = simpledialog.askstring('Initial State Entry', 'Please enter your initial state')
        if inputState is not None:
            if self.validateState(inputState):
                initialState = inputState
                self.reset()
                app.displayStateOnGrid(initialState)
            else:
                messagebox.showerror('Input Error', 'Invalid initial state')

    def selectAlgorithm(self, event=None):
       
        global algorithm
        try:
            choice = self.algorithmbox.selection_get()
            self.reset()
            algorithm = choice
        except:
            pass

    def fastForward(self, event=None):
        
        global statepointer
        self.stopFastForward()
        if statepointer < cost:
            app.stopbutton.configure(state='enabled')
            statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < cost <= 1000:
                ms = 20
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        
        global statepointer
        self.stopFastForward()
        if statepointer > 0:
            app.stopbutton.configure(state='enabled')
            statepointer -= 1
            ms = 50
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastBackward)
        else:
            self.stopFastForward()
        self.refreshFrame()

    @staticmethod
    def stopFastForward(event=None):
        
        if app._job is not None:
            app.stopbutton.configure(state='disabled')
            app.stepCount.after_cancel(app._job)
            app._job = None

    def resetStepCounter(self, event=None):
        
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer = 0
            self.refreshFrame()
    
    # =============================================================================================================== #
    ###     Helper Functions     ###

    def displaySearchAnalysis(self, force_display=False):
        
        if self.solved() or force_display is True:
            analytics = 'Analysis of ' + str(algorithm) + \
                        '\ninitial state = ' + str(initialState)
            if force_display:
                analytics += '\n< UNSOLVABLE >'
            analytics += '\n-------------------------------' \
                         '\n' + 'Nodes expanded: \n' + str(counter) + \
                         '\n' + 'Search depth: \n' + str(depth) + \
                         '\n' + 'Search cost: \n' + str(cost) + \
                         '\n' + 'Running Time: \n' + str(runtime) + ' s'
        else:
            analytics = ''
        app.analysisbox.configure(text=analytics)

    def displayStateOnGrid(self, state):
        
        if not self.validateState(state):
            state = '000000000'
        self.cell0.configure(text=self.adjustDigit(state[0]))
        self.cell1.configure(text=self.adjustDigit(state[1]))
        self.cell2.configure(text=self.adjustDigit(state[2]))
        self.cell3.configure(text=self.adjustDigit(state[3]))
        self.cell4.configure(text=self.adjustDigit(state[4]))
        self.cell5.configure(text=self.adjustDigit(state[5]))
        self.cell6.configure(text=self.adjustDigit(state[6]))
        self.cell7.configure(text=self.adjustDigit(state[7]))
        self.cell8.configure(text=self.adjustDigit(state[8]))

    @staticmethod
    def readyToSolve():
        
        return initialState is not None and algorithm is not None

    @staticmethod
    def solved():
       
        return len(path) > 0

    @staticmethod
    def solveState():
        
        global path, cost, counter, depth, runtime
        if str(algorithm) == 'BFS':
            main.BFS(initialState)
            path, cost, counter, depth, runtime = \
                main.bfs_path, main.bfs_cost, main.bfs_counter, main.bfs_depth, main.time_bfs
        elif str(algorithm) == 'UCS':
            main.UCS(initialState)
            path, cost, counter, depth, runtime = \
                main.ucs_path, main.ucs_cost, main.ucs_counter, main.ucs_depth, main.time_ucs
        elif str(algorithm) == 'HillClimbing':
            
            main.hillClimbingWithRandomRestart(initialState, max_restarts=1000)
            path, cost, counter, depth, runtime = \
                main.hc_path, main.hc_cost, main.hc_counter, main.hc_depth, main.time_hc
        elif str(algorithm) == 'IDFS':
            main.IDFS(initialState,10)
            path, cost, counter, depth, runtime = \
                main.idfs_path, main.idfs_cost, main.idfs_counter, main.idfs_depth, main.time_idfs        
        elif str(algorithm) == 'DFS':
            main.DFS(initialState)
            path, cost, counter, depth, runtime = \
                main.dfs_path, main.dfs_cost, main.dfs_counter, main.dfs_depth, main.time_dfs
        elif str(algorithm) == 'Greedy':
            main.GreedyManhattan(initialState)
            path, cost, counter, depth, runtime = \
                main.manhattan_path, main.manhattan_cost, main.manhattan_counter, main.manhattan_depth, main.time_manhattan
        elif str(algorithm) == 'A*':
            main.AStarSearch_euclid(initialState)
            path, cost, counter, depth, runtime = \
                main.euclid_path, main.euclid_cost, main.euclid_counter, round(main.euclid_depth), main.time_euclid

    def resetGrid(self):
       
        global statepointer
        statepointer = 0
        self.refreshFrame()
        app.stepCount.configure(text=self.getStepCountString())

    def reset(self):
        
        global path, cost, counter, runtime
        cost = counter = 0
        runtime = 0.0
        path = []
        self.resetGrid()
        app.analysisbox.configure(text='')

    @staticmethod
    def getStepCountString():
        
        return str(statepointer) + ' / ' + str(cost)

    @staticmethod
    def refreshFrame():
        
        if cost > 0:
            state = main.getStringRepresentation(path[statepointer])
            app.displayStateOnGrid(state)
            app.stepCount.configure(text=app.getStepCountString())
            app.displaySearchAnalysis()
        if statepointer == 0:
            app.resetbutton.configure(state='disabled')
            app.backbutton.configure(state='disabled')
            app.fastbackwardbutton.configure(state='disabled')
        else:
            app.resetbutton.configure(state='enabled')
            app.backbutton.configure(state='enabled')
            app.fastbackwardbutton.configure(state='enabled')

        if cost == 0 or statepointer == cost:
            app.fastforwardbutton.configure(state='disabled')
            app.nextbutton.configure(state='disabled')
        else:
            app.fastforwardbutton.configure(state='enabled')
            app.nextbutton.configure(state='enabled')

    @staticmethod
    def validateState(inputState):
       
        seen = []
        if inputState is None or len(inputState) != 9 or not inputState.isnumeric():
            return False
        for dig in inputState:
            if dig in seen or dig == '9':
                return False
            seen.append(dig)
        return True

    @staticmethod
    def adjustDigit(dig):
        
        if dig == '0':
            return ' '
        return dig


if __name__ == "__main__":
    global app
    root = tk.Tk()
    root.title('8-Puzzle Solver')
    app = InterfaceApp(root)
    app.run()
