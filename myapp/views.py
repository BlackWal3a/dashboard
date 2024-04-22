from django.shortcuts import render,redirect,HttpResponse
from django.db import IntegrityError
from .models import Invoice , UnitConversion, DeliveryOrder,Account,ExchangeRates
import pandas as pd
from datetime import datetime
from .functions import convert_quantity,get_initials_with_dots, from_unitcode_to_unitname,generate_textual_interpretation
from django.http import JsonResponse,HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import urllib.parse
from decimal import Decimal
from .forms import UnitForm,DateRangeForm,DateGeoRangeForm,CurrencyForm,SupplierDateRangeForm
#import auth
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login,logout
# Register your custom user model with Django admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.forms import NoteForm

@login_required
def edit_notes(request):
    account = request.user.account  # Assuming user has an associated Account object
    form = NoteForm(request.POST or None, instance=account)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or desired URL

    context = {
        'form': form,
    }
    return render(request, 'edit_notes.html', context)

#Save_Incoming Data
@csrf_exempt
@login_required
def save_date_view(request):
    if request.method == 'POST':
        # Handle tint data
        tint_value = request.POST.get('tint')
        print("Received tint value:", tint_value)
        if tint_value is not None:
            request.user.account.geography_global_selection = tint_value

        #Handle Dark Mode
        darkmode_value = request.POST.get('mode')
        print("Received mode value:", darkmode_value)
        if darkmode_value is not None:
            request.user.account.dark_mode = darkmode_value


        # Handle Geography filters
        geo_filter_id = request.POST.get('geo_id')
        print("Received id value:", geo_filter_id)
        if geo_filter_id is not None:
            request.user.account.geography_filter_id = geo_filter_id

        # Handle time_global_selection filter
        time_global_selection = request.POST.get('time_filter')
        print("Received id value:", time_global_selection)
        if time_global_selection is not None:
            request.user.account.time_global_selection = time_global_selection
           
        # Handle time_chart filter
        time_chart_filter = request.POST.get('chart_type')
        print("Received id value:", time_chart_filter)
        if time_chart_filter is not None:
            request.user.account.time_chart_type = time_chart_filter
             
        # Save the data to the database
        request.user.account.save(update_fields=['geography_global_selection'])

        # Handle form if needed
        form = DateRangeForm(request.POST, instance=request.user.account)
        if form.is_valid():
            form.save()  # Save the form without specifying fields
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@csrf_exempt
def save_geo_date(request):
    if request.method == 'POST':
        form = DateGeoRangeForm(request.POST, instance=request.user.account)

        if form.is_valid():
            form.save()  # Save the form without specifying fields
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

from django.http import JsonResponse

@csrf_exempt 
def save_supplier_date(request):
    if request.method == 'POST':
        form = SupplierDateRangeForm(request.POST, instance=request.user.account)

        if form.is_valid():
            form.save()  # Save the form without specifying fields
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Account  # Import your Account model

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def createaccount_view(request):
    if request.method == 'POST':
        uname = request.POST.get('name1')
        email = request.POST.get('email1')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if uname == "" or email == "" or password1 == "" or password2 == "":
            error_msg = 'Please fill all fields'
            return render(request, 'profile.html', {'error': error_msg})

        if password1 != password2:
            error_msg = 'Passwords do not match.'
            return render(request, 'profile.html', {'error': error_msg})

        if User.objects.filter(email=email).exists():
            error_msg = 'Email is already in use.'
            return render(request, 'profile.html', {'error': error_msg})

        if User.objects.filter(username=uname).exists():
            error_msg = 'Username is already in use.'
            return render(request, 'profile.html', {'error': error_msg})

        # Create User object
        my_user = User.objects.create_user(uname, email, password1, last_name="LT")

        # Create associated Account object
        account = Account.objects.create(user=my_user)

        # Set the unit to "LT" for the newly created account
        account.units = "LT"
        account.currency = "TND"
        account.geography_global_selection = 1
        account.suppliers_global_selection = 1
        account.dark_mode = 0
        account.time_global_selection = 1
        account.time_chart_type = 1 
        account.save()

        # Pass the created username and password to the template
        return render(request, 'profile.html', {'success': True, 'username': uname, 'password': password1})

    return render(request, 'profile.html')

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')  # Get the value of Remember Me checkbox

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Set session expiry based on Remember Me checkbox
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days expiry
            else:
                request.session.set_expiry(0)  # Browser session expiry
            return redirect('dashboard')  # Redirect to the profile page
        else:
            # Display an error message on the sign-in page
            return render(request, 'sign-in.html', {'error': True})

    return render(request, 'sign-in.html')

#Receive Invoices data
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # Get the raw data from the request body
            raw_data = request.body.decode('utf-8')
        
            # Convert the URL query string to JSON format
            decoded_data = urllib.parse.parse_qs(raw_data)
            
            # Convert the dictionary into a JSON object
            json_data = {key: value[0] for key, value in decoded_data.items()}
            print(json_data)
            unique_field = 'Id'
            existing_invoice = Invoice.objects.filter(**{unique_field: json_data[unique_field]}).first()

            # If the record exists, delete it
            if existing_invoice:
                existing_invoice.delete()

            # Create a new record
            invoice = Invoice.objects.create(**json_data)
            
            # Respond with the received data
            return JsonResponse({'data': json_data})
        except Exception as e:
            # Handle any exceptions and respond with an error message
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

#Receive DeliveryOrders data
@csrf_exempt
def receive_deliveryorders(request):
    if request.method == 'POST':
        try:
            # Get the raw data from the request body
            rawdv_data = request.body.decode('utf-8')
        
            # Convert the URL query string to JSON format
            decodeddv_data = urllib.parse.parse_qs(rawdv_data)
            print(decodeddv_data)
            # Convert the dictionary into a JSON object
            dv_data = {key: value[0] for key, value in decodeddv_data.items()}
            print(dv_data)
            unique_field = 'Id'
            existing_DeliveryOrder = DeliveryOrder.objects.filter(**{unique_field: dv_data[unique_field]}).first()

            # If the record exists, update it; otherwise, create a new record
            if existing_DeliveryOrder:
                # Update the existing record with the new data
                for key, value in dv_data.items():
                    setattr(existing_DeliveryOrder, key, value)
                existing_DeliveryOrder.save()
            else:
                # Create a new record
                invodeliveryorderice = DeliveryOrder.objects.create(**dv_data)

            # Respond with the received data
            return JsonResponse({'data': dv_data})
        except Exception as e:
            # Handle any exceptions and respond with an error message
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import ExchangeRates

@csrf_exempt
def receive_extchangerates(request):
    if request.method == 'POST':
        try:
            # Get the raw data from the request body
            raw_data = request.body.decode('utf-8')
        
            # Convert the URL query string to JSON format
            decoded_data = urllib.parse.parse_qs(raw_data)
            
            # Convert the dictionary into a JSON object
            json_data = {key: value[0] for key, value in decoded_data.items()}
            print(json_data)
            unique_field = 'Id'
            existing_invoice = ExchangeRates.objects.filter(**{unique_field: json_data[unique_field]}).first()

            # If the record exists, delete it
            if existing_invoice:
                existing_invoice.delete()

            # Create a new record
            invoice = ExchangeRates.objects.create(**json_data)
            
            # Respond with the received data
            return JsonResponse({'data': json_data})
        except Exception as e:
            # Handle any exceptions and respond with an error message
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Handle the case where the request method is not POST
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
    
@login_required
def overview_list(request: HttpRequest):
    if request.user.is_authenticated:
        account = request.user.account
        to_unit_code = account.units
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        # Now you can use last_name as needed
    
    # Get the value of overview_list from the request
    overview_list_value = request.GET.get('overview_list')
    
    # If overview_list_value is provided, store it in the session
    if overview_list_value is not None:
        request.session['previous_overview_list_value'] = overview_list_value
    
    # Use the stored value from the session if overview_list_value is None
    overview_list_value = overview_list_value or request.session.get('previous_overview_list_value')
    
    print(overview_list_value)
    # Print the received value for debugging
    #print("Received value:", overview_list_value)
    
    DelivOrd = DeliveryOrder.objects.all()        
    UnitConversion1 = UnitConversion.objects.all()
    # Assuming x1 and x2 are lists of dates and corresponding data
    x1 = [c.StartOperation for c in DelivOrd]
    x2 = [float(c.Quantity) for c in DelivOrd]
    x3 = [c.UnitCode for c in DelivOrd]
    #Convert the Fuel unit
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)
        
    # Create a DataFrame from the lists
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters})
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f')
   
    # Extract only the date component
    df['Date'] = df['Date'].dt.date 
    # Find the earliest date in the dataset
    earliest_date = df['Date'].min()
    latest_date = df['Date'].max()
    fixed_earliest_date = earliest_date
    # Initialize the end date as None
    end_date = None
    # Correcting the line to handle the case where overview_list_value is None
    
    # days = int(overview_list_value) if overview_list_value is not None else 7
    days = int(overview_list_value) if overview_list_value is not None else 7

    # Define the time increment using the corrected value of days
    time_increment = timedelta(days=days)

    dates = []
    data= []
    # Loop until the end date is found in the dataset
    while earliest_date <= latest_date:
        # Calculate the end date by adding the time increment to the earliest date
        end_date = earliest_date + time_increment
        
        # Perform your logic here based on the time range (e.g., summing consumption)
        sum_consumption = df.loc[(df['Date'] >= earliest_date) & (df['Date'] < end_date), 'Data'].sum()
        
        # Output the time range and sum of consumption (or other result of your logic)
        dates.append(earliest_date.strftime('%Y-%m-%d'))
        data.append(sum_consumption)
        # Update the earliest date to the end date for the next iteration
        earliest_date = end_date

    # End of loop when end date is found in the dataset
    print("End date found in the dataset.")
    total_sum = round(df['Data'].sum())
    Unit = to_unit_code
    if len(dates) <= 1:
          print("Not enough data")
    else:
          print("There is enough data")

    data = {
        'username' : username1,
        'labels1' : dates,
        'dataa1' : data,
        'start_month' : fixed_earliest_date,
        'end_month' : latest_date,
        'sum' : total_sum,
        'unit' : Unit,
        'dark_mode': dark_mode,
    }
    current_path = request.path
    return render(request, 'dashboard.html', {'data': data, 'current_path': current_path})


@login_required
def suppliers_view(request: HttpRequest):
    if request.user.is_authenticated:
        last_name = request.user.last_name  
        account = request.user.account
        to_unit_code = account.units
        dark_mode = int(account.dark_mode)
        
        # Now you can use last_name as needed
        username1 = request.user.username

    dv = DeliveryOrder.objects.all()
    print(to_unit_code)
    # Extract data from objects
    x1 = [c.StartOperation for c in dv]
    x2 = [float(c.Quantity) for c in dv]
    x3 = [c.UnitCode for c in dv]
    x4 = [c.Provider for c in dv]

    # Convert quantities to liters
    x2_in_liters = [convert_quantity(quantity, unit_code, to_unit_code) for quantity, unit_code in zip(x2, x3)]

    # Create DataFrame
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters, 'Provider': x4})

    # Convert 'Date' column to datetime format and extract date component
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f').dt.strftime('%d-%m-%Y')

    # Group by 'Date' and sum the 'Data' for each day
    daily_sum_df = df.groupby('Date')['Data'].sum().reset_index()

    # Sort daily_sum_df by 'Date' column
    sorted_daily_sum_df = daily_sum_df.sort_values(by='Date')

    # Extract sorted dates and corresponding data
    sorted_x1 = sorted_daily_sum_df['Date'].tolist()
    sorted_x2 = sorted_daily_sum_df['Data'].tolist()

    # Group by 'Provider' and sum the 'Data' for each provider
    sum_by_provider = df.groupby('Provider')['Data'].sum()

    # Sort providers by fuel quantities in descending order
    sorted_providers = sum_by_provider.sort_values(ascending=False)

    # Extract sorted provider names and fuel quantities
    provider_names_sorted = sorted_providers.index.tolist()
    provider_fuel_quantities_sorted = sorted_providers.tolist()

    # Get the provider with the highest fuel quantity
    most_provided_provider = provider_names_sorted[0]
    most_provided_provider_initials = get_initials_with_dots(most_provided_provider)

    # Process for suppliers
    formatted_suppliers_data = []
    # Iterate over sorted providers and format the data
    for country, quantity in sorted_providers.items():
        formatted_quantity = quantity  # Round to the nearest integer
        formatted_suppliers_data.append([country, formatted_quantity])
            
    print(formatted_suppliers_data)    
    # Calculate total fuel consumption
    total_sum = round(df['Data'].sum())

    # Prepare data dictionary
    data = {
        'username' : username1,
        'labels1': sorted_x1,
        'dataa1': sorted_x2,
        'sum': total_sum,
        'unit': to_unit_code,
        'formatted_suppliers_data' : formatted_suppliers_data,
        'provider_names': provider_names_sorted,
        'provider_fuel_quantities': provider_fuel_quantities_sorted,
        'top_provider': most_provided_provider,
        'top_provider_initials': most_provided_provider_initials,
        'dark_mode': dark_mode,

    }

    current_path = request.path
    return render(request, 'suppliers.html', {'data': data, 'current_path': current_path})


# Geo View Code ##########
@login_required
def geo_view(request: HttpRequest):
    if request.user.is_authenticated:
        account = request.user.account
        to_unit_code = account.units
        username1 = request.user.username
        selection_filter = account.geography_global_selection
        custom_Startdate = account.start_geo_date
        custom_Enddate = account.end_geo_date
        dark_mode = int(account.dark_mode)
        geo_filter_id = account.geography_filter_id
        
    print(geo_filter_id)
    dv = DeliveryOrder.objects.all()
    iv = Invoice.objects.all()
    # Extract data from objects DeliveryOrder
    x1 = [c.StartOperation for c in dv]
    x2 = [float(c.Quantity) for c in dv]
    x3 = [c.UnitCode for c in dv]
    x4 = [c.CountryCode for c in dv]
    x5 = [c.StopOver for c in dv]
    x6 = [c.Town for c in dv]
    
    # Extract data from objects Invoices
    y0 = [c.StartDate for c in iv]    
    y1 = [float(c.AmountIncludingTax) for c in iv]
    y2 = [c.UnitCode for c in iv]
    y3 = [c.CountryCode for c in iv]
    y4 = [c.StopOver for c in iv]
    y5 = [c.Town for c in iv]

    # Convert the Fuel unit DeliveryOrder
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)

    # Store delivery_orders_data into dataframe : df
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters, 'Countries': x4, 'StopOver': x5, 'Town': x6})

    # Store invoices_data into dataframe : df
    df1 = pd.DataFrame({'Date': y0,'Data': y1, 'Countries': y3, 'StopOver': y4, 'Town': y5 })
    
    # Initialize the end date as None
    end_date = None
    # If custom_startDate and custom_endDate are None, use earliest_date and latest_date from the DataFrame
    if custom_Startdate is None or custom_Enddate is None:
        if selection_filter == 1:
            earliest_date = df['Date'].min()
            latest_date = df['Date'].max()
        else:
            earliest_date = df1['Date'].min()
            latest_date = df1['Date'].max()
    else:
        earliest_date = custom_Startdate
        latest_date = custom_Enddate

    print(earliest_date)
    print(latest_date)
    
    # Filter the DataFrame to include only the data between the earliest date and the latest date
    df = df[(df['Date'] >= earliest_date) & (df['Date'] < latest_date)]
    
    # Group by 'Countries' and sum the 'Data' for each provider from deliveryOrders
    sum_by_country = df.groupby('Countries')['Data'].sum()
    sum_by_town = df.groupby('Town')['Data'].sum()
    sum_by_StopOver = df.groupby('StopOver')['Data'].sum()

    # Group by 'Countries' and sum the 'Data' for each provider from expenses
    expenses_sum_by_country = df1.groupby('Countries')['Data'].sum()
    expenses_sum_by_town = df1.groupby('Town')['Data'].sum()
    expenses_sum_by_StopOver = df1.groupby('StopOver')['Data'].sum()
    
    # Sort Countries by fuel quantities in descending order
    sorted_Countries = sum_by_country.sort_values(ascending=False)
    sorted_Town = sum_by_town.sort_values(ascending=False)
    sorted_StopOver= sum_by_StopOver.sort_values(ascending=False)
    
    # Sort Countries by expenses in descending order
    sorted_expenses_countries = expenses_sum_by_country.sort_values(ascending=False)
    sorted_expenses_Town = expenses_sum_by_town.sort_values(ascending=False)
    sorted_expenses_StopOver = expenses_sum_by_StopOver.sort_values(ascending=False)
 
    #End here for the moment
 
    # Extract sorted provider names and fuel quantities
    provider_names_sorted = sorted_Countries.index.tolist()
    provider_fuel_quantities_sorted = sorted_Countries.tolist()

    # Extract sorted provider names and expenses quantities
    provider_names_expenses_sorted = sorted_expenses_countries.index.tolist()
    provider_expenses_quantities_sorted = sorted_expenses_countries.tolist()

    # Check the value of select variable
    select = int(selection_filter)
    if select == 1:
        if geo_filter_id == 1:
            # Process for country
            formatted_data = [['Country', 'Fuel Consumption']]
            # Iterate over sorted providers and format the data
            for country, quantity in sorted_Countries.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([country, formatted_quantity])

            top_filter_selection = sorted_Countries.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)
        elif geo_filter_id == 2:
            # Process for country
            formatted_data = []
            # Iterate over sorted providers and format the data
            for town, quantity in sorted_Town.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([town, formatted_quantity])

            top_filter_selection = sorted_Town.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)
        elif geo_filter_id == 3:
            # Process for country
            formatted_data = []
            # Iterate over sorted providers and format the data
            for stopover, quantity in sorted_StopOver.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([stopover, formatted_quantity])

            top_filter_selection = sorted_Town.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)
    else:
        if geo_filter_id == 1:
            # Process for country
            formatted_data = [['Country', 'Fuel Consumption']]
            # Iterate over sorted providers and format the data
            for country, quantity in sorted_expenses_countries.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([country, formatted_quantity])

            top_filter_selection = sorted_expenses_countries.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)
        elif geo_filter_id == 2:
            # Process for country
            formatted_data = []
            # Iterate over sorted providers and format the data
            for town, quantity in sorted_expenses_Town.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([town, formatted_quantity])

            top_filter_selection = sorted_expenses_Town.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)
        elif geo_filter_id == 3:
            # Process for country
            formatted_data = []
            # Iterate over sorted providers and format the data
            for stopover, quantity in sorted_expenses_StopOver.items():
                formatted_quantity = quantity  # Round to the nearest integer
                formatted_data.append([stopover, formatted_quantity])

            top_filter_selection = sorted_expenses_StopOver.index[0]  # Extract the index (country name) of the first item in the sorted Series

            Unit = to_unit_code
            unit_name = from_unitcode_to_unitname(Unit)

    # Process towns and stopovers
    town_sum = df.groupby('Town')['Data'].sum().reset_index()
    stopover_sum = df.groupby('StopOver')['Data'].sum().reset_index()

    # Get the town and stopover with the maximum quantity
    top_town = df.loc[df['Data'].idxmax(), 'Town']
    top_stopover = df.loc[df['Data'].idxmax(), 'StopOver']

    top_country = sorted_Countries.index[0]
    top_town = sorted_Town.index[0]
    top_stopover = sorted_StopOver.index[0]
    data = {
        'username': username1,
        'formatted_data': formatted_data,
        'top_filter_selection': top_filter_selection,
        'top_country' : top_country,
        'top_town' : top_town,
        'top_stopover' : top_stopover,
        'unit': unit_name,
        'selection_filter_code': select,
        'dark_mode': dark_mode,
        'geo_filter':geo_filter_id,
    }
    current_path = request.path
    return render(request, 'geography.html', {'data': data, 'current_path': current_path})


#Time View Code ##########
@login_required
def time_view(request : HttpRequest):
    if request.user.is_authenticated:
        account = request.user.account
        selection_filter_code = account.time_global_selection
        chart_type = account.time_chart_type
        to_unit_code = account.units
        custom_startDate = account.start_date
        custom_endDate = account.end_date
        username1 = request.user.username
        dark_mode = int(account.dark_mode)

        # Now you can use last_name as needed
    # Get the value of overview_list from the request
    overview_list_value = request.GET.get('time_view')
    
    # If overview_list_value is provided, store it in the session
    if overview_list_value is not None:
        request.session['previous_overview_list_value'] = overview_list_value

    # Use the stored value from the session if overview_list_value is None
    overview_list_value = overview_list_value or request.session.get('previous_overview_list_value')
    
    if overview_list_value is None :
         every = 7
    else:
        every = overview_list_value
        
    # Print the received value for debugging
    # Print("Received value:", overview_list_value)
    
    DelivOrd = DeliveryOrder.objects.all()        
    iv = Invoice.objects.all()
    # Assuming x1 and x2 are lists of dates and corresponding data
    x1 = [c.StartOperation for c in DelivOrd]
    x2 = [float(c.Quantity) for c in DelivOrd]
    x3 = [c.UnitCode for c in DelivOrd]
    
    y1 = [c.StartDate for c in iv]
    y2 = [float(c.AmountIncludingTax) for c in iv]
    y3 = [c.CurrencyCode for c in iv]
    
    #Convert the Fuel unit
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)
        
    # Create a DeliveryOrder DataFrame from the lists
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters})
    
    # Create a Invoice DataFrame from the lists
    df1 = pd.DataFrame({'Date': y1, 'Data': y2})
    
    # Convert 'Date' column to datetime format in df
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S.%f')
   
    # Convert 'Date' column to datetime format in d1
    df1['Date'] = pd.to_datetime(df1['Date'], format='%d/%m/%Y %H:%M')
    
    # Extract only the date component
    df['Date'] = df['Date'].dt.date 
    df1['Date'] = df1['Date'].dt.date 
    
    # Initialize the end date as None
    end_date = None
    # If custom_startDate and custom_endDate are None, use earliest_date and latest_date from the DataFrame
    if custom_startDate is None or custom_endDate is None:
        if selection_filter_code == 1:
            earliest_date = df['Date'].min()
            latest_date = df['Date'].max()
        else:
            earliest_date = df1['Date'].min()
            latest_date = df1['Date'].max()
    else:
        earliest_date = custom_startDate
        latest_date = custom_endDate

    fixed_earliest_date = earliest_date
    # days = int(overview_list_value) if overview_list_value is not None else 7
    days = int(overview_list_value) if overview_list_value is not None else 7

    # Define the time increment using the corrected value of days
    time_increment = timedelta(days=days)

    dates = []
    data= []
    # Loop until the end date is found in the dataset
    while earliest_date <= latest_date:
        # Calculate the end date by adding the time increment to the earliest date
        end_date = earliest_date + time_increment

        if selection_filter_code == 1:
            # Perform your logic here based on the time range (e.g., summing consumption)
            sum_consumption = df.loc[(df['Date'] >= earliest_date) & (df['Date'] < end_date), 'Data'].sum()
            print(sum_consumption)
        else:
            # Perform your logic here based on the time range (e.g., summing consumption)
            sum_consumption = df1.loc[(df1['Date'] >= earliest_date) & (df1['Date'] < end_date), 'Data'].sum()
            print(sum_consumption)
            
        # Output the time range and sum of consumption (or other result of your logic)
        dates.append(earliest_date.strftime('%Y-%m-%d'))
        data.append(sum_consumption)
        # Update the earliest date to the end date for the next iteration
        earliest_date = end_date

    # End of loop when end date is found in the dataset
    print("End date found in the dataset.")
     
    total_sum = round(sum(data))
    Unit = to_unit_code
    
    if len(dates) <= 1:
          dates = []
          data = []
    else:
          print("There is enough data")

    enough_data = len(dates) > 1
    interpretation = generate_textual_interpretation(data, fixed_earliest_date, latest_date, time_increment,Unit)
    if chart_type == 1 :
        chart_name = 'line'
    else:
        chart_name = 'bar'
        
    print(chart_name)
    data = {
        'username': username1,
        'selection_filter_code':selection_filter_code,
        'chart_type' : chart_type,
        'chart_type_name' : chart_name,
        'enough_data': enough_data,
        'labels1' : dates,
        'dataa1' : data,
        'every': every,
        'start_month' : fixed_earliest_date,
        'end_month' : latest_date,
        'sum' : total_sum,
        'unit' : Unit,
        'text_interpretation' : interpretation,
        'dark_mode': dark_mode,

    }
    current_path = request.path
    return render(request, 'timeline.html', {'data': data, 'current_path': current_path}) 

#Forecasting View Code ##########
@login_required
def prevision_view(request):
    return render(request, 'rtl.html') 

from django.http import JsonResponse

@login_required
def profile_view(request):
    account = request.user.account  # Assuming there's a one-to-one relationship between User and Account
    unit = account.units
    currency = account.currency
    dark_mode = account.dark_mode
    if request.method == 'POST':
        if 'unit' in request.POST:
            form = UnitForm(request.POST, instance=account)
            if form.is_valid():
                account.units = form.cleaned_data['unit']
                account.save()
                # Return JSON response if it's an AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('profile')  # Redirect for non-AJAX requests
        elif 'currency' in request.POST:
            form = CurrencyForm(request.POST, instance=account)
            if form.is_valid():
                account.currency = form.cleaned_data['currency']
                account.save()
                # Return JSON response if it's an AJAX request
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('profile')  # Redirect for non-AJAX requests
    else:
        form = UnitForm(instance=account)
    
    data = {
        'dark_mode': dark_mode,
        'unit': unit,
        'currency': currency,
    }
    return render(request, 'profile.html', {'data': data, 'form': form})


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            print(f"Session data: {request.session.items()}")
            return redirect('profile')  # Change this to your profile URL
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile.html', {'form': form, 'errors': form.errors})
def handle_ajax_request(request):
    # Handle the AJAX request here
    if request.method == 'POST':
        # Process the AJAX request
        # For demonstration, let's just return a JsonResponse
        return JsonResponse({'success': True})

# aircrafts View Code
@login_required
def aircrafts_view(request):
    username1 = None  # Default value if user is not authenticated
    if request.user.is_authenticated:
        account = request.user.account   
        to_unit_code = account.units
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        
    dv = DeliveryOrder.objects.all()
    # Extract data from objects DeliveryOrder
    x1 = [c.StartOperation for c in dv]
    x2 = [float(c.Quantity) for c in dv]
    x3 = [c.UnitCode for c in dv]
    x4 = [c.AircraftCode for c in dv]
    x5 = [c.Aircraft for c in dv]
    
    # Convert the Fuel unit DeliveryOrder
    x2_in_liters = []
    for quantity, unit_code in zip(x2, x3):
        converted_quantity = convert_quantity(quantity, unit_code, to_unit_code)
        x2_in_liters.append(converted_quantity)

    # Store delivery_orders_data into dataframe : df
    df = pd.DataFrame({'Date': x1, 'Data': x2_in_liters, 'Aircraft': x5})
    
    # Group by 'Countries' and sum the 'Data' for each provider from deliveryOrders
    sum_by_aircraft = df.groupby('Aircraft')['Data'].sum()
    
    # Sort Countries by fuel quantities in descending order
    sorted_aircrafts = sum_by_aircraft.sort_values(ascending=False)
    
    # Extract sorted provider names and fuel quantities
    aircraft_names_sorted = sorted_aircrafts.index.tolist()
    aircraft_fuel_quantities_sorted = sorted_aircrafts.tolist()
    
    most_provided_provider = aircraft_names_sorted[0]

    unit_name = from_unitcode_to_unitname(to_unit_code)
    current_path = request.path
    data = {
        'username': username1,
        'dark_mode' : dark_mode,
        'unit': unit_name,
        'top_aircraft' : most_provided_provider,
        'aircraft_names': aircraft_names_sorted,
        'aircraft_fuel_quantities': aircraft_fuel_quantities_sorted,

    }
    return render(request, 'aircrafts.html', {'data': data, 'current_path': current_path})


#forecasting View Code ##########
@login_required
def forecasting_view(request):
    if request.user.is_authenticated:
        account = request.user.account
        username1 = request.user.username
        dark_mode = int(account.dark_mode)

    current_path = request.path
    data = {
        'username' : username1,
        'dark_mode' : dark_mode
    }
    return render(request, 'forecasting.html',{'data': data ,'current_path': current_path})

def logout_view(request):
    logout(request)
    return redirect('landingpage')

def landingpage_view(request):
    return render(request, 'landingpage.html')

from django.shortcuts import render

#Country-Details
def country_details(request):
    if request.user.is_authenticated:
        account = request.user.account
        to_unit_code = account.units
        filter_code = account.geography_global_selection
        
    country_code = request.GET.get('country', '')
    
    deliv_orders = DeliveryOrder.objects.filter(CountryCode=country_code)
    
    quantities = []
    units = []
    towns = []
    stopovers = []
    country_names = []
    
    for order in deliv_orders:
        quantities.append(float(order.Quantity))
        units.append(order.UnitCode)
        towns.append(order.Town)
        stopovers.append(order.StopOver)
        country_names.append(order.Country)
    
    quantities_in_liters = [convert_quantity(qty, unit, to_unit_code) for qty, unit in zip(quantities, units)]
    town_sum_df = pd.DataFrame({
        'Quantity': quantities_in_liters,
        'UnitCode': units,
        'Town': towns,
        'StopOver': stopovers,
        'CountryCode': country_names
    })
    town_sum = town_sum_df.groupby('Town')['Quantity'].sum().reset_index()
    stopover_sum = town_sum_df.groupby('StopOver')['Quantity'].sum().reset_index()
    
    top_town = town_sum_df.loc[town_sum_df['Quantity'].idxmax(), 'Town']
    top_stopover = town_sum_df.loc[town_sum_df['Quantity'].idxmax(), 'StopOver']

    country_name = country_names[0]
    print(town_sum.values.tolist())
    print(filter_code)
    data = {
        'towns': town_sum.values.tolist(),
        'stopover': stopover_sum.values.tolist(),
        'country_code': country_code,
        'country_name': country_name,
        'town_max_quantity':top_town,
        'stopover_max_quantity':top_stopover,
        'unit' : to_unit_code,
        'selection_filter_code': filter_code,
    }
    
    return render(request, 'country_details.html', {'data': data})

@login_required
def about_view(request): 
    if request.user.is_authenticated:
        account = request.user.account 
        username1 = request.user.username
        dark_mode = int(account.dark_mode)
        
    current_path = request.path
    data = {
        'username' : username1,
        'dark_mode' : dark_mode
    }
    return render(request, 'about.html',{'data':data,'current_path': current_path})