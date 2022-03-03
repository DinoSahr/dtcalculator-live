from datetime import datetime
from django.shortcuts import render
from .models import Receipts
import pymongo

# Create your views here.

DB_USER='dinosahrdesign'
DB_PASS='Pmvsdz8bHuPYBk4w'
AUTH_DB='dinosahrdb'


total = ""
total_before_tip = ""
assigned_percent = "" 
tip_amount = ""
documents = ""
document_count = ""
total_with_tip = ""
grandTotalSpendings = ""
grandtotalBeforeTips = ""
grandtotalBeforeTips = ""
grandtotalTipsPaid = ""
results = ""


CONNECTION_URL =  'mongodb+srv://{}:{}@cluster0.iqkvm.mongodb.net/{}?retryWrites=true&w=majority'.format(DB_USER, DB_PASS, AUTH_DB)

client = pymongo.MongoClient(CONNECTION_URL, ssl=True, tlsAllowInvalidCertificates= True)
get_db_name = client.get_database('dtcalculator-receipts')
get_collection = get_db_name.get_collection(name='Receipts')


def applicationHomeView(request):

    if request.method == "POST":
        
        if request.POST.get('receipt-total-container') and request.POST.get('tip-percent-container'):

            receiptDate = datetime.strftime(datetime.today(), "%m/%d/%Y, %H:%M:%S")
            receiptTotal = request.POST.get('receipt-total-container')
            assignedTip = request.POST.get('tip-percent-container')

            tipPercent = float(assignedTip) /100

            finalAssignedTip = round(float(receiptTotal) * tipPercent, 2)

            grandTotal = round(float(receiptTotal) + finalAssignedTip, 2)

            global systemError, successfulSubmission, total, total_before_tip, assigned_percent, tip_amount, documents, document_count, total_with_tip


            total_before_tip = receiptTotal
            assigned_percent = int(tipPercent * 100)
            tip_amount = finalAssignedTip
            total_with_tip = grandTotal

            receipt = {
                '"Receipt_Date"': receiptDate,
                '"Total_Before_Tip"': float(receiptTotal),
                '"Tip_Percent_Assigned"': int(tipPercent * 100),
                '"Tip_Amount"': finalAssignedTip,
                '"Grand_Total"': grandTotal,
            }

            
            #Number of Receipts Added
            document_count = get_collection.count({}) + 1
            

            try:
                get_collection.insert_one(receipt)
                successfulSubmission = "Your connection request to the database was successful."
            except Exception as e:
                systemError = "The connection request to the database failed."
                

    return render(
        request, 
        'index.html', {
            'grandTotal': total, 
            'total_before_tip': total_before_tip, 
            'assigned_percent': assigned_percent, 
            'tip_amount':  tip_amount, 
            'document_count': document_count,
            'total_with_tip':  total_with_tip,
        }
    )


#ABOUT US PAGE VIEW
def aboutView(request):
    return render(request, 'about.html', {})




#REPORTING PAGE VIEW
def reportingViews(request):

    global grandTotalSpendings, grandtotalBeforeTips, grandtotalBeforeTips, grandtotalTipsPaid, results

    #Get total numner of receipts added to the database
    total_receipts = get_collection.count({})
    
    #REPORT GENERATOR FUNCTION
    def runAggregationReport(query):
        QueryData = get_collection.aggregate([
            {
                '$group': {
                    '_id': '',
                    'QueryParam': {
                        '$sum': query,
                    }
                }
            }
        ])

        for qD in QueryData:
            results = qD['QueryParam']
            if results != 'null' or 'none':
                return round(results, 2)
            else:
                return 0


    return render(request, 'report.html', {
            'total_receipts': total_receipts,
            'grandTotalSpendings': runAggregationReport('$"Grand_Total"'), 
            'grandtotalBeforeTips': runAggregationReport('$"Total_Before_Tip"'), 
            'grandtotalTipsPaid': runAggregationReport('$"Tip_Amount"'), 
        }
    )


