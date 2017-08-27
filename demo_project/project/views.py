from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from .models import Project, Planning, Tender, TenderItem, Milestone, Transaction

from rest_framework.views import APIView
from rest_framework.response import Response




class ProjectData(APIView):

	def get(self, request, format=None):
		labels = []
		default_items = []
		project_label=[]
		number_of_tenderers=[]
		tender_year = []
		tender_number = []
		for key in Planning.objects.all():
			label=str(key.project)
			default_item=key.estimated_budget	
			labels.append(label)
			default_items.append(default_item)
		for i in Tender.objects.all():
			a = str(i.project)
			b = i.number_of_tenderers
			c = i.bid_start_date.year
			d = Tender.objects.filter(bid_start_date__year=c).count()
			project_label.append(a)
			number_of_tenderers.append(b)
			tender_year.append(c)
			tender_number.append(d)
		tender_start=[]
		haha = [tender_start.append(x) for x in tender_year if x not in tender_start]
		data = {
		"labels": labels,
		"default": default_items,
		"tender_labels":project_label,
		"tender_default":number_of_tenderers,
		"tender_start":tender_start,
		"tenders":tender_number
		}


		return Response(data)

