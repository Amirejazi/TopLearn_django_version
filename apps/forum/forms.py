from ckeditor.fields import RichTextFormField
from django import forms
from html_sanitizer import Sanitizer

from .allowed_fileds import allowed_tags, allowed_attributes


class CreateQuestionForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(required=True,
                            error_messages={'required': "عنوان سوال نمیتواند خالی باشد!"},
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان سوال'}))
    body = RichTextFormField(config_name='normal',
                             label='متن سوال',
                             required=True,
                             error_messages={'required': "متن سوال نمیتواند خالی باشد!"},
                             widget=forms.Textarea(attrs={'class': 'form-control question_body', 'placeholder': 'متن سوال'}))

    def cleaned_body(self):
        sanitizer = Sanitizer()
        sanitizer.tags = allowed_tags
        sanitizer.attributes = allowed_attributes
        sanitized_html = sanitizer.sanitize(self.body)
        return sanitized_html


class CreateAnswerForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    answer_body = RichTextFormField(config_name='normal',
                                    label='متن جواب',
                                    required=True,
                                    error_messages={'required': "متن جواب نمیتواند خالی باشد!"})

    def cleaned_body(self):
        sanitizer = Sanitizer()
        sanitizer.tags = allowed_tags
        sanitizer.attributes = allowed_attributes
        sanitized_html = sanitizer.sanitize(self.answer_body)
        return sanitized_html

    def cleaned_question_id(self):
        return self.question_id
