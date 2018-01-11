import io
import re
import os
import subprocess
import webbrowser

current_dir = os.path.dirname(os.path.realpath(__file__))
new_images = []
processed_images = []

new_images_dir = 'new'
processed_images_dir = 'processed'

# scan the directory for new image
while True:
    new_images = os.listdir(os.path.join(current_dir, new_images_dir))
    if len(new_images) == 0:
        continue
    
    # run tesseract
    image = new_images[0]
    # chi_sim, HanS
    subprocess.run(["tesseract", os.path.join(current_dir, new_images_dir, image), "result", "-l", "chi_sim", "--psm", "6"])


    # get the question only
    with io.open('result.txt', encoding="utf-8") as f:
        
        text = f.read()
        question = ''
        options = []

        #print("Raw: ", text)

        # first remove the question number
        for i, c in enumerate(text):
            if c.isdigit() and text[i+1] == '.':
                text = text[i+2:]
                break

        # second find the question mark
        for i, c in enumerate(text):
            if c == '?' or c == '7':
                question = text[:i]
                text = text[i+2:]
                break

        question = re.sub('[\s+]', '', question)

        # third list all options, assume they are separated by new line
        options = text.split('\n')
        options = [re.sub('[.·,"《》abcdABCD\s+]', '', choice) for choice in options if not choice.isspace() if choice != '']
        
        print(question)
        print(options)

    # search in browser
    url = "www.baidu.com/s?wd={}".format(question)    
    webbrowser.open(url)

    # move file to processed
    os.rename(os.path.join(current_dir, new_images_dir, image), os.path.join(current_dir, processed_images_dir, image))