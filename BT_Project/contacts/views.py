from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
# Create your views here.

def contact(request):
    if request.method == 'POST':
        listing_id = request.POST.get('listing_id')
        listing = request.POST.get('listing')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        user_id = request.POST.get('user_id')
        realtor_email = request.POST.get('realtor_email')


        #Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id = listing_id , user_id = user_id)
            if has_contacted:
                messages.error(request , 'You have already made inquiry for this listing')
                return redirect('/listings/'+listing_id)
        contact = Contact(listing = listing , listing_id = listing_id , name = name , emaiil= email , phone = phone ,message = message, user_id = user_id)

        contact.save()

        #Send email
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for '+ listing + '. Sign in into admin panel for more info',
            'jasonroy9978@gmail.com'
            [realtor_email,'techguyinfo@gmail.com'],
            fail_silently=False
        )

        messages.success(request , 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/'+ listing_id)

