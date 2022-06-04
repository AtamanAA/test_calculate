def pipe_thickness(yield_strength, test_pressure, 
					min_outside_diameter, k_welding, 
					k_industry, k_cycle):
	
	allowable_stresses = yield_strength / (k_industry * k_cycle)
	thickness = test_pressure * min_outside_diameter / (2 * allowable_stresses * float(k_welding) + test_pressure)
	thickness_round = round(thickness, 3)

	return thickness_round

class Thread:
	"""Описание и расчет резьбового соединения"""

	def __init__(self, axial_force, bolt_yield_strength, nut_yield_strength, 
					nominal_thread_diameter, thread_pitch, nut_active_height, nut_minimum_diameter,
					bolt_hole_diameter = 0, k_industry = 1.3, k_thread = 0.8):

		"""Инициализация вводных параметров"""
		self.axial_force = axial_force * 1000
		self.bolt_yield_strength = bolt_yield_strength
		self.nut_yield_strength = nut_yield_strength
		self.nominal_thread_diameter = nominal_thread_diameter
		self.thread_pitch = thread_pitch
		self.nut_active_height = nut_active_height
		self.nut_minimum_diameter = nut_minimum_diameter
		self.bolt_hole_diameter = bolt_hole_diameter
		self.k_industry = k_industry
		self.k_thread = float(k_thread)

		"""Определение геометрии резьбы"""
		#Число рабочих витков резьбы (максимум 8), z
		self.work_threads = min((self.nut_active_height / thread_pitch), 8)
		#Полная Высота профиля, H
		self.full_profile_height = 0.866025 * self.thread_pitch
		#Высота витка (профиля), h
		self.height_coil = 5 * self.full_profile_height / 8
		#Внутренний диаметр резьбы, d1
		self.internal_thread_diameter = self.nominal_thread_diameter - 2 * self.height_coil 
		#Средний диаметр резьбы, d2
		self.midle_thread_diameter = self.nominal_thread_diameter - 2 * 3 * self.full_profile_height / 8
		#Активная площадь сечения болта, Sb
		self.bolt_active_area = 3.14 * (self.internal_thread_diameter**2 - self.bolt_hole_diameter**2) / 4
		#Активная площадь сечения гайки, Sn
		self.nut_active_area = 3.14 * (self.nut_minimum_diameter**2 - self.nominal_thread_diameter**2) / 4

		"""Расчет допускаемых напряжений"""
		# Допускаемые напряжения для растяжения болта, [G]рб
		self.bolt_tension_stress_permis = self.bolt_yield_strength / self.k_industry
		# Допускаемые напряжения для растяжения гайки, [G]рг
		self.nut_tension_stress_permis = self.nut_yield_strength / self.k_industry
		# Допускаемые напряжения для смятия болта, [G]смб
		self.bolt_crush_stress_permis = 0.8 * self.bolt_tension_stress_permis
		# Допускаемые напряжения для смятия гайки, [G]смг
		self.nut_crush_stress_permis = 0.8 * self.nut_tension_stress_permis
		# Допускаемые напряжения для среза болта, [т]смб
		self.bolt_shear_stress_permis = 0.3 * self.bolt_tension_stress_permis
		# Допускаемые напряжения для среза гайки, [т]смг
		self.nut_shear_stress_permis = 0.3 * self.nut_tension_stress_permis

		"""Расчет действующих напряжений"""
		# Напряжения растяжения болта, [G]рб
		self.bolt_tension_stress = self.axial_force / self.bolt_active_area
		# Напряжения растяжения гайки, [G]рг
		self.nut_tension_stress = self.axial_force / self.nut_active_area
		# Напряжения смятия болта, [G]смб
		self.bolt_crush_stress = self.axial_force / (3.14 * self.midle_thread_diameter * self.height_coil * self.work_threads)
		# Напряжения смятия гайки, [G]смг
		self.nut_crush_stress = self.bolt_crush_stress
		# Напряжения среза болта, [т]смб
		self.bolt_shear_stress = self.axial_force / (3.14 * self.internal_thread_diameter * self.k_thread * self.work_threads * self.thread_pitch)
		# Напряжения среза гайки, [т]смг
		self.nut_shear_stress = self.bolt_shear_stress

		"""Расчет коэфициентов запаса"""
		# Коэффициент запаса растяжения болта, [G]рб
		self.k_bolt_tension = round((self.bolt_tension_stress_permis / self.bolt_tension_stress),1)
		# Коэффициент запаса растяжения гайки, [G]рг
		self.k_nut_tension = round((self.nut_tension_stress_permis / self.nut_tension_stress),1)
		# Коэффициент запаса смятия болта, [G]смб
		self.k_bolt_crush = round((self.bolt_crush_stress_permis / self.bolt_crush_stress),1)
		# Коэффициент запаса смятия гайки, [G]смг
		self.k_nut_crush = round((self.nut_crush_stress_permis / self.nut_crush_stress),1)
		# Коэффициент запаса среза болта, [т]смб
		self.k_bolt_shear = round((self.bolt_shear_stress_permis / self.bolt_shear_stress),1)
		# Коэффициент запаса среза гайки, [т]смг
		self.k_nut_shear = round((self.nut_shear_stress_permis / self.nut_shear_stress),1)
