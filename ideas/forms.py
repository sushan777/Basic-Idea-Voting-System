from django import forms
from .models import Comment

class IdeaForm(forms.Form):
	title = forms.CharField(label = 'Title')
	image = forms.ImageField(label = 'Image', required =False)
	description = forms.CharField(label = 'Description',widget = forms.Textarea)
	
	title.widget.attrs.update({'class':'form-control'})
	image.widget.attrs.update({'class':'form-control'})
	description.widget.attrs.update({'class':'form-control'})

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment', 'user', 'idea']
		widgets = {
			'comment' : forms.Textarea(attrs={
				'class': 'form-control',
				'rows': 2
			}),
			'user' : forms.HiddenInput(),
			'idea' : forms.HiddenInput(),
			}