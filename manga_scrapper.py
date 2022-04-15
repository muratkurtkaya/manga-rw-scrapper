import subprocess
import requests
from bs4 import BeautifulSoup
import os
import threading
import glob

class Chapter:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.pageUrl = self.url.split('/')[2]
        self.mangaName = ' '.join(self.url.split('/')[-2].split('chapter')[0].split('-')).rstrip()
        self.chapterNumber = url.split('chapter')[1].split('-')[1]

    def getNextChapter(self):
        possibleNextChapter = "https://" + self.pageUrl + self.soup.find_all(class_='nextchap')[1].get('href')
        if "reader" in possibleNextChapter:
            return possibleNextChapter
        else:
            return None

    def downloadChapterImages(self):
        images = self.soup.findAll('img')
        for image in images:
            imageSrc = image['src']
            if "chapter" in imageSrc:
                # print(imageSrc)
                r = requests.get(imageSrc)
                fileName = imageSrc.split('/')[-1][:-4].zfill(2) + ".jpg"
                with open("tmpImages/" + fileName, 'wb') as f:
                    f.write(r.content)

    def convertImagesIntoPdf(self):
        if not os.path.exists("mangas/" + self.mangaName):
            os.mkdir("mangas/" + self.mangaName)
        subprocess.call(["convert", "-density", "300", "tmpImages/*.jpg",
            "mangas/" + self.mangaName + "/" + self.mangaName + "-" + self.chapterNumber + ".pdf"])

    def deleteImages(self):
        files = glob.glob('tmpImages/*.jpg')
        for f in files:
            os.remove(f)

    def run(self):
        self.deleteImages()
        self.downloadChapterImages()
        print(self.mangaName +"-"+ self.chapterNumber)
        self.convertImagesIntoPdf()

if __name__ == '__main__':
    url = 'https://www.manga-raw.club/reader/en/storm-inn-chapter-1-eng-li/'
    # url = "https://www.manga-raw.club/reader/en/shindorim-chapter-10-eng-li/"
    chapter = Chapter(url)
    # print(chapter.chapterNumber)
    while True:
        chapter.run()

        if (chapter.getNextChapter() is None):
            break
        chapter = Chapter(chapter.getNextChapter())
    
    