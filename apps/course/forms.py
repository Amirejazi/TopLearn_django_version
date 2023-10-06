from django import forms
from apps.course.models import Course


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].help_text = "کلمات را با - جدا کنید"