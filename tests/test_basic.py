import pytest
from django.test import TestCase


class BasicTestCase(TestCase):
    """Test básico para verificar que el proyecto funciona."""
    
    def test_basic_math(self):
        """Test básico de matemáticas."""
        self.assertEqual(2 + 2, 4)
    
    def test_string_operations(self):
        """Test básico de strings."""
        self.assertEqual("hello".upper(), "HELLO")


@pytest.mark.django_db
def test_django_setup():
    """Test para verificar que Django está configurado correctamente."""
    from django.conf import settings
    assert settings.configured
