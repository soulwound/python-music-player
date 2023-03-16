<h1 align="center">PythonMusicPlayer</h1>

![GitHub top language](https://img.shields.io/github/languages/top/soulwound/python-music-player?style=flat-square)
![GitHub watchers](https://img.shields.io/github/watchers/soulwound/python-music-player?style=flat-square)
![GitHub repo file count](https://img.shields.io/github/directory-file-count/soulwound/python-music-player?style=flat-square)

<h2>Аудио плеер на python. Разработан при помощи модулей TKinter, Pygame и threading.</h2>
<h3>Протестирована и подтверждена работа с MP3 и WAV файлами</h3>
<p>В качестве директории с композициями стоит выбирать папку, содержащую только файлы аудио форматов, т.к. фильтрация файлов еще не реализована.</p>

<p>Внешний вид программы представляет из себя одно окно, включающее некоторый функционал.</p>
<image src="https://github.com/soulwound/python-music-player/blob/master/img/demo-pic-3.png" alt="Рабочая область плеера">
<image src="https://github.com/soulwound/python-music-player/blob/master/img/demo-pic-2.png" alt="Окно плеера во время воспроизведения">

<h3>Возможности программы на данный момент:</h3>
<ul>
  <li>Выбор папки с композициями по нажатию на кнопку в виде папки</li>
  <li>Выбор композиции из списка для ее дальнейшего воспроизведения</li>
  <li>Автоматический переход на следующий файл в плейлисте</li>
  <li>Регулировка громкости при помощи ползунка</li>
  <li>Приостановка и возобновление воспроизведения</li>
</ul>

<h2 align="center">Интересные моменты, с которыми я столкнулся и которые отличают данный проект от ему подобных</h2>
<p>Реализация ползунка громкости при помощи Scale из Tkinter показалась мне интересной идеей. Сделать эту функцию было не сложно, 
но по каким-то причинам в других проектах я такого не встречал.</p>

Здесь проходит создание объекта класса Scale и его кастомизация, а также передача параметру command функции, отвечающей за смену громкости.
```python
        self.volumeControl = tk.Scale(orient=tk.HORIZONTAL, length=130, from_=0.0, to=100.0, bg='#FCE0D5', bd=0,\
                                      activebackground='#B47EB2', command=self.change_volume, troughcolor='#99D0D3',\
                                      font=track_list_font, highlightthickness=0)
        self.volumeControl.set(50)
        self.volumeControl.place(x=650, y=500, height=50)
```
Функция смены громкости. Вызывается при изменении значения ползунком. Значение передается в mixer.music.set_volume
```python
    def change_volume(self, master):
        pg.mixer.music.set_volume(self.volumeControl.get()/100)
```
<p>Чтобы реализовать автоматический переход на следующую композицию при окончании текущей требовалось перехватывать событие окончания воспроизведения, 
но через зацикливание проверки это сделать не получилось. На помощь пришел модуль threading. Добавив цикличную проверку в другой поток, я реализовал эту функцию.</p>

Функция цикличной проверки
```python
def check_event():
    while True:
        time.sleep(0.5)
        for event in pg.event.get():
            if event.type == MUSIC_END:
                player.change_to_next_track()
```
Назначаю ее в другой поток
```python
check_thread = threading.Thread(target=check_event, daemon=True)
check_thread.start()
```
<h2>Далее я планирую:</h2>
<ul>
  <li>Добавить фильтрацию файлов, чтобы отсеивать все, кроме аудио форматов</li>
  <li>Добавить отображение обложки для воспроизводимой композиции</li>
  <li>Сделать progressbar для воспроизводимой композиции</li>
</ul>
