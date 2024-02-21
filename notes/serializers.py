from rest_framework.serializers import ModelSerializer
from notes.models import Note
from rest_framework import serializers
from users.serializers import UserSerializer

class NoteSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        note = Note.objects.create(**validated_data, user=self.context['request'].user)
        return note

