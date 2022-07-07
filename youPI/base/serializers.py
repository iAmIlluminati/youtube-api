from rest_framework.serializers import ModelSerializer
from .models import Keys, FetchData


class KeysSerializer(ModelSerializer):
    class Meta:
        model = Keys
        fields = '__all__'
        
class FetchDataSerializer(ModelSerializer):
    class Meta:
        model = FetchData
        fields = '__all__'