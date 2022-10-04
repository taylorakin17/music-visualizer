# create file in _posts/ with current date and title
# usage: python3 create_post.py "title of post"

import os
import datetime
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Create a new post')
    # add an optional argument called title
    parser.add_argument('--title', '-t', help='Title of the post', type=str)
    args = parser.parse_args()
    if args.title:
        title = args.title
    else:
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