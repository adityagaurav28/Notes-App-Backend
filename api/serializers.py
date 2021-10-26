from rest_framework.serializers import ModelSerializer
from . import models

class NoteSerializer(ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'