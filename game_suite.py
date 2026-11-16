import random
import tkinter as tk
from tkinter import messagebox

BG="#101321"; PANEL="#1b2033"; CYAN="#65e6df"; PINK="#ff70b7"; WHITE="#f4f5ff"; YELLOW="#ffd166"

class Arcade:
    def __init__(self,root):
        self.root=root; root.title("A-GPT ARCADE // 5 GAMES"); root.geometry("800x600"); root.minsize(650,500); root.configure(bg=BG)
        self.frame=tk.Frame(root,bg=BG); self.frame.pack(fill="both",expand=True); self.menu()
    def clear(self):
        for w in self.frame.winfo_children(): w.destroy()
    def heading(self,title,sub=""):
        tk.Label(self.frame,text=title,bg=BG,fg=CYAN,font=("Arial",27,"bold")).pack(pady=(24,4))
        tk.Label(self.frame,text=sub,bg=BG,fg=WHITE,font=("Arial",11)).pack(pady=(0,18))
    def button(self,text,fn):
        tk.Button(self.frame,text=text,command=fn,bg=PANEL,fg=WHITE,activebackground=CYAN,relief="flat",font=("Arial",14,"bold"),padx=18,pady=12,width=25).pack(pady=7)
    def menu(self):
        self.clear(); self.heading("A-GPT ARCADE","Five tiny games. One executable. Zero internet required.")
        for n,f in [("SNAKE",self.snake),("PONG",self.pong),("DODGE THE BLOCKS",self.dodge),("MEMORY MATCH",self.memory),("NUMBER GUESS",self.guess)]: self.button(n,f)
        tk.Label(self.frame,text="A-GPT PLAYGROUND • BUILD 001",bg=BG,fg="#858da8").pack(side="bottom",pady=18)
    def shell(self,title,hint):
        self.clear(); bar=tk.Frame(self.frame,bg=BG); bar.pack(fill="x",padx=18,pady=12)
        tk.Button(bar,text="← MENU",command=self.menu,bg=PANEL,fg=WHITE,relief="flat").pack(side="left")
        tk.Label(bar,text=title,bg=BG,fg=CYAN,font=("Arial",18,"bold")).pack(side="left",padx=20)
        tk.Label(self.frame,text=hint,bg=BG,fg=WHITE).pack(pady=5)
        self.canvas=tk.Canvas(self.frame,width=600,height=400,bg="#090d18",highlightthickness=1,highlightbackground="#343d5c"); self.canvas.pack(pady=12)
        self.root.focus_force()
    def snake(self):
        self.shell("SNAKE","Arrow keys move. Eat gold food. Avoid walls and yourself.")
        self.body=[(300,200),(280,200),(260,200)]; self.direction=(20,0); self.food=(400,200); self.dead=False; self.score=0
        self.score_id=self.canvas.create_text(12,12,anchor="nw",fill=WHITE,text="Score: 0")
        self.root.bind("<KeyPress>",self.snake_key); self.snake_tick()
    def snake_key(self,e):
        d={"Up":(0,-20),"Down":(0,20),"Left":(-20,0),"Right":(20,0)}.get(e.keysym)
        if d and d!=(-self.direction[0],-self.direction[1]): self.direction=d
    def snake_tick(self):
        if self.dead or not self.canvas.winfo_exists(): return
        x,y=self.body[0]; dx,dy=self.direction; h=(x+dx,y+dy)
        if h[0]<0 or h[0]>=600 or h[1]<0 or h[1]>=400 or h in self.body:
            self.dead=True; self.canvas.create_text(300,190,text="GAME OVER",fill=PINK,font=("Arial",30,"bold")); self.canvas.create_text(300,230,text=f"Score: {self.score}",fill=WHITE); return
        self.body.insert(0,h)
        if h==self.food:
            self.score+=1; self.food=(random.randrange(30)*20,random.randrange(20)*20); self.canvas.itemconfigure(self.score_id,text=f"Score: {self.score}")
        else: self.body.pop()
        self.canvas.delete("body"); self.canvas.delete("food")
        for px,py in self.body: self.canvas.create_rectangle(px,py,px+18,py+18,fill=CYAN,outline="",tags="body")
        fx,fy=self.food; self.canvas.create_oval(fx+2,fy+2,fx+18,fy+18,fill=YELLOW,outline="",tags="food")
        self.root.after(max(65,140-self.score*2),self.snake_tick)
    def pong(self):
        self.shell("PONG","W and S move your paddle. First to five points wins.")
        self.py=155; self.bx=300; self.by=200; self.vx=4; self.vy=3; self.ps=0; self.cs=0; self.running=True
        self.paddle=self.canvas.create_rectangle(25,self.py,38,self.py+90,fill=CYAN,outline="")
        self.ball=self.canvas.create_oval(291,191,309,209,fill=YELLOW,outline="")
        self.score_id=self.canvas.create_text(300,20,fill=WHITE,font=("Arial",16),text="0 : 0")
        self.root.bind("<KeyPress>",self.pong_key); self.pong_tick()
    def pong_key(self,e):
        if e.keysym.lower()=="w": self.py=max(0,self.py-25)
        if e.keysym.lower()=="s": self.py=min(310,self.py+25)
        if hasattr(self,"paddle"): self.canvas.coords(self.paddle,25,self.py,38,self.py+90)
    def pong_tick(self):
        if not self.running or not self.canvas.winfo_exists(): return
        self.bx+=self.vx; self.by+=self.vy
        if self.by<9 or self.by>391: self.vy=-self.vy
        if self.bx<43 and self.py-9<self.by<self.py+99: self.vx=abs(self.vx)*1.04
        if self.bx>557 and 150<self.by<250: self.vx=-abs(self.vx)*1.04
        if self.bx<0: self.cs+=1; self.bx,self.by,self.vx,self.vy=300,200,4,random.choice([-3,3])
        if self.bx>600: self.ps+=1; self.bx,self.by,self.vx,self.vy=300,200,-4,random.choice([-3,3])
        self.canvas.coords(self.ball,self.bx-9,self.by-9,self.bx+9,self.by+9); self.canvas.itemconfigure(self.score_id,text=f"{self.ps} : {self.cs}")
        if max(self.ps,self.cs)>=5:
            self.running=False; self.canvas.create_text(300,210,text="YOU WIN!" if self.ps>self.cs else "CPU WINS!",fill=PINK,font=("Arial",28,"bold")); return
        self.root.after(16,self.pong_tick)
    def dodge(self):
        self.shell("DODGE THE BLOCKS","Use LEFT and RIGHT arrows. Survive as long as possible.")
        self.dx=280; self.drops=[]; self.score=0; self.running=True
        self.player=self.canvas.create_rectangle(self.dx,350,self.dx+40,375,fill=CYAN,outline="")
        self.score_id=self.canvas.create_text(12,12,anchor="nw",fill=WHITE,text="Score: 0")
        self.root.bind("<KeyPress>",self.dodge_key); self.dodge_tick()
    def dodge_key(self,e):
        if e.keysym=="Left": self.dx=max(0,self.dx-25)
        if e.keysym=="Right": self.dx=min(560,self.dx+25)
        if hasattr(self,"player"): self.canvas.coords(self.player,self.dx,350,self.dx+40,375)
    def dodge_tick(self):
        if not self.running or not self.canvas.winfo_exists(): return
        if random.random()<.09: self.drops.append([random.randrange(580),-20,random.randrange(4,9)])
        for d in self.drops: d[1]+=d[2]
        self.drops=[d for d in self.drops if d[1]<410]; self.canvas.delete("drop")
        for x,y,s in self.drops:
            self.canvas.create_rectangle(x,y,x+18,y+18,fill=PINK,outline="",tags="drop")
            if x<self.dx+40 and x+18>self.dx and y<375 and y+18>350:
                self.running=False; self.canvas.create_text(300,200,text=f"GAME OVER • SCORE {self.score}",fill=YELLOW,font=("Arial",22,"bold")); return
        self.score+=1; self.canvas.itemconfigure(self.score_id,text=f"Score: {self.score}"); self.root.after(30,self.dodge_tick)
    def memory(self):
        self.shell("MEMORY MATCH","Find every matching pair. Click two cards at a time.")
        vals=list("AABBCCDDEEFF"); random.shuffle(vals); self.cards=[]; self.opened=[]; self.matched=set(); self.moves=0
        self.memory_label=tk.Label(self.frame,text="Moves: 0",bg=BG,fg=WHITE); self.memory_label.pack()
        for i,v in enumerate(vals):
            b=tk.Button(self.frame,text="?",width=6,height=2,bg=PANEL,fg=WHITE,font=("Arial",16,"bold"),command=lambda i=i:self.flip(i))
            b.place(x=75+(i%4)*165,y=155+(i//4)*75); self.cards.append((b,v))
    def flip(self,i):
        if i in self.matched or any(j==i for j,_ in self.opened) or len(self.opened)>=2: return
        b,v=self.cards[i]; b.config(text=v,bg="#3b3155"); self.opened.append((i,v))
        if len(self.opened)==2:
            self.moves+=1; self.memory_label.config(text=f"Moves: {self.moves}"); a,va=self.opened[0]; z,vz=self.opened[1]
            if va==vz:
                self.matched.update((a,z)); self.opened=[]
                if len(self.matched)==len(self.cards): messagebox.showinfo("Winner!",f"All pairs found in {self.moves} moves!")
            else: self.root.after(700,lambda:self.hide_pair(a,z))
    def hide_pair(self,a,z):
        for i in (a,z): self.cards[i][0].config(text="?",bg=PANEL)
        self.opened=[]
    def guess(self):
        self.shell("NUMBER GUESS","I'm thinking of a number from 1 to 100.")
        self.secret=random.randint(1,100); self.guesses=0
        tk.Label(self.frame,text="Enter a number:",bg=BG,fg=WHITE,font=("Arial",14)).pack(pady=12)
        self.entry=tk.Entry(self.frame,font=("Arial",18),justify="center"); self.entry.pack()
        tk.Button(self.frame,text="GUESS",command=self.check_guess,bg=CYAN,fg=BG,font=("Arial",12,"bold"),relief="flat",padx=18,pady=8).pack(pady=12)
        self.result=tk.Label(self.frame,text="Good luck!",bg=BG,fg=YELLOW,font=("Arial",14)); self.result.pack()
        self.entry.bind("<Return>",lambda e:self.check_guess())
    def check_guess(self):
        try: n=int(self.entry.get())
        except ValueError: self.result.config(text="Enter a whole number."); return
        if not 1<=n<=100: self.result.config(text="Pick from 1 to 100."); return
        self.guesses+=1
        if n==self.secret: self.result.config(text=f"Correct! Guesses: {self.guesses}")
        elif n<self.secret: self.result.config(text="Too low. Go higher!")
        else: self.result.config(text="Too high. Go lower!")

if __name__=="__main__":
    root=tk.Tk(); Arcade(root); root.mainloop()
