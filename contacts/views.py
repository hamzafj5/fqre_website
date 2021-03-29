from django.shortcuts import render, redirect
from .models import Contact
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method=='POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted=Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:   
                messages.error(request,'Your already made an inquiry on this listing.')
                return redirect('listing/'+listing_id)

        contact=Contact(listing=listing, listing_id=listing_id,name=name, email=email, phone=phone,message=message,user_id=user_id)

        contact.save()

        #send mail
        send_mail(
            'Property Listing Inquiry',
            'There has been an inquiry for '+ listing +'. Sign into the admin panel for more info.',
            'f2016266069@umt.edu.pk', #the email where mail will be sent from
            [realtor_email,'hamzafayyaz97@gmail.com'],
            fail_silently=False
        )

        messages.success(request,'Your request has been sub,itted. Someone will get back to you shortly.')
        return redirect('/listing/'+listing_id)