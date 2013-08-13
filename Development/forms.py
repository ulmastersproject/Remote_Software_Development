from django import forms

class Global:
    app_name = ''

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

        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough code!")
        return message