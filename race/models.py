# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Heats(models.Model):
    heat_id = models.AutoField(primary_key=True)
    heat_finished = models.IntegerField(blank=True, null=True)
    first_pass_id = models.PositiveIntegerField(blank=True, null=True)
    last_pass_id = models.PositiveIntegerField(blank=True, null=True)
    rtc_time_start = models.BigIntegerField()
    rtc_time_end = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'heats'


class Passes(models.Model):
    db_entry_id = models.AutoField(primary_key=True)
    pass_id = models.PositiveIntegerField(unique=True)
    transponder_id = models.PositiveIntegerField()
    rtc_time = models.BigIntegerField()
    strength = models.PositiveSmallIntegerField(blank=True, null=True)
    hits = models.PositiveSmallIntegerField(blank=True, null=True)
    flags = models.PositiveSmallIntegerField(blank=True, null=True)
    decoder_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'passes'


class Laps(models.Model):
    heat_id = models.PositiveIntegerField()
    pass_id = models.PositiveIntegerField(primary_key=True)
    transponder_id = models.PositiveIntegerField()
    rtc_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'laps'


class Karts(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    kart_number = models.PositiveIntegerField(primary_key=True)
    transponder_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'karts'
