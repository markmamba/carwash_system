from rest_framework import serializers
from users.models.users import User  # Ensure this points to your User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'user_type', 'phone_number', 'address', 'plate_no']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Create the user instance without saving it to the database yet
        user = User(**validated_data)
        # Hash the password
        user.set_password(validated_data['password'])
        # Now save the user to the database
        user.save()
        return user



