from django import forms
from core.models import Product,Category

class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Title'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'$'}))
    old_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'$'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Product Description'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Type'}))
    mfd = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local','placeholder':'eg: 20-11-20','class':'form-control'}))    
    specifications = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter Product Specifications'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Tags'}))
    stock_count = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Stock Count'}))
    life = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Product Life'}))
    digital = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Choose a category",
        required=True
    )
    class Meta:
        model=Product
        fields=[
            'title',
            'old_price',
            'price',
            'image',
            'description',
            'type',
            'mfd',
            'specifications',
            'tags',
            'stock_count',
            'life',
            'digital',
            'category'
        ]