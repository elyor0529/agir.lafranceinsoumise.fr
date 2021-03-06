from django.contrib import messages
from django.http import Http404, HttpResponseServerError
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic import DetailView

from agir.authentication.view_mixins import HardLoginRequiredMixin
from agir.payments.actions.subscriptions import terminate_subscription
from .models import Payment, Subscription
from .payment_modes import PAYMENT_MODES
from .types import PAYMENT_TYPES, SUBSCRIPTION_TYPES

PAYMENT_ID_SESSION_KEY = "_payment_id"


def payment_view(request,):
    pass


class PaymentView(DetailView):
    queryset = Payment.objects.filter(status=Payment.STATUS_WAITING)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment_mode = PAYMENT_MODES.get(self.object.mode)

        if payment_mode is None:
            return HttpResponseServerError()

        return payment_mode.payment_view(request, payment=self.object, *args, **kwargs)


class RetryPaymentView(DetailView):
    def get_queryset(self):
        return Payment.objects.filter(
            status__in=[
                Payment.STATUS_WAITING,
                Payment.STATUS_ABANDONED,
                Payment.STATUS_REFUSED,
            ]
        ).filter(
            mode__in=[mode.id for mode in PAYMENT_MODES.values() if mode.can_retry]
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment_mode = PAYMENT_MODES.get(self.object.mode)

        if payment_mode is None:
            return HttpResponseServerError()

        return payment_mode.retry_payment_view(
            request, payment=self.object, *args, **kwargs
        )


class SubscriptionView(DetailView):
    queryset = Subscription.objects.filter(
        status__in=(Subscription.STATUS_WAITING, Subscription.STATUS_ACTIVE)
    )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment_mode = PAYMENT_MODES.get(self.object.mode)

        if payment_mode is None:
            return HttpResponseServerError()

        return payment_mode.subscription_view(
            request, subscription=self.object, *args, **kwargs
        )


class TerminateSubscriptionView(HardLoginRequiredMixin, DetailView):
    template_name = "payments/subscription_terminate.html"

    def get_queryset(self):
        return Subscription.objects.filter(
            status=Subscription.STATUS_ACTIVE, person=self.request.user.person
        )

    def post(self, request, pk):
        subscription = self.get_object()
        terminate_subscription(subscription)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Votre paiement automatique a bien été supprimé.",
        )

        return redirect("view_payments")


def payment_return_view(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if payment.type in PAYMENT_TYPES and PAYMENT_TYPES[payment.type].success_view:
        return PAYMENT_TYPES[payment.type].success_view(request, payment=payment)
    else:
        return TemplateResponse(request, "payments/default_success_page.html")


def subscription_return_view(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    if subscription.type in SUBSCRIPTION_TYPES:
        return SUBSCRIPTION_TYPES[subscription.type].success_view(
            request, subscription=subscription
        )
