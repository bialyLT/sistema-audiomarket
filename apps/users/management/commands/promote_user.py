from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User, UserType


class Command(BaseCommand):
    help = 'Promover un usuario a administrador'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email del usuario a promover')
        parser.add_argument(
            '--demote',
            action='store_true',
            help='Degradar a comprador en lugar de promover a admin',
        )

    def handle(self, *args, **options):
        email = options['email']
        demote = options['demote']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f'No existe un usuario con el email "{email}"')
        
        if demote:
            # Degradar a comprador
            if user.user_type == UserType.ADMIN:
                user.user_type = UserType.BUYER
                user.is_staff = False
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Usuario "{user.get_full_name()}" degradado a comprador exitosamente.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'El usuario "{user.get_full_name()}" no es administrador.'
                    )
                )
        else:
            # Promover a administrador
            if user.user_type != UserType.ADMIN:
                user.user_type = UserType.ADMIN
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Usuario "{user.get_full_name()}" promovido a administrador exitosamente.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'El usuario "{user.get_full_name()}" ya es administrador.'
                    )
                )
        
        # Mostrar información del usuario
        self.stdout.write(f'\nInformación del usuario:')
        self.stdout.write(f'- Nombre: {user.get_full_name()}')
        self.stdout.write(f'- Email: {user.email}')
        self.stdout.write(f'- Tipo: {user.get_user_type_display()}')
        self.stdout.write(f'- Staff: {user.is_staff}')
        self.stdout.write(f'- Superuser: {user.is_superuser}')
