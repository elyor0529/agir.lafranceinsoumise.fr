from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.contrib.postgres.forms import JSONField
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _
from django_countries import countries
from django_countries.fields import LazyTypedChoiceField

from agir.donations.base_forms import SimpleDonationForm, SimpleDonorForm
from agir.donations.form_fields import AskAmountField
from agir.lib.data import departements_choices
from agir.lib.form_fields import IBANField
from agir.payments.payment_modes import PaymentModeField, PAYMENT_MODES
from agir.people.models import Person


class LoanForm(SimpleDonationForm):
    button_label = "Je prête !"

    amount = AskAmountField(
        label="Montant du prêt",
        max_value=settings.LOAN_MAXIMUM,
        min_value=settings.LOAN_MINIMUM,
        decimal_places=2,
        required=True,
        error_messages={
            "invalid": _("Indiquez le montant à prêter."),
            "min_value": format_lazy(
                _("Les prêts de moins de 400 € ne sont pas acceptés."),
                min=settings.LOAN_MINIMUM,
            ),
            "max_value": format_lazy(
                _(
                    "Les prêts de plus de {max} € ne peuvent être faits par carte bleue."
                ),
                max=settings.LOAN_MAXIMUM,
            ),
        },
        amount_choices=[10000, 5000, 2000, 1000, 400],
        show_tax_credit=False,
    )


class LenderForm(SimpleDonorForm):
    button_label = "Je prête {amount}"

    country_of_birth = LazyTypedChoiceField(
        required=True, label="Pays de naissance", choices=countries, initial="FR"
    )
    city_of_birth = forms.CharField(label="Ville de naissance", required=True)
    departement_of_birth = forms.ChoiceField(
        label="Département de naissance", choices=departements_choices, required=False
    )

    amount = forms.IntegerField(
        max_value=settings.LOAN_MAXIMUM * 100,
        min_value=settings.LOAN_MINIMUM * 100,
        required=True,
        widget=forms.HiddenInput,
    )

    payment_mode = PaymentModeField(
        payment_modes=[
            PAYMENT_MODES["system_pay_afce_pret"],
            PAYMENT_MODES["check_afce"],
        ],
        label="Comment souhaitez-vous prêtez l'argent ?",
    )

    iban = IBANField(
        label="Votre IBAN",
        required=True,
        allowed_countries=["FR"],
        help_text="Le numéro IBAN du compte sur lequel le remboursement du prêt sera effectué.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["declaration"].label = _(
            "Je certifie sur l'honneur être une personne physique et que le réglement de mon prêt ne provient pas d'une"
            " personne morale mais de mon compte ne banque personnel."
        )
        # retirer le help_text qui indique qu'un reçu fiscal sera émis (ce qui n'est pas le cas pour un prêt)
        self.fields["declaration"].help_text = None

        del self.fields["fiscal_resident"]

        self.helper.layout = layout.Layout(
            "amount",
            "declaration",
            "nationality",
            "first_name",
            "last_name",
            "gender",
            layout.Field("date_of_birth", placeholder="JJ/MM/AAAA"),
            "country_of_birth",
            "city_of_birth",
            "departement_of_birth",
            layout.Field("location_address1", placeholder="Ligne 1"),
            layout.Field("location_address2", placeholder="Ligne 2"),
            layout.Row(
                layout.Div("location_zip", css_class="col-md-4"),
                layout.Div("location_city", css_class="col-md-8"),
            ),
            "location_country",
            "contact_phone",
            "iban",
            "payment_mode",
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("country_of_birth", "") == "FR" and not cleaned_data.get(
            "departement_of_birth", ""
        ):
            self.add_error(
                "departement_of_birth",
                forms.ValidationError(
                    "Merci d'indiquer votre département de naissance",
                    code="departement",
                ),
            )

        return cleaned_data

    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "gender",
            "location_address1",
            "location_address2",
            "location_zip",
            "location_city",
            "location_country",
            "contact_phone",
            "subscribed",
            "date_of_birth",
        )


class ContractForm(forms.Form):
    """
    """

    acceptance = forms.BooleanField(
        required=True,
        label="Je déclare solennellement avoir pris connaissance du contenu"
        " du contrat et en accepter les termes.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(layout.Submit("valider", "Je signe le contrat"))
