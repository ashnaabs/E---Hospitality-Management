from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages
from . models import *
from . forms import *
import stripe
from Eproject import settings
from django.urls import reverse


# Create your views here.
def patient_reg(request):
    det=Registration.objects.all()
    if request.method=='POST':
        form=RegisterForm(request.POST,files=request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('reg_list')
    else:
        form=RegisterForm()

    return render(request,'reg.html',{'form':form,'det':det})

def login_patient(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data['patient_name']
            try:
                user = Registration.objects.get(patient_name=patient_name)
                # Assuming login is successful, redirect to history_list
                return redirect('history_list_id',patient_name=user.patient_name)  # Redirect to a success page.
            except Registration.DoesNotExist:
                messages.error(request, 'Invalid patient name')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def login_patient_slot(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data['patient_name']
            try:
                user = Registration.objects.get(patient_name=patient_name)
                patient_names = request.session.get('patient_names', [])
                if patient_name not in patient_names:
                    patient_names.append(patient_name)

                request.session['patient_names'] = patient_names
                # Assuming login is successful, redirect to history_list
                request.session['patient_name'] = patient_name
                return redirect('user_list')  # Redirect to a success page.
            except Registration.DoesNotExist:
                messages.error(request, 'Invalid patient name')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def patient_reg_list(request):
    det1=Registration.objects.all()

    return render(request,'reg_list.html',{'det1':det1})

def admin_patient_reg_list(request):
    det1=Registration.objects.all()

    return render(request,'admin_reg_list.html',{'det1':det1})

def deletebook(request,book_id):
    set1=Registration.objects.get(id=book_id)
    if request.method=='POST':
        set1.delete()
        return redirect('reg_list')

    return render(request,'deletebook.html',{'set1':set1})

def createdoctor(request):
    if request.method=='POST':
        form=DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('slot')


    else:

        form=DoctorForm()

    return render(request,'doctor.html',{'form':form})

def slots(request):
    det2=Slots.objects.all()
    if request.method=='POST':
        form=SlotForm(request.POST,files=request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form=SlotForm()

    return render(request,'slot.html',{'form':form,'det2':det2})

def slot_list(request):
    det3=Slots.objects.all()

    return render(request,'slot_list.html',{'det3':det3})

def user_slot_list(request):
    patient_name = request.session.get('patient_name')
    det3=Slots.objects.all()
    det1 = Registration.objects.all()

    return render(request,'user_slot_list.html',{'det3':det3,'det1':det1,'patient_name':patient_name})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Slots, Registration

def slot_list_result(request, doc_id, patient_name):
    det4 = get_object_or_404(Slots, id=doc_id)
    det1 = get_object_or_404(Registration, patient_name=patient_name)

    # Retrieve or initialize the session data for appointments
    appointments = request.session.get('appointments', [])
    print(f"Slot details: {det4}")
    print(f"Doctor associated with slot: {det4.doctor}")
    print(f"Doctor's name: {det4.doctor.doctor}")

    # Create an appointment record with necessary information
    appointment_info = {
        'patient_name': patient_name,
        'doctor': str(det4.doctor),  # Store the doctor's name as a string
        'date': str(det4.date)  # Convert the date to a string
    }

    # Append the new appointment
    appointments.append(appointment_info)

    # Save the updated appointments list back to the session
    request.session['appointments'] = appointments

    return render(request, 'slot_list_result.html', {
        'det4': det4,
        'patient_name': patient_name
    })





def patient_list(request):
    # Retrieve the session data
    appointments = request.session.get('appointments', [])

    return render(request, 'patient_list.html', {
        'appointments': appointments
    })


def admin_patient_list(request):
    # Retrieve the session data
    appointments = request.session.get('appointments', [])

    return render(request, 'admin_patient_list.html', {
        'appointments': appointments
    })



def slot_whole_list(request):
    patient_names = request.session.get('patient_names', [])
    return render(request, 'slot_whole_list.html', {'patient_names': patient_names})


def history_medical(request):
    det6=history.objects.all()
    if request.method=='POST':
        form=HistoryForm(request.POST,files=request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('history_list')
    else:
        form=HistoryForm()

    return render(request,'history.html',{'form':form,'det6':det6})

def payment(request):
    patient_name = request.session.get('patient_name')
    return render(request,'payment.html',{'patient_name':patient_name})

def hist_list(request):
    slot = Slots.objects.first()
    det6=history.objects.all()

    paginator = Paginator(det6, 1)  # to set how many objects need to be set on a page
    page_number = request.GET.get('page')  # retrieves page number from parameter 'page'
    try:
        page = paginator.get_page(page_number)  # attempts to retrieve the requested page from the Paginator.

    except EmptyPage:  # If the requested page number is invalid (e.g., beyond the total number of pages), an EmptyPage exception is caught.
        page = paginator.page(
            page_number.num_pages)  # In case of an EmptyPage exception, it retrieves the last available page instead (assuming page_number is an integer or convertible to one).


    return render(request,'history_list.html',{'det6':det6,'slot':slot,'page':page})

def updatehistory(request,pat_id):
    his = history.objects.get(id=pat_id)
    if request.method=='POST':
        form = HistoryForm(request.POST,request.FILES,instance=his)

        if form.is_valid():

            form.save()

            return redirect('history_list')
    else:
        form=HistoryForm(instance=his)

    return render(request,'updatehistory.html',{'form':form})

def update_slot(request,pat_id):
    his = Slots.objects.get(id=pat_id)
    if request.method=='POST':
        form = SlotForm(request.POST,request.FILES,instance=his)

        if form.is_valid():

            form.save()

            return redirect('list')
    else:
        form=SlotForm(instance=his)

    return render(request,'update_slot.html',{'form':form})

def delete_slot(request,pat_id):
    his=Slots.objects.get(id=pat_id)
    if request.method=='POST':
        his.delete()
        return redirect('list')

    return render(request,'delete_slot.html',{'his':his})

def prescription(request):
    det6=history.objects.all()
    return render(request, 'prescription.html', {'det6':det6})


def hist_list_id(request,patient_name):

    det6=history.objects.get(patient_name=patient_name)


    return render(request,'history_list_id.html',{'det6':det6})

def login_patient_payment(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data['patient_name']
            try:
                user = Registration.objects.get(patient_name=patient_name)
                patient_names = request.session.get('patient_names', [])

                if patient_name not in patient_names:
                    patient_names.append(patient_name)

                request.session['patient_names'] = patient_names
                # Assuming login is successful, redirect to history_list
                request.session['patient_name'] = patient_name

                # Assuming login is successful, redirect to history_list
                return redirect('billing')  # Redirect to a success page.
            except Registration.DoesNotExist:
                messages.error(request, 'Invalid patient name')
    else:
        form = LoginForm()


    return render(request, 'login.html', {'form': form})





import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def process_payment(request):
    patient_name = request.session.get('patient_name')
    patient_names = request.session.get('patient_names', [])

    if patient_name not in patient_names:
        patient_names.append(patient_name)

    request.session['patient_names'] = patient_names

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = int(form.cleaned_data['amount'] * 100)  # Convert to cents

            try:
                # Step 1: Create a PaymentIntent
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency='inr',
                    payment_method_types=['card'],
                )

                payment_amount = float(form.cleaned_data['amount'])
                payments = request.session.get('payments', [])

                # Store the payment info (patient name and amount) in the session
                payment_info = {'patient_name': patient_name, 'amount': payment_amount}
                payments.append(payment_info)
                request.session['payments'] = payments

                # Step 2: Confirm the PaymentIntent on the client side with the client secret
                return render(request, 'payment_confirmation.html', {
                    'client_secret': payment_intent['client_secret'],
                    'amount': form.cleaned_data['amount'],
                    'patient_name': patient_name,
                    'payments': payments,
                })
            except stripe.error.CardError as e:
                return redirect('payment_failed')
    else:
        form = PaymentForm()

    return render(request, 'make_payment.html', {'form': form, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, 'patient_name': patient_name})


def payment_success(request):

    patient_name = request.session.get('patient_name')
    amount = request.session.get('amount')

    patient_names = request.session.get('patient_names', [])
    amounts = request.session.get('amounts', [])



    if patient_name not in patient_names:
        patient_names.append(patient_name)

    if amount not in amounts:
        amounts.append(amount)

    request.session['patient_names'] = patient_names
    # Assuming login is successful, redirect to history_list
    request.session['patient_name'] = patient_name
    request.session['amount'] = amount

    return render(request, 'payment_confirmation.html', {'patient_name': patient_name,'patient_names':patient_names,'amount':amount})


def payment_success2(request):
    patient_name = request.session.get('patient_name')
    amount = request.session.get('amount')
    patient_names = request.session.get('patient_names', [])
    amounts=request.session.get('amounts',[])

    if patient_name not in patient_names:
        patient_names.append(patient_name)

    request.session['patient_names'] = patient_names
    # Assuming login is successful, redirect to history_list
    request.session['patient_name'] = patient_name

    if amount not in amounts:
        amounts.append(amount)

    request.session['amounts']=amounts
    request.session['amount']=amount

    return render(request, 'payment_success.html', {
        'patient_name': patient_name,'patient_names':patient_names,'amounts':amounts,'amount':amount
    })



def payment_error(request):
    return render(request, 'payment_error.html')


def payment_list(request):
    # Retrieve the session data
    payments = request.session.get('payments', [])

    return render(request, 'payment_list.html', {'payments': payments})

def admin_payment_list(request):
    # Retrieve the session data
    payments = request.session.get('payments', [])

    return render(request, 'admin_payment_list.html', {'payments': payments})



def appointment(request):
    return render(request,'app.html')

def medical_hist(request):
    return render(request,'hist.html')

def bill_payment(request):
    return render(request,'pay.html')

def Index(request):
    return render(request,'index.html')

def Index2(request):
    return render(request,'index2.html')

def doctor_index(request):
    return render(request,'doctor_index.html')

def admin_index(request):
    return render(request,'admin_index.html')

def pharmacy(request):
    return render(request,'pharm.html')

def pharm_success(request):
    return render(request,'pharm_success.html')

def admin_user_send(request,patient_name):
    return render(request,'admin_user_send.html',{'patient_name':patient_name})

def admin_mail_box(request,patient_name):
    return render(request,'admin_mail_box.html',{'patient_name':patient_name})

def admin_mail_result(request,patient_name):
    return render(request,'admin_mail_result.html',{'patient_name':patient_name})

def admin_panel(request):
    adm=admin_resource.objects.all()
    if request.method=='POST':
        form=AdminForm(request.POST,files=request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('resource')
    else:
        form=AdminForm()

    return render(request,'admin_resource.html',{'form':form,'adm':adm})

def resource(request):
    adm=admin_resource.objects.all()
    return render(request,'admin_index2.html',{'adm':adm})

def update_resource(request,ad_id):
    ad = admin_resource.objects.get(id=ad_id)
    if request.method=='POST':
        form = AdminForm(request.POST,request.FILES,instance=ad)

        if form.is_valid():

            form.save()

            return redirect('resource')
    else:
        form=AdminForm(instance=ad)

    return render(request,'update_resource.html',{'form':form})

def patient_resource(request):
    adm=admin_resource.objects.all()
    return render(request,'patient_health_resource.html',{'adm':adm})