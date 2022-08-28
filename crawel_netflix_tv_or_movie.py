import requests
from bs4 import BeautifulSoup
import re
from math import ceil
from time import time
#import try2  #d
import csv
from IMDB_API import IMDB_API

ITEM_PER_PAGE = 120

def get_number_of_elements(soup_instance):
    search_key_word_titles = soup_instance.find_all(string=re.compile(r"\d+ titles"))[0]
    title_number_pattern = r'(\d+) titles'
    return re.search(title_number_pattern, str(search_key_word_titles)).group(1)


def split_index_page(url_suffix:str, total_items_numbers:int):
    sub_page_number = total_items_numbers // ITEM_PER_PAGE + 1
    print('{0} has {1} movies/tv show,split into {2} segments'.format(url_suffix, total_items_numbers, sub_page_number))
    index_sub_page_urls = []
    for i in range(sub_page_number):
        print(url + f'/?start={i * 120}#results')
        index_sub_page_urls.append(url+f'/?start={i*120}#results')
    return index_sub_page_urls

def getHtmlList(url):

    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}
        r = requests.get(url, headers = headers, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text,'lxml')
        return soup
    except:
        pass

def transfer(select_t): # parameter need to be 'bs4.element.Tag'
    #print(type(select_t))
    #data = [i.text for i in select_t]
    data = [i for i in select_t]
    if len(data) == 1:
        return data[0]
    else:
        print('data not only one element')
def time_transfer(str1):
    h_pattern = r'(\d*)(?=hr)'
    m_pattern = r'(\d*)(?=m)'
    hour = re.search(h_pattern,str1)
    if hour:
        hour_1 = int(hour.group())
    else:
        hour_1 = 0
    minute = re.search(m_pattern,str1)
    if minute:
        minute_1 = int(minute.group())
    else:
        minute_1 = 0
    time1 = hour_1*60+minute_1
    return time1
def date_transfer(str1):
    pattern = r'(\d+)\w* (\w+) (\d+)(?= )'
    total = re.search(pattern,str1)
    try:
        year = total.group(3)
        day = total.group(1)
    except AttributeError:
        year = 'None'
        return None, year
    month = total.group(2)
    month_n = month_d[month]
    current = year+'/'+str(month_n)+'/'+day
    correct = int(year)*12 + int(month_n) +int(day)# 2020 Dec = 2020*12+ 12

    return current,year
    #return correct

def language_record(str1):
    pattern = r'(?<=Audio: )([\w, \[\]]+)(?!, )'
    pattern_check = r'Audio Description'
    pattern_desc = r'(?<=Audio Description[,:] )([\w ,\[\]]+)(?!, )'
    check = re.search(pattern_check,str1)
    language = re.search(pattern,str1).group()
    if check:
        try: # has audio description, but nothing in there : https://can.newonnetflix.info/info/81046255
            des_lan = re.search(pattern_desc,str1).group()
        except AttributeError:
            des_lan = ''
    else:
        des_lan = ''

    return language,des_lan

def find_desc (ite,test):
    check = False
    for i in ite:
        it = i.text
        if check == True:
            return it

        if test in it:
            check = True

    return []

def find_desc_tv (ite,test):
    check = False
    pattern1 = r'(?<=Status:) ([\w ]+)'

    l1 = []
    ite1 = iter(ite)
    for i in ite1:
        it = i.text

        if check == True:
            try:
                j = re.search(pattern1,it).group(1)
            except AttributeError: #no status
                j = ''
            l1.append(j)
            pattern2 = r'{0}(.+)'.format(j)
            if j == '':
                pattern2= r'(?<=Status:) (.+)'
            k = re.search(pattern2,it,flags = re.S)
            if k:
                l1.append(k.group(1))

            return l1
        if test in it:
            check = True


def rating_pro(dic1):
    percent = r'\d+(?=%)'
    base_10 = r'[\d.]+(?=/10)'
    base_100 = r'[\d.]+(?=/100)'
    base_5 = r'[\d.]+(?=/5)'
    l2 = []
    for i in dic1:
        if '%' in dic1[i]:
            tempt = re.search(percent,str(dic1[i])).group()
            dic1[i] = float(tempt)/100
            l2.append(float(tempt)/100)
        elif '/100' in dic1[i]:
            tempt = float(re.search(base_100, str(dic1[i])).group())
            dic1[i] = round((tempt / 100), 2)
            l2.append(round((tempt / 100), 2))
        elif '/10' in dic1[i]:
            tempt = float(re.search(base_10,str(dic1[i])).group())
            dic1[i] = round((tempt/10),2)
            l2.append(round((tempt/10),2))
        elif '/5' in dic1[i]:
            tempt = float(re.search(base_5, str(dic1[i])).group())
            dic1[i] = round((tempt /5), 2)
            l2.append(round((tempt /5), 2))
    return l2,dic1

def Movie_info(soup):
    total_content = soup.find_all('p')
    test3 = 'Cast'
    test4 = 'Director'
    test5 = 'Duration'
    test6 = 'Date Added'
    test7 = 'Certificate'
    test8 = 'Audio:'
    test10 = 'Subtitles:'

    test5_2 = 'Episode Length'
    test_tv_1 = 'Available Season'
    for i in total_content:
        i_t = i.text
        if test3 in i_t:
            data3_1 = i_t
        if test4 in i_t:
            data4_1 = i_t
        if test5 in i_t: #key word duration
            data5_1 = i_t
            if 'Part' in i_t: #switch to tv check with finding of parts
                return False
            elif 'Season' in i_t: # switch to tv check with finding of parts
                return False
        if test6 in i_t:
            data6_1 = i_t
        if test7 in i_t:
            data7_1 = i_t
        if test8 in i_t:
            data8_1 = i_t
        if test10 in i_t:
            data10_1 = i_t
        if test5_2 in i_t: #switch to tv-show check
            if special1 != 4 and special1 != 5 and special1 != 8 and special1 != 9 and special1 != 10 and special1 != 13:
                return False
        if test_tv_1 in i_t:
            return False


    record = []

    #data1 = soup.select('body > div.wrapper > section:nth-child(2) > h1')
    data1 = soup.find('h1')
    data1 = transfer(data1) # record 1 is name
    data1 = data1.replace('Info Page:', '')
    data1 = data1.strip(' ')
    #data2 = soup.select("body > div.wrapper > article > aside > div.genre > h5")#genre
    #data2 = strhtml.find_all('div', class_ ='wrapper')
    data2_1 = soup.select("body > div.wrapper > article > aside > div.genre > h5")
    data2_2 =[i.text for i in data2_1]
    data2_3 = data2_2[0].split(', ')
    data2 = ','.join(data2_3)
    #3-name of cast
    #data3_1 = soup.select('body > div.wrapper > article > p:nth-child(28)')#name of casts
    try:
        data3_2 = data3_1.lstrip('is Cast:')
    except UnboundLocalError:
        data3_2 ='None'
    #pattern = r'(?<=>)[\w ]+(?=</a>)'
    # data3 = re.findall(pattern,str(data3_1))
    data3_3 = data3_2.split(', ')
    data3 = ','.join(data3_3)


    #data4_1 = soup.select("body > div.wrapper > article > p:nth-child(26) > a") #record director
    # data4 = re.findall(pattern,str(data4_1))
    try:
        data4_2 = data4_1.lstrip('Director: ')
    except UnboundLocalError:
        data4_2 = 'None'

    data4_3 = data4_2.split(', ')    # use lost in case there are more than two director
    data4 = ','.join(data4_3)


    #data5_1 = soup.select("body > div.wrapper > article > p:nth-child(21)") # record the duration
    #data5_2 = [i.text for i in data5_1]
    #data5 = time_transfer(str(data5_2))
    data5_2 = data5_1.lstrip('Duration: ')

    #if 'Limited' in data5_2:
    #    data5 = 'None'

    if data1.lower() == 'A lion in the House'.lower():
        data5 = 225
    elif special1 == 13:
        data5 = 90
    else:
        data5 = time_transfer(str(data5_2))

    #6-available data
    #data6_1 = soup.select("body > div.wrapper > article > p:nth-child(8)") # available_date
    #data6_2 = [i.text for i in data6_1]
    #data6 = date_transfer(str(data6_2))
    data6_2 = data6_1.lstrip('Date Added')
    print('time is',data6_2)
    data6,year = date_transfer(data6_2)


    #data7_1 = soup.select("body > div.wrapper > article > p:nth-child(19) > span.ratingsblock") # parent control
    #data7 = transfer(data7_1)
    data7 = []
    pattern1 = r'(?<=Certificate: )([\w-]+)'
    data7_3 = re.findall(pattern1,data7_1)
    for n in data7_3:
        data7.append(n)
    data7 = ','.join(data7)
    #data8_1 = soup.select("body > div.wrapper > article > p:nth-child(22)")#language
    # data8_2 = transfer(data8_1)

    # data8 &9, Audio and audio description
    data8_2,data9_2 = language_record(data8_1)
    data8 = data8_2.split(', ')
    data9 = data9_2.split(', ')
    data8 = [i.rstrip() for i in data8]
    data9 = [i.rstrip() for i in data9]
    data8 = ','.join(data8)
    data9 = ','.join(data9)
    #data10 substitle
    try:
        data10_1 = data10_1.lstrip('Subtitles: ')
    except UnboundLocalError:
        data10 = ''
    else:
        data10_1 = data10_1.split(', ')
        data10 = [i.rstrip() for i in data10_1]
    data10 = ','.join(data10)
    #11 - description
    #data11_1 = soup.select("body > div.wrapper > article > p:nth-child(31)")
    #document.querySelector("body > div.wrapper > article > h4:nth-child(27)")
    #if str(data12_1) == '[<p></p>]': #show
    #    data12_1 = soup.select('body > div.wrapper > article > p:nth-child(26)')
    tmpt = soup.find_all({'h4','p'})
    test11 = 'Box Office Details:'
    data11 = find_desc(tmpt,test11)

    #data12_image_url
    sub_title = r'[\w ]+'
    http_key = r'https'
    if special1 == 1:
        data1 = 'The Hitman’s Bodyguard'
        data12 = 'https://art-s.nflximg.net/e13bd/f579a4c02254d9d8b831c505bbf5773a4e2e13bd.jpg'
    else:
        data12_key = re.search(sub_title,data1).group()
        k = soup.find_all('img',title =re.compile(data12_key),src = re.compile(http_key))
        data12 = k[0].get('src')


    #data17 rating
    data17_1 = soup.find_all('img', title=re.compile(r'rating \d'))
    pattern_17 = r'(?<!verage )([\w ]*)rating ([\d%\./]+)'
    dict_17 = {}
    for i in data17_1:
        j = re.search(pattern_17, str(i))
        if j:
            if j.group(1) !='Average ':
            # dict_17[j.group(2)] = 1
                dict_17[j.group(1)] = j.group(2)
    data17_xx, data17 = rating_pro(dict_17)
    #data18 = key_word
    try:
        data18 = IMDB_API(data1)
    except IndexError:
        data18 = ''

    global movie_number
    movie_number += 1
    current_id = id_movie+str(movie_number).zfill(4)
    record.append(current_id)
    record.append(data1)
    record.append(data2)
    record.append(data3)
    record.append(data4)
    record.append(data5)
    record.append(data6)
    record.append(data7)
    record.append(data8)
    record.append(data9)
    record.append(data10)
    record.append(data11)
    record.append(data12)
    record.append(data17)
    record.append(data18)

        #return str(data).strip('[]<p>/')
    return record

def tv_time_transfer(season,epl):
    mult = lambda x,y: x*y
    ep_n = 0
    for i in season:
        ep_n += mult(int(i),epl)
    return ep_n
def tv_info(soup):
    total_content = soup.find_all('p')
    test3 = 'Cast'
    test4 = 'Director'
    test5 = 'Duration'
    test5_a = 'Available Seasons'
    test5_b = 'Episode Length'
    test6 = 'Date Added'
    test7 = 'Certificate'
    test8 = 'Audio:'
    test10 = 'Subtitles:'
    test11 = 'Details:'

    for i in total_content:
        i_t = i.text
        if test3 in i_t:
            data3_1 = i_t
        if test4 in i_t:
            data4_1 = i_t
        if test5 in i_t:
            data5_1 = i_t
        if test5_a in i_t:
            data5_a = i_t
        if test5_b in i_t:
            data5_b = i_t
        if test6 in i_t:
            data6_1 = i_t
        if test7 in i_t:
            data7_1 = i_t
        if test8 in i_t:
            data8_1 = i_t
        if test10 in i_t:
            data10_1 = i_t
        if test11 in i_t:
            data11_1 = i_t

    record = []

    #data1 = soup.select('body > div.wrapper > section:nth-child(2) > h1')

    data1 = soup.find('h1')
    if special1 == 2:
        data1 = 'Inst@famous'
    else:
        data1 = transfer(data1) # record 1 is name

    data1 = data1.replace('Info Page:','')
    data1 = data1.strip(' ')

    #data2 = soup.select("body > div.wrapper > article > aside > div.genre > h5")#genre
    data2_1 = soup.select("body > div.wrapper > article > aside > div.genre > h5")
    data2_2 = [i.text for i in data2_1]
    data2 = data2_2[0].split(', ')
    data2 = ','.join(data2) # data2 version1
    #data3_1 = soup.select('body > div.wrapper > article > p:nth-child(28)')#name of casts
    try:
        data3_2 = data3_1.replace('Cast: ','')
    except UnboundLocalError:
        data3 = ['None']
    #pattern = r'(?<=>)[\w ]+(?=</a>)'
    # data3 = re.findall(pattern,str(data3_1))
    else:
        data3 = data3_2.split(', ')
    data3 = ','.join(data3)

    #4 - director
    #data4_1 = soup.select("body > div.wrapper > article > p:nth-child(26) > a") #record director
    # data4 = re.findall(pattern,str(data4_1))
    try:
        data4_2 = data4_1.replace('Director: ','')
    except UnboundLocalError:
        data4 = ['None']
    else:
        #data4_2 = data4_1.lstrip('Director: ')
        data4 = data4_2.split(', ')    # use lost in case there are more than two director

        if (len(data4) > 2 ):
            print('more than one director')
    data4 = ','.join(data4)
    #5-duration
    #data5_1 = soup.select("body > div.wrapper > article > p:nth-child(21)") # record the duration
    #data5_2 = [i.text for i in data5_1]
    #data5 = time_transfer(str(data5_2))
    data5_2 = data5_1.lstrip('Duration: ')
    pattern_5_ep = r'(\d+) Ep'

    try:
        data5_b_1 = data5_b.replace('Episode Length: ','')
    except UnboundLocalError:
        data5_b_1 = 'None'

    try: #use for case no available duration section
        data_check_point = data5_a
    except UnboundLocalError:
        data5_a = data5_1 #let available duration become duration section



    #except (AttributeError,ValueError):

    pattern_5 = r' Season[s]?'
    pattern_5_1 = r' Part[s]?'

    check = re.search(pattern_5, data5_a) # 5_a is the available season section:

    check1 = re.search(pattern_5_1, data5_a) # use parts as keyword
    if check:

        season_n = data5_2.rstrip(check.group())    # number of seasons

        season_ep =re.findall(pattern_5_ep, data5_a)
        try:

            season_epl = time_transfer(data5_b_1)

        except AttributeError:

            data5 = season_ep
        else:
            if season_ep == []:# did not find # of Ep for a season, but have episode time
                print('not found  # of Ep for a season')
                l_tmpt = []
                l_tmpt.append('case 3')
                l_tmpt.append(season_epl) # episode time
                l_tmpt.append(season_n) # number of season
                data5 = l_tmpt
            else:
                data5 = tv_time_transfer(season_ep,season_epl)
    elif check1:
        print('use parts as key word')
        season_ep = re.findall(pattern_5_ep, data5_a)
        if season_ep ==[]: #did not find information of ep in Duration: setence
            pattern_p_1 = r'(\d+) Part[s]?'
            current = re.findall(pattern_p_1,data5_a)
            if len(current) == 1:
                data5 = current[0]
            else:
                data5 = int(season_ep)
                print('still not work')
        else:
            data5 = int(season_ep) # the result is the number of ep in each season
    if data5_b_1 == 'None' and season_ep != []:    #no epicode length filed, but found eps for each season
        l_case2 = ['case 2']
        for i in season_ep:
            l_case2.append(int(i))
        data5 = l_case2
    try:
        test_data_5 = data5
    except UnboundLocalError: #last case, actually the same as the movie Duration: XX minutes
        data5 = time_transfer(str(data5_2))
    if special1 == 6:
        data1 = 'Immortal Classic'
    if special1 == 12:
        data1 = 'Bling Empire'
    if special1 == 14:
        data1 = 'The Netflix Afterparty'
    if special1 == 17:
        data1 =  'Sons of Adam'
    if special1 == 18:
        data1 = 'Nesr El-Saeed'
    if special1 == 19:
        data1 = 'KO One'
    if special1 == 20:
        data1 = 'Land of Hypocrisy - Ard El-Nefaaq'
    if special1 == 21:
        data1 = 'Lovey Dovey'
    if special1 == 22:
        data1 = "We've Further Comments"
    if special1 == 23:
        data1 = "Wolverine"
    if special1 == 24:
        data1 = "The Qin Empire"   #three season
    if special1 == 25:
        data1 = "Running Man Animation"
    if special1 == 26:
        data1 = 'REA（L）OVE'
    if special1 == 27:
        data1 = "Saimdang, Light's Diary"
    if special1 == 28:
        data1 = "Cobra Kai"
    if special1 == 30:
        data1 = "Khawatir"
    if special1 != 7 and special1 != 11 and special1 != 15 and special1 != 16 and special1 != 3:
        data5,data18,data2 = try2.run_t(data1)
        data2 = ','.join(data2.keys())
    #data6_1 = soup.select("body > div.wrapper > article > p:nth-child(8)") # available_date
    #data6_2 = [i.text for i in data6_1]s
    #data6 = date_transfer(str(data6_2))
    data6_2 = data6_1.lstrip('Date Added')
    print('This is',data6_2)
    data6,year = date_transfer(data6_2)


    #data7_1 = soup.select("body > div.wrapper > article > p:nth-child(19) > span.ratingsblock") # parent control
    #data7 = transfer(data7_1)
    data7 = []
    pattern1 = r'(?<=Certificate: )([\w-]+)'
    data7_3 = re.findall(pattern1, data7_1)
    for n in data7_3:
        data7.append(n)
    data7 = ','.join(data7)
    #data8_1 = soup.select("body > div.wrapper > article > p:nth-child(22)")#language
    # data8_2 = transfer(data8_1)

    # data8 &9, Audio and audio description
    data8_2,data9_2 = language_record(data8_1)
    data8 = data8_2.split(', ')
    data9 = data9_2.split(', ')
    data8 = [i.rstrip() for i in data8]
    data9 = [i.rstrip() for i in data9]
    data8 = ','.join(data8)
    data9 = ','.join(data9)
    #data10 substitle
    try:
        data10_1 = data10_1.lstrip('Subtitles: ')
    except UnboundLocalError:
        data10 = ['']
    else:
        data10_1 = data10_1.split(', ')
        data10 = [i.rstrip() for i in data10_1]
    data10 = ','.join(data10)
    #11 - description
    #data11_1 = soup.select("body > div.wrapper > article > p:nth-child(31)")
    #document.querySelector("body > div.wrapper > article > h4:nth-child(27)")
    #if str(data12_1) == '[<p></p>]': #show
    #    data12_1 = soup.select('body > div.wrapper > article > p:nth-child(26)')
    tmpt = soup.find_all({'h4','p'})
    test11_1 = 'Season Details:'
    data11_2 = find_desc_tv(tmpt,test11_1)
    try:
        data19 = data11_2[0]
        data11 = data11_2[1]
    except TypeError:
        data19 = ''
        data11 = data11_2
    #data11 = find_desc(tmpt,test11,test11_1)


    #data12_image_url
    #k = strhtml.find_all('img',title =re.compile(data1))
    #data12 = k[0].get('src')

    sub_title = r'[\w ]+'
    http_key = r'http'
    check7 = r'1994'
    if special1 == 14:
        data1 = 'Bridgerton - The Afterparty'
    if special1 == 17:
        data1 =  'Children of Adam'
    if special1 == 18:
        data1 = "The Eagle of El-Se'eed"
    if special1 == 19:
        data1 = 'K.O. One Re-act'
    if special1 == 20:
        data1 = 'he Land of Hypocrisy'
    if special1 == 21:
        data1 = 'แผนร้ายนายเจ้าเล่ห์'
    if special1 == 22:
        data1 = 'More to Say'
    if special1 == 23:
        data1 = "Marvel Anime: Wolverine"
    if special1 == 24:
        data1 = "Qin Empire: Alliance"
    if special1 == 25:
        data1 = "Running Man"
    if special1 == 26:
        data1 = 'REA(L)OVE'
    if special1 == 27:
        data1 = "Saimdang, Memoir of Colors"
    if special1 == 28:
        data1 = "Cobra Kai - The Afterparty"
    if special1 == 30:
        data1 = "Khawatir Compilation"
    data12_key = re.search(sub_title, data1).group()
    data12_key= data12_key.strip(' ')
    k = soup.find_all('img', title=re.compile(data12_key),src = re.compile(http_key))
    #k = soup.find_all('img', title=re.compile(check7))
    #[print('k is',n) for n in k]
    data12 = k[0].get('src')


    #data17 rating
    data17_1 = soup.find_all('img', title=re.compile(r'rating \d'))
    pattern_17 = r'(?<!verage )([\w ]*)rating ([\d%\./]+)'
    dict_17 = {}
    for i in data17_1:
        j = re.search(pattern_17,str(i))
        if j:
            #dict_17[j.group(2)] = 1
            dict_17[j.group(1)] = j.group(2)

    data17_xx,data17 = rating_pro(dict_17)

    if data17 == []:
        data17 = ['None']
    # 18 - History
    #document.querySelector("body > div.wrapper > article > aside > div:nth-child(1) > img")
    if special1 == 3:
        data8 = ['']
        data5 = [8*2]
    global tv_number
    tv_number += 1
    current_id = id_tv+str(tv_number).zfill(4)
    record.append(current_id)
    record.append(data1) #0 title
    record.append(data2) #1 genre
    record.append(data3) #2 cast
    record.append(data4) #3 director
    record.append(data5) #4 duration
    record.append(data6) #5
    record.append(data7) #6
    record.append(data8) #7
    record.append(data9) #8
    record.append(data10) #9
    record.append(data19) # the status of the tv
    record.append(data11) #10
    record.append(data12) #11
    record.append(data17) #12
    try:
        record.append(data18)  # S1E1: aired date
    except UnboundLocalError:
        data18 = 'None'
        record.append(data18)
    # data 20 is the key_words
    try:
        data20 = IMDB_API(data1)
    except IndexError:
        data20 = 'None'
    record.append(data20)

    return record


month_d = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8,
           'September': 9, 'October': 10, 'November': 11, 'December': 12}
url = 'https://can.newonnetflix.info/info/70108779'

url2 = 'https://can.newonnetflix.info/info/70270776'
url3 = 'https://can.newonnetflix.info/info/81210770'
url4 = 'https://can.newonnetflix.info/info/70108987'

# tv show
url5 = 'https://can.newonnetflix.info/info/81272752'
url1 = 'https://can.newonnetflix.info/info/80165247'  # tv show

# total search
url6 = 'https://can.newonnetflix.info/catalogue/a2z/movies'  # movie
url7 = 'https://can.newonnetflix.info/catalogue/a2z/tv_programmes'  # put main page here

# strhtml = requests.get(url)
time1 = time()#start timming
test_url = 'https://can.newonnetflix.info'
strhtml = getHtmlList(url7)  # is a soup class

nn = strhtml.find_all('a', {'class': 'infopop'}, href=re.compile('/info'))


def create_page_index():
    list_of_char_index = ['']
    for char_index in range(26):
        list_of_char_index.append(f"/{chr(ord('a') + char_index)}")
    return list_of_char_index

list_of_index = create_page_index()

#list_of_index = [ '/v', '/w', '/x', '/y', '/z'] # '' is missing

#change here to collect the tv or movie data for this time, you can place them in the same list to collect both of them together
list_of_type = ['https://can.newonnetflix.info/catalogue/a2z/tv_programmes']
                #
                  # the two main search page url to use
# list_of_type =['https://can.newonnetflix.info/catalogue/a2z/movies']
index_page_urls = [i + j for i in list_of_type for j in list_of_index]
record_n = set()
pattern_title = r'(\d+) titles'
count_total = 0
split_page_urls = []
for url in index_page_urls:
    html_t = getHtmlList(url)
    items_numbers_with_this_index = int(get_number_of_elements(html_t))
    count_total += items_numbers_with_this_index
    split_page_urls.extend(split_index_page(url, items_numbers_with_this_index))

print(f"Prediction: {count_total} movie/tv shows will be scrapped")
print('start crawling')
####special index-------------
special1 = 0
# ------------------------------initialize
total_count = 0
movie_number = 0
tv_number = 0
id_movie = '1'
id_tv = '2'
total_record = []# used for all the recording
for final_web in split_page_urls:
    record_n = set()
    strhtml = getHtmlList(final_web)
    print('start searching on ', final_web)
    nn = strhtml.find_all('a', {'class': 'infopop'}, href=re.compile('/info'))

    for n, i in enumerate(nn):
        record_n.add(test_url + i['href'])
        # print('nn is',record_n[n])
    total_movie = [i for i in record_n]
    print('total movies on this page is', len(total_movie))
    count = 0

    ''' 

    #used for case check
    url_t = 'https://can.newonnetflix.info/info/70108779'
    soup_tmpt = getHtmlList(url_t)



    record = Movie_info(soup_tmpt)
    if record == False:
        record = tv_info(soup_tmpt)
    [print(i) for i in record]


    '''

    # main program

    for i in total_movie:
        special1 = 0

        soup_tmpt = getHtmlList(i)
        print('processing', i)
        if i == 'https://can.newonnetflix.info/info/80119311':
            special1 = 1
            print('special 1 was found')

        if i == 'https://can.newonnetflix.info/info/81032812':
            special1 = 2
            print('special 2 was found')
        if i == 'https://can.newonnetflix.info/info/81014625':
            special1 = 3
            print('special 3 was found')
        if i =='https://can.newonnetflix.info/info/81004748':
            special1 = 4
            print('special 4 was found') # this is actually a movie
        if i == 'https://can.newonnetflix.info/info/80244680':
            special1 = 5
            print('special 5 was found') # this is a movie
        if i == 'https://can.newonnetflix.info/info/80066800':
            special1 = 6
            print('special 6 was found')
        if i == 'https://can.newonnetflix.info/info/80180544':
            special1 = 7 # not exit on tvdb
            print('special 7 was found')
        if i == 'https://can.newonnetflix.info/info/81342639':
            special1 = 8
            print('special 8 was found')
        if i == 'https://can.newonnetflix.info/info/81205737':
            special1 = 9 # this is a movie
            print('special 9 was found')
        if i == 'https://can.newonnetflix.info/info/81405382':
            special1 = 10 # this is a movie
            print('special 10 was found')
        if i == 'https://can.newonnetflix.info/info/80180681':
            special1 = 11 # can not find in tvdb
            print('special 11 was found')
        if i == 'https://can.newonnetflix.info/info/81351072':
            special1 = 12
            print('special 12 was found')
        if i == 'https://can.newonnetflix.info/info/80988062':
            special1 = 13  # is a movie and information of runtime is wrong on the search engine
            print('special 13 was found')
        if i == 'https://can.newonnetflix.info/info/80131435':
            special1 = 9
            print('special 14 was found')
        if i == 'https://can.newonnetflix.info/info/80019503':
            special1 = 9
            print('special 15 was found')
        if i == 'https://can.newonnetflix.info/info/81351071':
            special1 = 14 # different name on tvdb and netflix
            print('special 16 was found')
        if i == 'https://can.newonnetflix.info/info/80225915':
            special1 = 15  # a music tv show, not in tvdb
            print('special 17 was found')
        if i == 'https://can.newonnetflix.info/info/80227028':
            special1 = 16 # not in tvdb
            print('special 18 was found')
        if i == 'https://can.newonnetflix.info/info/81324272':
            special1 = 11
            print('special 19 was found')
        if i == 'https://can.newonnetflix.info/info/80226951':
            special1 = 9
            print('special 20 was found')
        if i == 'https://can.newonnetflix.info/info/81281632':
            special1 = 9
            print('special 21 was found')
        if i == 'https://can.newonnetflix.info/info/80232894':
            special1 = 9
            print('special 22 was found')
        if i == 'https://can.newonnetflix.info/info/80180588':
            special1 = 7  # not exit on tvdb
            print('special 23 was found')
        if i == 'https://can.newonnetflix.info/info/80230402':
            special1 = 7
            print('special 24 was found')
        if i == 'https://can.newonnetflix.info/info/80216677':
            special1 = 9
            print('special 25 was found')
        if i == 'https://can.newonnetflix.info/info/81214015':
            special1 = 9
            print('special 26 was found')
        if i == 'https://can.newonnetflix.info/info/80180711':
            special1 = 7
            print('special 27 was found')
        if i == 'https://can.newonnetflix.info/info/81018141':
            special1 = 9
            print('special1 28 was found')
        if i == 'https://can.newonnetflix.info/info/80220000':
            special1 = 9
            print('special1 29 was found')
        if i == 'https://can.newonnetflix.info/info/80183897':
            special1 = 9
            print('special 30 was found')
        if i == 'https://can.newonnetflix.info/info/80180601':
            special1 = 11
            print('special 31 was found')
        if i == 'https://can.newonnetflix.info/info/81029634':
            special1 = 7
            print('special 32 was found')
        if i == 'https://can.newonnetflix.info/info/81405851':
            special1 = 7
            print('special 33 was found')
        if i == 'https://can.newonnetflix.info/info/81001412':
            special1 = 9
            print('special 34 was found')
        if i == 'https://can.newonnetflix.info/info/81001413':
            special1 = 9
            print('special 35 was found')
        if i == 'https://can.newonnetflix.info/info/81223007':
            special1 = 7
            print('special 36 was found')
        if i == 'https://can.newonnetflix.info/info/80103310':
            special1 = 7 #electric test
            print('special 37 was found')
        if i == 'https://can.newonnetflix.info/info/80224476':
            special1 = 9
            print('special 38 was found')
        if i == 'https://can.newonnetflix.info/info/81162089':
            special1 = 9
            print('special 39 was found')
        if i == 'https://can.newonnetflix.info/info/80136790':
            special1 = 7
            print('special 40 was found')
        if i == 'https://can.newonnetflix.info/info/80004447':
            special1 = 7 #0 min house
            print('special 41 was found')
        if i == 'https://can.newonnetflix.info/info/81060232':
            special1 = 9
            print('special 42 was found')
        if i == 'https://can.newonnetflix.info/info/70178639':
            special1 = 9
            print('special 43 was found')
        if i == 'https://can.newonnetflix.info/info/80169755':
            special1 = 9 # a movie
            print('special 44 was found')
        if i == 'https://can.newonnetflix.info/info/80107030':
            special1 = 9
            print('special 45 was found')
        if i == 'https://can.newonnetflix.info/info/81104634':
            special1 = 9
            print('special 46 was found')
        if i == 'https://can.newonnetflix.info/info/81044582':
            special1 = 9
            print('special 47 was found')
        if i == 'https://can.newonnetflix.info/info/81034099':
            special1 = 7 # loggest one. netflix just has a collection but can not use the tvdb. too large
            print('special1 48 was found')
        if i == 'https://can.newonnetflix.info/info/80156995':
            special1 = 7
            print('special1 49 was found')
        if i == 'https://can.newonnetflix.info/info/80231156':
            special1 = 9
            print('special1 50 was found')
        if i == 'https://can.newonnetflix.info/info/80131281':
            special1 = 9
            print('special1 51 was found')
        if i =='https://can.newonnetflix.info/info/80131374':
            special1 = 9
            print('special1 52 was found')
        if i == 'https://can.newonnetflix.info/info/81328941':
            special1 = 9
            print('special1 53 was found')
        if i == 'https://can.newonnetflix.info/info/81150918':
            special1 = 9
            print('special1 54 was found')
        if i == 'https://can.newonnetflix.info/info/80131436':
            special1 = 9
            print('special1 55 was found')
        if i == 'https://can.newonnetflix.info/info/80083594':
            special1 = 9
            print('special1 56 was found')
        if i == 'https://can.newonnetflix.info/info/80163293':
            special1 = 7
            print('special1 57 was found')
        if i == 'https://can.newonnetflix.info/info/80174429':
            special1 = 7 # this one shown as a movie in tvdb but it is actually a tv show
            print('special 58 was found')
        if i == 'https://can.newonnetflix.info/info/80180591':
            special1 = 7  # not in tvdb
            print('special 58 was found')
        if i == 'https://can.newonnetflix.info/info/81412240':
            special1 = 9
            print('special 59 was found')
        if i == 'https://can.newonnetflix.info/info/81057249':
            special1 = 9
            print('special 60 was found')
        if i == 'https://can.newonnetflix.info/info/81030762':
            special1 = 7 # not on tvdb
            print('special 61 was found')
        if i == 'https://can.newonnetflix.info/info/80245626':
            special1 = 9
            print('special 62 was found')
        if i == 'https://can.newonnetflix.info/info/70304186':
            special1 = 9
            print('special 63 was found')
        if i == 'https://can.newonnetflix.info/info/70304188':
            special1 = 9
            print('special 64 was found')
        if i == 'https://can.newonnetflix.info/info/80185861':
            special1 = 9
            print('special 65 was found')
        if i == 'https://can.newonnetflix.info/info/80190990':
            special1 = 9
            print('special 66 was found')
        if i == 'https://can.newonnetflix.info/info/80131375':
            special1 = 9
            print('special 67 was found')
        if i == 'https://can.newonnetflix.info/info/70143440':
            special1 = 9
            print('special 68 was found')
        if i == 'https://can.newonnetflix.info/info/81131714':
            special1 = 9
            print('special 69 was found')
        if i == 'https://can.newonnetflix.info/info/80202234':
            special1 = 7
            print('special 70 was found')
        if i == 'https://can.newonnetflix.info/info/80174177':
            special1 = 9
            print('special 71 was found')
        if i == 'https://can.newonnetflix.info/info/80160125':
            special1 = 7
            print('special 72 was found')
        if i == 'https://can.newonnetflix.info/info/80123567':
            special1 = 7
            print('special 73 was found')
        if i == 'https://can.newonnetflix.info/info/81313134':
            special1 = 9
            print('special 74 was found')
        if i == 'https://can.newonnetflix.info/info/80157717':
            special1 = 7
            print('special 75 was found')
        if i == 'https://can.newonnetflix.info/info/80163222':
            special1 = 9 # start search tv
            print('special 76 was found')
        if i == 'https://can.newonnetflix.info/info/80158854':
            special1 = 9
            print('special 77 was found')
        if i == 'https://can.newonnetflix.info/info/80191512':
            special1 = 9
            print('special 78 was found')
        if i == 'https://can.newonnetflix.info/info/81021356':
            special1 = 9
            print('special 79 was found')
        if i == 'https://can.newonnetflix.info/info/81021357':
            special1 = 9
            print('special 80 was found')
        if i == 'https://can.newonnetflix.info/info/81010807':
            special1 = 9
            print('special 81 was found')
        if i == 'https://can.newonnetflix.info/info/81021358':
            special1 = 9
            print('special 82 was found')
        if i == 'https://can.newonnetflix.info/info/81405587':
            special1 = 7
            print('special 83 was found')
        if i == 'https://can.newonnetflix.info/info/81397020':
            special1 = 7
            print('special 84 was found')
        if i == 'https://can.newonnetflix.info/info/80191511':
            special1 = 9
            print('special 85 was found')
        if i == 'https://can.newonnetflix.info/info/81397516':
            special1 = 7
            print('special 86 was found')
        if i == 'https://can.newonnetflix.info/info/80157177':
            special1 = 7
            print('special 87 was found')
        if i == 'https://can.newonnetflix.info/info/80097608':
            special1 = 7
            print('special 88 was found')
        if i == 'https://can.newonnetflix.info/info/81054409':
            special1 = 9
            print('special 89 was found')
        if i == 'https://can.newonnetflix.info/info/81245404':
            special1 = 7
            print('special 90 was found')
        if i == 'https://can.newonnetflix.info/info/81286241':
            special1 = 9
            print('special1 91 was found')
        if i == 'https://can.newonnetflix.info/info/80149064':
            special1 = 9
            print('special1 92 was found')
        if i == 'https://can.newonnetflix.info/info/80192095':
            special1 = 9
            print('special1 93 was found')
        if i == 'https://can.newonnetflix.info/info/80180710':
            special1 = 7
            print('special1 94 was found')
        if i == 'https://can.newonnetflix.info/info/80180545':
            special1 = 7
            print('special 95 was found')
        if i == 'https://can.newonnetflix.info/info/81327402':
            special1 = 17 # son of adam
            print('special 96 was found')
        if i == 'https://can.newonnetflix.info/info/81097741':
            special1 = 9
            print('special 97 was found')
        if i == 'https://can.newonnetflix.info/info/81012137':
            special1 = 7
            print('special 98 was found')
        if i == 'https://can.newonnetflix.info/info/81184681':
            special1 = 7
            print('special 99 was found')
        if i == 'https://can.newonnetflix.info/info/81021977':
            special1 = 9
            print('special 100 was found')
        if i == 'https://can.newonnetflix.info/info/80994695':
            special1 = 9
            print('special 101 was found')
        if i == 'https://can.newonnetflix.info/info/80163296':
            special1 = 7
            print('special 102 was found')
        if i == 'https://can.newonnetflix.info/info/81019938':
            special1 = 9
            print('special 103 was found')
        if i == 'https://can.newonnetflix.info/info/80191081':
            special1 = 9
            print('special 104 was found')
        if i == 'https://can.newonnetflix.info/info/80191359':
            special1 = 9
            print('special 105 was found')
        if i == 'https://can.newonnetflix.info/info/80136793':
            special1 = 7
            print('special 106 was found')
        if i == 'https://can.newonnetflix.info/info/70259784':
            special1 = 7
            print('special 107 was found')
        if i == 'https://can.newonnetflix.info/info/70258566':
            special1 = 7
            print('special 108 was found')
        if i == 'https://can.newonnetflix.info/info/70221348':
            special1 = 7
            print('special 109 was found')
        if i == 'https://can.newonnetflix.info/info/70242630':
            special1 = 7
            print('special 110 was found')
        if i == 'https://can.newonnetflix.info/info/70242629':
            special1 = 7
            print('special 111 was found')
        if i == 'https://can.newonnetflix.info/info/70218316':
            special1 = 7
            print('special 112 was found')
        if i == 'https://can.newonnetflix.info/info/81049479':
            special1 = 18
            print('special 113 was found') #The Eagle of El-Se'eed
        if i == 'https://can.newonnetflix.info/info/81078819':
            special1 = 9
            print('special 114 was found')
        if i == 'https://can.newonnetflix.info/info/81403796':
            special1 = 7
            print('special 115 was found')
        if i == 'https://can.newonnetflix.info/info/81403816':
            special1 = 7
            print('special 116 was found')
        if i == 'https://can.newonnetflix.info/info/81311236':
            special1 = 7
            print('special 117 was found')
        if i == 'https://can.newonnetflix.info/info/80191075':
            special1 = 7
            print('special 118 was found')
        if i == 'https://can.newonnetflix.info/info/81049315':
            special1 = 7
            print('special 119 was found')
        if i == 'https://can.newonnetflix.info/info/81289898':
            special1 = 7
            print('special 120 was found')
        if i == 'https://can.newonnetflix.info/info/81164115':
            special1 = 7
            print('special 121 was found')
        if i == 'https://can.newonnetflix.info/info/80157276':
            special1 = 7
            print('special 122 was found')
        if i == 'https://can.newonnetflix.info/info/81442224':
            special1 = 7 # a background check
            print('special 123 was found')
        if i == 'https://can.newonnetflix.info/info/80208052':
            special1 = 7
            print('special 124 was found')
        if i == 'https://can.newonnetflix.info/info/80163295':
            special1 = 7
            print('special 125 was found')
        if i == 'https://can.newonnetflix.info/info/81030409':
            special1 = 7
            print('special 126 was found')
        if i == 'https://can.newonnetflix.info/info/70251818':
            special1 = 7
            print('special 127 was found') # too long ,can not be used for original search 245 epsoid
        if i == 'https://can.newonnetflix.info/info/81072951':
            special1 = 19 # ko one 29 episode, netflix has only 20 2013 season
            print('special 128 was found')
        if i == 'https://can.newonnetflix.info/info/81039073':
            special1 = 7
            print('special 129 was found')
        if i == 'https://can.newonnetflix.info/info/81088333':
            special1 = 7
            print('special 130 was found')
        if i == 'https://can.newonnetflix.info/info/81049511':
            special1 = 20 #The Land of Hypocrisy -----Land of Hypocrisy - Ard El-Nefaaq
            print('special 131 was found')
        if i == 'https://can.newonnetflix.info/info/80116008':
            special1 = 9
            print('special 132 was found')
        if i == 'https://can.newonnetflix.info/info/81058723':
            special1 = 9
            print('special 133 was found')
        if i == 'https://can.newonnetflix.info/info/80065492':
            special1 = 9
            print('special 134 was found')
        if i == 'https://can.newonnetflix.info/info/80993794':
            special1 = 21 # name changed
            print('special 135 was found')
        if i == 'https://can.newonnetflix.info/info/80192171':
            special1 = 9
            print('special 136 was found')
        if i == 'https://can.newonnetflix.info/info/80191496':
            special1 = 9
            print('special 137 was found')
        if i == 'https://can.newonnetflix.info/info/81049544':
            special1 = 22
            print('special 138 was found')
        if i == 'https://can.newonnetflix.info/info/81312606':
            special1 = 7
            print('special 139 was found')
        if i == 'https://can.newonnetflix.info/info/70205687':
            special1 = 23 #Marvel Anime: Wolverine
            print('special 140 was found')
        if i == 'https://can.newonnetflix.info/info/80191746':
            special1 = 9
            print('special 141 was found')
        if i == 'https://can.newonnetflix.info/info/81036448':
            special1 = 7
            print('special 142 was found')
        if i == 'https://can.newonnetflix.info/info/81054981':
            special1 = 9
            print('special 143 was found')
        if i == 'https://can.newonnetflix.info/info/70157347':
            special1 = 7 #339 episode, run out of time
            print('special 144 was found')
        if i == 'https://can.newonnetflix.info/info/81054980':
            special1 = 9
            print('special 145 was found')
        if i == 'https://can.newonnetflix.info/info/80191510':
            special1 = 9
            print('special 146 was found')
        if i == 'https://can.newonnetflix.info/info/81054979':
            special1 = 9
            print('special 147 was found')
        if i == 'https://can.newonnetflix.info/info/81239272':
            special1 = 9
            print('special 148 was found')
        if i == 'https://can.newonnetflix.info/info/80993087':
            special1 = 7
            print('special 149 was found')
        if i == 'https://can.newonnetflix.info/info/81168505':
            special1 = 9
            print('special 150 was found')
        if i == 'https://can.newonnetflix.info/info/81015994':
            special1 = 7
            print('special 151 was found')
        if i == 'https://can.newonnetflix.info/info/81009671':
            special1 = 9
            print('special 152 was found')
        if i == 'https://can.newonnetflix.info/info/81082125':
            special1 = 9
            print('special 153 was found')
        if i == 'https://can.newonnetflix.info/info/81012822':
            special1 = 9
            print('special 154 was found')
        if i == 'https://can.newonnetflix.info/info/81031038':
            special1 = 9
            print('special 155 was found')
        if i == 'https://can.newonnetflix.info/info/81031037':
            special1 = 9
            print('special 156 was found')
        if i == 'https://can.newonnetflix.info/info/80235766':
            special1 = 9
            print('special 157 was found')
        if i == 'https://can.newonnetflix.info/info/80180651':
            special1 = 7
            print('special 158 was found')
        if i == 'https://can.newonnetflix.info/info/70297439':
            special1 = 7
            print('special 159 was found')
        if i == 'https://can.newonnetflix.info/info/80235854':
            special1 = 9
            print('special 160 was found')
        if i == 'https://can.newonnetflix.info/info/81018634':
            special1 = 9
            print('special 161 was found')
        if i == 'https://can.newonnetflix.info/info/80191361':
            special1 = 9
            print('special 162 was found')
        if i == 'https://can.newonnetflix.info/info/80235767':
            special1 = 9
            print('special 163 was found')
        if i == 'https://can.newonnetflix.info/info/81221278':
            special1 = 7
            print('special 164 was found')
        if i == 'https://can.newonnetflix.info/info/80236099':
            special1 = 9
            print('special 165 was found')
        if i == 'https://can.newonnetflix.info/info/80235853':
            special1 = 9
            print('special 166 was found')
        if i == 'https://can.newonnetflix.info/info/80006232':
            special1 = 9
            print('special 167 was found')
        if i == 'https://can.newonnetflix.info/info/80236224':
            special1 = 9
            print('special 168 was found')
        if i == 'https://can.newonnetflix.info/info/80191362':
            special1 = 9
            print('special 169 was found')
        if i == 'https://can.newonnetflix.info/info/81039045':
            special1 = 7
            print('special 170 was found')
        if i == 'https://can.newonnetflix.info/info/81174988':
            special1 = 9
            print('special 171 was found')
        if i == 'https://can.newonnetflix.info/info/80151644':
            special1 = 9
            print('special 172 was found')
        if i == 'https://can.newonnetflix.info/info/80160597':
            special1 = 24 # name different
            print('special 173 was found')
        if i == 'https://can.newonnetflix.info/info/80108844':
            special1 = 7
            print('special 174 was found')
        if i == 'https://can.newonnetflix.info/info/81331228':
            special1 = 25 # real running man has 550 episode
            print('special 175 was found')
        if i == 'https://can.newonnetflix.info/info/81221345':
            special1 = 7
            print('special 176 was found')
        if i == 'https://can.newonnetflix.info/info/81040952':
            special1 = 9
            print('special 177 was found')
        if i == 'https://can.newonnetflix.info/info/80226927':
            special1 = 26 # chinese blanket
            print('special 178 was found')
        if i == 'https://can.newonnetflix.info/info/81035474':
            special1 = 9
            print('special 179 was found')
        if i == 'https://can.newonnetflix.info/info/80159899':
            special1 = 7
            print('special 180 was found')
        if i == 'https://can.newonnetflix.info/info/81146370':
            special1 = 9
            print('special 181 was found')
        if i == 'https://can.newonnetflix.info/info/80207879':
            special1 = 7
            print('special 182 was found')
        if i == 'https://can.newonnetflix.info/info/80191508':
            special1 = 9
            print('special 183 was found')
        if i == 'https://can.newonnetflix.info/info/81021976':
            special1 = 9
            print('special 184 was found')
        if i == 'https://can.newonnetflix.info/info/81167011':
            special1 = 7
            print('special 185 was found')
        if i == 'https://can.newonnetflix.info/info/81054415':
            special1 = 9
            print('special 186 was found')
        if i == 'https://can.newonnetflix.info/info/80006168':
            special1 = 9
            print('special 187 was found')
        if i == 'https://can.newonnetflix.info/info/80235524':
            special1 = 9
            print('special 188 was found')
        if i == 'https://can.newonnetflix.info/info/81002336':
            special1 = 7
            print('special 189 was found')
        if i == 'https://can.newonnetflix.info/info/81162075':
            special1 = 9
            print('special 190 was found')
        if i == 'https://can.newonnetflix.info/info/81021243':
            special1 = 9
            print('special 191 was found')
        if i == 'https://can.newonnetflix.info/info/81162074':
            special1 = 9 # manually
            print('special 192 was found')
        if i == 'https://can.newonnetflix.info/info/81162076':
            special1 = 9 # manually
            print('special 193 was found')
        if i == 'https://can.newonnetflix.info/info/81162073':
            special1 = 9 # manually
            print('special 194 was found')
        if i == 'https://can.newonnetflix.info/info/81036199':
            special1 = 9
            print('special 195 was found')
        if i == 'https://can.newonnetflix.info/info/80999069':
            special1 = 9
            print('special 196 was found')
        if i == 'https://can.newonnetflix.info/info/80999063':
            special1 = 9
            print('special 197 was found')
        if i == 'https://can.newonnetflix.info/info/80999067':
            special1 = 9
            print('special 198 was found')
        if i == 'https://can.newonnetflix.info/info/80135585':
            special1 = 9
            print('special 199 was found')
        if i == 'https://can.newonnetflix.info/info/81006335':
            special1 = 9
            print('special 199 was found')
        if i == 'https://can.newonnetflix.info/info/81035127':
            special1 = 9
            print('special 200 was found')
        if i == 'https://can.newonnetflix.info/info/80191360':
            special1 = 9
            print('special 201 was found')
        if i == 'https://can.newonnetflix.info/info/81035125':
            special1 = 9
            print('special 202 was found')
        if i == 'https://can.newonnetflix.info/info/81021355':
            special1 = 9
            print('special 203 was found')
        if i == 'https://can.newonnetflix.info/info/81035120':
            special1 = 9
            print('special 204 was found')
        if i == 'https://can.newonnetflix.info/info/81035126':
            special1 = 9
            print('special 205 was found')
        if i == 'https://can.newonnetflix.info/info/81245376':
            special1 = 7
            print('special 206 was found')
        if i == 'https://can.newonnetflix.info/info/81452597':
            special1 = 9
            print('special 207 was found')
        if i == 'https://can.newonnetflix.info/info/81049739':
            special1 = 7
            print('special 208 was found')
        if i == 'https://can.newonnetflix.info/info/80136792':
            special1 = 7
            print('special 209 was found')
        if i == 'https://can.newonnetflix.info/info/80180619':
            special1 = 7
            print('special 210 was found')
        if i == 'https://can.newonnetflix.info/info/81035117':
            special1 = 9
            print('special 211 was found')
        if i == 'https://can.newonnetflix.info/info/80185876':
            special1 = 9
            print('special 212 was found')
        if i == 'https://can.newonnetflix.info/info/81035121':
            special1 = 9
            print('special 213 was found')
        if i == 'https://can.newonnetflix.info/info/81035122':
            special1 = 9
            print('special 214 was found')
        if i == 'https://can.newonnetflix.info/info/80163533':
            special1 = 7
            print('special 215 was found')
        if i == 'https://can.newonnetflix.info/info/80111614':
            special1 = 7
            print('special 216 was found')
        if i == 'https://can.newonnetflix.info/info/80191404':
            special1 = 9
            print('special 217 was found')
        if i == 'https://can.newonnetflix.info/info/80106367':
            special1 = 7
            print('special 218 was found')
        if i == 'https://can.newonnetflix.info/info/81321375':
            special1 = 9
            print('special 219 was found')
        if i == 'https://can.newonnetflix.info/info/81206879':
            special1 = 7
            print('special 220 was found')
        if i == 'https://can.newonnetflix.info/info/81214399':
            special1 = 7
            print('special 221 was found')
        if i == 'https://can.newonnetflix.info/info/80131376':
            special1 = 9
            print('special 222 was found')
        if i == 'https://can.newonnetflix.info/info/80118179':
            special1 = 27
            print('special 223 was found')
        if i == 'https://can.newonnetflix.info/info/80204739':
            special1 = 7
            print('special 224 was found')
        if i == 'https://can.newonnetflix.info/info/80163430':
            special1 = 7
            print('special 225 was found')
        if i == 'https://can.newonnetflix.info/info/81344331':
            special1 = 28
            print('special 226 was found')
        if i == 'https://can.newonnetflix.info/info/81362863':
            special1 = 29 # this is a tv show
            print('special 227 was found')
            continue
        if i == 'https://can.newonnetflix.info/info/81386996':
            special1 = 30
            print('special 228 was found')
        if i == 'https://can.newonnetflix.info/info/81473619':
            special1 = 7
            print('special 229 was found')
        if i == 'https://can.newonnetflix.info/info/80227995':
            special1 = 7
            print('special 230 was found')
        if i == 'https://can.newonnetflix.info/info/81354663':
            special1 = 7
            print('special 231 was found')
        if i == 'https://can.newonnetflix.info/info/81351073':
            special1 = 9
            print('special 232 was found')
        if i == 'https://can.newonnetflix.info/info/81037868':
            special1 = 7
            print('special 233 was found')
        try:
            record = Movie_info(soup_tmpt)
        except AttributeError:
            print('the error i is', i)
            soup_tmpt = getHtmlList(i)
            record = Movie_info(soup_tmpt)
            if record != False: # search tv show only
                print('escape a movie')
                continue

        if record == False:  # switch to tv show
            #print('escape a tv show')
            #continue # force to search movie only
            print('a movie is switch to tv show check')
            record = tv_info(soup_tmpt)


        print('movie name is', record[1])
        total_record.append(record)
        count += 1
        total_count += 1
        if total_count%1000 == 0:
            print('--'*15)
            print('now have recording :' ,len(total_record))
        print('Successively record the {0} movies/tvshow on this page, totally store {1} data points'.format(count,
                                                                                                             total_count))

    # print('h5 is ',tmpt)
    # for i in strhtml:
    #    print(i)

    # record1 = tv_info(strhtml)
time2 = time()
fields = ['id','title', 'genre', 'cast', 'director','episode_time','available_date','parent_control','language','audio_description','subtitle','status','production_detail','image_url','rating','episode_airtime','key_words'] # use this line if you try to collect the movie data
#fields = ['id','title', 'genre', 'cast', 'director','duration','available_date','parent_control','language','audio_description','subtitle','production_detail','image_url','rating','key_words'] #use this line if you try to collect the tv_show data
print('time cost is',time2 - time1)
with open('netflix_tv_data_final_1.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)

    write.writerow(fields)
    write.writerows(total_record)
print('-----------------Summary-----------------------')
print('Congratulation, program finished ')
print('total number of data points: ',total_record)
print('sample of 10,1000,3000,6000 data points:')
print('10th record:')
[print(i) for i in total_record[10]]
print('500th record:-----------------')
[print(i) for i in total_record[500]]
#print('1000th record:-----------------')
#[print(i) for i in total_record[1000]]
#print('3000th record:-----------------')
#[print(i) for i in total_record[3000]]
#print('6000th record:-----------------')
#[print(i) for i in total_record[6000]]