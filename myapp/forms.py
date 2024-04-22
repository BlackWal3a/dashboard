from django import forms
from django.contrib.auth.models import User
from .models import Account

# forms.py
from django import forms
from .models import Account

class UnitForm(forms.ModelForm):
    # Define choices for the unit selection
    UNIT_CHOICES = [
        ('LT', 'Litre'),
        ('M3', 'Cubic Meter'),
        ('USG', 'US Gallon'),
        ('KG', 'KILOGRAMME'),
        ('T', 'TONNE'),
        ('HL', 'HECTOLITRE'),
        ('BL', 'Baril'),
        # Add more choices as needed
    ]

    # Define a ChoiceField for the unit selection
    unit = forms.ChoiceField(label='Units', choices=UNIT_CHOICES)

    class Meta:
        model = Account
        fields = ['unit']

# forms.py
from django import forms
from .models import Account

class CurrencyForm(forms.ModelForm):
    # Define choices for the currency selection
    CURRENCY_CHOICES = [
        ('USC', 'US Dollar (USC)'),
        ('USD', 'US Dollar (USD)'),
        ('EUR', 'Euro (EUR)'),
        ('TND', 'Tunisian Dinar (TND)'),
        ('MIL', 'Italian Lira (MIL)'),
        ('DZD', 'Algerian Dinar (DZD)'),
        ('BEF', 'Belgian Franc (BEF)'),
        ('EGP', 'Egyptian Pound (EGP)'),
        ('GBP', 'British Pound Sterling (GBP)'),
        ('ESP', 'Spanish Peseta (ESP)'),
        ('FRF', 'French Franc (FRF)'),
        ('GRD', 'Greek Drachma (GRD)'),
        ('ITL', 'Italian Lira (ITL)'),
        ('JOD', 'Jordanian Dinar (JOD)'),
        ('KWD', 'Kuwaiti Dinar (KWD)'),
        ('LYD', 'Libyan Dinar (LYD)'),
        ('LUF', 'Luxembourg Franc (LUF)'),
        ('MRO', 'Mauritanian Ouguiya (MRO)'),
        ('MAD', 'Moroccan Dirham (MAD)'),
        ('CHF', 'Swiss Franc (CHF)'),
        ('TRL', 'Turkish Lira (TRL)'),
        ('CFA', 'CFA Franc (CFA)'),
        ('A', 'Aruban Florin (A)'),
        ('DEM', 'German Mark (DEM)'),
        ('SAC', 'Salvadoran Colón (SAC)'),
        ('CZK', 'Czech Koruna (CZK)'),
        ('SEK', 'Swedish Krona (SEK)'),
        ('SKK', 'Slovak Koruna (SKK)'),
        ('SIT', 'Slovenian Tolar (SIT)'),
        ('SBD', 'Solomon Islands Dollar (SBD)'),
        ('ZAR', 'South African Rand (ZAR)'),
        ('LKR', 'Sri Lanka Rupee (LKR)'),
        ('SYP', 'Syrian Pound (SYP)'),
        ('TZS', 'Tanzanian Shilling (TZS)'),
        ('TTD', 'Trinidad and Tobago Dollar (TTD)'),
        ('AED', 'UAE Dirham (AED)'),
        ('VEB', 'Venezuelan Bolívar (VEB)'),
        ('VND', 'Vietnamese Dong (VND)'),
        ('XDR', 'Special Drawing Rights (XDR)'),
        ('CSD', 'Serbian Dinar (CSD)'),
        ('SRD', 'Surinamese Dollar (SRD)'),
        ('TJS', 'Tajikistani Somoni (TJS)'),
        ('UZS', 'Uzbekistani Som (UZS)'),
        ('MGA', 'Malagasy Ariary (MGA)'),
        ('TRY', 'Turkish Lira (TRY)'),
        ('RON', 'Romanian Leu (RON)'),
        ('AZN', 'Azerbaijani Manat (AZN)'),
        ('MZN', 'Mozambican Metical (MZN)'),
        ('ZWN', 'Zimbabwean Dollar (ZWN)'),
        ('SDG', 'Sudanese Pound (SDG)'),
        ('GHS', 'Ghanaian Cedi (GHS)'),
        ('VEF', 'Venezuelan Bolívar (VEF)'),
        ('ZWR', 'Zimbabwean Dollar (ZWR)'),
        ('TMT', 'Turkmenistani Manat (TMT)'),
        ('CUC', 'Cuban Convertible Peso (CUC)'),
        ('SSP', 'South Sudanese Pound (SSP)'),
        ('ZMW', 'Zambian Kwacha (ZMW)'),
        ('ZWL', 'Zimbabwean Dollar (ZWL)'),
        ('NGN', 'Nigerian Naira (NGN)'),
        ('RUB', 'Russian Ruble (RUB)'),
        ('HNL', 'Honduran Lempira (HNL)'),
        ('KPW', 'North Korean Won (KPW)'),
        ('LSL', 'Lesotho Loti (LSL)'),
        ('AMD', 'Armenian Dram (AMD)'),
        ('BOB', 'Bolivian Boliviano (BOB)'),
        ('ETB', 'Ethiopian Birr (ETB)'),
        ('GMD', 'Gambian Dalasi (GMD)'),
        ('NLG', 'Dutch Guilder (NLG)'),
        ('SLL', 'Sierra Leonean Leone (SLL)'),
        ('SOS', 'Somali Shilling (SOS)'),
        ('SVC', 'Salvadoran Colón (SVC)'),
        ('SZL', 'Swazi Lilangeni (SZL)'),
        ('THB', 'Thai Baht (THB)'),
        ('TMM', 'Turkmenistani Manat (TMM)'),
        ('TOP', 'Tongan Pa\'anga (TOP)'),
        ('UAH', 'Ukrainian Hryvnia (UAH)'),
        ('UGX', 'Ugandan Shilling (UGX)'),
        ('UYU', 'Uruguayan Peso (UYU)'),
        ('VUV', 'Vanuatu Vatu (VUV)'),
        ('WST', 'Samoan Tala (WST)'),
        ('XCD', 'East Caribbean Dollar (XCD)'),
        ('YER', 'Yemeni Rial (YER)'),
        ('ZWD', 'Zimbabwean Dollar (ZWD)'),
        ('HRK', 'Croatian Kuna (HRK)'),
        ('HUF', 'Hungarian Forint (HUF)'),
        ('IEP', 'Irish Pound (IEP)'),
        ('ILS', 'Israeli Shekel (ILS)'),
        ('IQD', 'Iraqi Dinar (IQD)'),
        ('ISK', 'Iceland Krona (ISK)'),
        ('KGS', 'Kyrgyzstani Som (KGS)'),
        ('KMF', 'Comorian Franc (KMF)'),
        ('KZT', 'Kazakhstani Tenge (KZT)'),
        ('LAK', 'Laotian Kip (LAK)'),
        ('LRD', 'Liberian Dollar (LRD)'),
        ('LTL', 'Lithuanian Litas (LTL)'),
        ('AFN', 'Afghan Afghani (AFN)'),
        ('ALL', 'Albanian Lek (ALL)'),
        ('AOA', 'Angolan Kwanza (AOA)'),
        ('ARS', 'Argentine Peso (ARS)'),
        ('ATS', 'Austrian Schilling (ATS)'),
        ('AUD', 'Australian Dollar (AUD)'),
        ('AWG', 'Aruban Florin (AWG)'),
        ('AZM', 'Azerbaijani Manat (AZM)'),
        ('BHD', 'Bahraini Dinar (BHD)'),
        ('BIF', 'Burundian Franc (BIF)'),
        ('BMD', 'Bermudian Dollar (BMD)'),
        ('BND', 'Brunei Dollar (BND)'),
        ('BRL', 'Brazilian Real (BRL)'),
        ('BSD', 'Bahamian Dollar (BSD)'),
        ('BTN', 'Bhutanese Ngultrum (BTN)'),
        ('BYR', 'Belarusian Ruble (BYR)'),
        ('CAD', 'Canadian Dollar (CAD)'),
        ('CLP', 'Chilean Peso (CLP)'),
        ('COP', 'Colombian Peso (COP)'),
        ('CUP', 'Cuban Peso (CUP)'),
        ('CVE', 'Cape Verdean Escudo (CVE)'),
        ('CYP', 'Cypriot Pound (CYP)'),
        ('DKK', 'Danish Krone (DKK)'),
        ('DOP', 'Dominican Peso (DOP)'),
        ('EEK', 'Estonian Kroon (EEK)'),
        ('ERN', 'Eritrean Nakfa (ERN)'),
        ('FIM', 'Finnish Markka (FIM)'),
        ('FJD', 'Fijian Dollar (FJD)'),
        ('FKP', 'Falkland Islands Pound (FKP)'),
        ('GEL', 'Georgian Lari (GEL)'),
        ('GHC', 'Ghanaian Cedi (GHC)'),
        ('GIP', 'Gibraltar Pound (GIP)'),
        ('GNF', 'Guinean Franc (GNF)'),
        ('MDL', 'Moldovan Leu (MDL)'),
        ('MGF', 'Malagasy Franc (MGF)'),
        ('MKD', 'Macedonian Denar (MKD)'),
        ('MMK', 'Myanmar Kyat (MMK)'),
        ('MNT', 'Mongolian Tugrik (MNT)'),
        ('MOP', 'Macanese Pataca (MOP)'),
        ('MTL', 'Maltese Lira (MTL)'),
        ('MUR', 'Mauritian Rupee (MUR)'),
        ('MVR', 'Maldivian Rufiyaa (MVR)'),
        ('MWK', 'Malawian Kwacha (MWK)'),
        ('MXN', 'Mexican Peso (MXN)'),
        ('MYR', 'Malaysian Ringgit (MYR)'),
        ('MZM', 'Mozambican Metical (MZM)'),
        ('NAD', 'Namibian Dollar (NAD)'),
        ('NIO', 'Nicaraguan Córdoba (NIO)'),
        ('NOK', 'Norwegian Krone (NOK)'),
        ('NPR', 'Nepalese Rupee (NPR)'),
        ('NZD', 'New Zealand Dollar (NZD)'),
        ('OMR', 'Omani Rial (OMR)'),
        ('PAB', 'Panamanian Balboa (PAB)'),
        ('PEN', 'Peruvian Nuevo Sol (PEN)'),
        ('PGK', 'Papua New Guinean Kina (PGK)'),
        ('PLN', 'Polish Złoty (PLN)'),
        ('PTE', 'Portuguese Escudo (PTE)'),
        ('PYG', 'Paraguayan Guarani (PYG)'),
        ('ROL', 'Romanian Leu (ROL)'),
        ('RWF', 'Rwandan Franc (RWF)'),
        ('SDD', 'Sudanese Dinar (SDD)'),
        ('SGD', 'Singapore Dollar (SGD)'),
        ('BDT', 'Bangladeshi Taka (BDT)'),
        ('BBD', 'Barbadian Dollar (BBD)'),
        ('BZD', 'Belize Dollar (BZD)'),
        ('XOF', 'CFA Franc BCEAO (XOF)'),
        ('BAM', 'Bosnia-Herzegovina Convertible Mark (BAM)'),
        ('BWP', 'Botswana Pula (BWP)'),
        ('BGN', 'Bulgarian Lev (BGN)'),
        ('KHR', 'Cambodian Riel (KHR)'),
        ('XAF', 'CFA Franc BEAC (XAF)'),
        ('KYD', 'Cayman Islands Dollar (KYD)'),
        ('CNY', 'Chinese Yuan (CNY)'),
        ('TWD', 'Taiwan Dollar (TWD)'),
        ('CDF', 'Congolese Franc (CDF)'),
        ('CRC', 'Costa Rican Colón (CRC)'),
        ('DJF', 'Djiboutian Franc (DJF)'),
        ('XPF', 'CFP Franc (XPF)'),
        ('GYD', 'Guyanaese Dollar (GYD)'),
        ('HKD', 'Hong Kong Dollar (HKD)'),
        ('INR', 'Indian Rupee (INR)'),
        ('IDR', 'Indonesian Rupiah (IDR)'),
        ('IRR', 'Iranian Rial (IRR)'),
        ('JMD', 'Jamaican Dollar (JMD)'),
        ('JPY', 'Japanese Yen (JPY)'),
        ('KES', 'Kenyan Shilling (KES)'),
        ('KRW', 'South Korean Won (KRW)'),
        ('LVL', 'Latvian Lats (LVL)'),
        ('LBP', 'Lebanese Pound (LBP)'),
        ('ANG', 'Netherlands Antillean Guilder (ANG)'),
        ('PKR', 'Pakistan Rupee (PKR)'),
        ('PHP', 'Philippine Peso (PHP)'),
        ('QAR', 'Qatari Riyal (QAR)'),
        ('STD', 'São Tomé and Príncipe Dobra (STD)'),
        ('SAR', 'Saudi Riyal (SAR)'),
        ('SCR', 'Seychellois Rupee (SCR)'),
    ]

    # Define a ChoiceField for the currency selection
    currency = forms.ChoiceField(label='Currency', choices=CURRENCY_CHOICES)

    class Meta:
        model = Account
        fields = ['currency']


class DateRangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
   
class DateGeoRangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['start_geo_date', 'end_geo_date']
        widgets = {
            'start_geo_date': forms.DateInput(attrs={'type': 'date'}),
            'end_geo_date': forms.DateInput(attrs={'type': 'date'}),
        }
             
class SupplierDateRangeForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['start_supplier_date', 'end_supplier_date']
        widgets = {
            'start_supplier_date': forms.DateInput(attrs={'type': 'date'}),
            'end_supplier_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
from django import forms
from myapp.models import Account

class NoteForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['notes']