class Thread:
	def __init__(self, axial_force, bolt_yield_strength, nut_yield_strength, 
					nominal_thread_diameter, thread_pitch, nut_active_height, nut_minimum_diameter,
					bolt_hole_diameter = 0, k_industry = 1.3, k_thread = 0.8):		
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

		# Thread geometry	
		self.work_threads = min((self.nut_active_height / thread_pitch), 8) # z (max=8)
		self.full_profile_height = 0.866025 * self.thread_pitch # H		
		self.height_coil = 5 * self.full_profile_height / 8 # h		
		self.internal_thread_diameter = self.nominal_thread_diameter - 2 * self.height_coil # d1		
		self.midle_thread_diameter = self.nominal_thread_diameter - 2 * 3 * self.full_profile_height / 8 # d2		
		self.bolt_active_area = 3.14 * (self.internal_thread_diameter**2 - self.bolt_hole_diameter**2) / 4 # Sb		
		self.nut_active_area = 3.14 * (self.nut_minimum_diameter**2 - self.nominal_thread_diameter**2) / 4 # Sn

		# Calculation stress permis
		self.bolt_tension_stress_permis = self.bolt_yield_strength / self.k_industry # [G]рб		
		self.nut_tension_stress_permis = self.nut_yield_strength / self.k_industry #[G]рг		
		self.bolt_crush_stress_permis = 0.8 * self.bolt_tension_stress_permis # [G]смб		
		self.nut_crush_stress_permis = 0.8 * self.nut_tension_stress_permis # [G]смг		
		self.bolt_shear_stress_permis = 0.3 * self.bolt_tension_stress_permis # [т]смб		
		self.nut_shear_stress_permis = 0.3 * self.nut_tension_stress_permis # [т]смг

		# Calculation of effective stresses		 
		self.bolt_tension_stress = self.axial_force / self.bolt_active_area # [G]рб		
		self.nut_tension_stress = self.axial_force / self.nut_active_area # [G]рг		 
		self.bolt_crush_stress = (self.axial_force /
			(3.14 * self.midle_thread_diameter * self.height_coil * self.work_threads)) # [G]смб		 
		self.nut_crush_stress = self.bolt_crush_stress # [G]смг		 
		self.bolt_shear_stress = (self.axial_force / 
			(3.14 * self.internal_thread_diameter * self.k_thread * self.work_threads * self.thread_pitch)) # [т]смб		 
		self.nut_shear_stress = self.bolt_shear_stress # [т]смг

		# Calculation of the safety factor		
		self.k_bolt_tension = round((self.bolt_tension_stress_permis / self.bolt_tension_stress),1) # [G]рб		
		self.k_nut_tension = round((self.nut_tension_stress_permis / self.nut_tension_stress),1) # [G]рг		  
		self.k_bolt_crush = round((self.bolt_crush_stress_permis / self.bolt_crush_stress),1) # [G]смб		
		self.k_nut_crush = round((self.nut_crush_stress_permis / self.nut_crush_stress),1) # [G]смг		
		self.k_bolt_shear = round((self.bolt_shear_stress_permis / self.bolt_shear_stress),1) # [т]смб		 
		self.k_nut_shear = round((self.nut_shear_stress_permis / self.nut_shear_stress),1) # [т]смг
