from django.shortcuts import render

# Create your views here.



import csv
import requests

from massmail import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

def send_mass_mail_confirm(request):
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

            # Get the selected template from the form data
            template = request.POST.get('template')
            subject = request.POST.get('subject')
            if template in('',None):
                return HttpResponse('please select template')
            if subject in('',None):
                return HttpResponse('please select subject')


            for row in csv_data:
                email = row[0]
                name = row[0]

                # Prepare email data using the selected template
                context = {
                    'name': name,
                    'subject': subject
                }
                html_content = render_to_string(template, context)

                data = {
                    'from': 'Steve Parker  steve@affluencebizdata.com',
                    'to': email,
                    'subject': subject,
                    'html': html_content
                }

                # Send email using Mailgun API
                response = requests.post(
                    f'https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages',
                    auth=('api', settings.MAILGUN_API_KEY),
                    data=data
                )

                if response.status_code == 200:
                    print(f'Successfully sent email to {email}')
                else:
                    print(f'Error sending email to {email}: {response.content}')

            return HttpResponseRedirect('/success/')

    return render(request, 'send_mass_mail.html')



def success(request):
    return HttpResponse('success')


def send_mass_mail(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']

        csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())

        # Display email list in template
        email_list = []
        for row in csv_data:
            email_list.append(row[0])

        context = {
            'email_list': email_list,
            'csv_file': csv_file,
        }

        return render(request, 'home.html', context)

    return render(request, 'send_mass_mail.html')


def dashboard(request):
    return render(request,'dashboard.html')