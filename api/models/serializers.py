from rest_framework import serializers
from api.models.customer import Customer, Address
from api.models.cloth import Cloth
from api.models.pincode import Pincode
from api.models.order import Order, ReferenceImage, Measurement
from rest_framework.validators import ValidationError, UniqueValidator


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        app_label = 'Customer'
        fields = '__all__'
        # exclude = [
        #     'otp'
        # ]
        # fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'mobile_number': {
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
                ],
                # 'otp': {'write_only': True},
            }
        }

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ['id', 'name', 'description', 'image',
                  'material', 'color', 'pricePermeter']
        depth = 1

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class ReferenceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceImage
        fields = '__all__'


class OrderGetSerializer(serializers.ModelSerializer):
    cloth = ClothSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__' 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        print('instance', instance.measurementId)
        images = ReferenceImage.objects.filter(orderId=instance.id).values()
        response['reference'] = images
        
        if(instance.measurementId):
            measurements = Measurement.objects.filter(id=str(instance.measurementId)).values()
            response['measurements'] = measurements[0]['value']
            response['measurement_for'] = measurements[0]['measurement_for']
        
        if(instance.cloth_pickuplocation):
            res = Address.objects.filter(id=str(instance.cloth_pickuplocation)).values()
            response['cloth_pickuplocation'] = res[0]
        
        if(instance.measurementAddress):
            res = Address.objects.filter(id=str(instance.measurementAddress)).values()
            response['measurementAddress'] = res[0]
        
        if(instance.deliveryAddress):
            res = Address.objects.filter(id=str(instance.deliveryAddress)).values()
            response['deliveryAddress'] = res[0]

        return response

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields = '__all__'