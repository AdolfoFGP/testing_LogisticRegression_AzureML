from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def reverse(request):
    user_text = request.GET['usertext']
    reversed_text = user_text[::-1]

    lista_text = user_text.split()
    num_caract = len(lista_text)

    return render(request, 'reverse.html', {'usertext':user_text,
                                            'reversedtext':reversed_text,
                                            'numcaract':num_caract})