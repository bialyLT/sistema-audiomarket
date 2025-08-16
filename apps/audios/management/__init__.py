from django.core.management.base import BaseCommand
from apps.audios.models import Category, Genre, Tag


class Command(BaseCommand):
    help = 'Crea categorías, géneros y tags iniciales para el marketplace de audios'

    def handle(self, *args, **options):
        # Crear categorías
        categories_data = [
            {
                'name': 'Música', 
                'description': 'Pistas musicales de todos los géneros',
                'icon': 'fas fa-music'
            },
            {
                'name': 'Efectos de Sonido', 
                'description': 'Efectos sonoros para producciones audiovisuales',
                'icon': 'fas fa-volume-up'
            },
            {
                'name': 'Loops e Instrumentales', 
                'description': 'Loops musicales y pistas instrumentales',
                'icon': 'fas fa-repeat'
            },
            {
                'name': 'Podcasts', 
                'description': 'Contenido hablado y podcasts',
                'icon': 'fas fa-microphone'
            },
            {
                'name': 'Audiolibros', 
                'description': 'Libros narrados y contenido educativo',
                'icon': 'fas fa-book-open'
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Categoría creada: {category.name}')
                )

        # Crear géneros para música
        musica_category = Category.objects.get(name='Música')
        musica_genres = [
            'Rock', 'Pop', 'Jazz', 'Blues', 'Hip-Hop', 'Rap', 'Reggae',
            'Country', 'Folk', 'Electronic', 'House', 'Techno', 'Ambient',
            'Classical', 'Opera', 'Symphony', 'R&B', 'Soul', 'Funk',
            'Disco', 'Punk', 'Metal', 'Alternative', 'Indie', 'Grunge'
        ]

        for genre_name in musica_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                category=musica_category,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Género musical creado: {genre_name}')

        # Crear géneros para efectos de sonido
        fx_category = Category.objects.get(name='Efectos de Sonido')
        fx_genres = [
            'Naturaleza', 'Animales', 'Transporte', 'Urbano', 'Industrial',
            'Sci-Fi', 'Terror', 'Ambiente', 'Impactos', 'Transiciones'
        ]

        for genre_name in fx_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                category=fx_category,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Género FX creado: {genre_name}')

        # Crear géneros para loops
        loops_category = Category.objects.get(name='Loops e Instrumentales')
        loops_genres = [
            'Drum Loops', 'Bass Lines', 'Guitar Riffs', 'Piano', 'Strings',
            'Brass', 'Percussion', 'Vocal Samples', 'Synthesizer'
        ]

        for genre_name in loops_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                category=loops_category,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Género de loops creado: {genre_name}')

        # Crear géneros para podcasts
        podcast_category = Category.objects.get(name='Podcasts')
        podcast_genres = [
            'Educativo', 'Entretenimiento', 'Noticias', 'Deportes',
            'Tecnología', 'Salud', 'Negocios', 'Historia', 'Ciencia'
        ]

        for genre_name in podcast_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                category=podcast_category,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Género podcast creado: {genre_name}')

        # Crear géneros para audiolibros
        audiobook_category = Category.objects.get(name='Audiolibros')
        audiobook_genres = [
            'Ficción', 'No Ficción', 'Romance', 'Misterio', 'Fantasía',
            'Biografía', 'Autoayuda', 'Historia', 'Infantil', 'Juvenil'
        ]

        for genre_name in audiobook_genres:
            genre, created = Genre.objects.get_or_create(
                name=genre_name,
                category=audiobook_category,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Género audiolibro creado: {genre_name}')

        # Crear tags populares
        tags_data = [
            {'name': 'Energético', 'color': '#FF6B35'},
            {'name': 'Relajante', 'color': '#4ECDC4'},
            {'name': 'Romántico', 'color': '#FF69B4'},
            {'name': 'Épico', 'color': '#8B5CF6'},
            {'name': 'Motivacional', 'color': '#F59E0B'},
            {'name': 'Melancólico', 'color': '#6B7280'},
            {'name': 'Festivo', 'color': '#EF4444'},
            {'name': 'Misterioso', 'color': '#374151'},
            {'name': 'Nostálgico', 'color': '#84CC16'},
            {'name': 'Experimental', 'color': '#06B6D4'},
            {'name': 'Comercial', 'color': '#3B82F6'},
            {'name': 'Cinematográfico', 'color': '#7C3AED'},
            {'name': 'Minimalista', 'color': '#10B981'},
            {'name': 'Vintage', 'color': '#D97706'},
            {'name': 'Futurista', 'color': '#EC4899'},
        ]

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            if created:
                self.stdout.write(f'Tag creado: {tag.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Datos iniciales creados exitosamente!\n'
                f'Categorías: {Category.objects.count()}\n'
                f'Géneros: {Genre.objects.count()}\n'
                f'Tags: {Tag.objects.count()}'
            )
        )
