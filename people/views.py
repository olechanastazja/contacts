from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PersonModelForm
from group.models import Group
from .models import Person
import json
from django.http import HttpResponse


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
        form = PersonModelForm(request.user)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = PersonModelForm(request.user, request.POST)
        if form.is_valid():
            # person = Person(**form.cleaned_data, user=request.user)
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            person.group.set(form.cleaned_data['group'])
        return redirect('people:person-list')


class PersonDeleteView(PersonObjectMixin, View):
    template_name = 'people/person_delete.html'

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
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PersonModelForm(instance=obj, user=request.user)

            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PersonModelForm(instance=obj, user=request.user, data=request.POST)
            print(obj)
            print(request.user)
            print(request.POST)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            return redirect('people:person-list')
        return render(request, self.template_name, context)


class PersonListView(View):
    template_name = "people/person_list.html"

    def get(self, request, *args, **kwargs):
        queryset = Person.objects.filter(user=request.user)
        context = {
            'object_list': queryset,
            'contacts_page': 'active'
        }
        return render(request, self.template_name, context)


class PersonView(PersonObjectMixin, View):
    template_name = "people/person_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Person.objects.filter(first_name__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.FIELD)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)