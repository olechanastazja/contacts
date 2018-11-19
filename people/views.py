from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PersonModelForm, GroupModelForm
from django.contrib import messages
from .models import Person, Group


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
            person = Person(**form.cleaned_data, user=request.user)
            person.save()
        messages.add_message(request, messages.SUCCESS, 'Added person successfully!')
        return redirect('people:person-list')


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

    def get(self, request, *args, **kwargs):
        queryset = Person.objects.filter(user=request.user)
        context = {'object_list': queryset}
        return render(request, self.template_name, context)


class PersonView(PersonObjectMixin, View):
    template_name = "people/person_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)


class GroupObjectMixin(object):
    model = Group

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class GroupCreateView(View):
    template_name = 'people/group_create.html'

    def get(self, request, *args, **kwargs):
        form = GroupModelForm()
        context = {
            'form': form
        }
        return render(request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        form = GroupModelForm(request.POST)
        if form.is_valid():
            group = Group(**form.cleaned_data, user=request.user)
            group.save()
        messages.add_message(request, messages.SUCCESS, 'Added group successfully!')
        return redirect('people:group-list')


class GroupDeleteView(PersonObjectMixin, View):
    template_name = 'people/group_detail.html'

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


class GroupUpdateView(GroupModelForm, View):

    template_name = "people/group_update.html"

    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = GroupModelForm(instance=obj)
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


class GroupListView(View):
    template_name = "people/group_list.html"

    def get(self, request, *args, **kwargs):
        queryset = Group.objects.filter(user=request.user)
        context = {'object_list': queryset}
        return render(request, self.template_name, context)


class GroupView(PersonObjectMixin, View):
    template_name = "people/group_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)



