import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JUSOR.settings')
django.setup()

from django.apps import apps

def clear_database():
    # Get all models
    all_models = apps.get_models()

    for model in all_models:
        # Delete all instances of the model
        model.objects.all().delete()
        print(f"Deleted all instances of {model.__name__}")

if __name__ == "__main__":
    clear_database()
    print("All data has been deleted.")