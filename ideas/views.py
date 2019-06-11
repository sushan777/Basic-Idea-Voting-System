from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . forms import IdeaForm
from . models import Idea, Comment, Vote
from django.http import HttpResponse, JsonResponse
from django.contrib import auth, messages
from django.utils.datastructures import MultiValueDictKeyError
from .forms import IdeaForm, CommentForm
from django.views.generic import ListView
from django.core.mail import send_mail


from django.template.loader import render_to_string
from rest_framework import generics
from .serializers import IdeaSerializer

# Create your views here.

@login_required(login_url="accounts:login")
def create(request):
	if request.method == 'POST':
		form = IdeaForm(request.POST or None, request.FILES or None)
		if form.is_valid:
			idea = Idea()
			idea.user = request.user
			# idea.title = form.cleaned_data['title']
			idea.title = request.POST['title']
			idea.description = request.POST['description']
			try:
				idea.image = request.FILES['image']
			except MultiValueDictKeyError:
				pass
			idea.save()
			messages.add_message(request,messages.SUCCESS,"Successfully created!")
			return redirect('accounts:dashboard')

		else:
			return render(request, 'ideas/create.html', {'page_title':'Add Your Idea','form':form})

	else:
		form = IdeaForm()
		return render(request, 'ideas/create.html', {'page_title':'Add Your Idea','form':form})
	# form = IdeaForm(request.POST or None)

	# if request.method == 'POST':
		
	# 	if form.is_valid:
	# 		return HttpResponse('Valid')

	# else:
	# 	return render(request, 'ideas/create.html', {'page_title':'Add Your Idea','form':form})

@login_required(login_url="accounts:login")
def delete(request, idea_id):
	user = request.user
	try:
		idea = Idea.objects.get(pk=idea_id)
	except Idea.DoesNotExist:
		messages.add_message(request,messages.ERROR,"Invalid request!")
		return redirect('accounts:dashboard')
	if user == idea.user:
		idea.delete()
		messages.add_message(request,messages.SUCCESS,"Successfully Deleted!")
		return redirect('accounts:dashboard')

	messages.add_message(request,messages.ERROR,"Invalid request!")
	return redirect('accounts:dashboard')
	
@login_required(login_url="accounts:login")
def edit(request, idea_id):
	user = request.user
	try:
		idea = Idea.objects.get(pk=idea_id)
	except Idea.DoesNotExist:
		messages.add_message(request,messages.ERROR,"Invalid request!")
		return redirect('accounts:dashboard')

	form = IdeaForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			idea.user = request.user
			idea.title = request.POST['title']
			idea.description = request.POST['description']
			try:
				idea.image = request.FILES['image']
			except MultiValueDictKeyError:
				pass
			idea.save()
			messages.add_message(request,messages.SUCCESS,"Successfully Edited {}!".format(request.POST['title']))
			return redirect('accounts:dashboard')

		else:
			return render(request, 'ideas/create.html', {'page_title':'Edit your idea','form':form, 'id':idea.id})


	else:
		form = IdeaForm(initial={'title':idea.title , 'description':idea.description})
		return render(request, 'ideas/create.html', {'page_title':'Edit your idea','form':form, 'id':idea.id})

def view(request, idea_id):
	idea = get_object_or_404(Idea, pk = idea_id)
	comment_form = CommentForm(initial={'user':request.user.id, 'idea':idea_id})
	comments = Comment.objects.filter(idea=idea_id)
	vote = Vote.objects.filter(user=request.user,idea=idea)
	data = {
		'page_title':idea.title,
		'idea':idea,
		'comment_form':comment_form,
		'comments':comments,
		'vote':'No'
	}
	if vote.count()> 0:
		data['vote'] = vote[0].vote

	html_email = render_to_string('ideas/view.html',data)

	send_mail('Test','Test Message','TestFrom',['abc@gmail.com'],'ideas/view.html',html_message = html_email)
	return render(request, 'ideas/view.html', {
												'page_title':idea.title,
												'idea':idea, 
												'comment_form':comment_form,
												'comments':comments,
												})


def comment(request):

	if str(request.user) == 'AnonymousUser':
		messages.add_message(request,messages.ERROR,"Invalid Request!")
		return redirect('accounts:login')


	if str(request.user.id) == request.POST['user']:
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request,messages.SUCCESS,"Successfully Commented!")
			return redirect('ideas:view',idea_id = request.POST['idea'])
	messages.add_message(request,messages.ERROR,"Invalid Request!")
	return redirect('accounts:dashboard')


def vote(request, idea_id):
	user = request.user
	if user.id == None:
		return JsonResponse({'class': 'error', 'message': 'You should login to vote'})
	try:
		idea = Idea.objects.get(pk=idea_id)
	except Idea.DoesNotExist:
		return JsonResponse({'class': 'error', 'message': 'Invalid request'})

	vote = Vote.objects.filter(user=user, idea=idea)
	print(vote)


	if vote.count() == 0:
		voteObj = Vote(vote = request.POST['vote'], user=user, idea=idea)
		voteObj.save()
		if request.POST['vote'] == 'U':
			return JsonResponse({'class': 'success', 'message': 'Successfully Liked'})
		return JsonResponse({'class': 'success', 'message': 'Successfully DisLiked'})
		
	vote.delete()
	return JsonResponse('VoteDeleted',safe=False)



class IdeaList(ListView):

	model = Idea
	template_name = 'accounts/dashboard.html'
	context_object_name = 'ideas'


class IdeaApiList(generics.ListAPIView):
	queryset = Idea.objects.all()
	serializer_class = IdeaSerializer


class IdeaApiDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Idea.objects.all()
	serializer_class = IdeaSerializer