import requests
import json
import re
import time
import datetime


from twocaptcha import TwoCaptcha

sess = requests.Session()

#### 請填入 2recaptcha api id
solver = TwoCaptcha('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')


header = requests.utils.default_headers()
header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

#### 請填入header request 中的 X-CSRF-Token & X-XSRF-TOKEN
header['X-CSRF-Token'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=='
header['X-XSRF-TOKEN'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=='

header['Origin'] = 'https://www.buygames.com.tw'
header['content-type'] = 'application/json;charset=UTF-8'

#### 綠界第三方支付專用header
e_header = requests.utils.default_headers()
e_header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
e_header['Host'] = 'payment.ecpay.com.tw'
e_header['Origin'] = 'https://www.buygames.com.tw'

put_header = requests.utils.default_headers()
#### put 收貨付款方式 專用header
put_header['X-XSRF-TOKEN'] = header['X-XSRF-TOKEN']
put_header['X-CSRF-Token'] = header['X-CSRF-Token']
####
put_header['Host'] = 'www.buygames.com.tw'
put_header['Content-Type'] = 'application/json;charset=UTF-8'
put_header['X-Requested-With'] = 'XMLHttpRequest'
put_header['Origin'] = 'https://www.buygames.com.tw'
put_header['Referer'] = 'https://www.buygames.com.tw/cart'
put_header['content-type'] = 'application/json;charset=UTF-8'


bill_data={}

#### 使用者cookie
user_cookie = {
        '_shop_shopline_session_id_v3': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        'XSRF-TOKEN': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
#
sess.cookies.update(
    user_cookie
)
#

def addcar():
    #### 欲購入之商品 id
    product_no = '615ad40ee152b2001159c50f'  ## sofi
    # product_no = '6183b749f530a400201bcc73' ##test product_no
    # product_no = '6189e09d824efa3dbeccde6c' ##switch
    # product_no = '6180ed42e23cd144f6db33ab' ##ps5

    #### 欲購入項目請參照其他的form_data提交方式做更改
    form_data = json.dumps({
        "item": {
            "product_id": product_no,
            "quantity": 1,
            "type": "product",
            "variation_id": None,
            "blacklisted_delivery_option_ids": [],
            "triggering_item_id": None
        },
        "cart_options": {
            "skip_calculate_order": True
        }
    })
    header['origin'] = 'https://www.buygames.com.tw'
    header['referer'] = f'https://www.buygames.com.tw/products/{product_no}'
    res = sess.post(
        'https://www.buygames.com.tw/api/merchants/undefined/cart/items',
        headers=header,
        data=form_data
    )
    print(res.text)
    print('-------------------------------------------')
    form_data = json.loads(res.text)['data']

    return form_data


def get_carpage(data):
    header['referer'] = f'https://www.buygames.com.tw/orders/{data["order_id"]}'
    res = sess.get(
        'https://www.buygames.com.tw/cart',
        headers=header,
    )
    data['fee'] = re.findall('class="pull-right"\>NT\$(.*?)\<\/span\>', res.text)[1]
    print(data['fee'])
    print('-------------------------------------------')
    return data

def put_sendmethod():
    res = sess.put(
        'https://www.buygames.com.tw/cart/form',
        headers=put_header,
        data=json.dumps({
            "delivery_option_id": "60f0e9ea4d94950038b4121b",
            "delivery_data": {}
            })
        )
    return

def put_paymethod():
    res = sess.put(
        'https://www.buygames.com.tw/cart/form',
        headers=put_header,
        data=json.dumps({
                "payment_id": "61238eb74a4bb60014225d31"
            })
        )
    return

def delete_car(item_id):
    res = sess.delete(
        f'https://www.buygames.com.tw/api/merchants/60d5a4047b095a0017afd93c/cart/items?item_id={item_id}',
        headers=header,
        data=json.dumps({
            "cart_options": {
                "skip_calculate_order": False,
                "cache_key": "/cart"
            }
        })
    )
    print(res.text)

def get_checkoutpage():
    res = sess.get(
        'https://www.buygames.com.tw/checkout',
        headers=header
    )
    key = re.findall('sitekey: "(.*?)"', res.text)[0]
    try:
        print('please wait...')
        reslut = solver.recaptcha(
            sitekey=key,
            url='https://www.buygames.com.tw/checkout',
            invisible = 1
        )
    except Exception as e:
        print(e)
    print(reslut)
    return reslut['code']

def check_out(g_token):
    header['Referer'] = 'https://www.buygames.com.tw/checkout'

####根據現況自行調整form_data
    form_data = json.dumps(
        {
        "order": {
            "delivery_option": {
            "_id": "60f0e9ea4d94950038b4121b",
            "created_at": "2021-07-16T02:07:38.406Z",
            "updated_at": "2021-08-05T08:08:53.291Z",
            "owner_id": "60d5a4047b095a0017afd93c",
            "form_fields": [],
            "region_type": "tw_tcat_roomtemp",
            "name_translations": {
                "en": "Tcat - Room Temp.",
                "zh-hant": "宅配"
            },
            "description_translations": {
                "zh-hant": "黑貓宅急便配送"
            },
            "delivery_time_description_translations": {},
            "show_description_on_checkout": False,
            "requires_customer_address": True,
            "config_data": {
                "sender_name": "地下街軟體世界",
                "order_mode": "manual",
                "sender_phone": "0225055090",
                "sender_address": "台北市中山區建國北路二段109號1樓",
                "contract_code": "2497319201",
                "delivery_target_area": "localOnly",
                "execute_shipment_permission": True,
                "delivery_time_required": False,
                "tcat_egs_id": 3,
                "product_name": "delivery_options.options.7_11_cross_border.null"
            },
            "fee_type": "flat_weight",
            "time_slots": [
                {
                "key": 4,
                "description": "tcat.time_slot.04"
                },
                {
                "key": 1,
                "description": "tcat.time_slot.01"
                },
                {
                "key": 2,
                "description": "tcat.time_slot.02"
                }
            ],
            "delivery_type": "post",
            "supported_countries": [
                "TW"
            ],
            "fee": {
                "cents": 130,
                "currency_symbol": "NT$",
                "currency_iso": "TWD",
                "label": "NT$130",
                "dollars": 130
            },
            "accepted_countries": [
                "TW"
            ],
            "delivery_rates": [
                {
                "_id": "610b9beb94b66c002366b763",
                "countries": [
                    "TW"
                ],
                "created_at": "2021-08-05T08:06:03.705Z",
                "delivery_areas": [],
                "delivery_config": {},
                "delivery_option_id": "60f0e9ea4d94950038b4121b",
                "fee": {
                    "cents": 130,
                    "currency_symbol": "NT$",
                    "currency_iso": "TWD",
                    "label": "NT$130",
                    "dollars": 130
                },
                "fee_data": None,
                "name": None,
                "rate_limit": 1,
                "updated_at": "2021-08-05T08:06:03.705Z"
                },
                {
                "_id": "610b9beb94b66c002366b764",
                "countries": [
                    "TW"
                ],
                "created_at": "2021-08-05T08:06:03.721Z",
                "delivery_areas": [],
                "delivery_config": {},
                "delivery_option_id": "60f0e9ea4d94950038b4121b",
                "fee": {
                    "cents": 130,
                    "currency_symbol": "NT$",
                    "currency_iso": "TWD",
                    "label": "NT$130",
                    "dollars": 130
                },
                "fee_data": None,
                "name": None,
                "rate_limit": -1,
                "updated_at": "2021-08-05T08:06:03.721Z"
                }
            ]
            },
            "payment_method": {
            "_id": "61238eb74a4bb60014225d31",
            "fee_percent": 0,
            "fee_multiplier": 0,
            "instructions_translations": {
                "zh-hant": "繳費期限為24小時，若超過期限，請勿進行繳費。"
            },
            "show_description_on_checkout": False,
            "fee_amount": {
                "cents": 0,
                "currency_symbol": "NT$",
                "currency_iso": "TWD",
                "label": "",
                "dollars": 0
            },
            "name_translations": {
                "en": "CVS (Print out the bills by CVS and pay in the store)",
                "zh-hant": "超商代碼繳費（711 - ibon / 全家 FamiPort）"
            },
            "type": "ecpay",
            "excluded_delivery_option_ids": [],
            "instruction_media": [],
            "config_data": {
                "ecpay_payment": "CVS",
                "checkout_conditions": None
            }
            },
            "seller_id": "60d5a4047b095a0017afd93c",
            "delivery_data": {
            "recipient_is_customer": True,
            "recipient_name": "XXX",
            "recipient_phone": "XXXXXXXXXX",
            "time_slot_key": "4"
            },
            "custom_fields_translations": [],
            "invoice": {
            "invoice_type": "0",
            "carrier_type": "0"
            },
            "delivery_address": {
            "logistic_codes": [
                "1200007",
                "1200099"
            ],
            "address_node_ids": [
                "5fcddeb08a8bb77659d0e3f4",
                "5fcddeb08a8bb77659d0e3f5"
            ],
            "city": "桃園市",
            "address_2": "中壢區",
            "postcode": "320",
            "address_1": "興仁路3段19號",
            "recipient_name": "XXX",
            "recipient_phone": "XXXXXXXXXX",
            "country": "TW"
            },
            "customer_name": "XXX",
            "customer_phone": "XXXXXXXXXX",
            "save_customer_phone": True,
            "order_remarks": "",
            "coupons": [],
            "user_phones": [
            "0976790683"
            ],
            "pay_session": {}
        },
        "saveFields": {
            "phone": False,
            "delivery_address": True,
            "all": False,
            "marketing": False,
            "customer_info": {},
            "default_address": True,
            "time_zone_offset": 8
        },
        "benchatFields": {
            "subscriptions": {
            "facebook": "[]"
            }
        },
        "is_fast_checkout": False,
        "page_id": "",
        "g-recaptcha-response": g_token
        }
    )
    res = sess.post(
        'https://www.buygames.com.tw/api/orders/checkout',
        headers=header,
        data=form_data
    )
    print(res.text)
    pay_data = json.loads(res.text)['order']['ecpay_form']
    print(pay_data)
    return pay_data

def aiocheck_out(pay_data):

    form_data = {
        'MerchantID':pay_data['MerchantID'],
        'MerchantTradeNo':pay_data['MerchantTradeNo'],
        'MerchantTradeDate':pay_data['MerchantTradeDate'],
        'PaymentType':pay_data['PaymentType'],
        'TotalAmount':pay_data['TotalAmount'],
        'TradeDesc':pay_data['TradeDesc'],
        'ItemName':pay_data['ItemName'],
        'ChoosePayment':pay_data['ChoosePayment'],
        'ClientBackURL':pay_data['ClientBackURL'],
        'ReturnURL':pay_data['ReturnURL'],
        'OrderResultURL':pay_data['OrderResultURL'],
        'PaymentInfoURL':pay_data['PaymentInfoURL'],
        'ItemURL':pay_data['ItemURL'],
        'Remark':pay_data['Remark'],
        'ChooseSubPayment':pay_data['ChooseSubPayment'],
        'DeviceSource':pay_data['DeviceSource'],
        'ExpireDate':pay_data['ExpireDate'],
        'CheckMacValue':pay_data['CheckMacValue']
    }
    res = sess.post(
        'https://payment.ecpay.com.tw/Cashier/AioCheckOut',
        headers=e_header,
        data=form_data
    )
    # print(res.text)
    bill_data['TradeAmount'] = re.findall('name="TradeAmount" type="hidden" value="(.*?)"', res.text)[0]
    bill_data['timeStamp'] = re.findall('name="timeStamp" value="(.*?)"', res.text)[0]
    bill_data['merchantId'] = re.findall('id="merchantId" value="(.*?)"', res.text)[0]
    bill_data['merchantTradeNo'] = re.findall('name="merchantTradeNo" value="(.*?)"', res.text)[0]
    bill_data['tradeType'] = re.findall('name="tradeType" value="(.*?)"', res.text)[0]
    bill_data['mid'] = re.findall('name="mid" value="(.*?)"', res.text)[0]
    bill_data['allPayTradeID'] = re.findall('name="allPayTradeID" value="(.*?)"', res.text)[0]
    bill_data['macValue'] = re.findall('name="macValue" value="(.*?)"', res.text)[0]
    bill_data['TradeAmount'] = re.findall('name="TradeAmount" type="hidden" value="(.*?)"', res.text)[0]
    bill_data['TradeTotalAMT'] = re.findall('id="TradeTotalAMT" value="(.*?)"', res.text)[0]
    bill_data['paymentName'] = '10002@8@ATM_CHINATRUST'
    bill_data['SetBindingCredit'] = ''
    bill_data['IsBindingCredit'] = ''
    bill_data['PayerCellPhone'] = ''
    bill_data['PayerName'] = ''

    bill_data['CardNo'] = 0
    bill_data['CardValidMM'] = 0
    bill_data['CardValidYY'] = 0
    bill_data['CardAuthCode'] = 0
    bill_data['CreditCardID'] = 0

    bill_data['TradeInstmt'] = ''
    bill_data['InstallmentAmount'] = ''
    bill_data['CellPhone'] = ''
    bill_data['CardHolder'] = ''
    bill_data['PlatformID'] = ''
    bill_data['AllPayID'] = ''
    bill_data['AccountID'] = ''
    bill_data['IngronAuth'] = ''
    bill_data['EnableMobileServerCall'] = ''
    bill_data['EnableWebServerCall'] = ''
    bill_data['BankCode'] = ''
    bill_data['paymentMethodToken'] = ''
    bill_data['Email'] = ''
    bill_data['CountryCode'] = ''
    bill_data['ZipCode'] = ''
    bill_data['AreaID'] = ''
    bill_data['Address'] = ''
    bill_data['IsRecord'] = ''
    bill_data['PreAddress'] = ''


    bill_data['Redeem'] = re.findall('id="Redeem" value="(.*?)"', res.text)[0]
    bill_data['Language'] = re.findall('name="Language" value="(.*?)"', res.text)[0]
    # print(bill_data)
    return bill_data



def create_bill(bill_data):
    e_header['Origin'] = 'https://payment.ecpay.com.tw'
    e_header['Content-Type'] = 'application/x-www-form-urlencoded'
    e_header['Referer'] = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut'

    res = sess.post(
        'https://payment.ecpay.com.tw/Cashier/RetainPaymentType',
        headers=e_header,
        data=bill_data
    )
    with open('bill.html', 'w') as b:
        b.write(res.text)

    b.close()

def print_nowtime():
    return datetime.datetime.now()


time_diff = lambda x, y, z: x - (y - z).seconds

if __name__ == "__main__":
    start_time = print_nowtime()
    try:
        # delete_car('619362631907c900355a82b4')
        g_tonken = get_checkoutpage()
        token_gettime = print_nowtime()
        #### 設定程序啟動時間 扣除 solver 解碼時間
        sleep_time = time_diff(118, token_gettime, start_time)
        print(sleep_time)
        time.sleep(sleep_time)
        print('start check out')
        print_nowtime()

        data = addcar()

        put_sendmethod()
        put_paymethod()

        pay_data = check_out(g_tonken)
        
    except Exception as e:
        print(e)
    end_time = print_nowtime()
    print(end_time-start_time)

    # bill_data = aiocheck_out(pay_data)

    # create_bill(bill_data)


