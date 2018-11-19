from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PersonModelForm
from django.contrib import messages
from .models import Person


def home(request):
    return render(request, 'people/home.html')


class PersonObjectMixin(object):
    model = Person
    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class PersonCreateView(View):
    template_name = 'people/person_create.html'

    def get(self, request, *args, **kwargs):
        form = PersonModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        form = PersonModelForm(request.POST)
        if form.is_valid():
            form.save()
        context = {
            'form': form
        }
        messages.add_message(request, messages.SUCCESS, 'Added person successfully!')
        return render(request, self.template_name, context)


class PersonDeleteView(PersonObjectMixin, View):
    template_name = 'people/person_detail.html'

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/')

        return render(request, self.template_name, context)


class PersonUpdateView(PersonObjectMixin, View):
    template_name = "people/person_update.html"

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PersonModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PersonModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)


class PersonListView(View):
    template_name = "people/person_list.html"
    queryset = Person.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.get_queryset()}
        return render(request, self.template_name, context)


class PersonView(PersonObjectMixin, View):
    template_name = "people/person_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

