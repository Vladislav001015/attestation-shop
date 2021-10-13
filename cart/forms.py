from django import forms

from cart.models import Order
from phonenumber_field.formfields import PhoneNumberField

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    receiver_number = PhoneNumberField(label='Номер телефона получателя')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {
            'placeholder': 'Введите имя',
            'class': 'form-control',
            'required': True
        }
        self.fields['last_name'].widget.attrs = {
            'placeholder': 'Введите фамилию',
            'class': 'form-control',
            'required': True

        }
        self.fields['address'].widget.attrs = {
            'placeholder': 'Улица, дом и номер квартиры',
            'class': 'form-control',
            'required': True
        }


        self.fields['receiver_number'].widget.attrs = {
            'placeholder': 'Номер телефона получателя',
            'class': 'form-control',
            'required': False
        }
        self.fields['date_delivery'].widget.attrs = {
            'placeholder': 'Дата доставки',
            'class': 'form-control',
            'required': False
        }

        self.fields['comment'].widget.attrs = {
            'placeholder': 'Комментарий к заказу',
            'class': 'form-control',
            'required': False
        }

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'receiver_number',
                  'date_delivery', 'comment', )
        widgets = {
            'date_delivery': forms.DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Дата доставки',
                                                    'type': 'date'}),
        }
