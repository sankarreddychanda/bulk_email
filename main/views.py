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
            template = request.POST.get('content')
            print(template)
            subject = request.POST.get('subject')
            if subject is None or template is None:
                return HttpResponse('Please provide both subject and HTML content.')

            html_content_str = template


            for row in csv_data:
                email = row[0]
                name = row[0]

                # Prepare email data using the selected template
                context = {
                    'name': name,
                    'subject': subject
                }
                html_content = html_content_str

                data = {
                    'from': 'Steve Anderson  steve@affluencebizdata.com',
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

    return render(request, 'send_mass_mail_list.html')


def dashboard(request):
    return render(request,'dashboard.html')
# def summernote(request):
#     return render(request,'email_template.html')



def summernote(request):
    if request.method == 'POST':
        selected_template = request.POST.get('template')

        if selected_template:
            # Render the template below the form
            return render(request, 'email_template.html', {'selected_template': selected_template})

    # Return the initial form view if no template is selected or the request method is not POST
    return render(request, 'email_template.html')
