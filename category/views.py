from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .models import Category, CategoryGroup
from transaction.models import Transaction
from decimal import Decimal
from django.db.models import Sum
from inthebank.views import view_title_context_data
from django.urls import reverse
	

class CategoryListView(ListView):
	model = CategoryGroup
	context_object_name = 'category_group_list'
	template_name = 'category_list.html'

class CategoryCreateView(CreateView):
	model = Category
	template_name = 'create_form.html'	
	fields=['name',]
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['cat_group']=CategoryGroup.objects.get(pk=self.kwargs['group_pk'])
		return context
	
	def form_valid(self, form):
		group = CategoryGroup.objects.get(pk=self.kwargs['group_pk'])
		form.instance.group = group
		return super(CategoryCreateView, self).form_valid(form)
	
	def get_success_url(self, **kwargs):
		return reverse('category-list')
	
class SpendingView(TemplateView):
	template_name='spending_list.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		view_title='Spending by Category in'
		view_url='spending-list'
		
		context, view_date=view_title_context_data(self, context, view_url, view_title)


		##Group Category, Amount (sum of transactions), Budget
		##Table: Date, Description, Amount
		spending_list=[]
	
		#All Groups
		cat_group_list=CategoryGroup.objects.all().order_by('name')
	
		for cat_group in cat_group_list:

			#List of categories in the group
			cat_list=[]
			cat_list_in_group = Category.objects.filter(group=cat_group)
			group_sum = Transaction.objects.filter(
				category__in=cat_list_in_group,
				date__month=view_date.month,
				date__year=view_date.year).aggregate(Sum('amount'))
		
			#Each Category in the group
			for cat in cat_list_in_group:
				tran_list=Transaction.objects.filter(
					category=cat,
					date__month=view_date.month,
					date__year=view_date.year).order_by('date')
				cat_sum=tran_list.aggregate(Sum('amount'))
			
				cat_list.append((cat,cat_sum,tran_list))
			
			group_list=(cat_group,group_sum,cat_list)
			spending_list.append(group_list)	
	
		context['spending_list']=spending_list
	
		return context



