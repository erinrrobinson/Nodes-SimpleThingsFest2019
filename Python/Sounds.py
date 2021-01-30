import freesound
import os
import pydub
import FileFolder


class Sounds:
    TOKEN = "TOKEN"
    AUTH_TYPE = "AUTH"
    dir = "SOUNDS DIRECTORY"
    Sounds = None

    def __init__(self, search_word, num_of_sounds):
        self.SearchWord = search_word
        self.nSounds = num_of_sounds

        #Delete and remake directory
        FileFolder.delete_folder(self.dir)
        FileFolder.make_folder(self.dir)

        # Download sounds
        self.sound_download()

        # Rename sounds
        self.rename_sounds()

        # Convert sounds
        self.convert_sounds()

        # Remove mp3s
        FileFolder.remove_files(self.dir, "mp3")

    def sound_download(self):
        client = freesound.FreesoundClient()
        client.set_token(self.TOKEN, self.AUTH_TYPE)
        self.Sounds = client.text_search(query=self.SearchWord, page_size=4,
                                         fields="id,name,previews", duration=(1, 5))
        for sound in self.Sounds:
            sound.retrieve_preview("", self.dir + sound.name + ".aiff")
            print('Generated file: ' + sound.name)

    def rename_sounds(self):
        filenum = 1
        for filename in os.listdir(self.dir):
            dst = "haiku" + str(filenum) + ".mp3"
            src = self.dir + filename
            dst = self.dir + dst

            # rename() function will rename all the files
            os.rename(src, dst)

            filenum += 1

    def convert_sounds(self):
        sound_count = 0
        for i in range(1, self.nSounds + 1):
            if FileFolder.does_file_exist(self.dir + 'haiku' + str(i) + '.mp3'):
                original_file = self.dir + 'haiku' + str(i) + '.mp3'
                converted_file = self.dir + 'haiku' + str(i) + '.wav'
                sound = pydub.AudioSegment.from_mp3(original_file)
                sound.export(converted_file, format="wav")
                sound_count += 1
        print('Number of sounds generated: ' + str(sound_count))
