import time
import vlc
import datetime
import hashlib

import pafy
import urllib
import re

from pathlib import Path
from gtts import gTTS

instance = vlc.Instance()
player = instance.media_player_new()

#def playyoutubesong(self, textToSearch):
#        url = query_youtube_video(textToSearch)[0]
#        v = pafy.new(url)
#        media = instance_vlc.media_new(v.getbest().url)
#        player_vlc.set_media(media)
#        player_vlc.play()

def youtube(query):
    query_string = urllib.parse.urlencode({'search_query' : query},  {'safeSearch':'strict'})
    html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url = "http://www.youtube.com/watch?v=" + search_results[0]
    print('Got YouTube URL: %s' % url)

    video = pafy.new(url)
    title = video.title
    print('Title: %s' % title)
    bestaudio = video.getbestaudio()
    #print(bestaudio.url)
    playurl = bestaudio.url

    #bestaudio.download()

    #oldtitlepath = "/home/pi/computer/" + title
    #os.rename(oldtitlepath, 'song.webm')
    #command = "runuser -l pi -c 'cvlc --play-and-exit /home/pi/computer/song.webm &'"
    #subprocess.call(command, shell=True)

    media = instance.media_new(playurl)
    player.set_media(media)
    player.play()
    time.sleep(1)
    duration = player.get_length() / 1000
    print('Duration: %d' % duration)


        
def md5(text):
      return hashlib.md5(text.encode('utf-8')).hexdigest()


def mp3playfunc(filename):     
      print ('Αναπαραγωγή αρχείου ήχου: %s' % filename)
      
      media = instance.media_new(filename)
      player.set_media(media)
      
      playing = set([1,2,3,4])
      
      player.play()

      time.sleep(1)

      time_left = True
      while time_left == True:
          time.sleep(0.3)
          song_time = player.get_state()
          if song_time not in playing:
              time_left = False


def gttsfunc(text):
      filename='gtts-' + md5(text) + '.mp3'

      if not Path(filename).is_file():
            #print ('Δημιουργία αρχείου ήχου με κείμενο: %s' % text)         
            tts = gTTS('%s' % text, 'el')
            tts.save(filename)

      mp3playfunc(filename)


def sayWaitForCommand():
    gttsfunc('Παρακαλώ')


def sayWaitForCommandTwice():
    gttsfunc('Είπα παρακαλώ')


def sayWaitForCommandTriple():
    gttsfunc('Εντάξει εσύ το παράκανες')


def takeAction(tokens):
      print('Σε άκουσα να λες το όνομά μου!')

      #print(tokens)

      cmd=['άναψε', 'φώτα']
      if set(cmd).issubset(tokens) :
                gttsfunc('Θα το έκανα αν μου είχατε τοποθετήσει ένα ρελέ')

      cmd=['ώρα', 'είναι']
      if set(cmd).issubset(tokens):
                gttsfunc('Η ώρα είναι %s' % time.strftime('%I:%M'))

      cmd1=['μέρα', 'είναι']
      cmd2=['μέρα', 'έχουμε']
      if set(cmd1).issubset(tokens) or \
         set(cmd2).issubset(tokens):
                weekDayStr=['Κυριακή','Δευτέρα','Τρίτη','Τετάρτη','Πέμπτη','Παρασκευή','Σάββατο']
                weekDayNum=int(time.strftime('%w'))
                gttsfunc('Σήμερα είναι %s' % weekDayStr[weekDayNum])

      cmd1=['χτύπα', 'κουδούνι']
      cmd2=['χτυπά', 'κουδούνι']
      cmd3=['βάρα', 'κουδούνι']
      if set(cmd1).issubset(tokens) or \
         set(cmd2).issubset(tokens) or \
         set(cmd3).issubset(tokens):
                gttsfunc('Θα χτυπήσω το κουδούνι τώρα')
                mp3playfunc('bell.mp3')

      cmd1=['πηγαίνεις', 'σχολείο']
      cmd2=['ποιο', 'πας', 'σχολείο']
      cmd3=['ποιο', 'είναι', 'σχολείο']
      if set(cmd1).issubset(tokens) or \
         set(cmd2).issubset(tokens) or \
         set(cmd3).issubset(tokens):
                gttsfunc('Πηγαίνω στο πρώτο επαγγελματικό λύκειο πύργου')


      cmd1=['παίξε', 'youtube']
      cmd2=['βάλε', 'youtube']
      if set(cmd1).issubset(tokens) or \
         set(cmd2).issubset(tokens):
            gttsfunc('Σύντομα θα αρχίσει η αναπαραγωγή')
            tokens.append('τραγούδι')
            tokens2 = [x for x in tokens if (x not in cmd1) and (x not in cmd2)]
            removeWords=['από', 'βάλε', 'μουσική']
            tokens3 = [x for x in tokens2 if x not in removeWords]

            querystr=" ".join(tokens3)
            print('Query youtube with text: %s' % querystr)
            youtube(querystr)


      #else:
      #gttsfunc('Συγνώμη δεν κατάλαβα τι είπατε')
