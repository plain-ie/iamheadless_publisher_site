from django.shortcuts import render
from django.views import View


class BaseViewSet(View):

    template = None

    def get(self, request, language):

        if language is None:
            return redirect()

        return render(request, self.get_template(), context=self.get_context())

    def get_template(self):
        return self.template

    def get_context(self):
        return {}

    def get_item(self):
        return {}
