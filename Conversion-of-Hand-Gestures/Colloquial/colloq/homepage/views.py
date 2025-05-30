from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cmath
# Create your views here.
def button(request):
	return render(request,'home.html')
def output(request):
	data="Hello World this is python"

	return render(request,'home.html',{'data':data})

import cv2
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from googletrans import Translator
import os, requests, time
from xml.etree import ElementTree
from playsound import playsound

def write_to_file(output):
	file1 = open('TargetText.txt','w')
	file1.write(output)
	file1.close()

def test(request):
	classifier = load_model('D:/Musthafa/Stud_Projects/2024/Conversion-of-Hand-Gestures/Colloquial/Trained_model.h5')
#classifier.evaluate()

#Prediction of single image

	#img_name = input('Enter Image Name:')
	image_path = 'D:/Musthafa/Stud_Projects/2024/Conversion-of-Hand-Gestures/Colloquial/colloq/'+request.POST['url']

	test_image = image.load_img(image_path, target_size=(64, 64))
	test_image = image.img_to_array(test_image)
	test_image = np.expand_dims(test_image, axis = 0)
	result = classifier.predict(test_image)
	#training_set.class_indice
	if result[0][0] == 1:
		output='All The Best'
	elif result[0][1] == 1:
		output='Whar Aer you doing'
	elif result[0][2]==1:
		output='nice work, let me cedlebrate'
	elif result[0][3] == 1:
		output='we are good to go'

	write_to_file(output)
	return render(request,'result.html',{'output':output})



	
	
def upload_img(request):
	if request.method=="POST":
		uploded_file = request.FILES["upload"]
		fs = FileSystemStorage()
		filename = fs.save(uploded_file.name,uploded_file)
		uploaded_file_url1 = fs.url(filename)
		#request.session['img'] = uploded_file_url1
		#request.session['img'] = uploded_file_url1
		return render(request,'home.html',{'uploaded':1,'uploadurl':uploaded_file_url1})

	
def nothing(x):
	pass

image_x, image_y = 64,64

def predictor():
	classifier = load_model('D:/Musthafa/Stud_Projects/2024/Conversion-of-Hand-Gestures/Colloquial/colloq/homepage/Trained_model.h5')
	test_image = image.load_img('1.png', target_size=(64, 64))
	test_image = image.img_to_array(test_image)
	test_image = np.expand_dims(test_image, axis = 0)
	result = classifier.predict(test_image)
	if result[0][0]==1:
		return 'All The Best'
	elif result[0][1]==1:
		return 'Bye'
	elif result[0][2]==1:
		return 'Hello'
	elif result[0][3]==1:
		return 'Peace'


def dynamic(request):
	cam = cv2.VideoCapture(0)

	cv2.namedWindow("Trackbars")

	cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
	cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
	cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
	cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
	cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
	cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

	cv2.namedWindow("test")

	img_counter = 0

	img_text = ''
	while True:
		ret, frame = cam.read()
		frame = cv2.flip(frame,1)
		l_h = cv2.getTrackbarPos("L - H", "Trackbars")
		l_s = cv2.getTrackbarPos("L - S", "Trackbars")
		l_v = cv2.getTrackbarPos("L - V", "Trackbars")
		u_h = cv2.getTrackbarPos("U - H", "Trackbars")
		u_s = cv2.getTrackbarPos("U - S", "Trackbars")
		u_v = cv2.getTrackbarPos("U - V", "Trackbars")


		img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)

		lower_blue = np.array([l_h, l_s, l_v])
		upper_blue = np.array([u_h, u_s, u_v])
		imcrop = img[102:298, 427:623]
		hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower_blue, upper_blue)
		
		cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
		cv2.imshow("test", frame)
		cv2.imshow("mask", mask)
		
		#if cv2.waitKey(1) == ord('c'):
			
		img_name = "1.png"
		save_img = cv2.resize(mask, (image_x, image_y))
		cv2.imwrite(img_name, save_img)
		print("{} written!".format(img_name))
		img_text = predictor()
			

		if cv2.waitKey(1) == 27:
			break


	cam.release()
	cv2.destroyAllWindows()

	return render(request,'home.html',{})
from googletrans import Translator
import os, requests, time
from xml.etree import ElementTree
from playsound import playsound

#language = 1
translator = Translator()

class TextToSpeech(object):
	def __init__(self, subscription_key,language):
		self.subscription_key = subscription_key
		self.language=language
		file1 = open("TargetText.txt","r")
		text = file1.readline()
		print(text)
		self.tts = text
		self.timestr = time.strftime("%Y%m%d-%H%M")
		self.access_token = None

	def get_token(self):
		fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
		headers = {
		'Ocp-Apim-Subscription-Key': self.subscription_key
		}
		response = requests.post(fetch_token_url, headers=headers)
		self.access_token = str(response.text)

	def save_audio(self):
		base_url = 'https://westus.tts.speech.microsoft.com/'
		path = 'cognitiveservices/v1'
		constructed_url = base_url + path
		headers = {
		'Authorization': 'Bearer ' + self.access_token,
		'Content-Type': 'application/ssml+xml',
		'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
		'User-Agent': 'YOUR_RESOURCE_NAME'
		}
		xml_body = ElementTree.Element('speak', version='1.0')

		if int(self.language)==1:
			print("English")
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24kRUS)')
			voice.text = self.tts
			lang = "English"
	   
		###DUTCH
		elif int(self.language) == 2:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'nl-NL')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'nl-NL')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (nl-NL, HannaRUS)')
			translation = translator.translate(self.tts,src = 'en', dest='nl')
			print("The translation of text",self.tts,"in Dutch is",translation.text)
			
			voice.text = translation.text
			lang = 'DUTCH'
		   
			###French
		elif int(self.language) == 3:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'fr-FR')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (fr-FR, Julie, Apollo)')
			translation = translator.translate(self.tts,src = 'en', dest='fr')
			print("The translation of text ",self.tts,"in French is",translation.text)
			
			voice.text = translation.text
			lang = 'French'
				
			###German
		elif int(self.language) == 4:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (de-DE, Hedda)')
			translation = translator.translate(self.tts,src = 'en', dest='de')
			print("The translation of text ",self.tts,"in German is",translation.text)
			
			voice.text = translation.text
			lang = 'German'

			###Italian
		elif int(self.language) == 5:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'it-IT')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'it-IT')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (it-IT, LuciaRUS)')
			translation = translator.translate(self.tts,src = 'en', dest='de')
			print("The translation of text ",self.tts,"in Italian is",translation.text)
			voice.text = translation.text
			lang = 'Italian'

			###Portuguese
		elif int(self.language) == 6:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'pt-BR')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'pt-BR')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (pt-BR, HeloisaRUS)')
			translation = translator.translate(self.tts,src = 'en', dest='pt')
			print("The translation of text ",self.tts,"in Portuguese is",translation.text)
			voice.text = translation.text
			lang = 'Portuguese'

		##spanish
		elif int(self.language) == 7:
			xml_body = ElementTree.Element('speak', version='1.0')
			xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'es-ES')
			voice = ElementTree.SubElement(xml_body, 'voice')
			voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'es-ES')
			voice.set('name', 'Microsoft Server Speech Text to Speech Voice (es-ES, HelenaRUS)')
			translation = translator.translate(self.tts,src = 'en', dest='es')
			print("The translation of text ",self.tts,"in Spanish is",translation.text)
			
			voice.text = translation.text
			lang = 'Spanish'

		else:
			print("Problem in language")

			
		body = ElementTree.tostring(xml_body)

		response = requests.post(constructed_url, headers=headers, data=body)
		if response.status_code == 200:
		   with open(self.tts+"_"+lang+"_"+voice.text+'.wav','wb') as audio:
				   audio.write(response.content)
				   print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
				   os.system("aplay  "+self.tts+"_"+lang+"_"+voice.text+'.wav')                   
		else:
		   print ("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
		 


def speech(request):
	file1 = open("TargetText.txt","r")
	text = file1.readline()
	from googletrans import Translator
	import pyttsx3  # Example text-to-speech library
	s_language = request.POST["lang"]
	language=""
	if(s_language=='1'):
		language="en"
	elif(s_language=='2'):
		language="nl"
	elif(s_language=='3'):
		language="fr"
	elif(s_language=='4'):
		language="de"
	elif(s_language=='5'):
		language="it"
	elif(s_language=='6'):
		language="pt"
	elif(s_language=='7'):
		language="es"
	
	translator = Translator()
	translated_text = translator.translate(text,src="en", dest=language ).text
	print(translated_text)
	# Initialize text-to-speech engine
	engine = pyttsx3.init()
	engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Set voice

	# Set the text to be spoken (translated text)
	engine.say(translated_text)

	# Save the audio (modify based on your text-to-speech library)
	engine.runAndWait()  # This might save the audio to a temporary location

	# Render the result (assuming you have a template)
	return render(request, 'result.html', {})
def captureImage():

	cam=cv2.VideoCapture(0)
	cv2.namedWindow("Preprocessing")
	img_counter=0

	while True:
		ret,frame=cam.read()
		cv2.imshow("test",frame)
		if not ret:
			break
		k=cv2.waitKey(1)

		if k%256==27:
			print("Escape hit.Closing..")
			break
		elif k%256==32:
			img_name="Image_{}.png".format(img_counter)
			print("Image file saved as ",img_name)
			cv2.imwrite(img_name,frame)
			img_counter+=1
	cam.release()
	cv2.destroyAllWindows()
	return img_name

def cropImage(imgName):
	im=cv2.imread(imgName)
	fromCenter=False
	r=cv2.selectROI(im,fromCenter)
	#r=cv2.selectROI(im)
	
	imgCrop=im[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
	cv2.imwrite("Cropped.png",imgCrop)
	#cv2.imshow("Image",imgCrop)
	#cv2.waitKey(0)
	return imgCrop

def rgbtoGray(blur):
	filtered=cv2.imread("Blurred.png",0)
	cv2.imwrite("Gray.png",filtered)
	#cv2.imshow("Grayscale",filtered)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return filtered

def binary():
	hand=cv2.imread("Gray.png")
	ret,the=cv2.threshold(hand,210,255,cv2.THRESH_BINARY_INV)
	cv2.imwrite("Binary.png",the)
	#cv2.imshow("Test",the)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return the

def cont(the):
	converted=cv2.cvtColor(the,cv2.COLOR_BGR2GRAY)
	_,contours,_=cv2.findContours(converted.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	hull=[cv2.convexHull(c) for c in contours]
	final=cv2.drawContours(the,hull,-1,(255,0,0))
	cv2.imwrite("Convex Hull.png",final)
	#cv2.imshow("Convex Hull.png",final)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

def blur(crop):
	blur=cv2.GaussianBlur(crop,(3,3),0)
	cv2.imwrite("Blurred.png",blur)
	#cv2.imshow("Blurred.png",blur)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return blur

def morphology(conv):
	kernel=np.ones((5,5),np.uint8)
	dilate=cv2.dilate(conv,kernel,iterations=1)
	erosion=cv2.erode(dilate,kernel,iterations=1)
	cv2.imwrite("Filter.png",erosion)
	cv2.imshow("Filter.png",erosion)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def preprocess(request):
	name=captureImage()
	crop=cropImage(name)
	blurred=blur(crop)
	rgb=rgbtoGray(blurred)
	conv=binary()
	morphology(conv)
