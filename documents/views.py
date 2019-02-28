from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from myapp.models import Demand


def documents_list(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	return render(request, 'documents/documents_list.html')