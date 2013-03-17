from django import forms

from models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',) # User will be filled in by the view.

    def save(self, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        super(self, UserProfileForm).save(*args, **kwargs)
