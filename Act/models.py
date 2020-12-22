# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.urls import reverse


class NotificationState(models.Model):
	name = models.CharField(max_length=30,db_column="name",blank=True,unique=True)
	isActive = models.BooleanField(db_column="isActive",default=True)
	red = models.IntegerField(db_column="red",default=0)
	green = models.IntegerField(db_column="green",default=0)
	blue = models.IntegerField(db_column="blue",default=0)
	background_red = models.IntegerField(db_column="background_red",default=255)
	background_green = models.IntegerField(db_column="background_green",default=255)
	background_blue = models.IntegerField(db_column="background_blue",default=255)

	def __str__(self):
		return '<State: %s: %s>' % (self.pk, self.name)
	class Meta:
		db_table = 'NotificationState'
		verbose_name_plural="Состояния задач"
		verbose_name="Состояние"
		ordering=["name",]

class Notification(models.Model):
	name = models.CharField(max_length=150,db_column="name",blank=True)
	comment = models.TextField(db_column="comment",blank=True)
	isActive = models.BooleanField(db_column="isActive",default=True)
	begin=models.DateTimeField(db_column="begin",auto_now_add=True,db_index=True)
	def __str__(self):
		return '<Задача: %s: %s от %s>' % (self.pk, self.name,self.begin)
	class Meta:
		db_table = 'Notification'
		verbose_name_plural="Список задач"
		verbose_name="Задача"
		ordering=["-id",]
	def get_form_url(self):
		return reverse('Notification:NotificationFullForm', args=[str(self.id)])

class ScreenImage(models.Model):
	parent = models.ForeignKey('Notification',db_column="parent",on_delete=models.CASCADE,null=True,blank=True)
	image_base64 = models.TextField(db_column="image_base64",blank=True)
	period=models.DateTimeField(db_column="period",default=datetime.datetime.now,db_index=True,blank=True)
	class Meta:
		db_table = 'ScreenImage'

class Act(models.Model):
	name = models.CharField(max_length=150,db_column="name",blank=True)
	isActive = models.BooleanField(db_column="isActive",default=True)
	parent = models.ForeignKey('Notification',db_column="parent",on_delete=models.CASCADE,null=True,blank=True)
	state = models.ForeignKey('NotificationState', db_column="state",on_delete=models.PROTECT,null=True,blank=True, default=1)
	period=models.DateTimeField(db_column="period",default=datetime.datetime.now,db_index=True,blank=True)
	comment = models.TextField(db_column="comment",blank=True)
	def __str__(self):
		return '<Этап: %s: %s from %s -%s>' % (self.pk, self.name,self.parent,self.state)
	class Meta:
		db_table = 'Act'
		verbose_name_plural="Список этапов задач"
		verbose_name="Этап"
		ordering=["parent","-id",]
	def save(self, *args, **kwargs):
		super(Act, self).save(*args, **kwargs)

		history,isCreated=ActHistory.objects.get_or_create(period=self.period,act=self)
		history.state=self.state
		history.save()
		if isCreated:
			print("Создан новый ActHistory")
		else:
			print("Перезаписан существующий ActHistory")


class SubActComments(models.Model):
	act = models.ForeignKey('Act', db_column="act",on_delete=models.CASCADE,null=True,blank=True)
	period=models.DateTimeField(db_column="period",default=datetime.datetime.now,db_index=True,blank=True)
	comment = models.TextField(db_column="comment",blank=True)
	class Meta:
		db_table = 'SubActComments'
		verbose_name_plural="Комментарии этапов"
		verbose_name="Комментарий к этапу"
		ordering=["-period"]
	def save(self, *args, **kwargs):
		super(SubActComments, self).save(*args, **kwargs)
		history=HistorySubActComments()
		history.actComment=self;
		history.comment=self.comment;
		history.save()

class HistorySubActComments(models.Model):
	actComment = models.ForeignKey('SubActComments', db_column="actComment",on_delete=models.CASCADE,null=True,blank=True)
	comment = models.TextField(db_column="comment",blank=True)
	period=models.DateTimeField(db_column="period",default=datetime.datetime.now,db_index=True,blank=True)
	class Meta:
		db_table = 'HistorySubActComments'
		verbose_name_plural="Истории изменений комментариев этапов"
		verbose_name="История изменений комментия этапа"
		ordering=["-period"]

class ActHistory(models.Model):
	period=models.DateTimeField(db_column="period",default=datetime.datetime.now,db_index=True,blank=True)
	act = models.ForeignKey('Act', db_column="act",on_delete=models.CASCADE,null=True,blank=True)
	state = models.ForeignKey('NotificationState', db_column="state",on_delete=models.PROTECT,null=True,blank=True)
	def __str__(self):
		return '<История состояний: %s: %s |%s-%s|>' % (self.pk, self.period,self.act,self.state)
	class Meta:
		db_table = 'NotificationHistory'
		verbose_name_plural="Истории изменения состояний"
		verbose_name="История состояния"
		ordering=["-act","-period"]
		unique_together = [['period', 'act']]

