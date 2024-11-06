# Generated by Django 5.1.2 on 2024-11-04 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(unique=True)),
                ('StaffUsername', models.CharField(max_length=20)),
                ('Staff', models.CharField(max_length=20)),
                ('Date', models.DateTimeField()),
                ('Category', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('Authority', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Applicant', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('StartDate', models.DateTimeField()),
                ('FinishedDate', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BroadCategory', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Staff', models.CharField(max_length=50)),
                ('Equipment', models.CharField(max_length=200)),
                ('Procedure', models.CharField(max_length=50)),
                ('Sample', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Regulation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SamplePurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Submitter', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Sample', models.CharField(max_length=50)),
                ('Specification', models.CharField(max_length=50)),
                ('Manufacturer', models.CharField(max_length=50)),
                ('BatchNumber', models.CharField(max_length=50)),
                ('RequiredQuantity', models.IntegerField()),
                ('ActualQuantity', models.IntegerField()),
                ('ApplicationTime', models.DateTimeField()),
                ('DeliveryTime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=20, unique=True)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('TraFinTime', models.DateTimeField()),
                ('TraCertification', models.CharField(max_length=100, unique=True)),
                ('ExamTime', models.DateTimeField()),
                ('TestFile', models.CharField(max_length=100, unique=True)),
                ('AuthCertification', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Equipment', models.CharField(max_length=50)),
                ('Manufacturer', models.CharField(max_length=50)),
                ('Photo', models.CharField(max_length=50)),
                ('Detail', models.CharField(max_length=200)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('Equipment', 'Manufacturer', 'Photo'), name='UniqueEquipment')],
            },
        ),
        migrations.CreateModel(
            name='EquipPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Submitter', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('EquipmentName', models.CharField(max_length=50)),
                ('Manufacturer', models.CharField(max_length=50)),
                ('Photo', models.CharField(max_length=100)),
                ('State', models.CharField(default='Pending', max_length=50)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('State', 'Pending'), ('State', 'Finished'), _connector='OR'), name='CheckEquipPurchaseState')],
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Submitter', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
                ('Staff', models.CharField(max_length=200)),
                ('EquipmentName', models.CharField(max_length=200)),
                ('Regulation', models.CharField(max_length=200)),
                ('Sample', models.CharField(max_length=200)),
                ('State', models.CharField(default='Pending', max_length=20)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('State', 'Pending'), ('State', 'Finished'), _connector='OR'), name='CheckReminderState')],
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sample', models.CharField(max_length=50)),
                ('Specification', models.CharField(max_length=50)),
                ('Manufacturer', models.CharField(max_length=50)),
                ('BatchNumber', models.CharField(max_length=50)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('Sample', 'Specification', 'Manufacturer', 'BatchNumber'), name='UniqueSample')],
            },
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BroadCategory', models.CharField(max_length=50)),
                ('Category', models.CharField(max_length=50)),
                ('Project', models.CharField(max_length=50)),
                ('StandardName', models.CharField(max_length=50)),
                ('StandardNumber', models.CharField(max_length=50)),
                ('ClauseNumber', models.CharField(max_length=50)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('Category', 'Project', 'StandardName', 'StandardNumber', 'ClauseNumber'), name='UniqueStandard')],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=20, unique=True)),
                ('Password', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=20, unique=True)),
                ('PhoneNumber', models.CharField(max_length=20)),
                ('Institution', models.CharField(max_length=20)),
                ('Identity', models.CharField(max_length=20)),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('Identity', 'SupportStaff'), ('Identity', 'TestStaff'), ('Identity', 'Administer'), ('Identity', 'PotentialCustomer'), _connector='OR'), name='CheckUserIdentity')],
            },
        ),
    ]