import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import pygame as pg
import os
import threading
import time

pg.init()

MUSIC_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(MUSIC_END)


class Player:
    def __init__(self, master, tracklist=None, directory=None):
        if tracklist is None:
            tracklist = []
        if directory is None:
            directory = ''
        self.tracks_path = ''

        # creating track list
        track_list_font = tk.font.Font(family='Modern', size=15, weight='bold')
        self.trackList = tk.Listbox(bg='#99D0D3', bd=0, selectbackground='#2E958C', font=track_list_font, fg='#B47EB2')
        self.trackList.place(x=0, y=0, relwidth=0.25, relheight=1)
        self.playlist = []
        for track in tracklist:
            self.trackList.insert(0, track)
            self.playlist.append(track)
            self.tracks_path = f'{directory}/'

        # choose folder button
        self.trackListImg = tk.PhotoImage(file='img\\tracklist.png')
        self.trackListBtn = tk.Button(image=self.trackListImg, bg='#FCE0D5', bd=0)
        self.trackListBtn.place(x=210, y=10, width=50, height=50)
        self.trackListBtn.config(command=self.get_folder)

        # player control buttons
        self.play_btn = tk.PhotoImage(file='img\\play.png')
        self.next_btn = tk.PhotoImage(file='img\\next.png')
        self.prev_btn = tk.PhotoImage(file='img\\prev.png')
        self.play_control_btn_pause = tk.PhotoImage(file='img\\pause.png')
        self.play_control_btn_unpause = tk.PhotoImage(file='img\\unpause.png')
        self.playBtn = tk.Button(image=self.play_btn, bg='#FCE0D5', bd=0, command=self.play_selected_track)
        self.nextBtn = tk.Button(image=self.next_btn, bg='#FCE0D5', bd=0, command=self.change_to_next_track)
        self.prevBtn = tk.Button(image=self.prev_btn, bg='#FCE0D5', bd=0, command=self.change_to_prev_track)
        self.playControlBtn = tk.Button(image=self.play_control_btn_pause, bg='#FCE0D5', bd=0, command=self.pause_track)
        self.prevBtn.place(x=370, y=500, width=50, height=50)
        self.playControlBtn.place(x=440, y=500, width=50, height=50)
        self.playBtn.place(x=510, y=500, width=50, height=50)
        self.nextBtn.place(x=580, y=500, width=50, height=50)

        # album pic, but not now
        self.albumCover = tk.PhotoImage(file='img\\default.png')
        self.albumCoverShow = tk.Label(image=self.albumCover)
        self.albumCoverShow.place(x=350, y=125, width=300, height=300)
        self.playlist.reverse()
        self.playing_now = None

        # volume control slider
        self.volumeControl = tk.Scale(orient=tk.HORIZONTAL, length=130, from_=0.0, to=100.0, bg='#FCE0D5', bd=0,\
                                      activebackground='#B47EB2', command=self.change_volume, troughcolor='#99D0D3',\
                                      font=track_list_font, highlightthickness=0)
        self.volumeControl.set(50)
        self.volumeControl.place(x=650, y=500, height=50)

        # playing song showing
        self.playingFont = tk.font.Font(family='Modern', size=18, weight='normal')
        self.playingTitle = tk.Label(font=self.playingFont, text='Тишина...', bg='#99D0D3')
        self.playingTitle.place(x=270, y=450, width=460)

    def get_folder(self):
        folder = tk.filedialog.askdirectory()
        for files in os.walk(folder):
            for filename in files:
                self.__init__(self, filename, folder)
                
    # volume change func
    def change_volume(self, master):
        pg.mixer.music.set_volume(self.volumeControl.get()/100)

    def change_track_list(self, tracklist):
        for track in tracklist:
            self.trackList.insert(0, track)

    # pause func
    def pause_track(self):
        self.playControlBtn.config(image=self.play_control_btn_unpause, command=self.unpause_track)
        pg.mixer.music.pause()

    # unpause func
    def unpause_track(self):
        self.playControlBtn.config(image=self.play_control_btn_pause, command=self.pause_track)
        pg.mixer.music.unpause()

    # play previous
    def change_to_prev_track(self):
        if self.playlist.index(self.playing_now) == 0:
            self.playing_now = self.playlist[len(self.playlist)-1]
            pg.mixer.music.load(f'{self.tracks_path}{self.playing_now}')
            pg.mixer.music.play()
        else:
            self.playing_now = self.playlist[self.playlist.index(self.playing_now) - 1]
            pg.mixer.music.load(f'{self.tracks_path}{self.playing_now}')
            pg.mixer.music.play()
        self.playingTitle.config(text=self.playing_now[:-4])

    # go to next
    def change_to_next_track(self):
        if self.playlist.index(self.playing_now) + 1 == len(self.playlist):
            self.playing_now = self.playlist[0]
            pg.mixer.music.load(f'{self.tracks_path}{self.playing_now}')
            pg.mixer.music.play()
        else:
            self.playing_now = self.playlist[self.playlist.index(self.playing_now) + 1]
            pg.mixer.music.load(f'{self.tracks_path}{self.playing_now}')
            pg.mixer.music.play()
        self.playingTitle.config(text=self.playing_now[:-4])

    # play chosen track in tracklist
    def play_selected_track(self):
        try:
            selected = list(self.trackList.curselection())
            selected_tracks = ''.join([self.trackList.get(i) for i in selected])
            track_path = self.tracks_path + str(selected_tracks)
            pg.mixer.music.load(track_path)
            pg.mixer.music.play()
            self.playing_now = selected_tracks
            self.playingTitle.config(text=self.playing_now[:-4])
        except:
            pass


# check tracks end and go to the next track
def check_event():
    while True:
        time.sleep(0.5)
        for event in pg.event.get():
            if event.type == MUSIC_END:
                player.change_to_next_track()


main = tk.Tk()
player = Player(main)
main.title('SoulMusic')
main.configure(bg='#FCE0D5')
main.iconbitmap('img\\appicon.ico')
main.resizable(False, False)
main.geometry('800x600')

#second thread for check tracks end
check_thread = threading.Thread(target=check_event, daemon=True)
check_thread.start()
main.mainloop()
