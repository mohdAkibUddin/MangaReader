import string
import requests
from bs4 import BeautifulSoup
import os
from shutil import make_archive, rmtree

mangaName = input('Enter the name of the manga exactly as it appears on mangapanda.com: ')
chapter = input('What chapter do you want to read? Enter integers only: ')
fileDirectory = input('Copy and paste the path of the directory you would like the manga to be stored in (Or press '
                      'enter to use the default storage): ')
if fileDirectory == '':
    fileDirectory = "mangaStorage"
mangaName = mangaName.replace(' ', '-')
mangaNameClean = ''
for letter in mangaName:
    if letter not in (string.punctuation.replace('-', '')):
        mangaNameClean += letter
mangaName = mangaNameClean

nameAndChapter = '/' + mangaName + '_chapter_' + chapter
access_rights = 0o777
try:
    os.mkdir(fileDirectory + nameAndChapter, access_rights)
except PermissionError:
    print("failed to access manga panda")
else:
    print("successfully accessed manga panda")

url = requests.get('http://www.mangapanda.com/' + mangaName + '/' + chapter)
sourceCode = url.text
soup = BeautifulSoup(sourceCode, 'html.parser')

pageCount = soup.find_all("div", {"id": "selectpage"})
x = str(pageCount)
totalPages = int(x.strip('</div>]')[-3:])

for pageNum in range(1, totalPages + 1):
    url = requests.get('http://www.mangapanda.com/' + mangaName + '/' + chapter + '/' + str(pageNum))
    sourceCode = url.text
    soup = BeautifulSoup(sourceCode, "html.parser")
    images = soup.find_all("img", {"id": "img"})
    for image in images:
        urlOfImage = requests.get(image['src'])
        with open(fileDirectory + nameAndChapter + '/' + mangaName + str(pageNum) + '.jpg', 'wb') as picture:
            picture.write(urlOfImage.content)
    print(str(pageNum) + " pages downloaded")

baseName = fileDirectory + nameAndChapter
make_archive(baseName, "zip", baseName)
nameOfZipFile = fileDirectory + nameAndChapter + '.zip'
rmtree(baseName)
os.rename(nameOfZipFile, baseName + '.cbz')


