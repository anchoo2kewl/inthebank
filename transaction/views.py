from .forms import TransactionFormSet, ChooseFileForm
from .models import Transaction, ScheduledTransaction
import csv
import 	datetime
from dateutil.relativedelta import relativedelta #external library/extension python-dateutil
from decimal import Decimal
from django.views.generic.edit import FormView
from django.urls import reverse

class ChooseFileView(FormView):
	template_name = 'choosefile.html'
	form_class = ChooseFileForm

	def form_valid(self, form):
		self.filename=form.cleaned_data['filename']
		self.bank=form.cleaned_data['bank']
		return super().form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse('transaction-import', kwargs={'bank':self.bank,'filename':self.filename})


class TransactionImportView(FormView):
	template_name = 'transaction_import.html'
	success_url = '/'
	form_class = TransactionFormSet

	def get_initial(self):
	
		initial=super(TransactionImportView, self).get_initial()
		filename=self.kwargs['filename']
		bank=self.kwargs['bank']
		
		with open(filename) as csvfile:
			if bank == 'PC':
				next(csvfile)
			readCSV = csv.reader(csvfile, delimiter=',')

			data_list=[]
	
			#Import Data from CSV file
			#Format is for TD or President's Choice
			for row in readCSV:
				if bank=='TD':
					date=datetime.datetime.strptime(row[0], '%m/%d/%Y').date()
					description=row[1].strip()
					if row[2]:
						amount=Decimal(row[2].replace(',',''))
						amount=amount*-1
					if row[3]:
						amount=Decimal(row[3].replace(',',''))
				if bank=='PC':
					date=datetime.datetime.strptime(row[3], '%m/%d/%Y').date()
					description=row[0].strip()
					amount=Decimal(row[5])
					
				#Looks for older matching transactions so can apply category
				t=Transaction.objects.filter(description=description)
				if t:
					category=t[0].category
				else:
					category='None'
				
				#Looks for duplicate imports, does not import
				duplicate=Transaction.objects.filter(
					description=description,
					date=date,
					amount=amount,
					)
				if not duplicate:
					data_list.append([date,description,amount,category])

		#Initial data from import for Form
		initial=[{'date': d, 'description':desc, 'amount':a, 'category':c} for d, desc, a, c in data_list ]

		return initial
		
	def form_valid(self, formset):
		for form in formset:
			t=form.save()
		
		st=ScheduledTransaction.objects.filter(transaction__description=t.description).first()
		if st:
			if st.repeat_every == 'AM':
				st.working_date = t.date + relativedelta(months=+1)
			elif st.repeat_every == 'AB':
				st.working_date = t.date + relativedelta(weeks=+2)
			elif st.repeat_every == 'SM':
				st.working_date = st.working_date + relativedelta(months=+1)
			elif st.repeat_every == 'B':
				st.working_date = st.working_date + relativedelta(weeks=+2)
			st.save()

		return super().form_valid(form)
