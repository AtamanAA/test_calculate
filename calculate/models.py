from django.db import models
from django.contrib.auth.models import User


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