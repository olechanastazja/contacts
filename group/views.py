from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Group
from .forms import GroupModelForm


class GroupObjectMixin(object):
    model = Group

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class GroupCreateView(View):
    template_name = 'group/group_create.html'

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
        return redirect('group:group-list')


class GroupDeleteView(GroupObjectMixin, View):
    template_name = 'group/group_delete.html'

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


class GroupUpdateView(GroupObjectMixin, View):

    template_name = "group/group_update.html"

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
            form = GroupModelForm(request.POST, instance=obj)

            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form

        return redirect('group:group-list')


class GroupListView(View):
    template_name = "group/group_list.html"

    def get(self, request, *args, **kwargs):
        queryset = Group.objects.filter(user=request.user)
        context = {
            'object_list': queryset,
            'group_page': 'active'
        }
        return render(request, self.template_name, context)


class GroupView(GroupObjectMixin, View):
    template_name = "group/group_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {'object': self.get_object()}
        return render(request, self.template_name, context)

