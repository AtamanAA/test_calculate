from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PipePressureThickness(forms.Form):
	"""Форма ввода данных для расчета толщины стенки трубы высокого давления"""
	yield_strength = forms.FloatField(label = "Межа текучості матеріалу", min_value=1, max_value = 3000, initial = 300)
	test_pressure = forms.FloatField(label = "Розрахунковий тиск (p)", min_value=0.001, max_value = 3000,)
	min_outside_diameter = forms.FloatField(label = "Зовнішній діаметр (D)", min_value=1, max_value = 10000,)	
	k_industry = forms.FloatField(label = "Заданний коєфіциент запасу", min_value=1, max_value = 10, initial = 1.3)
	k_cycle = forms.FloatField(label = "Коефіцієнт запасу на витривалість", min_value=1, max_value = 10, initial = 1)
		
	k_welding_choice = (
		(1, 'Безшовна'),
		(0.6, 'Електрозварювальна'),
		)
	k_welding = forms.ChoiceField(label = "Вид труби", choices=k_welding_choice,
									widget=forms.Select(attrs={"class": "selector"}))



class ThreadForm(forms.Form):
	"""Форма ввода данных для прочностного расчета резьбового соединения"""
	axial_force = forms.FloatField(label = "Осьове навантаження (F)", min_value=0.001, max_value = 1000, help_text = "кН ")
	bolt_yield_strength = forms.FloatField(label = "Межа текучості болта", min_value=1, max_value = 3000, initial = 300, help_text = "МПа")
	nut_yield_strength = forms.FloatField(label = "Межа текучесті гайки", min_value=1, max_value = 3000, initial = 300, help_text = "МПа")
	nominal_thread_diameter = forms.FloatField(label = "Діаметр різьби (M)", min_value=1, max_value = 1000, help_text = "мм")
	thread_pitch = forms.FloatField(label = "Шаг різьби", min_value=0.25, max_value = 20, help_text = "мм")
	nut_active_height = forms.FloatField(label = "Висота гайки (L)", min_value=1, max_value = 1000, help_text = "мм")
	nut_minimum_diameter = forms.FloatField(label = "Зовнішній діаметр гайки (Dг)", min_value=2, max_value = 1500, help_text = "мм")
	bolt_hole_diameter = forms.FloatField(label = "Діаметр отвору в болті (Dо)", min_value=0, max_value = 990, initial = 0, help_text = "мм")
	k_industry = forms.FloatField(label = "Заданний коєфіциент запасу", min_value=1, max_value = 10, initial = 1.3)

	k_thread_choice = (
		(0.8, 'Метрична'),
		(0.65, 'Трапецевидна'),
		(0.5, 'Прямокутна'),
		)
	k_thread = forms.ChoiceField(label = "Тип профіля різьби", choices=k_thread_choice,
									widget=forms.Select(attrs={"class": "selector"}))

	def clean_bolt_hole_diameter(self):
		"""Валидатор для диаметра отверстия в болте"""
		nominal_thread_diameter = self.cleaned_data['nominal_thread_diameter']
		bolt_hole_diameter = self.cleaned_data['bolt_hole_diameter']
		thread_pitch = self.cleaned_data['thread_pitch']
		max_bolt_hole_diameter = nominal_thread_diameter - 2 * thread_pitch
		
		if bolt_hole_diameter > max_bolt_hole_diameter:
			raise ValidationError('Діаметр отвору в болті більше діаметра по западинах різьби')
		
		return bolt_hole_diameter


	def clean_nut_minimum_diameter(self):
		"""Валидатор для диаметра гайки"""
		nut_minimum_diameter = self.cleaned_data['nut_minimum_diameter']
		nominal_thread_diameter = self.cleaned_data['nominal_thread_diameter']		
		thread_pitch = self.cleaned_data['thread_pitch']
		min_permis_nut_diameter = nominal_thread_diameter + 2 * thread_pitch
				
		if nut_minimum_diameter < min_permis_nut_diameter:
			raise ValidationError('Зовнішній діаметр гайки менше діаметра різьби')
		
		return nut_minimum_diameter


# def validate_even(value):
# 	"""Пример функции валидации четного числа"""
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is not an even number'),
#             params={'value': value},
#         )

class SumPostForm(forms.Form):
	"""Форма для отладки и тестов"""
	#first_number = forms.CharField(max_length=255, label = "Первое число")
	#second_number = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label = "Второе число", required = False)
	#first_number = forms.DecimalField(label = "Первое число", max_value = 500, decimal_places = 3)
	# first_number = forms.FloatField(label = "Первое число", max_value = 50, help_text = "text_2")
	# second_number = forms.FloatField(label = "Второе число", max_value = 50)
	# name = forms.CharField(error_messages={'required': 'Please enter your name'})
	# os_choice = (
	# 	('Win10', 'Win10'),
	# 	('Win8', 'Win8'),
	# 	('Win7', 'Win7'),
	# 	)
	#operating_system = forms.CharField(blank = True, null = True, choices=os_choice)
	# a = []
	# test_list = forms.ChoiceField(label = "Тестовый список", choices=os_choice, widget=forms.Select(attrs={"class": "selector"}))
	# test_list_2 = forms.MultipleChoiceField(choices=os_choice)

	# name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
	# 						"placeholder": "Recipe name"}))

	# #even_field = forms.IntegerField(validators=[validate_even])

	# def clean_second_number(self):
	# 	first_number = self.cleaned_data['first_number']
	# 	second_number = self.cleaned_data['second_number']
	# 	if second_number > first_number:
	# 		raise ValidationError('Второе число не должно быть больше первого')
	# 	return second_number

