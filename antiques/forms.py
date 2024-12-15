from django import forms
from .models import Antique, Category

class AntiqueForm(forms.ModelForm):
    class Meta:
        model = Antique
        fields = ['title', 'slug', 'image', 'maker', 'description', 'category', 'origin', 'material', 'year_made', 'condition', 'price', 'stocks', 'stocks_available']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Set queryset untuk field kategori
            self.fields['category'].queryset = Category.objects.all()