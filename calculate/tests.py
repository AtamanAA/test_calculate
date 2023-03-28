from django.test import TestCase
from .thread import Thread
from .models import PipeHighPressure


class PipeThicknessTest(TestCase):
    def test_thickness_k_1(self):
        expected = 0.82        
        actual = PipeHighPressure.calculate(yield_strength=300, test_pressure=10, min_outside_diameter=50,
                                k_industry=1, k_cycle=1, k_welding=1).thickness
        self.assertEqual(actual, expected)
    
    def test_thickness_k_industry(self):
        expected = 1.61
        actual = PipeHighPressure.calculate(yield_strength=300, test_pressure=10, min_outside_diameter=50,
                                k_industry=2, k_cycle=1, k_welding=1).thickness   
        self.assertEqual(actual, expected)

    def test_thickness_k_weldind(self):
        expected = 1.02
        actual = PipeHighPressure.calculate(yield_strength=300, test_pressure=10, min_outside_diameter=50,
                                k_industry=1, k_cycle=1, k_welding=0.8).thickness      
        self.assertEqual(actual, expected)

    def test_thickness_k_cycle(self):
        expected = 1.61
        actual = PipeHighPressure.calculate(yield_strength=300, test_pressure=10, min_outside_diameter=50,
                                k_welding=1, k_industry=1, k_cycle=2).thickness       
        self.assertEqual(actual, expected)

    def test_thickness_zero_k(self):
        with self.assertRaises(ZeroDivisionError):
            PipeHighPressure.calculate(yield_strength=300, test_pressure=-10, min_outside_diameter=50,
                            k_welding=0, k_industry=0, k_cycle=0).thickness 


class ThreadTest(TestCase):
    thread = Thread(axial_force=10, bolt_yield_strength=300, nut_yield_strength=300, 
					nominal_thread_diameter=10, thread_pitch=1.5, nut_active_height=10, nut_minimum_diameter=40,
					bolt_hole_diameter = 0, k_industry = 1.3, k_thread = 0.8)

    def test_k_bolt_tension(self):
        expected = 1.3        
        actual = self.thread.k_bolt_tension
        self.assertEqual(actual, expected)

    def test_k_nut_tension(self):
        expected = 27.2        
        actual = self.thread.k_nut_tension
        self.assertEqual(actual, expected)
    
    def test_k_bolt_crush(self):
        expected = 2.8        
        actual = self.thread.k_bolt_crush
        self.assertEqual(actual, expected)

    def test_k_nut_crush(self):
        expected = 2.8        
        actual = self.thread.k_nut_crush
        self.assertEqual(actual, expected)
    
    def test_k_bolt_shear(self):
        expected = 1.5        
        actual = self.thread.k_bolt_shear
        self.assertEqual(actual, expected)

    def test_k_nut_shear(self):
        expected = 1.5        
        actual = self.thread.k_nut_shear
        self.assertEqual(actual, expected)

    def test_thread_k_industry_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Thread(axial_force=10, bolt_yield_strength=300, nut_yield_strength=300, 
					nominal_thread_diameter=10, thread_pitch=1.5, nut_active_height=10, nut_minimum_diameter=40,
					bolt_hole_diameter = 0, k_industry = 0, k_thread = 0.8)
            
