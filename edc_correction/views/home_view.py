from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin


class HomeView(EdcBaseViewMixin, TemplateView):

    app_config_name = 'edc_correction'
    namespace = 'edc_correction'
    template_name = 'edc_correction/home.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(navbar_item_selected='home')
        return context
