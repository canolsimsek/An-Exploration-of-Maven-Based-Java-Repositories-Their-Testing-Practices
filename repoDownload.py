import requests
import os
from github import Github, UnknownObjectException

TOKEN = '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'
GITHUBSEARCHURL = 'https://api.github.com/search/repositories?q=topic:ai+language:java&sort=stars&order=desc&per_page=100&page=2'

headers = {'Authorization': 'token ' + TOKEN}
req2 = requests.get(GITHUBSEARCHURL)
result = req2.json()
parent_dir = 'D:\deneme3\RAPOR\project_src'

items = result['items']
github = Github(login_or_token=TOKEN)


def sanitize_dirname(dirname):
    invalid_chars = [':', '.', '\\', '/', '*', '?', '<', '>', '|']
    for ch in invalid_chars:
        dirname = dirname.replace(ch, '-')
    return dirname


def downloadIfPomExists(github, item):
    global item_count
    item_count = item_count + 1
    print(item_count)
    repoToBeDownloaded = item

    try:
        repo = github.get_repo(item['full_name'])
        have_pom = pomCheck(repo)
        
        if have_pom:
            directory = sanitize_dirname(repoToBeDownloaded['name'])
            path = os.path.join(parent_dir, directory)

            makeDirAndClone(parent_dir, repoToBeDownloaded, directory)
            print('Downloaded: {repo_name}'.format(repo_name=repoToBeDownloaded['full_name']))

    except Exception as e:
        print(e)


def makeDirAndClone(parent_dir, repoToBeDownloaded, directory):
    try:
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        os.chdir(parent_dir)
        os.system(('git clone --depth 1 --branch master {repo_url} {name}').format(repo_url=repoToBeDownloaded['clone_url'], name=directory))

    except Exception as e:
        print(e)


def pomCheck(repo):
    try:
        repo.get_contents(path='pom.xml')
        return True

    except UnknownObjectException as e:
        return False


item_count = 0
for item in items:
    downloadIfPomExists(github, item)
