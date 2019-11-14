import urllib.request

id = 'q_NQs_GLa_U'
url = 'https://img.youtube.com/vi/'+id+'/maxresdefault.jpg'
urllib.request.urlretrieve(url, 'image1.jpg')
