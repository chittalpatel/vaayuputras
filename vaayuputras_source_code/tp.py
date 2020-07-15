import requests
from pprint import pprint
# dict={'windfarm_name':'AB Tehachapi Wind Farm'}
# # url = 'https://vaayuputras.eu-gb.cf.appdomain.cloud/api/prediction/{}?format=json'.format(dict['windfarm_name'])
# # data=requests.get(url).json()
# # pprint(data)



# dict={'apikey':'12ae2735827eb45ba74acb1d262bc8d0c0452b3b'}
# url = 'https://vaayuputras.eu-gb.cf.appdomain.cloud/api/user_prediction?format=json'
# headers = {'Authorization': 'Token {}'.format(dict['apikey'])}
# data=requests.get(url,headers=headers).json()
# pprint(data)
# #
# #
# #
dict={'FCR':7.00,'IC':2.50,'WFC':2.00,'CF':40.00,'RPKWh':0.07,'LLC':10000.00}
url = 'https://vaayuputras.eu-gb.cf.appdomain.cloud/api/eco_calc/{}/{}/{}/{}/{}/{}?format=json'.format(dict['FCR'],dict['IC'],
                                                                                                       dict['WFC'],dict['CF'],dict['RPKWh'],dict['LLC'])
pprint(requests.get(url).json())



