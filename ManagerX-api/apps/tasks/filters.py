import django_filters

from apps.tasks.models import Task, SubTask
from django.db.models import Q


class TaskListFilter(django_filters.FilterSet):
    subtask_assign_to = django_filters.CharFilter(method='filter_by_subtask_assign_to')
    subtask_assigned_by_user = django_filters.CharFilter(method='filter_subtask_assigned_by_user')
    status = django_filters.CharFilter(method='filter_by_status')
    exclude_created_expertise_data = django_filters.BooleanFilter(method='filter_by_exclude_created_expertise_data')
    exclude_generated_conclusion = django_filters.BooleanFilter(method='filter_by_exclude_generated_conclusion')

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['comment']

    def filter_by_subtask_assign_to(self, queryset, name, value):
        return queryset.filter(subtasks__assign_to__id=value)

    def filter_subtask_assigned_by_user(self, queryset, name, value):
        return queryset.filter(subtasks__creator__id=value)

    def filter_by_status(self, queryset, name, value):
        # Split the comma-separated list of statuses
        status_list = value.split(',')
        return queryset.filter(status__in=status_list)

    def filter_by_exclude_created_expertise_data(self, queryset, name, value):
        if value:  # Exclude tasks with existing expertise data if value is True
            return queryset.exclude(expertise_data__isnull=False)
        return queryset

    def filter_by_exclude_generated_conclusion(self, queryset, name, value):
        if value:
            # Filter where conclusionNumber is either an empty string or NULL
            return queryset.filter(
                Q(expertise_data__conclusionNumber='') | Q(expertise_data__conclusionNumber__isnull=True))
        return queryset

class SubtaskListFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='filter_by_status')

    class Meta:
        model = SubTask
        fields = '__all__'
        exclude = ['comment']

    def filter_by_status(self, queryset, name, value):
        # Split the comma-separated list of statuses
        status_list = value.split(',')
        return queryset.filter(status__in=status_list)