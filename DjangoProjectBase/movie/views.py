from django.shortcuts import render, redirect
from .models import Movie
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

# Cargar la API Key desde el archivo .env en la raíz del proyecto
django_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(django_project_root, '..', 'openAI.env')
load_dotenv(dotenv_path=env_path)
client = OpenAI(api_key=os.environ.get("openai_apikey"))

# Función para calcular similitud de coseno
def cosine_similarity(a, b):
    """Calculates the cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def home(request):
    return redirect('movie:recommend')

def about(request):
    return render(request, 'movie/about.html')

def signup(request):
    return render(request, 'movie/signup.html')

def statistics_view(request):
    total_movies = Movie.objects.count()
    movies_with_embeddings = Movie.objects.filter(emb__isnull=False).count()
    context = {
        'total_movies': total_movies,
        'movies_with_embeddings': movies_with_embeddings,
    }
    return render(request, 'movie/statistics.html', context)

def recommend_view(request):
    """
    View para la página de recomendación de películas.
    - Muestra un formulario en una petición GET.
    - Procesa el prompt del usuario en una petición POST, encuentra la película más similar
      y la muestra.
    """
    best_movie = None
    prompt = ""
    error_message = None

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        if prompt:
            try:
                # 1. Generar embedding del prompt del usuario
                response = client.embeddings.create(
                    input=[prompt],
                    model="text-embedding-3-small"
                )
                prompt_emb = np.array(response.data[0].embedding, dtype=np.float32)

                # 2. Recorrer la base de datos y comparar
                max_similarity = -1
                movies_with_embeddings = Movie.objects.filter(emb__isnull=False)
                
                if not movies_with_embeddings.exists():
                    error_message = "No hay películas con embeddings en la base de datos para comparar."
                else:
                    for movie in movies_with_embeddings:
                        movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
                        similarity = cosine_similarity(prompt_emb, movie_emb)

                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_movie = movie
            except Exception as e:
                error_message = f"Ocurrió un error al procesar tu solicitud: {e}"
        else:
            error_message = "Por favor, ingresa una descripción."

    context = {
        'best_movie': best_movie,
        'prompt': prompt,
        'error_message': error_message,
    }
    return render(request, 'movie/recommend.html', context)