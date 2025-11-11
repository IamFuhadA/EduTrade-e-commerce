from django.core.management.base import BaseCommand
from django.utils.text import slugify
from EduApp.models import Category, Book, Accessory
from django.core.files.base import ContentFile
from django.conf import settings
import io
from PIL import Image


class Command(BaseCommand):
    help = "Seed initial Categories, Books, and Accessories"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding data..."))

        def make_placeholder_png(size=(300, 300), color=(200, 200, 200)):
            img = Image.new("RGB", size, color)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return ContentFile(buf.getvalue())

        def assign_image_if_missing(instance, field_name: str, filename_slug: str, base_color=(200, 200, 200)):
            field = getattr(instance, field_name, None)
            if field and not field.name:
                content = make_placeholder_png(color=base_color)
                safe_name = f"{slugify(filename_slug) or 'image'}.png"
                field.save(safe_name, content, save=False)
                instance.save(update_fields=[field_name])

        categories = [
            {"name": "Fiction", "description": "Fictional literature"},
            {"name": "Non-Fiction", "description": "Informative and factual"},
            {"name": "Science", "description": "Science and research"},
            {"name": "Kids", "description": "Children's books"},
            {"name": "Technology", "description": "Computers and technology"},
            {"name": "Stationery", "description": "School supplies and stationery"},
        ]

        created_categories = {}
        for c in categories:
            slug = slugify(c["name"])[:160]
            obj, created = Category.objects.get_or_create(
                name=c["name"],
                defaults={"slug": slug, "description": c.get("description", "")},
            )
            # ensure slug is set if existing without slug
            if not obj.slug:
                obj.slug = slug
                obj.save(update_fields=["slug"])
            # seed icon if missing
            assign_image_if_missing(obj, "icon", filename_slug=f"{obj.name}-icon", base_color=(150, 200, 255))
            created_categories[obj.name] = obj
            self.stdout.write(f"Category {'created' if created else 'exists'}: {obj.name}")

        books = [
            {"category": "Science", "title": "Physics Essentials", "author": "R. Kumar", "publisher": "EduPress", "price": 799.00},
            {"category": "Science", "title": "Chemistry Workbook Grade 10", "author": "S. Patel", "publisher": "LabLearn", "price": 649.00},
            {"category": "Science", "title": "Biology Concepts", "author": "T. Mehta", "publisher": "GreenLeaf", "price": 720.00},
            {"category": "Technology", "title": "Introduction to Python", "author": "A. Verma", "publisher": "CodeWorks", "price": 950.00},
            {"category": "Technology", "title": "Web Development Basics", "author": "N. Shah", "publisher": "TechEdu", "price": 880.00},
            {"category": "Technology", "title": "Data Structures Illustrated", "author": "V. Rao", "publisher": "AlgoPub", "price": 1020.00},
            {"category": "Non-Fiction", "title": "World History Overview", "author": "K. Das", "publisher": "Knowledge House", "price": 700.00},
            {"category": "Non-Fiction", "title": "Geography Atlas Student Edition", "author": "M. Nair", "publisher": "MapWorks", "price": 560.00},
            {"category": "Non-Fiction", "title": "Mathematics Grade 9", "author": "P. Gupta", "publisher": "NumberOne", "price": 690.00},
            {"category": "Non-Fiction", "title": "Mathematics Grade 10", "author": "P. Gupta", "publisher": "NumberOne", "price": 710.00},
            {"category": "Science", "title": "Astronomy for Beginners", "author": "L. Iyer", "publisher": "SkyLine", "price": 630.00},
            {"category": "Science", "title": "Environmental Science", "author": "H. Roy", "publisher": "EarthPub", "price": 675.00},
            {"category": "Kids", "title": "Times Tables Practice", "author": "Bright Team", "publisher": "BrightKids", "price": 250.00},
            {"category": "Kids", "title": "Phonics Starter", "author": "Bright Team", "publisher": "BrightKids", "price": 260.00},
            {"category": "Kids", "title": "Science Experiments for Kids", "author": "A. Joy", "publisher": "PlayLearn", "price": 340.00},
            {"category": "Technology", "title": "Django for Beginners", "author": "W. Dev", "publisher": "CodeWorks", "price": 999.00},
            {"category": "Technology", "title": "Computer Networks Simplified", "author": "S. Bhat", "publisher": "NetPub", "price": 890.00},
            {"category": "Technology", "title": "Database Systems 101", "author": "R. Singh", "publisher": "DataHouse", "price": 940.00},
            {"category": "Non-Fiction", "title": "English Grammar Guide", "author": "J. Thomas", "publisher": "LangWorks", "price": 520.00},
            {"category": "Non-Fiction", "title": "Essay Writing Workbook", "author": "J. Thomas", "publisher": "LangWorks", "price": 480.00},
            {"category": "Science", "title": "Statistics Made Easy", "author": "C. Menon", "publisher": "StatPress", "price": 590.00},
            {"category": "Science", "title": "Algebra Refresher", "author": "P. Kumar", "publisher": "NumberOne", "price": 560.00},
            {"category": "Science", "title": "Geometry Essentials", "author": "P. Kumar", "publisher": "NumberOne", "price": 570.00},
            {"category": "Science", "title": "Trigonometry Crash Course", "author": "V. Jain", "publisher": "NumberOne", "price": 585.00},
            {"category": "Non-Fiction", "title": "Economics Basics", "author": "S. Rao", "publisher": "SocioPub", "price": 640.00},
            {"category": "Non-Fiction", "title": "Civics and Society", "author": "D. Pillai", "publisher": "SocioPub", "price": 610.00},
            {"category": "Science", "title": "Practical Physics Lab Manual", "author": "R. Kumar", "publisher": "EduPress", "price": 620.00},
            {"category": "Science", "title": "Organic Chemistry Guide", "author": "S. Patel", "publisher": "LabLearn", "price": 760.00},
            {"category": "Science", "title": "Human Anatomy Illustrated", "author": "T. Mehta", "publisher": "GreenLeaf", "price": 980.00},
            {"category": "Non-Fiction", "title": "Study Skills and Time Management", "author": "A. Bose", "publisher": "FocusPress", "price": 450.00},
            {"category": "Non-Fiction", "title": "Exam Strategies Handbook", "author": "A. Bose", "publisher": "FocusPress", "price": 460.00},
        ]

        for b in books:
            obj, created = Book.objects.get_or_create(
                title=b["title"],
                defaults={
                    "category": b["category"],
                    "author": b.get("author", ""),
                    "publisher": b.get("publisher", ""),
                    "price": b.get("price"),
                    "description": b.get("description", ""),
                },
            )
            # seed cover image if missing
            assign_image_if_missing(obj, "cover_image", filename_slug=f"{obj.title}-cover", base_color=(220, 180, 180))
            self.stdout.write(f"Book {'created' if created else 'exists'}: {obj.title}")

        accessories = [
            {"category": "Stationery", "name": "A4 Spiral Notebook", "brand": "NoteMate", "price": 120.00, "specs": "200 pages, ruled"},
            {"category": "Stationery", "name": "A5 Pocket Notebook", "brand": "NoteMate", "price": 80.00, "specs": "120 pages, plain"},
            {"category": "Stationery", "name": "Ballpoint Pens (Pack of 10)", "brand": "WriteOn", "price": 150.00, "specs": "0.7mm blue"},
            {"category": "Stationery", "name": "Gel Pens (Pack of 5)", "brand": "WriteOn", "price": 130.00, "specs": "0.5mm assorted"},
            {"category": "Stationery", "name": "Highlighters (Pack of 6)", "brand": "MarkIt", "price": 199.00, "specs": "Pastel colors"},
            {"category": "Stationery", "name": "Erasers (Pack of 4)", "brand": "CleanSlate", "price": 60.00, "specs": "Dust-free"},
            {"category": "Stationery", "name": "Pencil Sharpener", "brand": "SharpPro", "price": 55.00, "specs": "Double hole"},
            {"category": "Stationery", "name": "Mechanical Pencil", "brand": "WriteOn", "price": 110.00, "specs": "0.5mm"},
            {"category": "Stationery", "name": "Ruler 30cm", "brand": "ClassKit", "price": 40.00, "specs": "Transparent"},
            {"category": "Stationery", "name": "Geometry Box", "brand": "ClassKit", "price": 220.00, "specs": "Compass, protractor, set squares"},
            {"category": "Stationery", "name": "Sticky Notes (Pack)", "brand": "NoteMate", "price": 90.00, "specs": "3x3, assorted"},
            {"category": "Stationery", "name": "Index Cards (Pack of 100)", "brand": "NoteMate", "price": 85.00, "specs": "3x5, ruled"},
            {"category": "Stationery", "name": "Binder A4", "brand": "FilePro", "price": 180.00, "specs": "2-ring"},
            {"category": "Stationery", "name": "Binder Dividers", "brand": "FilePro", "price": 70.00, "specs": "Set of 10"},
            {"category": "Stationery", "name": "Document Sleeves (Pack of 50)", "brand": "FilePro", "price": 160.00, "specs": "A4 clear"},
            {"category": "Stationery", "name": "Backpack Student", "brand": "EduGear", "price": 1199.00, "specs": "Water-resistant, 25L"},
            {"category": "Stationery", "name": "Lunch Box", "brand": "EduGear", "price": 350.00, "specs": "BPA-free"},
            {"category": "Stationery", "name": "Water Bottle 1L", "brand": "EduGear", "price": 299.00, "specs": "Steel"},
            {"category": "Technology", "name": "USB Flash Drive 32GB", "brand": "TechLine", "price": 499.00, "specs": "USB 3.0"},
            {"category": "Technology", "name": "Over-Ear Headphones", "brand": "SoundStudy", "price": 1099.00, "specs": "Wired, noise-reducing"},
            {"category": "Technology", "name": "Scientific Calculator", "brand": "CalcPro", "price": 899.00, "specs": "FX-991 equivalent"},
            {"category": "Science", "name": "Microscope Starter Kit", "brand": "LabLearn", "price": 3499.00, "specs": "Up to 600x"},
            {"category": "Science", "name": "Dissection Kit", "brand": "LabLearn", "price": 799.00, "specs": "11 tools"},
            {"category": "Science", "name": "Periodic Table Wall Chart", "brand": "ClassKit", "price": 299.00, "specs": "Laminated A2"},
            {"category": "Kids", "name": "Crayons (Pack of 24)", "brand": "ArtKid", "price": 140.00, "specs": "Non-toxic"},
            {"category": "Kids", "name": "Washable Markers (Pack of 12)", "brand": "ArtKid", "price": 180.00, "specs": "Broad tip"},
            {"category": "Kids", "name": "Drawing Book A3", "brand": "ArtKid", "price": 120.00, "specs": "40 pages"},
            {"category": "Stationery", "name": "Desk Planner Weekly", "brand": "PlanRight", "price": 199.00, "specs": "Undated"},
            {"category": "Stationery", "name": "Whiteboard Markers (Pack of 4)", "brand": "MarkIt", "price": 160.00, "specs": "Assorted"},
            {"category": "Stationery", "name": "Mini Whiteboard A4", "brand": "ClassKit", "price": 220.00, "specs": "With eraser"},
            {"category": "Stationery", "name": "Stapler Medium", "brand": "OfficeGo", "price": 190.00, "specs": "With staples"},
            {"category": "Stationery", "name": "Pencil Case", "brand": "EduGear", "price": 160.00, "specs": "Zipper, large"},
        ]

        for a in accessories:
            obj, created = Accessory.objects.get_or_create(
                name=a["name"],
                defaults={
                    "category": a["category"],
                    "brand": a.get("brand", ""),
                    "price": a.get("price"),
                    "specs": a.get("specs", ""),
                },
            )
            if created:
                self.stdout.write(f"Accessory created: {obj.name}")
            else:
                updated = False
                if obj.category != a["category"]:
                    obj.category = a["category"]
                    updated = True
                if obj.brand != a.get("brand", obj.brand):
                    obj.brand = a.get("brand", obj.brand)
                    updated = True
                if a.get("price") is not None and obj.price != a.get("price"):
                    obj.price = a.get("price")
                    updated = True
                if obj.specs != a.get("specs", obj.specs):
                    obj.specs = a.get("specs", obj.specs)
                    updated = True
                if updated:
                    obj.save()
                    self.stdout.write(f"Accessory updated: {obj.name}")
                else:
                    self.stdout.write(f"Accessory exists: {obj.name}")
            # seed accessory image if missing
            assign_image_if_missing(obj, "image", filename_slug=f"{obj.name}-image", base_color=(180, 200, 180))

        self.stdout.write(self.style.SUCCESS("Seeding completed."))

