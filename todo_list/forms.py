from django import forms

from todo_list.models import Task

from django.utils import timezone


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("content", "deadline", "tags")
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3}),
            "deadline": forms.DateInput(
                format="%Y-%m-%d", attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def clean_deadline(self):
        data = self.cleaned_data.get("deadline")
        if data and data < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past")
        return data
