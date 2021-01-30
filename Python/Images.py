from google_images_download import google_images_download
import os
import FileFolder

class Images:
    extension = "jpg"
    download_path = "IMAGE DIRECTORY"

    def __init__(self, search_word, num_of_images):
        self.List = [search_word, self.extension]
        s = " "
        self.SearchWord = s.join(self.List)
        self.nImages = num_of_images

        # Delete and remake directory
        FileFolder.delete_folder(self.download_path)
        FileFolder.make_folder(self.download_path)

        # Get images
        self.get_images()

        # Do the renaming because the API returns 1.<filename>.gif, 2.<filename>.gif etc...
        self.rename_images()

    def get_images(self):
        response = google_images_download.googleimagesdownload()
        arguments = {"keywords": self.SearchWord,
                     "format": self.extension,
                     "limit": self.nImages,
                     "output_directory": self.download_path,
                     "no_directory": True
                     }
        response.download(arguments)

    def rename_images(self):
        for i in range(1, self.nImages + 1):
            for filename in os.listdir(self.download_path):
                if filename.startswith(str(i) + "."):
                    os.rename(os.path.join(self.download_path, filename),
                              os.path.join(self.download_path, "image" + str(i) + ".gif"))
                else:
                    continue
