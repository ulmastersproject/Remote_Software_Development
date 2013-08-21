"""
Project Title: Remote Software Development
Author: Santhosh Kumar Balasa Ramnath
Supervisor: Dr. John Nelson
University: University of Limerick
Year: 2012 - 2013
"""

from django import forms

#Creating a Global class to store the name of the App
class Global:
    app_name = ''

#Using the built in Develoment form in Django Framework
class DevelopmentForm(forms.Form):
    App_Name = forms.CharField(max_length=100)
    Python_Code = forms.CharField(widget=forms.Textarea)

    def clean_Python_Code(self):
        Global.app_name = self.cleaned_data['App_Name']
        message = self.cleaned_data['Python_Code']
        message += "\n\nprint \" \""
        file_object = open("/home/ulmastersproject/Remote_Software_Development/App/" + Global.app_name + ".py", "wb+")
        file_object.write(message)
        file_object.close()

        #Make sure the user has inputted right amount of code
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough code!")
        return message


# DropBox SDK libraries
from dropbox import client, rest, session

#  Authentication
APP_KEY = 'ar6snxa76ndx5iz'
APP_SECRET = 'cq1wjz72vdou2bq'
ACCESS_TYPE = 'app_folder'

#  Creating Dropbox session
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
request_token = sess.obtain_request_token()

#  Make the user sign in and authorize this token
url = sess.build_authorize_url(request_token)
print "url:", url
print "Please authorize in the browser. After you're done, press enter."
raw_input()

#  This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)
print "linked account:", client.account_info()

#  Upload the reguired executable file into DropBox location
f_upload = open('E:/Final MEng Project/Project.exe', 'rb')

#  File named in DropBox
response = client.put_file('/MEng_Project.exe', f_upload)
print "uploaded:", response

#  Download the required executable file from Dropbox location
f_download = client.get_file('/MEng_Project.exe')
out = open('E:/Final MEng Project/MEng_Project_from_Dropbox.exe', 'wb')
out.write(f_download.read())
out.close()
