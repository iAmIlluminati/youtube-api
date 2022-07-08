from rest_framework.serializers import ModelSerializer
from .models import Keys, FetchedData


class KeysSerializer(ModelSerializer):
    class Meta:
        model = Keys
        fields = '__all__'
        
class FetchedDataSerializer(ModelSerializer):
    class Meta:
        model = FetchedData
        fields = '__all__'