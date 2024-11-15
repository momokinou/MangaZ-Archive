# MangaZ Archiving script

If you're using Brave as a browser, you have almost nothing to do.

You'll need Python 3 and some package:

- pip install selenium
- pip install undetected-chromedriver
- pip install beautifulsoup4
- pip install requests
- pip install pillow
- pip install setup tool

and a chromedriver:

- For Windows: https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/win64/chromedriver-win64.zip
- For Linux: https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/linux64/chromedriver-linux64.zip

Unzip the chromedriver. Place the chromedriver FOLDER in the project folder.

Screen of the correct project folder:
![Correct folder](https://cdn.discordapp.com/attachments/1304539356886728766/1305546971972370592/image.png?ex=6734159e&is=6732c41e&hm=36db03e62d45da4cc65612f03e7051300ba13cf3083fe560901fe622266cec58& "Correct folder")

Tested only on windows.

1. Do you have a number on the total size of all the manga?

- 4609 manga + 865 r18

2. Does it download the samples for the paid content?

- It does download the samples for the paid content + it is downloaded in a special folder named "paywall".

3. Do author and book title come with the download or will that have to be edited?

- With each manga, you get a .json where you can find the authors, providers, description and links to all chapters/books
