from django.shortcuts import render

# Create your views here.

def instructions(request):
    """Instructions list"""
    return render(request, "instructions/instructions_index.html")


def pipe_pressure(request):
    """Pipe pressure instruction"""
    return render(request, "instructions/pipe_pressure_instruction.html")