# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AtpStock(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'atp_stock'
        unique_together = (('productid', 'weekid', 'year'),)


class AtpStockArchive(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    archivedate = models.DateField()
    archivedby = models.CharField()

    class Meta:
        managed = False
        db_table = 'atp_stock_archive'
        unique_together = (('productid', 'weekid', 'year'),)


class Intransit(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year, eta) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    eta = models.DateField()

    class Meta:
        managed = False
        db_table = 'intransit'
        unique_together = (('productid', 'weekid', 'year', 'eta'),)


class IntransitArchive(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year, eta) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    eta = models.DateField()
    archivedate = models.DateField()
    archivedby = models.CharField()

    class Meta:
        managed = False
        db_table = 'intransit_archive'
        unique_together = (('productid', 'weekid', 'year', 'eta'),)


class PalletInfo(models.Model):
    productid = models.CharField(primary_key=True)
    palletcapacity = models.FloatField(blank=True, null=True)
    palletweight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pallet_info'


class Ready(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ready'
        unique_together = (('productid', 'weekid', 'year'),)


class ReadyArchive(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    archivedate = models.DateField()
    archivedby = models.CharField()

    class Meta:
        managed = False
        db_table = 'ready_archive'
        unique_together = (('productid', 'weekid', 'year'),)


class ReadyArchiveTest(models.Model):
    productid = models.CharField(max_length=255)
    quantity = models.FloatField()
    weekid = models.IntegerField()
    year = models.IntegerField()
    archivedate = models.DateField()
    archivedby = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ready_archive_test'


class Sales(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sales'
        unique_together = (('productid', 'weekid', 'year'),)


class SalesArchive(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    archivedate = models.DateField()
    archivedby = models.CharField()

    class Meta:
        managed = False
        db_table = 'sales_archive'
        unique_together = (('productid', 'weekid', 'year'),)


class TestTable(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_table'


class ToBeProduced(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year, etd) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    etd = models.DateField()

    class Meta:
        managed = False
        db_table = 'to_be_produced'
        unique_together = (('productid', 'weekid', 'year', 'etd'),)


class ToBeProducedArchive(models.Model):
    productid = models.CharField(primary_key=True)  # The composite primary key (productid, weekid, year, etd) found, that is not supported. The first column is selected.
    quantity = models.FloatField(blank=True, null=True)
    weekid = models.IntegerField()
    year = models.IntegerField()
    etd = models.DateField()
    archivedate = models.DateField()
    archivedby = models.CharField()

    class Meta:
        managed = False
        db_table = 'to_be_produced_archive'
        unique_together = (('productid', 'weekid', 'year', 'etd'),)


class TransportationInfo(models.Model):
    transportationid = models.CharField(primary_key=True)  # The composite primary key (transportationid, year) found, that is not supported. The first column is selected.
    transportationname = models.CharField()
    transportationcapacity = models.IntegerField()
    transportationcost = models.FloatField(blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'transportation_info'
        unique_together = (('transportationid', 'year'),)


class TransportationInfoArchive(models.Model):
    transportationid = models.CharField(primary_key=True)  # The composite primary key (transportationid, year, archivedate) found, that is not supported. The first column is selected.
    transportationname = models.CharField()
    transportationcapacity = models.IntegerField()
    transportationcost = models.FloatField(blank=True, null=True)
    year = models.IntegerField()
    archivedate = models.DateField()

    class Meta:
        managed = False
        db_table = 'transportation_info_archive'
        unique_together = (('transportationid', 'year', 'archivedate'),)


class UserRoles(models.Model):
    roleid = models.CharField(primary_key=True)
    rolename = models.CharField()

    class Meta:
        managed = False
        db_table = 'user_roles'


class Users(models.Model):
    userid = models.CharField(primary_key=True)
    roleid = models.ForeignKey(UserRoles, models.DO_NOTHING, db_column='roleid')
    username = models.CharField()
    userpassword = models.CharField()
    useremail = models.CharField()

    class Meta:
        managed = False
        db_table = 'users'
