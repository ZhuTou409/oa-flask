from DataBaseModels.SaleOrderModels.sale_order_model import SaleOrderFormKey, SaleOrderFormModel
from DataBaseModels.CustomerModels.customer_model import CustomerModel, CustomerFormKey, CustomerType
from DataBaseModels.TransportInfoModels.voyage_model import VoyageModel, VoyageFormKey
from FormModule.form_def import LoginFormKey
from flask import request, jsonify, session, Blueprint
from app import ServerInstance

auth_flask_form = Blueprint('auth_flask_form', __name__)


@auth_flask_form.route('/saleOrder/newForm', methods=['GET', 'POST'])
def SubmitSaleOrderForm():
    """
    进入销售表单提交页面
    """
    returnData = {}
    # 委托方联系人数据
    listEntrustCustomer = CustomerModel.GetAllCustomerInfoList(CustomerType.ENTRUST_CUSTOM)
    # 收货方联系人数据
    listReceiveCustomer = CustomerModel.GetAllCustomerInfoList(CustomerType.RECEIVE_CUSTOM)
    # 航班
    listVoyageModels = VoyageModel.GetAllVoyageInfoList()
    returnData[LoginFormKey.ENTRUST_CUSTOMER] = listEntrustCustomer
    returnData[LoginFormKey.RECEIVE_CUSTOMER] = listReceiveCustomer
    returnData[LoginFormKey.VOYAGE] = listVoyageModels
    return jsonify(returnData)


@auth_flask_form.route('/saleOrder/form/submitNewForm', methods=['GET', 'POST'])
def SubmitSaleOrderForm():
    if request.method == 'POST':
        data = request.get_json(silent=True)
        print("post data:{}".format(str(data)))

        # 委托方联系人数据
        szEntrustCustomerName = data.get(LoginFormKey.ENTRUST_CUSTOMER_NAME)
        EntrustCustomerObj = CustomerModel.FindCustomer(CustomerType.ENTRUST_CUSTOM, szEntrustCustomerName)
        if EntrustCustomerObj is None:
            # 创建新的对象
            dictNewCustomer = {
                CustomerFormKey.CUSTOMER_NAME: data.get(CustomerFormKey.CUSTOMER_NAME),
                CustomerFormKey.PHONE_NUMBER: data.get(CustomerFormKey.PHONE_NUMBER),
                CustomerFormKey.ADDRESS: data.get(CustomerFormKey.ADDRESS),
                CustomerFormKey.COMPANY: data.get(CustomerFormKey.COMPANY),
                CustomerFormKey.REGISTER_NAME: data.get(CustomerFormKey.REGISTER_NAME)
            }
            EntrustCustomerObj = CustomerModel(dictNewCustomer[CustomerFormKey.CUSTOMER_NAME], dictNewCustomer[CustomerFormKey.REGISTER_NAME], CustomerType.ENTRUST_CUSTOM,dictNewCustomer)

        # 收货方联系人数据
        szReceiveCustomerName = data.get(LoginFormKey.RECEIVE_CUSTOMER_NAME)
        ReceiveCustomerObj = CustomerModel.FindCustomer(CustomerType.RECEIVE_CUSTOM, szReceiveCustomerName)
        if ReceiveCustomerObj is None:
            # 创建新的对象
            dictNewCustomer = {
                CustomerFormKey.CUSTOMER_NAME: data.get(CustomerFormKey.CUSTOMER_NAME),
                CustomerFormKey.PHONE_NUMBER: data.get(CustomerFormKey.PHONE_NUMBER),
                CustomerFormKey.ADDRESS: data.get(CustomerFormKey.ADDRESS),
                CustomerFormKey.COMPANY: data.get(CustomerFormKey.COMPANY),
                CustomerFormKey.REGISTER_NAME: data.get(CustomerFormKey.REGISTER_NAME)
            }
            ReceiveCustomerObj = CustomerModel(dictNewCustomer[CustomerFormKey.CUSTOMER_NAME], dictNewCustomer[CustomerFormKey.REGISTER_NAME], CustomerType.RECEIVE_CUSTOM,dictNewCustomer)