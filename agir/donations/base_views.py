from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView

import agir.donations.base_forms


def serialize_form(form):
    data = form.cleaned_data
    return {k: form[k].data for k in data}


class FormToSessionMixin:
    session_namespace = None

    def form_valid(self, form):
        """Enregistre le contenu du formulaire dans la session avant de rediriger vers le formulaire suivant.
        """
        self.request.session[self.session_namespace] = serialize_form(form)
        return super().form_valid(form)


class BaseAskAmountView(FormToSessionMixin, FormView):
    form_class = agir.donations.base_forms.SimpleDonationForm
    session_namespace = "_donation_"


class BasePersonalInformationView(UpdateView):
    form_class = None
    template_name = "donations/personal_information.html"
    payment_mode = None
    payment_type = None
    session_namespace = "_donation_"
    first_step_url = None
    persisted_data = ["amount"]

    def redirect_to_first_step(self):
        return redirect(self.first_step_url)

    def dispatch(self, request, *args, **kwargs):
        self.persistent_data = {}
        form = self.get_form()
        for k in self.persisted_data:
            field = form.fields[k]

            if k in request.GET:
                value = request.GET[k]
            elif k in request.session.get(self.session_namespace, {}):
                value = request.session[self.session_namespace][k]
            else:
                value = field.initial

            try:
                value = field.clean(value)
            except ValidationError:
                return self.redirect_to_first_step()

            self.persistent_data[k] = value

        return super().dispatch(request, *args, **kwargs)

    def clear_session(self):
        if self.session_namespace in self.request.session:
            del self.request.session[self.session_namespace]

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user.person
        else:
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        initial = kwargs.pop("initial", {})

        return {**kwargs, "initial": {**initial, **self.persistent_data}}

    def get_context_data(self, **kwargs):
        kwargs["branded_layout"] = (
            "front/nsp_layout.html"
            if self.request.GET.get("nsp")
            else "front/layout.html"
        )
        return super().get_context_data(**self.persistent_data, **kwargs)

    def get_metas(self, form):
        return {
            "nationality": form.cleaned_data["nationality"],
            "subscribed_lfi": form.cleaned_data.get("subscribed_lfi", False),
            **{
                k: v for k, v in form.cleaned_data.items() if k in form._meta.fields
            },  # person fields
            "contact_phone": form.cleaned_data["contact_phone"].as_e164,
        }
