from flask import Flask, request, render_template, send_file
app = Flask(__name__)
import zipfile
import random
import os
from os.path import exists
import requests
from bs4 import BeautifulSoup
def download(url):
    file = requests.get(url)
    filename = file.headers['Content-Disposition'].split('=')[1]
    filec = open(filename, 'wb')
    filec.write(file.content)
    filec.close()
    return filename
def processFile(file, zips=300):
    file_size = os.path.getsize(file)
    zipy = int(zips) * 1024 * 1024
    name = file.split('.')[0]
    if file_size > zipy:
    	mult_file = zipfile.MultiFile(file,zipy)
    	zip = zipfile.ZipFile(mult_file,  mode='w', compression=zipfile.ZIP_DEFLATED)
    	zip.write(file)
    	zip.close()
    	mult_file.close()
    	print('Iniciando subida')
    	txt = ''
    	sdf = 1
    	files = '{'
    	while sdf != 0:
    		if exists(file+'.7z.00'+str(sdf)):
    			print('Subiendo '+name+'.7z.00'+str(sdf))
    			files += upload(file+'.7z.00'+str(sdf),'https://anuarioeco.uo.edu.cu/index.php/aeco','techdev','@A1a2a3mo', 5329)+','
    			sdf += 1
    		else:
    			files += '}'
    			sdf = 0
    			files = files.replace(',}', '}')
    			return files
    else:
    			return '{'+upload(file,'https://anuarioeco.uo.edu.cu/index.php/aeco','techdev','@A1a2a3mo', 5329)+'}'
def upload(path,host, username, password, repo, proxy=''):
		upload = requests.session()
		var = 1
		while var == 1:
			try:
				token1 = upload.get(host+'/login',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},proxies=dict(http=proxy,https=proxy))
			except:
				token1 = upload.get(host+'/login',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},proxies=dict(http=proxy,https=proxy))
			else:
				var = 0
		token2 = BeautifulSoup(token1.text,"html.parser")
		token = token2.find('input',attrs={"name":"csrfToken"})["value"]
		logIn = upload.post(host+'/login/signIn', params={'csrfToken':token, 'password':password, 'remember':1,'source':'','username':username},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}, proxies=dict(http=proxy,https=proxy))
		if 'Salir' in logIn.text:
			token1 = upload.get(host+'/submission/wizard/2?submissionId='+str(repo)+'#step-2',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}, proxies=dict(http=proxy,https=proxy))
			token = token1.text.split('"csrfToken":"')[1].split('"')[0]
			precarga = upload.get(host+'/submission/wizard/2?submissionId='+str(repo), headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36","X-Csrf-Token":token}, proxies=dict(http=proxy,https=proxy))
			fileUpload = upload.post(host+'/api/v1/submissions/'+str(repo)+'/files', data={'fileStage':'2','name[es_ES]':path,'name[en_US]':path},  files={'file':open(path,'rb')},headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36","X-Csrf-Token":token}, proxies=dict(http=proxy,https=proxy))
			FileID = str(fileUpload.text.split('_href":"')[1].split('"')[0]).replace(str('\/'), '/').split('/')[-1]
			link = host+'/$$$call$$$/api/file/file-api/download-file?submissionFileId='+FileID+'&submissionId='+str(repo)+'&stageId=1'
			t = requests.get(host+'/login',headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"},proxies=dict(http=proxy,https=proxy))
			tok = BeautifulSoup(t.text,"html.parser")
			toke = tok.find('input',attrs={"name":"csrfToken"})["value"]
			response = '["logintoken":"'+toke+'","url:"'+link+'","name":"'+path+'"]'
			return response
def nameRamdom():
    populaton = '1234567890'
    name = "".join(random.sample(populaton,4))
    return name

@app.route('/<path:api>', methods=['GET','POST'])
def home(api):
	if api == 'upload':
		url = request.form['url']
		filename = download(url)
		fl = processFile(filename)
		return fl
	elif api == 'revise':
		return 'Api disponible'
	else:
		return 'Servicio no encontrado'
app.run(port=8989)