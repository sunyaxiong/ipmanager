from datetime import date

from django.contrib import admin


class ZoneFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "区域"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'ipNet__zone__name'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('运维管理区', "运维管理区"),
            ('XXX管理区', "XXX管理区"),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '运维管理区':
            return queryset.filter(ipNet__zone__name="运维管理区")
        if self.value() == 'XXX管理区':
            return queryset.filter(ipNet__zone__name="XXX管理区")

