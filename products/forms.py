from django import forms
from .models import Produk

class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']
        widgets = {
            'nama_produk': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'harga': forms.NumberInput(attrs={
                'class': 'form-control', 
                'required': True,
                'min': '0',
                'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57)'
            }),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_harga(self):
        harga = self.cleaned_data.get('harga')
        if harga < 0:
            raise forms.ValidationError("Harga tidak boleh minus")
        return harga