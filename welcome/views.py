from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from ideas.models import Idea
from django.db.models import Count, Q


def home(request):
	# ideas = Idea.objects.all().order_by('-created')
	ideas = Idea.objects.all().annotate(num_comment=Count('comment'),
		num_upvotes=Count('vote', distinct=True, filter=Q(vote__vote__contains='U')),
		num_downvotes=Count('vote', distinct=True, filter=Q(vote__vote='D')),
		)
	# ideas = Idea.objects.filter(comment__id="1").order_by('-created')

	return render(request, 'welcome/index.html', {'page_title':'Home', 'ideas':ideas})