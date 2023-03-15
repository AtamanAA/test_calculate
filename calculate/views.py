from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PipeHighPressureForm, ThreadForm
from .services import Thread
from .models import Material, PipeHighPressure



def index(request):
	"""Home page"""
	return render(request, 'calculate/index.html')

def pipe_pressure(request):
	"""Pipe thickness calculation"""
	# Initial value
	thickness = 0
	outside_radius = 0	

	if request.method == 'POST':
		form = PipeHighPressureForm(request.POST)
		if form.is_valid():			
			yield_strength = form.cleaned_data['yield_strength']
			test_pressure = form.cleaned_data['test_pressure']
			min_outside_diameter = form.cleaned_data['min_outside_diameter']
			k_welding = form.cleaned_data['k_welding']
			k_industry = form.cleaned_data['k_industry']
			k_cycle = form.cleaned_data['k_cycle']
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']

			pipe = PipeHighPressure.calculate(yield_strength, test_pressure, min_outside_diameter, 
												k_industry, k_cycle, k_welding)
			thickness = pipe.thickness
			outside_radius = pipe.outside_radius

			if 'create' in request.POST:
				# Save calculate in BD
				if PipeHighPressure.create(request.user, yield_strength, test_pressure, min_outside_diameter, 
										k_industry, k_cycle, k_welding, name, description):
					messages.success(request, ("Розрахунок успішно збережено!"))
				else:
					messages.error(request, ("Розрахунок не вдалося зберегти, т.к. товщина стінки перевищує зовнішній радіус "))

	else:
		form = PipeHighPressureForm()	
	return render(request, 'calculate/pipe_pressure.html', 
					{'form': form,
					 'thickness': thickness,
					 'outside_radius': outside_radius,})

def thread(request):
	"""Thread calculation"""
	# Initial values
	k_bolt_tension = 0	
	k_nut_tension = 0	
	k_bolt_crush = 0
	k_nut_crush = 0		
	k_bolt_shear = 0		
	k_nut_shear = 0

	if request.method == 'POST':
		form = ThreadForm(request.POST)
		if form.is_valid():
			# Form processing
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

			#Create thread instance
			thread = Thread(axial_force, bolt_yield_strength, nut_yield_strength, 
							nominal_thread_diameter, thread_pitch, nut_active_height, 
							nut_minimum_diameter, bolt_hole_diameter, k_industry, k_thread)

			# Calculate safety factors
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

def materials(request):
	"""Materials table"""
	materials_list = Material.get_all()
	return render(request, 'calculate/materials.html', {'materials_list':materials_list})


def pipe_results(request):
	"""Pipe pressure results table"""
	if request.user.is_superuser:		
		pipe_results = PipeHighPressure.get_all()
	elif request.user.is_authenticated:
		pipe_results = PipeHighPressure.get_by_user(request.user.id)
	else:
		pipe_results = []
	return render(request, 'calculate/pipe_results.html', {'pipe_results':pipe_results})


def pipe_detail(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			pipe_id = request.POST['pipeid']
			pipe = PipeHighPressure.get_by_id(pipe_id)
			form = PipeHighPressureForm(request.POST)

			if form.is_valid():
				yield_strength = form.cleaned_data['yield_strength']
				test_pressure = form.cleaned_data['test_pressure']
				min_outside_diameter = form.cleaned_data['min_outside_diameter']
				k_welding = form.cleaned_data['k_welding']
				k_industry = form.cleaned_data['k_industry']
				k_cycle = form.cleaned_data['k_cycle']
				name = form.cleaned_data['name']
				description = form.cleaned_data['description']

			if 'calculate' in request.POST:
				pipe_temp = PipeHighPressure.calculate(yield_strength, test_pressure, min_outside_diameter, 
														k_industry, k_cycle, k_welding)
				thickness_temp = pipe_temp.thickness
				outside_radius_temp = pipe_temp.outside_radius
				return render(request, 'calculate/pipe_detail.html', {'pipe':pipe, 'form': form, 
																		'thickness_temp': thickness_temp, 
																		'outside_radius_temp':outside_radius_temp})

			elif 'update' in request.POST:
				if pipe.update(yield_strength, test_pressure, min_outside_diameter, 
							k_industry, k_cycle, k_welding, name, description):
					messages.success(request, (f"Розрахунок {pipe.name} успішно змінено!"))
					return redirect('pipe_results')
				else:
					messages.error(request, ("Розрахунок не вдалося зберегти, т.к. товщина стінки перевищує зовнішній радіус "))
					return render(request, 'calculate/pipe_detail.html', {'pipe':pipe, 'form':form})

			elif 'delete' in request.POST:
				pipe_name = pipe.name
				pipe.delete_by_id(pipe_id)
				messages.error(request, (f"Ви видалили розрахунок {pipe_name}!"))
				return redirect('pipe_results')
			else:
				form = PipeHighPressureForm(initial = pipe.to_dict())
				thickness_temp = pipe.thickness
				outside_radius_temp = pipe.outside_radius
				return render(request, 'calculate/pipe_detail.html', {'pipe':pipe, 'form':form, 
																		'thickness_temp':thickness_temp,
																		'outside_radius_temp':outside_radius_temp})
		else:
			messages.error(request, ("Оберіть розрахунок!"))		
			return redirect('pipe_results')
	return render(request, 'calculate/1.html', {'pipe':pipe, 'form':form})
