from users.models import IndividualOwner, CompanyOwner

class GetUser:
    @staticmethod
    def get_owner(user):
        try:
            return IndividualOwner.objects.get(user=user)
        except IndividualOwner.DoesNotExist:
            return CompanyOwner.objects.get(user=user)
        except CompanyOwner.DoesNotExist:
            return None
        except Exception as e:
            return None