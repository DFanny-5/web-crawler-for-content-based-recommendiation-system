import tvdb_api
import tv_api_d as d_api
def search_detail(name,key):
    t = tvdb_api.Tvdb(apikey = key)
    try:
        episode = t[name]
    except tvdb_api.TvdbShowNotFound:
        episode = ['None']
    return episode
#need for using tv_api_d
def run_t (name):
    api_k = 'e71fabcb-a59a-4524-89ef-38a22a5b29e0'
    pin = 'K2STOGNN'
    toke = d_api.get_token(api_k,pin)

    name = name
    key = "392da9a4c7a2499799f9b28ecdf74e25"
    result = search_detail(name,key)
    record1 = {} # S1E1: runtime
    record2 = {} # S1E1: aired time
    record3 = {} # genre : id
    for i in result.keys():
        for j in result[i]:

            ll = result[i][j]['id']
            r_key = 'S{0}E{1}'.format(i, j)
            resp = d_api.epiod_info(ll, toke)   #use api to fond the episode detail
            record1[r_key] = resp['data']['runtime']
            record2[r_key] = resp['data']['aired']
        ser_id = result[i][j]['seriesId']

    #for x,y in record1.items():
    #    print('{0} : {1}'.format(x,y))

    genre_result = d_api.genre_info(ser_id,toke)
    for i in genre_result:
        record3[i['name']] = i['id']
    return record1,record2,record3


# the detail info of episode search with an id is :  resp = d_api.epiod_info(ll,toke)
api_k = 'e71fabcb-a59a-4524-89ef-38a22a5b29e0'
pin = 'K2STOGNN'
toke = d_api.get_token(api_k,pin)


name = 'La Esclava Blanca'
key = "392da9a4c7a2499799f9b28ecdf74e25"
result = search_detail(name,key)

#resp = d_api.epiod_info(ll,toke)

#print(result[1][1].keys())
#print('That is',result[1][1]['seriesId'])
#print('This is',result[1][1]['language'])

#[print(i,result[i]) for i in result]
#print('this is',result['id'])
#episode = t['s'].data
#print(episode)

#_getShowData