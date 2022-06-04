from django.shortcuts import render
from django.http import HttpResponse
from .forms import SumPostForm, PipePressureThickness, ThreadForm
from .services import pipe_thickness, Thread

# Create your views here.

def index(request):
	"""Домащняя страница"""
	return render(request, 'calculate/index.html')

def pipe_pressure(request):
	"""Страница расчета толщины стенки трубы высокого давления"""
	# Стартовые значения расчетных параметров
	thickness = 0
	outside_radius = 0
	zero = 0

	if request.method == 'POST':
		form = PipePressureThickness(request.POST)
		if form.is_valid():
			# Обработка формы
			yield_strength = form.cleaned_data['yield_strength']
			test_pressure = form.cleaned_data['test_pressure']
			min_outside_diameter = form.cleaned_data['min_outside_diameter']
			k_welding = form.cleaned_data['k_welding']
			k_industry = form.cleaned_data['k_industry']
			k_cycle = form.cleaned_data['k_cycle']

			#Расчет толщины стенки
			thickness = pipe_thickness(yield_strength, test_pressure, 
										min_outside_diameter, k_welding, 
										k_industry, k_cycle)
			#Расчет наружного радиуса для валидации
			outside_radius = min_outside_diameter / 2
			
	else:
		form = PipePressureThickness()	
	return render(request, 'calculate/pipe_pressure.html', 
					{'form': form, 'thickness': thickness, 'outside_radius': outside_radius, 'zero': zero})


def thread(request):
	"""Страница расчета резьбового соединения(основная)"""
	# Стартовые значения расчетных параметров
	k_bolt_tension = 0	
	k_nut_tension = 0	
	k_bolt_crush = 0
	k_nut_crush = 0		
	k_bolt_shear = 0		
	k_nut_shear = 0

	if request.method == 'POST':
		form = ThreadForm(request.POST)
		if form.is_valid():
			# Обработка формы
			axial_force = form.cleaned_data['axial_force']
			bolt_yield_strength = form.cleaned_data['bolt_yield_strength']
			nut_yield_strength = form.cleaned_data['nut_yield_strength']
			nominal_thread_diameter = form.cleaned_data['nominal_thread_diameter']
			thread_pitch = form.cleaned_data['thread_pitch']
			nut_active_height = form.cleaned_data['nut_active_height']
			nut_minimum_diameter = form.cleaned_data['nut_minimum_diameter']
			bolt_hole_diameter = form.cleaned_data['bolt_hole_diameter']
			k_industry = form.cleaned_data['k_industry']
			k_thread = form.cleaned_data['k_thread']

			#Создание экзепляра резьбы по вводным данным
			thread = Thread(axial_force, bolt_yield_strength, nut_yield_strength, 
							nominal_thread_diameter, thread_pitch, nut_active_height, 
							nut_minimum_diameter, bolt_hole_diameter, k_industry, k_thread)

			#Расчет коэфициентов запаса
			k_bolt_tension = thread.k_bolt_tension		
			k_nut_tension = thread.k_nut_tension	
			k_bolt_crush = thread.k_bolt_crush		
			k_nut_crush = thread.k_nut_crush		
			k_bolt_shear = thread.k_bolt_shear		
			k_nut_shear = thread.k_nut_shear
	else:
		form = ThreadForm()	
	return render(request, 'calculate/thread.html',
					 {'form': form, 
					 'k_bolt_tension': k_bolt_tension,
					 'k_nut_tension': k_nut_tension,
					 'k_bolt_crush': k_bolt_crush,
					 'k_nut_crush': k_nut_crush,
					 'k_bolt_shear': k_bolt_shear,
					 'k_nut_shear': k_nut_shear,})


"""Песочница для тестов"""


def suma(x, y):
	result = (x + y)
	return result

def division(x, y):
	result = (x / y)
	return result

def multiplication(x, y):
	result = (x * y)
	return result
	
def sandbox(request):
	"""Тестовая страница"""
	summ = 0
	mult = 0
	div = 0
	if request.method == 'POST':
		form = SumPostForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			a = form.cleaned_data['first_number']
			b = form.cleaned_data['second_number']
			summ = suma(a, b)
			mult = multiplication(a, b)
			div = division(a, b)
			print(summ)
	else:
		form = SumPostForm()	
	return render(request, 'calculate/sandbox.html', {'form': form, 'summ': summ, 'mult': mult, 'div': div})

def sandbox_results(request):
	"""Вывод результата тестовой страницы"""
	
	value = summ(10, 35)
	return HttpResponse(f"Результат расчета: {value}")
# 	#return render(request, 'calculate/pipe_pressure.html')