from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Finder, Searcher
from django.http import HttpResponse
from django.db.models import Q
from django.db.models.functions import Lower, Trim

def finder_detail(request, pk):
    item = get_object_or_404(Finder, pk=pk)
    return render(request, 'finder_detail.html', {'item': item})

from django.shortcuts import render
from django.db.models import Q
from django.db.models.functions import Lower, Trim
from .models import Finder

def searcher(request):
    if request.method == "POST":
        
        name = request.POST.get("name", "").strip().lower()
        description = request.POST.get("description", "").strip().lower()
        location = request.POST.get("location", "").strip().lower()

        
        print("POST DATA:", request.POST)
        print("CLEAN INPUTS:", name, description, location)

        
        matches = Finder.objects.annotate(
            clean_name=Trim(Lower('name')),
            clean_description=Trim(Lower('description')),
            clean_location=Trim(Lower('location'))
        ).filter(
            
            Q(clean_name__icontains=name) &
            (Q(clean_description__icontains=description) | Q(clean_location__icontains=location))
        )

        
        print("MATCHES FOUND:", matches.count())

        return render(request, "searcher_result.html", {
            "name": name,
            "description": description,
            "location": location,
            "matches": matches
        })

    return render(request, "searcher.html")

def finder_contact(request, pk):
    
    item = get_object_or_404(Finder, pk=pk)
    
    
    posted_by = item.posted_by
    
    context = {
        "item": item,
        "posted_by": posted_by,
    }
    return render(request, "finder_contact.html", context)