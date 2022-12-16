from django.shortcuts import render
from .forms import PipePressureThickness, ThreadForm
from .services import pipe_thickness, Thread


def index(request):
	"""Home page"""
	return render(request, 'calculate/index.html')

def pipe_pressure(request):
	"""Pipe thickness calculation"""
	# Initial value
	thickness = 0
	outside_radius = 0
	zero = 0

	if request.method == 'POST':
		form = PipePressureThickness(request.POST)
		if form.is_valid():
			# Form processing
			yield_strength = form.cleaned_data['yield_strength']
			test_pressure = form.cleaned_data['test_pressure']
			min_outside_diameter = form.cleaned_data['min_outside_diameter']
			k_welding = form.cleaned_data['k_welding']
			k_industry = form.cleaned_data['k_industry']
			k_cycle = form.cleaned_data['k_cycle']

			# Calculate parametr
			thickness = pipe_thickness(yield_strength, test_pressure, 
										min_outside_diameter, k_welding, 
										k_industry, k_cycle)
			outside_radius = min_outside_diameter / 2
			
	else:
		form = PipePressureThickness()	
	return render(request, 'calculate/pipe_pressure.html', 
					{'form': form,
					 'thickness': thickness,
					 'outside_radius': outside_radius,
					 'zero': zero,})


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