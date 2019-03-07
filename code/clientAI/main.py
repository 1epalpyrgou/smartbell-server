import speech_recognition as spreg
#import unicodedata
from nltk.corpus import stopwords
import aicommands

assistant_name=['βαγγέλη', 'βαγγελάκη']
stopwordsGreek=stopwords.words('greek')

   
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def main():
      recog = spreg.Recognizer()

      aiCalled=False
      calledAI=0

      while True:
         with spreg.Microphone(sample_rate = 48000, chunk_size = 8192) as source:
            print('Σε ακούω, πες κάτι:')
            recog.adjust_for_ambient_noise(source)      
            speech = recog.listen(source)

         try:
            print('Περίμενε λίγο... εξετάζω αν με φώναξες...')
            requestText = recog.recognize_google(speech, language='el-GR').lower()      
            print('Σε άκουσα να λες: %s' % requestText)

            tokens = [t for t in requestText.split()] 
            #print (tokens)

            tokens = [i for i in tokens if not i in stopwordsGreek]
            #print(tokens)

            aiTokens=[]

            for i in range(0, len(tokens)):
                if aiCalled:
                    aiTokens.append(tokens[i])
                if not aiCalled and tokens[i] in assistant_name:
                     aiCalled=True

            aiTokens = [x for x in aiTokens if x not in assistant_name]
                  
            if aiCalled==True and aiTokens:
                  aicommands.takeAction(aiTokens)
                  aiCalled=False
                  calledAI=0
            elif aiCalled==True and not aiTokens and calledAI==0:
                  aicommands.sayWaitForCommand()
                  calledAI=1
            elif aiCalled==True and not aiTokens and calledAI==1:
                  aicommands.sayWaitForCommandTwice()
                  calledAI=2
            elif aiCalled==True and not aiTokens and calledAI==2:
                  aicommands.sayWaitForCommandTriple()
                  aiCalled=False
                  calledAI=0
           
         except spreg.UnknownValueError:
            print('Δεν αναγνώρισα κάποιο κείμενο')
            
         except spreg.RequestError as e: 
            print('Ουπς.. Υπάρχει κάποιο πρόβλημα αυτή τη στιγμή με την υπηρεσία αναγνώρισης φωνής')


if __name__== '__main__':
    main()
      
