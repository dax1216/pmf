from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Company
from .tasks import run_pmf_score

# Create your views here.


class SearchView(generic.CreateView):
    model = Company
    template_name = "pmf/search.html"
    fields = ("name",)

    def post(self, request, *args, **kwargs):
        if Company.objects.filter(name=request.POST.get("name")).exists():
            return HttpResponseRedirect(reverse("pmf:list"))

        res = super().post(request, *args, **kwargs)
        run_pmf_score.delay(self.object.id)
        return res

    def get_success_url(self):
        return reverse("pmf:list")


class PmfListView(generic.ListView):
    model = Company
    template_name = "pmf/list.html"

    def get_queryset(self):
        return Company.objects.all().order_by("-id")
