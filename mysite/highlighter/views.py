from django.shortcuts import render

# Create your views here.

import highlighter.backend as backend

# def test():
# 	print(backend.get_summary("123"))

from .models import SummaryEntry, LabelType
from .form import SummaryForm


#try this later

# from django.views.generic.edit import CreateView

# class higlighter_view(CreateView):
#     model = SummaryEntry
#     fields = fields = ["title", "original", "labels"]


def highlighter_view(r, *args, **kwargs):
	#obj = SummaryEntry.objects.get(id=1)
	# context = {
	# 'field': obj.field1,
	# }

	##### this also works for render form only ####
	# form = SummaryForm(r.POST or None)
	# if form.is_valid():
	# 	form.save()
	# 	form = SummaryForm()
	# context = {
	# 	'form': form,
	# 	'processed_text': 'nothing set.'
	# }
	# return render(r, "highlighter_temp.html", context)
	################################################

	#vars: cleaned_data, labels
	cleaned_data = {}
	labels = []
	s = None
	form = SummaryForm()
	if r.method == "POST":
		form = SummaryForm(r.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			labels = cleaned_data.pop('labels')
			s = SummaryEntry.objects.create(**cleaned_data)
			s.labels.set(labels)

		else:
			form = SummaryForm()
			print("errors in form", form.errors)
	else:
		print("not a POST method")

	#process here
	processed_text = backend.get_summary(cleaned_data, labels)
	if s is not None:
		print("value of s", s)
		s.processed =processed_text

	context={
		#'object': obj, # so that we don't have to map out everything, when keys change
		'form':form,
		'processed_text': processed_text,
	}
	#print ("field 1 of object", obj.field1)
	return render(r, 'highlighter_temp.html', context)
	# this is still relative to templates directory!!