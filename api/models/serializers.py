from rest_framework import serializers
from api.models.customer import Customer
from api.models.company import Company
from api.models.category import Category
from api.models.property import Property

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name','description', 'logo', 'banner', 'isVerified']

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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','description', 'icon']

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        # fields = "__all__"
        exclude = ['category']