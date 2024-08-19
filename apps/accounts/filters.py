import django_filters

from apps.accounts.models import UserAccount


class UserListFilter(django_filters.FilterSet):
    class Meta:
        model = UserAccount
        fields = ('id', 'username', 'email', 'first_name', 'last_name', )
