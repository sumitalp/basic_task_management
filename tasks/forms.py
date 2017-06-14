from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from tasks.models import Task
from django.contrib.auth import get_user_model


class AddTaskForm(ModelForm):
    # The picklist showing allowable groups to which a new list can be added
    # determines which groups the user belongs to. This queries the form object
    # to derive that list.
    def __init__(self, user, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_user_model().objects.all()
        self.fields['assigned_to'].label_from_instance = \
            lambda obj: "%s (%s)" % (obj.get_full_name(), obj.username)

    due_date = forms.DateField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'due_date_picker'})
    )

    class Meta:
        model = Task
        exclude = []


class EditTaskForm(ModelForm):
    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.
    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        # self.fields['assigned_to'].queryset = get_user_model().objects.filter(groups__in=[self.instance.list.group])

    class Meta:
        model = Task
        exclude = ('created_date', 'created_by',)
