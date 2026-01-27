import requests
import hashlib
from django.core.management.base import BaseCommand
from products.models import Produk, Kategori, Status
from datetime import datetime, timedelta, timezone

class Command(BaseCommand):
    help = 'Mengambil data dari API FastPrint dan menyimpannya ke database'

    def handle(self, *args, **kwargs):
        wib_zone = timezone(timedelta(hours=7))
        wib_time = datetime.now(wib_zone)
        
        username_date = wib_time.strftime("%d%m%y")
        hour = wib_time.strftime("%H")
        
        username = f"tesprogrammer{username_date}C{hour}"
        password_raw = f"bisacoding-{wib_time.strftime('%d')}-{wib_time.strftime('%m')}-{wib_time.strftime('%y')}"
        password_md5 = hashlib.md5(password_raw.encode()).hexdigest()

        self.stdout.write(f"Attempting connect with User: {username}")
        self.stdout.write(f"Attempting connect with Password-raw: {password_raw}")
        self.stdout.write(f"Attempting connect with Password-md5: {password_md5}")

        url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
        
        payload = {
            'username': username,
            'password': password_md5
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get('error') == 1:
                 self.stdout.write(self.style.ERROR(f"API Error: {data.get('ket', 'Unknown')}"))
                 return

            items = data.get('data', [])
            
            self.stdout.write(f"Berhasil mengambil {len(items)} data. Mulai menyimpan...")

            for item in items:
                if not item['nama_produk']:
                    continue

                kategori_obj, _ = Kategori.objects.get_or_create(
                    nama_kategori=item['kategori']
                )

                status_obj, _ = Status.objects.get_or_create(
                    nama_status=item['status']
                )

                harga_clean = str(item['harga']).replace('.', '').replace('Rp', '').strip()
                
                if not harga_clean.isdigit():
                    harga_clean = 0

                Produk.objects.update_or_create(
                    id_produk=int(item['id_produk']),
                    defaults={
                        'nama_produk': item['nama_produk'],
                        'harga': harga_clean,
                        'kategori': kategori_obj,
                        'status': status_obj
                    }
                )
            
            self.stdout.write(self.style.SUCCESS('Data berhasil disinkronisasi!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Terjadi kesalahan: {e}"))