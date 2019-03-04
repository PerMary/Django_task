from django.shortcuts import render, get_object_or_404
from .models import Product, Position, Demand
from .forms import DemandForm, PositionForm
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required


#Список созданных заявок
@login_required
def demand_list(request):
	demands = Demand.objects.order_by('created_date')
	if request.user.groups.filter(name="Начальники") or request.user.groups.filter(name="Админ") or request.user.groups.filter(name="Конструктора") or request.user.groups.filter(name="Экономисты"):
		print('hello')
		return render(request, 'myapp/demand_list.html', {'demands': demands})
	else:
		demands = Demand.objects.order_by('created_date').filter(user=request.user)
		return render(request, 'myapp/demand_list.html', {'demands': demands})

#Создание новой заявки
@login_required
@permission_required('myapp.add_demand', 'non' )
def demand_new(request):
	if request.method == "POST":
		form = DemandForm(request.POST)
		if form.is_valid():
			demand = form.save(commit=False)
			demand.created_date = timezone.now()
			demand.user = request.user
			demand.save()
			return redirect('demand_detail', id_demand=demand.id)
	else:
		form = DemandForm()
		return render (request, 'myapp/demand_new.html', {'form': form})

#Ограничение доступа
def non(request):
	return render(request, 'myapp/non.html')

#Редактирование заявки
@login_required
@permission_required('myapp.change_demand', 'non' )
def demand_edit(request,id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	if request.user.groups.filter(name="Начальники") or demand.user == request.user or request.user.groups.filter(name="Админ"):
		if request.method == "POST":
			form = DemandForm(request.POST, instance=demand)
			if form.is_valid():
				demand = form.save(commit=False)
				demand.save()
				return redirect('demand_list')
		else:
			form = DemandForm(instance=demand)
		return render (request, 'myapp/demand_edit.html', {'form': form})
	else:
		return render (request, 'myapp/non.html')

#Просмотр конкретной завяки (описание с таблицей позиций)
# @login_required
# def demand_detail(request, id_demand):
# 	demand = get_object_or_404(Demand, id=id_demand)
# 	positions = Position.objects.filter(id_demand=id_demand)
# 	return render(request, 'myapp/demand_detail.html', {'demand': demand, 'positions': positions})

#Просмотр конкретной заявки
@login_required
def demand_detail(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	positions = Position.objects.filter(id_demand=id_demand)
	return render(request, 'myapp/demand_detail.html', {'demand': demand, 'positions': positions})

#Удаление заявки
@login_required
@permission_required('myapp.delete_demand', 'non' )
def demand_remove(request,id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	if demand.user == request.user or request.user.groups.filter(name="Начальники") or request.user.groups.filter(name="Админ"):
		if request.method == "POST":
			demand.delete()
			return redirect('demand_list')
		else:
			return render (request, 'myapp/demand_remove.html')
	else:
		return render (request, 'myapp/non.html')

#Добавление новой позиции
@login_required
@permission_required('myapp.add_position', 'non' )
def position_new(request, id_demand):
	demand = get_object_or_404(Demand, id=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			position = form.save(commit=False)
			position.id_demand = demand
			position.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
		form = PositionForm()
	return render(request, 'myapp/position_new.html', {'demand': demand, 'form': form})

#Редактирование позиции
@login_required
@permission_required('myapp.change_position', 'non')
def position_edit(request, id_demand, id_position):
	position = Position.objects.get(id=id_position)
	demand = get_object_or_404(Demand, id=id_demand)
	if request.method == "POST":
		form = PositionForm(request.POST)
		if form.is_valid():
			position = form.save(commit=False)
			position.id = id_position
			position.id_demand = demand
			position.save()
			return redirect('demand_detail', id_demand=id_demand)
	else:
		form = PositionForm(instance=position)
	return render(request, 'myapp/position_edit.html', {'demand': demand, 'form': form})


#Удаление позиции
@login_required
#@permission_required('myapp.delete_position', 'non')
def position_remove(request,id_demand, id_position):
	demand = get_object_or_404(Demand, id=id_demand)
	position = Position.objects.get(id=id_position)
	if demand.user == request.user or request.user.groups.filter(name="Начальники") or request.user.groups.filter(name="Админ"):
		if request.method == "POST":
			position.id = id_position
			position.id_demand = demand
			position.delete()
			return redirect('demand_detail', id_demand=demand.id)
		else:
			return render (request, 'myapp/position_remove.html', {'demand': demand})
	else:
		return render (request, 'myapp/non.html')

