# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext_lazy as _


USER_ROLES = (
    ('programmer', u'Программист'),
    ('designer', u'Дизайнер'),
    ('manager', u'Менеджер'),
    ('student', u'Студент'),
    ('other', u'Другое'),
)


class SponsorProfile(models.Model):

    sponsor_email = models.EmailField(_('email'), max_length=75)

    def __unicode__(self):
        return self.sponsor_email


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                        verbose_name=_('user'),
                        unique=True,
                        related_name='profile',)
    avatar = models.CharField(_('Avatar'), max_length=80,
                              blank=True, null=True)
    username = models.CharField(_('Username'), max_length=100)
    user_skills = models.TextField(_('User skills'))
    user_role = models.CharField(_('User role'), max_length=30,
                           choices=USER_ROLES)
    contact = models.CharField(_('Contact'), max_length=40, null=True)
    phone = models.CharField(_('Phone'), max_length=40, blank=True, null=True)
    has_idea = models.BooleanField(_('Has idea'), default=False)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)
    project = models.ForeignKey('UserProject', verbose_name=_('project'),
                               related_name=_('members'),
                               blank=True, null=True)
    confirmed = models.BooleanField('Confirmed', default=False)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __unicode__(self):
        return self.user.username

    @property
    def in_team(self):
        try:
            team =  self.project or self.group
        except:
            return False
        if team:
            return True

    @property
    def team(self):
        if self.in_team:
            return self.project if self.project else self.group

    @property
    def empty(self):
        if self.username and self.user_skills and self.contact:
            return False
        return True

    @property
    def can_join(self):
        if not self.empty and not self.team:
            return True
        return False

    @property
    def can_left(self):
        if not self.empty and self.team.owner != self:
            return True
        return False

    @models.permalink
    def get_absolute_url(self):
        return ('profile_detail', None, {'pk':str(self.pk)})


class UserProject(models.Model):
    created = models.DateTimeField(_('Created'), auto_now=True)
    owner = models.OneToOneField(UserProfile,
                        verbose_name=_('owner'),
                        unique=True,
                        related_name='group',
                        blank=True,null=True,
                        default='')
    avatar = models.CharField(_('Avatar'), max_length=80,
                              blank=True, null=True)
    title = models.CharField(_('Title'), max_length=100)
    text_idea = models.TextField(_('Text idea'), blank=True, null=True)
    require = models.CharField(_('Require staff'), max_length=350, blank=True, null=True)
    is_full = models.BooleanField(_('Is full'), default=False)
    pirvate = models.BooleanField(_('Private'), default=False)
    archived = models.BooleanField(_('Archived'), default=False)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('-created',)

    def __unicode__(self):
        return '%s - %s' % (self.owner, self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', None, {'pk':str(self.pk)})


class Message(models.Model):
    created = models.DateTimeField(_('Created'), auto_now=True)
    text = models.TextField(_('Message'))
    title = models.CharField(_('Title'), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-created',)

    def __unicode__(self):
        if self.title:
            return u'%s' % self.title
        else:
            return ''


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_user_profile, sender=User)
