# Generated by Django 2.1.3 on 2018-11-14 14:59

from django.db import migrations, models
import django.db.models.deletion


add_allocations_triggers = """
CREATE FUNCTION check_allocation_lt_payment() RETURNS TRIGGER AS $process_allocation$
    DECLARE
       payment_amount INTEGER;
    BEGIN
        SELECT price INTO payment_amount FROM payments_payment WHERE id = NEW.payment_id;
        IF payment_amount < NEW.amount THEN
            RAISE EXCEPTION integrity_constraint_violation;
        END IF;
        RETURN NEW;
    END
$process_allocation$ LANGUAGE plpgsql;
    
CREATE FUNCTION check_payment_gt_allocation() RETURNS TRIGGER AS $process_donation$
    DECLARE 
        allocation INTEGER;
    BEGIN
        SELECT donations_operation.amount INTO allocation FROM donations_operation WHERE payment_id = OLD.id;
        IF allocation IS NOT NULL AND (allocation > NEW.price OR  OLD.id <> NEW.id) THEN
            RAISE EXCEPTION integrity_constraint_violation;
        END IF;
        RETURN NEW;
    END
$process_donation$ LANGUAGE plpgsql;

CREATE TRIGGER check_allocation_lt_payment BEFORE INSERT OR UPDATE ON donations_operation
    FOR EACH ROW EXECUTE PROCEDURE check_allocation_lt_payment();

CREATE TRIGGER check_payment_gt_allocation BEFORE UPDATE ON payments_payment
    FOR EACH ROW EXECUTE PROCEDURE check_payment_gt_allocation();
"""

remove_operation_triggers = """
DROP TRIGGER check_allocation_lt_payment ON donations_operation;
DROP TRIGGER check_payment_gt_allocation ON payments_payment;
DROP FUNCTION check_allocation_lt_payment();
DROP FUNCTION check_payment_gt_allocation();
"""


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("groups", "0028_auto_20181024_1757"),
        ("payments", "0007_auto_20180724_2040"),
    ]

    operations = [
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        editable=False, verbose_name="opération en centimes d'euros"
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="groups.SupportGroup",
                    ),
                ),
                (
                    "payment",
                    models.OneToOneField(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="payments.Payment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Spending",
            fields=[],
            options={"proxy": True, "indexes": []},
            bases=("donations.operation",),
        ),
        migrations.RunSQL(
            sql=add_allocations_triggers, reverse_sql=remove_operation_triggers
        ),
    ]