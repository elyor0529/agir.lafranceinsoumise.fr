# Generated by Django 2.0.5 on 2018-06-06 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0032_auto_20180426_1716"),
        ("events", "0048_remove_canceled_field"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name="IdentifiedGuest",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        )
                    ],
                    options={"db_table": "events_rsvp_guests_form_submissions"},
                ),
                migrations.AlterField(
                    model_name="rsvp",
                    name="guests_form_submissions",
                    field=models.ManyToManyField(
                        related_name="guest_rsvp",
                        through="events.IdentifiedGuest",
                        to="people.PersonFormSubmission",
                    ),
                ),
                migrations.AddField(
                    model_name="identifiedguest",
                    name="rsvp",
                    field=models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="identified_guests",
                        to="events.RSVP",
                    ),
                ),
                migrations.AddField(
                    model_name="identifiedguest",
                    name="submission",
                    field=models.ForeignKey(
                        db_column="personformsubmission_id",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="people.PersonFormSubmission",
                    ),
                ),
            ]
        ),
        migrations.AddField(
            model_name="identifiedguest",
            name="status",
            field=models.CharField(
                choices=[
                    ("AP", "En attente du paiement"),
                    ("CO", "Confirmé"),
                    ("CA", "Annulé"),
                ],
                default="CO",
                max_length=2,
                verbose_name="Statut",
            ),
        ),
    ]
