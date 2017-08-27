# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator
from django.core.validators import MinValueValidator

# Create your models here.
class Project(models.Model):
    partner = models.ForeignKey(User, related_name = 'partner', help_text='Monitoring Partner')
    monitoring_agent = models.ManyToManyField(User, related_name = 'monitoring_agent', blank = True)
    IFB_Number = models.CharField(max_length = 200)
    title = models.CharField(max_length = 500)
    description = models.TextField(null = True, blank = True)

    def __str__(self):
        return 'Project IFB No: {}'.format(self.IFB_Number)



class Planning(models.Model):
    
    SOURCE_OF_FUND=(
        ('Government Budget','Government Budget'),
        ('Loan','Loan'),
        ('Investment', 'Investment'),
    )

    CURRENCY = (
        ('NPR', 'Nepalese Rupees'),
        ('USD', 'US Dollar'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    source_of_fund = models.CharField(max_length=100, choices = SOURCE_OF_FUND, default = 'Government Budget')
    rationale = models.TextField(null = True, blank = True, help_text='Aim of this project')
    estimated_budget = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True)
    currency = models.CharField(max_length=30, choices = CURRENCY, default = 'Nepalese Rupees')

    # for planning log

    def __str__(self):
        return 'Project IFB No: {}'.format(self.project)



class Tender(models.Model):

    PROCUREMENT_METHOD=(
        ('NCB','National Competitive Bidding'),
        ('ICB','International Competitive Bidding'),
        ('LIB', 'Limited International Bidding'),
        ('Commodity Purchase', 'Commodity Purchase'),
        ('Direct Purchase', 'Direct Purchase'),
        ('FBS', 'Fixed Budget Selection'),
        ('Force Account','Force Account'),
        ('LCS', 'List Cost Selection'),
        ('QBS', 'Quality Based Selection'),
        ('QCBS', 'Quality and Cost Based Selection'),
        ('Ration', 'Ration'),
        ('Sealed Quotation', 'Sealed Quotation'),
        ('User Committee', 'User Committee'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, null = True, blank = True, help_text='Procuring Entity Name')
    address = models.CharField(max_length = 100, null = True, blank = True, help_text='Procuring Entity Address')
    email = models.EmailField(max_length = 100, null = True, blank = True, help_text='Procuring Entity Email')
    phone = models.CharField(max_length = 15, null = True, blank = True, help_text='Procuring Entity Phone')
    url = models.TextField(validators=[URLValidator()], null = True, blank = True, help_text='example: www.example.com')
    # procuring_entity_url = models.URLField(max_length=100, blank=True)
    method = models.CharField(max_length=70, choices = PROCUREMENT_METHOD, default='National Competitive Bidding', help_text='Procurement Method')
    detail = models.TextField(null = True, blank = True, help_text = 'Procurement Method Detail')
    description = models.TextField(null = True, blank = True, help_text = 'Tender Description')
    bid_start_date = models.DateField(null=True, blank=True, help_text = 'Tender Start Date')
    bid_end_date = models.DateField(null=True, blank=True, help_text = 'Tender End Date')
    # tender_period = models.CharField(max_length = 20, null = True, blank = True)
    enquiry_date = models.DateField(null=True, blank=True, help_text = 'Last Tender Enquiry Date')
    has_enquiries = models.BooleanField(default = False)
    estimated_cost = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True)
    eligibilty_criteria = models.TextField(null = True, blank = True)
    # award_period = models.CharField(max_length = 20, null = True, blank = True)
    number_of_tenderers = models.PositiveIntegerField(null=True, blank=True)


    def __str__(self):
        return 'Project IFB No: {}, Procurement Method : {}'.format(self.project,self.name)



class TenderItem(models.Model):
    tender = models.ForeignKey(Tender, related_name='tender_items')
    title = models.CharField(max_length = 300, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    classification = models.CharField(max_length = 200, null = True, blank = True)
    quantity = models.PositiveIntegerField(default = 0, null = True, blank = True, help_text='Tender Item Quantity')
    rate = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True, help_text='Tender Item Rate')
    unit = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True, help_text='Tender Item Unit')

    def __str__(self):
        return self.title



class Milestone(models.Model):

    MILESTONE_STATUS=(
        ('Achieved','Achieved'),
        ('Remained','Remained'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null = True, blank = True, help_text = 'Title of milestone')
    due_date = models.DateField(null = True, blank = True, help_text='Remaining days for project to end')
    date_modified = models.DateField(null = True, blank = True, help_text='Project Extended Date,if any')
    feedback = models.TextField(null = True, blank = True)
    status = models.CharField(max_length=30, choices = MILESTONE_STATUS, null = True, blank = True, help_text='Current status of project')

    def __str__(self):
        return 'Project IFB No: {}, Due Date: {}'.format(self.project,self.due_date)


#model for Transaction stage
class Transaction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, null = True, blank = True)
    date = models.DateField(null = True, blank = True, help_text = 'Transaction Date')
    amount = models.FloatField(validators = [MinValueValidator(0)],default = 0, null = True, blank = True, help_text = 'Transaction Amount')
    provider_organization_name = models.CharField(max_length = 70, null = True, blank = True)
    receiver_organization_name = models.CharField(max_length = 70, null = True, blank = True)
    amendment_changes = models.TextField(null = True, blank = True)

    def __str__(self):
        return 'Project IFB No: {}, Transaction Amount: {}'.format(self.project,self.amount)

