from .models import Address, CompanyOwner, IndividualOwner, Owner
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils.sendmail import SendEmail
from .utils.generate_pin import GeneratePin
User = get_user_model()


class AddressSerlizer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['phone_number', 'city']

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['contact']


class IndividualOwnerCreaterSerializer(serializers.ModelSerializer):
    contact = AddressSerlizer()
    username = serializers.CharField(source='user.username', required=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    
    middle_name = serializers.CharField(
        source='user.middle_name', required=False, allow_null=True, default=None)
    # password = serializers.CharField(
    #     style={"input_type": "password"}, write_only=True)

    class Meta:
        model = IndividualOwner
        fields = ['username', 'first_name', 'middle_name',
                  'last_name'] + OwnerSerializer.Meta.fields

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        pin = GeneratePin()
        verification_pin = pin.gen_pin()

        # Update the user fields
        if user_data:
            username = user_data.get('username')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            middle_name = user_data.get('middle_name')

        (user_instance, created) = User.objects.get_or_create(
            username=username,
            defaults={'first_name': first_name,
                      'last_name': last_name, 'middle_name': middle_name, "email": username, 'verification_pin': verification_pin}
        )
        if created:
            mail_server = SendEmail()
            mail_server.send_welcome_email([username], verification_pin)
        else:
            raise serializers.ValidationError("User already exists")

        # Create the address
        contact = validated_data.pop('contact')
        address_instance = Address.objects.create(**contact)

        ind_owner_instance = IndividualOwner.objects.create(
            owner_type="Individual", contact=address_instance, user_id=user_instance.id)

        return ind_owner_instance


class IndividualOwnerUpdateSerializer(serializers.ModelSerializer):
    contact = AddressSerlizer()
    username = serializers.CharField(source='user.username', required=True)
    first_name = serializers.CharField(source='user.first_name', required=True)
    last_name = serializers.CharField(source='user.last_name', required=True)
    middle_name = serializers.CharField(
        source='user.middle_name', required=False, allow_null=True, default=None)

    class Meta:
        model = IndividualOwner
        fields = ['username', 'first_name', 'middle_name',
                  'last_name'] + OwnerSerializer.Meta.fields

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_instance = instance.user
            user_instance.first_name = user_data.get(
                'first_name', user_instance.first_name)
            user_instance.last_name = user_data.get(
                'last_name', user_instance.last_name)
            user_instance.middle_name = user_data.get(
                'middle_name', user_instance.middle_name)
            user_instance.save()

        contact_data = validated_data.pop('contact', None)
        if contact_data:
            address_instance = instance.contact
            address_instance.phone_number = contact_data.get(
                'phone_number', address_instance.phone_number)
            address_instance.city = contact_data.get(
                'city', address_instance.city)
            address_instance.save()

        return super().update(instance, validated_data)


class CompanyOwnerCreateSeralizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    contact = AddressSerlizer()

    class Meta:
        model = CompanyOwner
        fields = ['username', 'company_name'] + \
            OwnerSerializer.Meta.fields

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        company_name = validated_data.pop("company_name")
        pin = GeneratePin()
        verification_pin = pin.gen_pin()
        if user_data:
            username = user_data.get('username')

        # Validating the user
        (user_instance, created) = User.objects.get_or_create(
            username=username,
            defaults={"email": username}
        )
        if created:
            mail_server = SendEmail()
            mail_server.send_welcome_email([username], verification_pin)
        else:
            raise serializers.ValidationError("User data is required")

        # Creating the address
        contact = validated_data.pop('contact')
        addrese_instance = Address.objects.create(**contact)

        # Creating the company owner
        company_onwer_instance = CompanyOwner.objects.create(
            owner_type="Company", contact=addrese_instance, user_id=user_instance.id, company_name=company_name)

        return company_onwer_instance

    def update(self, instance, validated_data):
        company_name = validated_data.pop("company_name")
        if company_name:
            user_instance = instance.user
            user_instance.company_name = company_name
            user_instance.save()

        contact_data = validated_data.pop('contact')
        if contact_data:
            address_instance = instance.contact
            address_instance.phone_number = contact_data.get(
                'phone_number', address_instance.phone_number)
            address_instance.city = contact_data.get(
                'city', address_instance.city)
            address_instance.save()
        return super().update(instance, validated_data)

class CompanyOwnerUpdateSeralizer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    contact = AddressSerlizer()

    class Meta:
        model = CompanyOwner
        fields = ['username', 'company_name'] + \
            OwnerSerializer.Meta.fields

    def update(self, instance, validated_data):
        company_name = validated_data.get("company_name")
        user_instance = instance.user
        if company_name:
            user_instance.company_name = company_name
            user_instance.save()

        contact_data = validated_data.pop('contact')
        if contact_data:
            address_instance = instance.contact
            address_instance.phone_number = contact_data.get(
                'phone_number', address_instance.phone_number)
            address_instance.city = contact_data.get(
                'city', address_instance.city)
            address_instance.save()

        # Check if instance has been updated
        instance = super().update(instance, validated_data)

        return super().update(instance, validated_data)


class UserEmailVerificationSerializer(serializers.ModelSerializer):
    username = serializers.EmailField()
    verification_pin = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'verification_pin']

    def validate(self, attrs):
        username = attrs.get('username')
        verification_pin = attrs.get('verification_pin')

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if user.verification_pin == 1:
            raise serializers.ValidationError("Email already verified")

        if int(verification_pin) != user.verification_pin:
            raise serializers.ValidationError("Invalid verification pin")

        return attrs

    def update(self, instance, validated_data):
        user = User.objects.get(username=validated_data.get('username'))
        user.verification_pin = 1
        user.save()
        return instance


class UserPasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def update(self, validated_data):
        pin = GeneratePin()
        password_reset_pin = pin.gen_pin()
        username = validated_data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        user.password_reset_pin = password_reset_pin
        user.save()
        email_sever = SendEmail()
        email_sever.send_password_reset_email(
            [username], passcode=password_reset_pin)
        return user


class UserPasswordResetUpdateSerlizer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        username = validated_data.get('username')
        password_reset_pin = validated_data.get("password_reset_pin")
        password = validated_data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if user.password_reset_pin != password_reset_pin:
            raise serializers.ValidationError("Invalid reset link")

        user = User.objects.get(username=username)
        user.password_reset_pin = 1
        user.set_password(password)
        user.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'password']

class UserPasswordSetUpSerlizer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def update(self, instance, validated_data):
        
        username = validated_data.get("username")
        password = validated_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        user.set_password(password)
        user.save()

        return user
