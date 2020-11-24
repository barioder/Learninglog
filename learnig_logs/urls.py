"""urls in the learning logs"""
from django.urls import path
from . import views

app_name = "learnig_logs"
urlpatterns = [
	# home page
	path ('', views.index, name = 'index'),
	
	#topics page
	path ('topics/',views.topics,name = 'topics'),
	
	#detail for single topic
	path ('topics/<int:topic_id>', views.topic, name = 'topic'),
	
	#details for addinng a new topic 
	path ('new_topic/',views.new_topic, name= 'new_topic'),
	
	#page adding new entry
	path ('new_entry/<int:topic_id>/',views.new_entry, name = 'new_entry'),
	
	#editing page
	path ('edit_page/<int:entry_id>', views.edit_entry, name = 'edit_entry'),
]