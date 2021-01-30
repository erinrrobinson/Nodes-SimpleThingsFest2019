from Haiku import Haiku
from Images import Images
from Sounds import Sounds
from datetime import datetime, timedelta


class Project:
    Haiku = None
    Images = None
    Sounds = None

    def __init__(self, search_word, num_files, timeout):
        self.SearchWord = search_word
        self.Num_Files = num_files
        self.Timeout = timeout
        self.generate_images()
        self.generate_haiku_text()
        print("!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!")

        print("!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!")
        self.generate_sounds()


    def generate_haiku_text(self):
        start = datetime.now()
        print('***Generating Haiku Text...***')
        self.Haiku = Haiku(self.SearchWord, self.Timeout)
        print('***Finished generating Haiku Text in ' + str(datetime.now() - start) + ' seconds***')

    def generate_sounds(self):
        start = datetime.now()
        print('***Generating Sounds...***')
        self.Sounds = Sounds(self.SearchWord, self.Num_Files)
        print('***Finished generating Sounds in ' + str(datetime.now() - start) + ' seconds***')

    def generate_images(self):
        start = datetime.now()
        print('***Generating Images...***')
        self.Images = Images(self.SearchWord, self.Num_Files)
        print('***Finished generating Images in ' + str(datetime.now() - start) + ' seconds***')


