from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from users.models import User


class SearchListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "search/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["hide_search"] = True
        context["users_list"] = (
            get_user_model()
            .objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
            .distinct()
        )
        context["users_count"] = context["users_list"].count()
        context["total_results"] = (
            + context["users_count"]
        )
        return context


@login_required
def get_suggestions(request):
    query = request.GET.get("term", "")
    user = list(
        get_user_model().objects.filter(
            Q(username__icontains=query) | Q(name__icontains=query)
        )
    )

    data_retrieved = user
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, get_user_model()):
            data_json["id"] = data.username
            data_json["name"] = data.name

        results.append(data_json)

    return JsonResponse(results, safe=False)
