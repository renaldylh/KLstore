from django import forms
from .models import Antique
from category.models import Category

class AntiqueForm(forms.ModelForm):
    class Meta:
        model = Antique
        fields = ['title', 'slug', 'image', 'maker', 'description', 'category',
                  'origin', 'material', 'year_made', 'condition', 'price',
                  'stocks', 'stocks_available']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Antique Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}),
            'stocks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Stocks'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for category to all available categories
        self.fields['category'].queryset = Category.objects.all()

        # Set default value for category if this is an update form (if instance has pk)
        if self.instance and self.instance.pk:
            self.fields['category'].initial = self.instance.category
