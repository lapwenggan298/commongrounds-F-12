from django import forms

from .models import Book, BookReview

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment', 'user_review', 'anon_reviewer']
        #widgets = {'anon_reviewer': forms.HiddenInput()}


    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['user_review'].initial = user_profile
            self.fields['user_review'].disabled = True
            self.fields['anon_reviewer'].widget = forms.HiddenInput()
            self.fields['anon_reviewer'].required = False
        else:
            self.fields['user_review'].required = False
            self.fields['user_review'].widget = forms.HiddenInput()
            self.fields['anon_reviewer'].initial = "Anonymous"
            self.fields['anon_reviewer'].disabled = True


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'synopsis', 'genre', 'available_to_borrow', 'contributor',]


    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['contributor'].initial = user_profile
            self.fields['contributor'].disabled = True


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['contributor']


class BookFormFactory:
    @classmethod
    def getForm(cls, context):
        forms_map = {
            "review": BookReviewForm,
            "contribute": BookContributeForm,
            "update": BookUpdateForm,
        }
        return forms_map.get(context)