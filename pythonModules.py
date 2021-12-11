from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

from urllib.error import URLError
from urllib.error import HTTPError

# button-group--pagination
# unstyled
# https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page=3
# https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page=500

# url = 'https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules'

# path = 'full_python_modules.csv'


def module_info(res):
    modules_cnt = res.find(class_='unstyled').find_all('li')


def new_bs(url):
    try:
        res = urlopen(url)
    except URLError as e:
        print('server error!', e)
        return None
    except HTTPError as e:
        print('response error!', e)
        return None
    html = res.read()
    return BeautifulSoup(html, 'html.parser')

# bs = new_bs('https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page=500')

# module_info(bs)


def storePyModule(path, url):
    bs = new_bs(url)
    if bs != None:
        data = module_info(bs)
    else:
        print(url)
    with open(path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

# Get number of latest-page


def latest_page_number():
    return 2

# Get number of first-page


def first_page_number():
    return 1

# extract modules-data
# name, version, time, description, link
# [ {name:, version:, time: ,desc:, link}, {same} ]

# get name of module


def module_name(module):
    try:
        name = module.find(
            class_='package-snippet__title').find(class_='package-snippet__name').get_text().strip()
        return name
    except AttributeError:
        return "doesn't has a name!"


def module_version(module):
    try:
        version = module.find(
            class_='package-snippet__title').find(class_='package-snippet__version').get_text().strip()
        return version
    except AttributeError:
        return "doesn't has a version!"


def module_time(module):
    try:
        released_time = module.find(
            class_='package-snippet__title').find(class_='package-snippet__released')
        # if released_time.has_attr('title'):
        #     released_time = released_time.attrs['title']
        # else:
        #     released_time = released_time.get_text()
        # print(released_time.attrs['title'])
        return released_time.get_text().strip('\n').strip()
    except AttributeError:
        return "doesn't has a released time!"


def module_desc(module):
    try:
        description = module.find(
            class_='package-snippet__description').get_text().strip()
        return description
    except AttributeError:
        return "doesn't has a description!"


def module_link(module):
    link = 'https://pypi.org/'
    module_link = module.find('a', {'class': 'package-snippet'})
    if(module_link != None):
        if module_link.has_attr('href'):
            link += module_link.attrs['href']
        else:
            link = 'none!'
        return link
    else:
        return "doesn't has link!"


def get_module_data(module):
    name = module_name(module)
    version = module_version(module)
    time = module_time(module)
    desc = module_desc(module)
    link = module_link(module)
    mdoule_data = {'name':name, 'version':version, 'released_time':time, 'description':desc, 'link':link}
    # print('module_data: ')
    # print('')
    return mdoule_data


def extractModules(modulesSoup):
    # modules-data
    modules_data = []
    # fetch all modules in page
    modules_cnt = modulesSoup.find(
        class_='unstyled').find_all('li')  # <li> tag
    # calc number of modules in page
    numberFModules = len(modules_cnt)
    #  استخراج كل مكتبة علي حدي
    for module in modules_cnt:
        # get module-date
        module_data = get_module_data(module)  # {}
        # insert module-data
        modules_data.append(module_data)
    return modules_data

# Save page-modules-data


def storePageModulesCsv(modules_data):
    return ''


def pythonModules():
    standardUrl = 'https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page='

    firstPage = first_page_number()  # 1
    latestPage = latest_page_number()  # 500

    while firstPage <= latestPage:
        # handle URL
        url = standardUrl+str(firstPage)
        # ready bs
        modulesSoup = new_bs(url)
        if modulesSoup != None:
            # extract modules-info from url
            modules_data = extractModules(modulesSoup)
            # store modules-data in csv file
            # modulesInfo = storePageModulesCsv(modules_data)
            print('------------')
            print('> url: ', url)
            print(modules_data)
            print('------------')
            # print('> modules: ', modulesInfo.modules_num)
            # if modulesInfo.success:
            #     print('success store!')
            # else:
            #     print('failed store!')
            # print('------------')
        else:
            print('------------')
            print('error in url: ', url)
            print('------------')
        firstPage += 1


pythonModules()

# # print('https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page=',str(1))

# # print(len('https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page='))


# strr = '''https://pypi.org/search/?c=Topic+%3A%3A+Software+Development+%3A%3A+Libraries+%3A%3A+Python+Modules&page='''
# # print(strr[0])
# # strr[len(strr)+1]='1'
# # print(strr.split())
# i =1
# print(strr+str(i))
