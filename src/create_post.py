# create file in _posts/ with current date and title
# usage: python3 create_post.py "title of post"

import os
import datetime
import sys

def main():
    # get title from command line
    title = sys.argv[1]

    if title == "":
        title = "weekly_update"

    # get date of the monday of the current week
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    date = monday.strftime('%Y-%m-%d')

    # create filename
    filename = date + '-' + title.replace(' ', '_') + '.md'

    # create file
    with open(os.path.join('../docs/_posts', filename), 'w') as f:
        f.write('---\n')
        f.write('title: ' + 'Week of ' + '\n')
        f.write('date: ' + date + '\n')
        f.write('---\n')

if __name__ == '__main__':
    main()