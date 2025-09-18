import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Displays the embedding of a randomly selected movie."

    def handle(self, *args, **kwargs):
        # 1. Selecciona una película al azar que tenga un embedding guardado.
        # Usamos filter(emb__isnull=False) para asegurarnos de no elegir una sin embedding.
        random_movie = Movie.objects.filter(emb__isnull=False).order_by('?').first()

        if not random_movie:
            self.stderr.write(self.style.ERROR("No se encontraron películas con embeddings en la base de datos."))
            return

        self.stdout.write(self.style.SUCCESS(f"🎬 Película seleccionada al azar: '{random_movie.title}'"))

        # 2. Recupera el embedding guardado en formato binario.
        embedding_bytes = random_movie.emb

        # 3. Convierte los bytes de nuevo a un array de NumPy.
        # Es crucial usar el mismo dtype (np.float32) que se usó al guardar.
        embedding_array = np.frombuffer(embedding_bytes, dtype=np.float32)

        # 4. Muestra el embedding en la consola.
        self.stdout.write("✨ Vector del Embedding:")
        self.stdout.write(str(embedding_array))
        self.stdout.write(f"\nDimensiones del vector: {embedding_array.shape}")