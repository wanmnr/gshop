from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Account
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class AccountCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new Account instances.
    Handles password hashing and provides comprehensive validation.
    """
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Account
        fields = [
            'username', 'email', 'password', 'confirm_password',
            'first_name', 'last_name', 'phone_number', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_username(self, value):
        """Validate username length and uniqueness."""
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value.lower()

    def validate_email(self, value):
        """Validate email format and uniqueness."""
        return value.lower()

    def validate(self, data):
        """Validate password match and complexity."""
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        
        password = data.get('password')
        if len(password) < 8:
            raise serializers.ValidationError({
                'password': "Password must be at least 8 characters long."
            })
        
        return data

    def create(self, validated_data):
        """Create and return a new Account instance."""
        try:
            validated_data.pop('confirm_password')
            account = Account(**validated_data)
            account.set_password(validated_data['password'])
            account.save()
            return account
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}")
            raise serializers.ValidationError("Failed to create account.")

class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving Account details.
    Excludes sensitive information and includes computed fields.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'phone_number', 'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_full_name(self, obj):
        """Return the user's full name."""
        return f"{obj.first_name} {obj.last_name}".strip()

class AccountUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing Account instances.
    Handles partial updates and password changes.
    """
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'address', 'current_password',
            'new_password', 'confirm_new_password'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
        }

    def validate(self, data):
        """Validate password change if requested."""
        if 'new_password' in data or 'current_password' in data:
            if not all(key in data for key in ['current_password', 'new_password', 'confirm_new_password']):
                raise serializers.ValidationError({
                    'password': "All password fields are required for password change."
                })
            
            if not self.instance.check_password(data['current_password']):
                raise serializers.ValidationError({
                    'current_password': "Current password is incorrect."
                })
            
            if data['new_password'] != data['confirm_new_password']:
                raise serializers.ValidationError({
                    'confirm_new_password': "New passwords do not match."
                })

        return data

    def update(self, instance, validated_data):
        """Update and return an existing Account instance."""
        try:
            # Handle password change if requested
            if 'new_password' in validated_data:
                instance.set_password(validated_data['new_password'])
                # Remove password fields from validated_data
                validated_data.pop('current_password', None)
                validated_data.pop('new_password', None)
                validated_data.pop('confirm_new_password', None)

            # Update other fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
        except Exception as e:
            logger.error(f"Error updating account: {str(e)}")
            raise serializers.ValidationError("Failed to update account.")