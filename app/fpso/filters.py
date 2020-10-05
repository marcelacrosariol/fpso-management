from rest_framework.filters import SearchFilter
from . import models


class StatusSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        params = super(StatusSearchFilter, self).get_search_terms(request)
        try:
            status_param = [models.Equipment.get_status_options(params[0])]
        except:
            status_param = None
        return status_param