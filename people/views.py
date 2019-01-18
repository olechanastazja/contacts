from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PersonModelForm, AddressModelForm, PhoneModelForm, EmailModelForm
from .models import Person, Address, PhoneNumber, EmailAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
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


class AddressObjectMixin(object):
    model = Address

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class PhoneObjectMixin(object):
    model = PhoneNumber

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class EmailObjectMixin(object):
    model = EmailAddress

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(self.model, id=id)
        return obj


class PersonCreateView(LoginRequiredMixin, View):
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
            person = form.save(commit=False)
            person.user = request.user
            person.save()
            person.group.set(form.cleaned_data['group'])
            messages.success(request, 'Person has been created')
        return redirect('people:person-list')


class PersonDeleteView(LoginRequiredMixin, PersonObjectMixin, View):
    template_name = 'people/person_delete.html'

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        print(obj)
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


class PersonUpdateView(LoginRequiredMixin,PersonObjectMixin, View):
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
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
            return redirect('people:person-list')
        return render(request, self.template_name, context)


class PersonListView(LoginRequiredMixin,View):
    template_name = "people/person_list.html"

    def get(self, request, *args, **kwargs):
        queryset = Person.objects.filter(user=request.user)
        context = {
            'object_list': queryset,
            'contacts_page': 'active'
        }
        return render(request, self.template_name, context)


class PersonView(LoginRequiredMixin,PersonObjectMixin, View):
    template_name = "people/person_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        obj = self.get_object()
        context = {'object': obj}
        request.session['redirect_id'] = obj.id
        return render(request, self.template_name, context)


class PersonGroupsView(LoginRequiredMixin,PersonObjectMixin, View):
    template_name = "people/group_people.html"

    def get(self, request, id, *args, **kwargs):
        person = self.get_object()
        context = {
            'person': person,
            'groups': person.group.all()
        }
        return render(request, self.template_name, context)


def load_persons(request):
    q = request.GET.get('term', ' ').capitalize()
    search_qs = Person.objects.filter(user=request.user, first_name__startswith=q) | \
                Person.objects.filter(user=request.user, last_name__startswith=q)
    return render(request, 'people/ajax_list.html', {'object_list': search_qs})


class AddressCreate(LoginRequiredMixin,PersonObjectMixin, View):
    template_name = "address/address_add.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        print(obj.id)
        if obj is not None:
            form = AddressModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }

        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AddressModelForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.save()
                address.people.add(obj)
                messages.success(request, 'Your address has been added!')
                return redirect("people:person-list")

        form = AddressModelForm()
        context = {
            'object': obj,
            'form': form
        }

        return render(request, self.template_name, context)


class AddressUpdate(LoginRequiredMixin,AddressObjectMixin, View):
    template_name = "address/address_edit.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AddressModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = AddressModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                context = {
                    'object': obj,
                    'form': form
                }
                messages.success(request, 'Your address has been updated!')
                redirect_id = request.session['redirect_id']
                return redirect("people:person-detail", redirect_id)
        form = AddressModelForm()
        context = {
            'object': obj,
            'form': form
        }
        return redirect(request, self.template_name, context)


def address_delete(request, id):
    if request.method == "POST":
        address = Address.objects.get(id=id)
        address.delete()
        redirect_id = request.session['redirect_id']
        messages.success(request, 'Your address has been removed!')
        return redirect("people:person-detail",  redirect_id)


class PhoneCreate(LoginRequiredMixin,PersonObjectMixin, View):
    template_name = "phone/phone_add.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PhoneModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }

        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PhoneModelForm(request.POST)
            if form.is_valid():
                phone = form.save(commit=False)
                phone.person = obj
                phone.save()
                messages.success(request, 'Your phone has been added!')
                return redirect("people:person-list")
        messages.error(request, form.errors.get('phone_number'))
        form = PhoneModelForm()
        context = {
            'object': obj,
            'form': form
        }
        return render(request, self.template_name, context)


class PhoneUpdate(LoginRequiredMixin,PhoneObjectMixin, View):
    template_name = "phone/phone_edit.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PhoneModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = PhoneModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                context = {
                    'object': obj,
                    'form': form
                }
                messages.success(request, 'Your phone has been updated!')
                return redirect("people:person-detail", id=obj.person.id)
        messages.error(request, form.errors.get('phone_number'))
        form = PhoneModelForm()
        context = {
            'object': obj,
            'form': form
        }
        return render(request, self.template_name, context)


def phone_delete(request, id):
    if request.method == "POST":
        phone = PhoneNumber.objects.get(id=id)
        phone.delete()
        messages.success(request, 'Your phone has been removed!')
        return redirect("people:person-detail",  id=phone.person.id)


class EmailCreate(LoginRequiredMixin,PersonObjectMixin, View):
    template_name = "email/email_add.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = EmailModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = EmailModelForm(request.POST)
            if form.is_valid():
                email = form.save(commit=False)
                email.person = obj
                email.save()
                messages.success(request, 'Your email has been added!')
                return redirect("people:person-list")
        form = EmailModelForm()
        messages.error(request, 'Invalid data! Correct that and try again!')
        context = {
            'object': obj,
            'form': form
        }
        return render(request, self.template_name, context)


class EmailUpdate(LoginRequiredMixin,EmailObjectMixin, View):
    template_name = "email/email_edit.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = EmailModelForm(instance=obj)
            context = {
                'object': obj,
                'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = EmailModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                context = {
                    'object': obj,
                    'form': form
                }
                messages.success(request, 'Your email has been updated!')
                return redirect("people:person-detail",  id=obj.person.id)
        form = EmailModelForm()
        context = {
            'object': obj,
            'form': form
        }
        return render(request, self.template_name, context)


def email_delete(request, id):
    if request.method == "POST":
        email = EmailAddress.objects.get(id=id)
        email.delete()
        messages.success(request, 'Your email has been removed!')
        return redirect("people:person-detail",  id=email.person.id)

