from django.shortcuts import render
from Remote_Software_Development.Development.forms import DevelopmentForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Include the Dropbox SDK libraries
from dropbox import client, rest, session

import subprocess
import os

#DropBox Integration

APP_KEY = 'jgrn1vwmfcp0lpf'
APP_SECRET = 'reftv8sfas3bte5'
ACCESS_TYPE = 'app_folder'

dropbox_sess = None
dropbox_request_token = None
dropbox_url = None

def Remote_Software_Development(request):
    if request.method == 'POST':
        form = DevelopmentForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            return HttpResponseRedirect('/Submitted_Code')
    else:
        form = DevelopmentForm()
    return render(request, 'Development_form.html', {'form': form})

def Submitted_code(request):
    global dropbox_sess
    global dropbox_request_token
    global dropbox_url

    dropbox_sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
    dropbox_request_token = dropbox_sess.obtain_request_token()
    # Make the user sign in and authorize this token
    dropbox_url = dropbox_sess.build_authorize_url(dropbox_request_token)
    Code_Errors = "App was successfully executed without any Errors!"
    Code_Output = "App failed to Execute!"
    Execute = None

    file_location = "/home/ulmastersproject/Remote_Software_Development/App/Code.py"
    file_object = open(file_location, "rb+")
    message = "".join(file_object.readlines())
    file_object.close()
    Execute = subprocess.Popen(['python', file_location], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    Executed_results = Execute.communicate()

    if Execute.returncode == 0:
        Code_Output = "".join(Executed_results)
    else:
        Code_Errors = "".join(Executed_results)
    return render(request, 'submitted_code.html', {'message': message, 'output':Code_Output,
                'errors':Code_Errors, 'dropbox_url':dropbox_url})

def Add_to_dropbox(request):
    global dropbox_sess
    global dropbox_request_token

    access_token = dropbox_sess.obtain_access_token(dropbox_request_token)
    dropbox_client = client.DropboxClient(dropbox_sess)

    #Delete if there is any previously created tar files
    command0 = 'rm -rf /home/ulmastersproject/Remote_Software_Development/App/Remote_Software.tar'
    os.system(command0)

    #Converting the given user code (.py) to an executable using pyinstaller library
    command1 = 'python /home/ulmastersproject/Remote_Software_Development/App/pyinstaller-2.0/pyinstaller.py -D /home/ulmastersproject/Remote_Software_Development/App/Code.py'
    os.system(command1)

    #The executable directory is compressed through tar
    command2 = 'tar -cvf /home/ulmastersproject/Remote_Software_Development/App/Remote_Software.tar /home/ulmastersproject/Remote_Software_Development/App/pyinstaller-2.0/Code/dist/Code'
    os.system(command2)

    #The generated Code (folder) inside pyinstaller-2.0 is deleted after creating into Remote_Software.tar
    command3 = 'rm -rf /home/ulmastersproject/Remote_Software_Development/App/pyinstaller-2.0/Code'
    os.system(command3)

    f = open('/home/ulmastersproject/Remote_Software_Development/App/Remote_Software.tar', 'rb')
    #response = dropbox_client.put_file('/Remote_Software.tar', f, overwrite=True)
    response = dropbox_client.put_file('/Remote_Software.tar', f, overwrite=True)
    f.close()

    return HttpResponse("Your App is successfully uploaded into your DropBox location \n Response:- " + str(response))
