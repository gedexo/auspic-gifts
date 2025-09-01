from django.core.management.base import BaseCommand
from products.models import City, Pincode

KERALA_PINCODES = [
    # Format: {"city": "City Name", "pincode": "Pincode"}
    {"city": "Thiruvananthapuram", "pincode": "695001"},
    {"city": "Thiruvananthapuram", "pincode": "695002"},
    {"city": "Thiruvananthapuram", "pincode": "695003"},
    {"city": "Thiruvananthapuram", "pincode": "695004"},
    {"city": "Kollam", "pincode": "691001"},
    {"city": "Kollam", "pincode": "691002"},
    {"city": "Kollam", "pincode": "691003"},
    {"city": "Alappuzha", "pincode": "688001"},
    {"city": "Alappuzha", "pincode": "688002"},
    {"city": "Alappuzha", "pincode": "688003"},
    {"city": "Kottayam", "pincode": "686001"},
    {"city": "Kottayam", "pincode": "686002"},
    {"city": "Kottayam", "pincode": "686003"},
    {"city": "Ernakulam", "pincode": "682001"},
    {"city": "Ernakulam", "pincode": "682002"},
    {"city": "Ernakulam", "pincode": "682003"},
    {"city": "Thrissur", "pincode": "680001"},
    {"city": "Thrissur", "pincode": "680002"},
    {"city": "Thrissur", "pincode": "680003"},
    {"city": "Palakkad", "pincode": "678001"},
    {"city": "Palakkad", "pincode": "678002"},
    {"city": "Palakkad", "pincode": "678003"},
    {"city": "Malappuram", "pincode": "676505"},
    {"city": "Malappuram", "pincode": "676506"},
    {"city": "Malappuram", "pincode": "676507"},
    {"city": "Kozhikode", "pincode": "673001"},
    {"city": "Kozhikode", "pincode": "673002"},
    {"city": "Kozhikode", "pincode": "673003"},
    {"city": "Wayanad", "pincode": "673121"},
    {"city": "Wayanad", "pincode": "673122"},
    {"city": "Wayanad", "pincode": "673123"},
    {"city": "Kannur", "pincode": "670001"},
    {"city": "Kannur", "pincode": "670002"},
    {"city": "Kannur", "pincode": "670003"},
    {"city": "Kasaragod", "pincode": "671121"},
    {"city": "Kasaragod", "pincode": "671122"},
    {"city": "Kasaragod", "pincode": "671123"},
]

class Command(BaseCommand):
    help = "Load Kerala cities and pincodes"

    def handle(self, *args, **kwargs):
        for entry in KERALA_PINCODES:
            city, created = City.objects.get_or_create(name=entry["city"])

            # Add pincodes only if they don't exist
            if not Pincode.objects.filter(city=city, code=entry["pincode"]).exists():
                Pincode.objects.create(city=city, code=entry["pincode"])
                self.stdout.write(self.style.SUCCESS(f"✅ Added {entry['pincode']} - {city.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Skipping duplicate: {entry['pincode']}"))
