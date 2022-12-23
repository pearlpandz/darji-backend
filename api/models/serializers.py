from rest_framework import serializers
from api.models.customer import Customer
from api.models.cloth import Cloth
from api.models.order import Order, ReferenceImage
from rest_framework.validators import ValidationError, UniqueValidator


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        app_label = 'Customer'
        fields = '__all__'
        # fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'mobileNumber': {
                'validators': [
                    UniqueValidator(
                        queryset=Customer.objects.all(),
                        message="mobile number already exist",
                    )
                ]
            },
            'email': {
                "required": "email is required",
                'validators': [
                    UniqueValidator(
                        queryset=Customer.objects.all(),
                        message="email already exist",
                    )
                ]
            }
        }

    def create(self, validated_data):
        provider = validated_data.get('provider', None)
        instance = self.Meta.model(**validated_data)
        if provider is not 'oauth':
            password = validated_data.pop('password', None)

            if password is not None:
                instance.set_password(password)
            instance.save()
        return instance


class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ['id', 'name', 'description', 'image',
                  'material', 'color', 'pricePermeter']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ReferenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceImage
        fields = '__all__'
