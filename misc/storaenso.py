
# coding: utf-8


import os
import pandas as pd
import numpy as np
import warnings
import openpyxl
warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,.2f}'.format




print "Please save all data to corresponding folder(YYYYMM)"
Input = raw_input('Pls enter the last day of reported month:YYYYMMDD(for example:20161231):')

entered_month = Input[:6]
enteredLastDay = Input[-2:] + '.' + Input[4:6]+ '.'  + Input[:4]


# In[14]:

os.chdir('C:/automation-Nordea-factoring-reconciliation/')
pathReport = entered_month + '_automatically_generated_Reports'
if not os.path.exists(pathReport):
    os.makedirs(pathReport)
    
pathEvidence = entered_month + '_Evidence'
if not os.path.exists(pathEvidence):
    os.makedirs(pathEvidence)


position = {'EUR':'C', 'AUD':'D', 'GBP':'E', 'USD':'F', 'SEK':'G'}
position1Table = {161009:'C8', 161885:'C9', 161029:'C10', 161845:'C11'}

path = os.getcwd()
path_entered_month = path + '/' + entered_month
path_return = path_entered_month + '/' + 'Return files'

cc_codes = ['01','207','220','290','31','350','40','438']
ccy_of_companys = ['EUR','SEK','SEK','SEK','EUR','EUR','EUR','SEK']

cc_ccy_map = dict(zip(cc_codes, ccy_of_companys))



cc_Names = ['Stora Enso Oyj',
            'Stora Enso Fors AB',
            'Stora Enso Skoghall AB' ,
            'Stora Enso Pulp AB' ,
            'Stora Enso Packaging Oy' ,
            'Stora Enso Amsterdam B.V.' ,
            'Stora Enso Ingerois Oy' ,
            'Stora Enso Packaging AB']

			


cc_Name_map = dict(zip(cc_codes, cc_Names))



# # Collection all

# In[16]:

path_collection = path_entered_month + '/' + 'Collections'

collection_templete_file_name = path + '/templete_reconciliation_report/Collection_run_templete.xlsx'
collection_all = pd.ExcelFile(collection_templete_file_name).parse("Sheet1")


col_collection = collection_all.columns

for folderName in os.listdir(path_collection):

    for endFileName in os.listdir(path_collection + '/' + folderName):


        if ('fbl5' not in endFileName.lower())&        ('pdf' not in endFileName.lower())&        ('xlsx' in endFileName.lower()):

            collection_one = pd.ExcelFile(path_collection + '/' + folderName+ '/'  + endFileName).parse("Sheet1")
            collection_one = collection_one[collection_one.columns[0:23]]
            collection_one.columns = col_collection[0:23]
            
            collection_one['sourceFolder'] = folderName
            collection_one['sourceFileName'] = endFileName
            
            collection_all = pd.concat([collection_all, collection_one])


collection_all = collection_all.reset_index(drop = True)

def prepare_COLLECTION(company_code):
    global collection_all
    print 'Company code: ', company_code
    collection = collection_all[collection_all.CoCd == int(company_code)]

    collection = collection.reset_index(drop = True)


    collection.to_csv(pathEvidence + '/' + 'collection_evidence_file_%s.csv' %(company_code), sep = ';', index = False)


    if len(collection_all.Document.unique()) > 1:
        collection_all = collection_all[collection_all.Document != 'Bank costs']

    collection_append = pd.DataFrame({ 'Sum' : collection.groupby(['Crcy'])['Amount'].sum() }).reset_index()

    print collection_append
    print '\n\n\n'
    
    return collection_append



def write_all(sheet):
    sheet = writeInfo(sheet)
    sheet = writeBeginningBalance(sheet)
    sheet = write_Discount(sheet)
    sheet = writeReturn(sheet)
    sheet = writeCOLLECTION(sheet)
    sheet = writeCorrection(sheet)
    sheet = write1stTable(sheet)
    return sheet


def writeInfo(sheet):
    sheet['B2'] = int(company_code)
    sheet['B4'] = local_ccy
    sheet['B3'] = name
    sheet['B5'] = enteredLastDay
    return sheet

def writeBeginningBalance(sheet):
    for i in xrange(len(df_begin_balance.index)):
        sheet['%s15' %(position[str(df_begin_balance.ix[i, 'Document currency'])])] = float(df_begin_balance.ix[i, 'Sum_Amount_doc_ccy'])

    return sheet

def write_Discount(sheet):

    sheet['H23'] = discount_Value_Float

    return sheet



def writeReturn(sheet):
    for i in xrange(len(return_append.index)):
        sheet['%s16' %(position[str(return_append.ix[i, 'Crcy'])])] = (-1) * float(return_append.ix[i, 'sum'])

    return sheet


def writeCOLLECTION(sheet):
    for i in xrange(len(collection_append.index)):
        sheet['%s17' %(position[str(collection_append.ix[i, 'Crcy'])])] = float(collection_append.ix[i, 'Sum'])

    return sheet

def writeCorrection(sheet):
    if int(company_code) in list(correction_all['Company Code']):
        correctionValue = float(correction_all[correction_all['Company Code'] == int(company_code)]['Amount in doc. curr.'])
        if local_ccy == 'EUR':
            sheet['C18'] = correctionValue
        if local_ccy == 'SEK':
            sheet['G18'] = correctionValue
        
    return sheet

def write_Rev(sheet):
    for i in xrange(len(rev_append.index)):
        sheet['%s19' %(position[str(rev_append.ix[i, 'Document Currency'])])] = float(rev_append.ix[i, 'Sum'])
    return sheet


def write1stTable(sheet):
    for i in xrange(len(df.index)):
        sheet['%s' %(position1Table[df.ix[i, 'Account']])] =  float(df.ix[i, 'Amount in local cur'])

    return sheet


df_return_templete_file_name = path + '/templete_reconciliation_report/RET EUR templete.xlsx'

df_return = pd.ExcelFile(df_return_templete_file_name).parse("Sheet1")
col_return = df_return.columns


for fileName in os.listdir(path_return):
    df_one_return = pd.ExcelFile(path_return + '/'  + fileName).parse("Sheet1")
    df_one_return = df_one_return[df_one_return.columns[:15]]
    df_one_return.columns = col_return[:-1]
    
    df_one_return['sourceFileName'] = fileName
    
    df_return = pd.concat([df_return, df_one_return])

df_return = df_return.reset_index(drop = True)
df_return['Amount.1'] = df_return['Amount.1'].astype(float)
df_return['Amount'] = df_return['Amount'].astype(float)

df_return = df_return[df_return.CoCd.notnull()]

df_return.CoCd = df_return.CoCd.astype(int)


# In[20]:

def prepare_returnFiles(company_code):
    global df_return
    
    df_return_for_this_cc = df_return[(df_return.CoCd == int(company_code))].reset_index(drop = True)
    
    df_return_for_this_cc.to_csv(pathEvidence + '/' + 'Return_files_evidence_file_%s.csv' %(company_code), sep = ';', index = False)

    return_append = pd.DataFrame({ 'sum' : df_return_for_this_cc.groupby(['Crcy'])['Amount'].sum() }).reset_index()
    print 'Return files:'
    print return_append
    
    return return_append


# In[ ]:




# In[ ]:




# In[21]:

for company_code in cc_codes:
    print '\n\n***********************************************************'
    print '\n***********************************************************'
    print company_code
    local_ccy = cc_ccy_map[company_code]
    name = cc_Name_map[company_code]
    print 'local currency:' , local_ccy
    print '\n'
    
    # Read the data for first table
    df = pd.ExcelFile(path_entered_month + '/' + "Nordea_rec file SAP data for GLS_%s.xlsx" %entered_month).parse("Sheet1")
    df = df.dropna(how='all')
    df = df[df.CoCd == float(company_code)]
    df = df[~df.Account.isnull()].reset_index(drop = True)
    df.CoCd = df.CoCd.astype(int)
    df.Account = df.Account.astype(int)
    
    
    #Beginning balance
    print 'Working on beginning balance...\n'
    file_name_begin = '161009_beginning balance.xlsx'
    df_begin = pd.ExcelFile(path_entered_month + '/' + file_name_begin).parse("Sheet1")
    df_begin = df_begin.dropna(subset=['Document Number'])
    df_begin['Company Code'] = df_begin['Company Code'].astype(int)
    df_begin['Document Number'] = df_begin['Document Number'].astype(int)
    df_begin = df_begin[df_begin['Company Code'] == int(company_code)]
    df_begin_balance = pd.DataFrame({ 'Sum_Amount_doc_ccy' : df_begin.groupby(['Document currency'])['Amount in doc. curr.'].sum() }).reset_index()
    

    #Discount
    print 'Working on discount...\n'
    file_name_discount = '161019_discounts.xlsx'
    df_discount = pd.ExcelFile(entered_month + '/' + file_name_discount).parse("Sheet1")
    #df_discount = df_discount.dropna(subset=['Document Number'])
    df_discount = df_discount[df_discount['Document Number'].isnull()]
    discount_Value_Float = 0
    if len(df_discount[df_discount['Company Code'] == int(company_code)])>0:
        discount_Value_Float = float(df_discount[df_discount['Company Code'] == int(company_code)]['Amount in local currency'])
    
        
    discount_Value_Float

    
    #Collection
    collection_append = prepare_COLLECTION(company_code = company_code)
    
    
    # Return files
    return_append = prepare_returnFiles(company_code)

    # # Correction

    print '\nWorking on Correcction...\n'

    file_name_correction = '161009_corrections_%s.xlsx' %(entered_month)
    file_name_correction


    correction_all = pd.ExcelFile(path_entered_month + '/' + file_name_correction).parse("Sheet1")
    correction_all = correction_all.dropna(subset=['Company Code'])
    correction_all = correction_all[correction_all['Document Number'].isnull()]
    correction_all = correction_all[['Company Code', 'Document currency', 'Amount in doc. curr.']].reset_index(drop = True)
    correction_all['Company Code'] = correction_all['Company Code'].astype(int)


    # # Revenue recognition 161029 correction
    print 'Working on Revenue recognition 161029 correction... \n'

    revenueFileName = 'cc %s_ZFI_FACT_REVREC_201612.xlsx' %(company_code)
    revenueFileName

    rev_nameWithPath = path_entered_month + '/' + 'Revenue recognition 161029 correction' + '/'  + revenueFileName


    if os.path.exists(rev_nameWithPath):
        revenue = pd.ExcelFile(rev_nameWithPath).parse("Sheet1")
        rev_append = pd.DataFrame({ 'Sum' : revenue.groupby(['Document Currency'])['Invoice amount DC'].sum() }).reset_index()
        print rev_append


    # # Write functions

    xfile = openpyxl.load_workbook('templete_reconciliation_report/Nordea factoring reconciliation_161009_161029__templete.xlsx')
    sheet = xfile.get_sheet_by_name('Reconciliation')

   


    sheet = write_all(sheet)


    rev_nameWithPath = path_entered_month + '/' + 'Revenue recognition 161029 correction' + '/'  + 'Revenue.xlsx'
    revenueAll = pd.ExcelFile(rev_nameWithPath).parse("Sheet1")
    if int(company_code) in revenueAll['Company Code'].unique():
        revenue = revenueAll[revenueAll['Company Code'] == int(company_code)]
        if int(company_code) == 1:
            revenue = revenue[revenue['GL1 Factoring'] == 161009]
        rev_append = pd.DataFrame({ 'Sum' : revenue.groupby(['Document Currency'])['Invoice amount DC'].sum() }).reset_index()
        rev_append = rev_append.reset_index(drop = True)
        print rev_append
        
        sheet = write_Rev(sheet)

    print '\n\nNow gerenating report for this company...'
    xfile.save(pathReport+ '/5.2 Factoring CAS (CC%s GL 161009_161029)__%s.xlsx' %(company_code,entered_month))
    print '\nReport generated ! Evidence files saved !  Great!'


# In[22]:

print '\n\n#########################################################'
print '                 All completed,  Great                       '
print '#########################################################\n\n'

raw_input('\n\nPress ENTER to exit\n\n')
