from django import forms
from .models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    extra_image_1 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    extra_image_2 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    extra_image_3 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    extra_image_4 = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def save_extra_images(self, product):
        for i in range(1, 5):
            img = self.cleaned_data.get(f'extra_image_{i}')
            if img:
                ProductImage.objects.create(product=product, image=img)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
