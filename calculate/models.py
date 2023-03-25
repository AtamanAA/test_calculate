from django.db import models
from django.contrib.auth.models import User
from .services import Thread


class PipeHighPressure(models.Model):
    K_WELDING_CHOICES = [
		(1, 'Безшовна'),
		(0.6, 'Електрозварювальна'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, max_length=128)
    yield_strength = models.FloatField(default=300)
    test_pressure = models.FloatField()
    min_outside_diameter = models.FloatField()	
    k_industry = models.FloatField(default=1.3)
    k_cycle = models.FloatField(default=1)
    k_welding = models.FloatField(max_length=40, choices=K_WELDING_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def thickness(self):	
        self.allowable_stresses = self.yield_strength / (self.k_industry * self.k_cycle)
        self.thickness_pipe = (self.test_pressure * self.min_outside_diameter /
                    (2 * self.allowable_stresses * float(self.k_welding) + self.test_pressure))
        self.thickness_round = round(self.thickness_pipe, 2)
        return self.thickness_round

    @property
    def outside_radius(self): 
        return self.min_outside_diameter / 2

    def __str__(self):
        return f"Pipe {self.name} with thickness: {self.thickness}"

    def __repr__(self):
        return f"Pipe High Pressure (id={self.id})"

    @staticmethod
    def get_by_id(pipe_id):
        return PipeHighPressure.objects.get(id=pipe_id) if PipeHighPressure.objects.filter(id=pipe_id) else None

    @staticmethod
    def get_by_user(user_id):
        return PipeHighPressure.objects.filter(user=user_id)
    
    @staticmethod
    def get_by_user_order_by_created(user_id):
        return PipeHighPressure.objects.filter(user=user_id).order_by('created_at',).reverse()

    @staticmethod
    def get_all():
        return list(PipeHighPressure.objects.all())

    @staticmethod
    def calculate(yield_strength, test_pressure, min_outside_diameter, k_industry, k_cycle, k_welding):
        pipe = PipeHighPressure()        
        pipe.yield_strength = yield_strength
        pipe.test_pressure = test_pressure
        pipe.min_outside_diameter = min_outside_diameter
        pipe.k_industry = k_industry
        pipe.k_cycle = k_cycle
        pipe.k_welding = k_welding
        return pipe

    @staticmethod
    def create(user, yield_strength, test_pressure, min_outside_diameter, k_industry, k_cycle, k_welding, 
                name="noname", description = "nodescr"):
        pipe = PipeHighPressure().calculate(yield_strength, test_pressure, min_outside_diameter, 
                                            k_industry, k_cycle, k_welding)
        pipe.user = user
        pipe.name = name
        pipe.description = description
        if pipe.thickness < pipe.outside_radius:
            pipe.save()
            return True
        else:
            return False

    @staticmethod
    def delete_by_id(pipe_id):
        try:
            pipe = PipeHighPressure.objects.get(pk=pipe_id)
            pipe.delete()
            return True
        except:
            return False        

    def update(self, yield_strength=None, test_pressure=None, min_outside_diameter=None, 
                k_industry=None, k_cycle=None, k_welding=None, name=None, description=None):
        if yield_strength:
            self.yield_strength = yield_strength
        if test_pressure:
            self.test_pressure = test_pressure
        if min_outside_diameter:
            self.min_outside_diameter = min_outside_diameter
        if k_industry:
            self.k_industry = k_industry
        if k_cycle:
            self.k_cycle = k_cycle
        if k_welding:
            self.k_welding = k_welding
        if name:
            self.name = name
        if description:
            self.description = description
        if self.thickness < self.outside_radius:
            self.save()
            return True
        else:
            return False

    def to_dict(self):
        pipe_dict = {"id": self.id,
                    "user": self.user,
                    "name": self.name,
                    "description": self.description,
                    "yield_strength": self.yield_strength,
                    "test_pressure": self.test_pressure,
                    "min_outside_diameter": self.min_outside_diameter,
                    "k_industry": self.k_industry,
                    "k_cycle": self.k_cycle,
                    "k_welding": self.k_welding,
                    "created_at": self.created_at,
                    "thickness": self.thickness,
                    }
        return pipe_dict


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)    
    type = models.CharField(max_length=40)
    condition = models.CharField(max_length=40, blank=True,)
    hardness = models.FloatField(help_text="HB")
    yield_strenght = models.FloatField(help_text="МПа")

    def __str__(self):
        return f"{self.name} {self.type} {self.condition}"

    def __repr__(self):
        return f"Material(id={self.pk})"

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all materials
        """
        return list(Material.objects.all())


class ThreadConnection(models.Model):
    K_THREAD_CHOICES = [
		(0.8, 'Метрична'),
		(0.65, 'Трапецевидна'),
        (0.5, 'Прямокутна'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, max_length=128)
    axial_force = models.FloatField()
    bolt_yield_strength = models.FloatField(default=300)
    nut_yield_strength = models.FloatField(default=300)
    nominal_thread_diameter = models.FloatField()
    thread_pitch = models.FloatField()
    nut_active_height = models.FloatField()
    nut_minimum_diameter = models.FloatField()
    bolt_hole_diameter = models.FloatField()
    k_industry = models.FloatField()
    k_thread = models.FloatField(max_length=40, choices=K_THREAD_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread {self.name} {self.nominal_thread_diameter} x {self.thread_pitch}"

    def __repr__(self):
        return f"Thread (id={self.id})"

    @property
    def __thread(self):
        object = Thread(self.axial_force, self.bolt_yield_strength, self.nut_yield_strength, 
                        self.nominal_thread_diameter, self.thread_pitch, self.nut_active_height, 
                        self.nut_minimum_diameter, self.bolt_hole_diameter, self.k_industry, self.k_thread)
        return object

    @property    
    def k_bolt_tension(self): 	
        return self.__thread.k_bolt_tension

    @property    
    def k_nut_tension(self): 	
        return self.__thread.k_nut_tension
    
    @property    
    def k_bolt_crush(self): 	
        return self.__thread.k_bolt_crush

    @property    
    def k_nut_crush(self): 	
        return self.__thread.k_nut_crush

    @property    
    def k_bolt_shear(self): 	
        return self.__thread.k_bolt_shear

    @property    
    def k_nut_shear(self): 	
        return self.__thread.k_nut_shear
    
    @property    
    def k_min(self):
        k_min = min(self.k_bolt_tension, self.k_nut_tension, self.k_bolt_crush, self.k_nut_crush, self.k_bolt_shear, self.k_nut_shear)	
        return k_min

    @staticmethod
    def get_by_id(thread_id):
        return ThreadConnection.objects.get(id=thread_id) if ThreadConnection.objects.filter(id=thread_id) else None

    @staticmethod
    def get_by_user(user_id):
        return ThreadConnection.objects.filter(user=user_id)
    
    @staticmethod
    def get_by_user_order_by_created(user_id):
        return ThreadConnection.objects.filter(user=user_id).order_by('created_at',).reverse()

    @staticmethod
    def get_all():
        return list(ThreadConnection.objects.all())

    @staticmethod
    def calculate(axial_force, bolt_yield_strength, nut_yield_strength, nominal_thread_diameter, thread_pitch, 
                    nut_active_height, nut_minimum_diameter, bolt_hole_diameter, k_industry, k_thread):        
        thread = ThreadConnection()        
        thread.axial_force = axial_force
        thread.bolt_yield_strength = bolt_yield_strength
        thread.nut_yield_strength = nut_yield_strength
        thread.nominal_thread_diameter = nominal_thread_diameter
        thread.thread_pitch = thread_pitch
        thread.nut_active_height = nut_active_height
        thread.nut_minimum_diameter = nut_minimum_diameter
        thread.bolt_hole_diameter = bolt_hole_diameter
        thread.k_industry = k_industry
        thread.k_thread = k_thread
        return thread

    @staticmethod
    def create(user, axial_force, bolt_yield_strength, nut_yield_strength, nominal_thread_diameter, thread_pitch, 
                nut_active_height, nut_minimum_diameter, bolt_hole_diameter, k_industry, k_thread, 
                name="noname", description = "nodescr"):
        thread = ThreadConnection().calculate(axial_force, bolt_yield_strength, nut_yield_strength, nominal_thread_diameter, 
                                                thread_pitch, nut_active_height, nut_minimum_diameter, bolt_hole_diameter, 
                                                k_industry, k_thread)
        thread.user = user
        thread.name = name
        thread.description = description

        max_bolt_hole_diameter = thread.nominal_thread_diameter - 2 * thread.thread_pitch
		
        if thread.bolt_hole_diameter <= max_bolt_hole_diameter:
            thread.save()
            return True
        else:
            return False

    @staticmethod
    def delete_by_id(thread_id):
        try:
            thread = ThreadConnection.objects.get(pk=thread_id)
            thread.delete()
            return True
        except:
            return False

    def update(self, axial_force=None, bolt_yield_strength=None, nut_yield_strength=None, 
                    nominal_thread_diameter=None, thread_pitch=None, nut_active_height=None, 
                    nut_minimum_diameter=None, bolt_hole_diameter=None, k_industry=None, k_thread=None,
                    name=None, description=None):
        if axial_force:
            self.axial_force = axial_force
        if bolt_yield_strength:
            self.bolt_yield_strength = bolt_yield_strength
        if nut_yield_strength:
            self.nut_yield_strength = nut_yield_strength
        if nominal_thread_diameter:
            self.nominal_thread_diameter = nominal_thread_diameter
        if thread_pitch:
            self.thread_pitch = thread_pitch
        if nut_active_height:
            self.nut_active_height = nut_active_height
        if nut_minimum_diameter:
            self.nut_minimum_diameter = nut_minimum_diameter
        if bolt_hole_diameter:
            self.bolt_hole_diameter = bolt_hole_diameter
        if k_industry:
            self.k_industry = k_industry
        if k_thread:
            self.k_thread = k_thread
        if name:
            self.name = name
        if description:
            self.description = description
        max_bolt_hole_diameter = self.nominal_thread_diameter - 2 * self.thread_pitch
        if self.bolt_hole_diameter <= max_bolt_hole_diameter:
            self.save()
            return True
        else:
            return False

    def to_dict(self):
        thread_dict = {"id": self.id,
                    "user": self.user,
                    "name": self.name,
                    "description": self.description,
                    "axial_force": self.axial_force,
                    "bolt_yield_strength": self.bolt_yield_strength,
                    "nut_yield_strength": self.nut_yield_strength,
                    "nominal_thread_diameter": self.nominal_thread_diameter,
                    "thread_pitch": self.thread_pitch,
                    "nut_active_height": self.nut_active_height,
                    "nut_minimum_diameter": self.nut_minimum_diameter,
                    "bolt_hole_diameter": self.bolt_hole_diameter,
                    "k_industry": self.k_industry,
                    "k_thread": self.k_thread,
                    "created_at": self.created_at,
                    "k_bolt_tension": self.k_bolt_tension,
                    "k_nut_tension": self.k_nut_tension,
                    "k_bolt_crush": self.k_bolt_crush,
                    "k_nut_crush": self.k_nut_crush,
                    "k_bolt_shear": self.k_bolt_shear,
                    "k_nut_shear": self.k_nut_shear,
                    }
        return thread_dict