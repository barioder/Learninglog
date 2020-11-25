from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm,EntryForm
from django.http import Http404
# Create your views here.

def index (request):
	"""the home page for learnig log."""
	return render(request, "learnig_logs/index.html")

@login_required
def topics(request):
	"""show all the topics."""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics':topics}
	return render (request , 'learnig_logs/topics.html',context)

@login_required
def topic (request, topic_id):
	"""show a signle topic and all its entries"""
	topic = Topic.objects.get(id=topic_id)
	if topic.owner != request.user:
		raise Http404
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries': entries}
	return render (request, 'learnig_logs/topic.html', context)

@login_required	
def new_topic (request):
	"""add a new topic."""
	if request.method != 'POST':
		#No data submitted; create a blank form.
		form = TopicForm()
	else:
		#post data submitted; process data
		form = TopicForm (data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return redirect ('learnig_logs:topics')
			
	#display a blank or invalid form.
	context = {'form' : form }
	
	return render (request, 'learnig_logs/new_topic.html',context)
	
@login_required
def new_entry(request,topic_id):
	#to add an entry to a specific topic
	topic = Topic.objects.get(id=topic_id)
	if request == 'GET':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learnig_logs:topic', topic_id = topic_id)
		else:
			print (form.errors)
	context = {'topic':topic , 'form':form}
	return render (request, 'learnig_logs/new_entry.html', context)
	
	
	
@login_required	
def edit_entry(request, entry_id):
	
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404
		
	if request.method != 'POST':
		form = EntryForm(instance = entry)
	else :
		form = EntryForm(instance = entry,data = request.POST)
		if form.is_valid():
			form.save()
			return redirect ('learnig_logs:topic', topic_id = topic.id)
			
	context = {'entry':entry,"topic":topic,"form":form}
	return render (request , 'learnig_logs/edit_entry.html',context)	