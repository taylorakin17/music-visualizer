# create file in _posts/ with current date and title
# usage: python3 create_post.py "title of post"

import os
import datetime

def main():
    # get title from command line
    title = input("Title: ")
    if title == "":
        title = "weekly_update"
    # get current date
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # create filename
    filename = date + '-' + title.replace(' ', '_') + '.md'

    # create file
    with open(os.path.join('../docs/_posts', filename), 'w') as f:
        f.write('---\n')
        f.write('title: ' + '"Week of "' + '\n')
        f.write('date: ' + date + '\n')
        f.write('---\n')

if __name__ == '__main__':
    main()