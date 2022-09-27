from django import forms

class TaskForm(forms.Form):
    judul_task = forms.CharField(max_length=50, label="Judul Task", required=True)
    deskripsi_task = forms.CharField(max_length=200, label="Deskripsi Task", required=True, widget=forms.Textarea)