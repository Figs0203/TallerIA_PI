import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie

class Command(BaseCommand):
    help = "Finds corresponding images in the media folder and updates the movie's image field."

    def handle(self, *args, **kwargs):
        # 📂 Directorio base donde se encuentran las imágenes.
        # Django busca dentro de la carpeta definida en MEDIA_ROOT.
        image_folder_path = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')
        
        if not os.path.isdir(image_folder_path):
            self.stderr.write(self.style.ERROR(f"Image directory not found: {image_folder_path}"))
            return

        self.stdout.write("Starting to update movie images...")

        movies_to_update = []
        updated_count = 0
        not_found_count = 0

        # 🎬 Obtenemos todas las películas de la base de datos
        all_movies = Movie.objects.all()

        for movie in all_movies:
            # 🖼️ Construimos el nombre esperado para el archivo de imagen (ej: 'Inception.jpg')
            # NOTA: Asumimos que el archivo se llama exactamente como el título con extensión .jpg.
            # Si tus archivos tienen otro formato (ej: 'inception.jpg'), deberás ajustar esta lógica.
            expected_image_name = f"m_{movie.title}.png"
            
            # Ruta completa en el sistema de archivos para verificar si existe
            full_image_path = os.path.join(image_folder_path, expected_image_name)

            # Ruta relativa que se guardará en la base de datos (ej: 'movie/images/Inception.jpg')
            db_image_path = os.path.join('movie/images', expected_image_name)

            if os.path.exists(full_image_path):
                # Si la imagen existe, actualizamos el campo 'image' del objeto movie en memoria
                movie.image = db_image_path
                movies_to_update.append(movie)
                self.stdout.write(self.style.SUCCESS(f"Found image for '{movie.title}'"))
            else:
                # Si no existe, lo reportamos
                not_found_count += 1
                self.stdout.write(self.style.WARNING(f"Image not found for '{movie.title}' (expected: {expected_image_name})"))

        # 🚀 Actualizamos todas las películas en una sola consulta para mayor eficiencia
        if movies_to_update:
            updated_count = len(movies_to_update)
            Movie.objects.bulk_update(movies_to_update, ['image'])
            self.stdout.write(self.style.SUCCESS(f"\nSuccessfully updated {updated_count} movie images in the database."))
        
        if not_found_count > 0:
            self.stdout.write(self.style.WARNING(f"{not_found_count} images were not found."))