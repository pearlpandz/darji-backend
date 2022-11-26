from rest_framework import serializers
from api.models.customer import Customer
from api.models.cloth import Cloth

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        app_label = 'Customer'
        fields = '__all__'
        # fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ['id', 'name','description', 'image','material','color','pricePermeter']