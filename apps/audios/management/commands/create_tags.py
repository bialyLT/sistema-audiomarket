from django.core.management.base import BaseCommand
from apps.audios.models import Tag


class Command(BaseCommand):
    help = 'Crea tags iniciales para el marketplace de audios'

    def handle(self, *args, **options):
        # Tags generales
        tags_data = [
            # Estado de ánimo
            'Alegre', 'Triste', 'Energético', 'Relajante', 'Dramático',
            'Romántico', 'Misterioso', 'Épico', 'Nostálgico', 'Inspirador',
            
            # Tempo
            'Lento', 'Moderado', 'Rápido', 'Variable',
            
            # Instrumentos principales
            'Piano', 'Guitarra', 'Batería', 'Violín', 'Bajo', 'Saxofón',
            'Trompeta', 'Flauta', 'Sintetizador', 'Cuerdas', 'Vientos',
            
            # Uso recomendado
            'Comercial', 'Video', 'Podcast', 'Juego', 'Documental',
            'Corporativo', 'Presentación', 'Fondo', 'Intro', 'Outro',
            'Transición', 'Logo', 'Publicidad', 'YouTube', 'Instagram',
            
            # Características técnicas
            'Loop', 'Sin Copyright', 'Original', 'Remix', 'Cover',
            'Instrumental', 'Vocal', 'Acapella', 'Solo', 'Ensemble',
            
            # Géneros adicionales
            'Acústico', 'Electrónico', 'Orgánico', 'Experimental',
            'Minimalista', 'Orquestal', 'Urbano', 'Folclórico',
            
            # Calidad
            'HD', 'Estéreo', 'Mono', '24bit', '32bit', '44kHz', '48kHz',
            
            # Duración aproximada
            'Corto', 'Medio', 'Largo', 'Extended'
        ]

        created_count = 0
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_count += 1
                self.stdout.write(f'Tag creado: {tag.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Proceso completado. Tags creados: {created_count}/{len(tags_data)}'
            )
        )
