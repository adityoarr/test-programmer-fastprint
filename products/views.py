from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from .models import Produk
from .forms import ProdukForm

def produk_list(request):    
    produks = Produk.objects.filter(status__nama_status__iexact="bisa dijual").order_by('id_produk')
    return render(request, 'products/list.html', {'produks': produks})

def produk_create(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST)
        if form.is_valid():
            produk_baru = form.save(commit=False)
            max_id = Produk.objects.aggregate(Max('id_produk'))['id_produk__max']
            if max_id is None:
                produk_baru.id_produk = 1
            else:
                produk_baru.id_produk = max_id + 1
            produk_baru.save()
            return redirect('produk_list')
    else:
        form = ProdukForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'Tambah Produk'})

def produk_edit(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('produk_list')
    else:
        form = ProdukForm(instance=produk)
    return render(request, 'products/form.html', {'form': form, 'title': 'Edit Produk'})

def produk_delete(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    produk.delete()
    return redirect('produk_list')