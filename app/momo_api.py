import json
import urllib
import uuid
import hmac
import hashlib


def CreateOrderByMomo(total):
    endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOBKUN20180529" #"MOMOEQ4F20201024"  # busssiness momo
    accessKey = "klm05TvNBzhg7h7j" #"6UJmuB7yc8rrMah4"  # busssiness momo
    serectkey = "at67qH6mk8w5Y1nAyMoYKMWACiEi2bsa" #"0S9J1b5u1eJtTUFEOVlYxOkIMmrQW70c"  # busssiness momo
    orderInfo = "pay with MoMo"  # thông tin về order
    returnUrl = "http://localhost:5000/payment"  # redicrect sau đi hoàn tất thanh toán
    notifyUrl = "http://localhost:5000/"
    amount = str(total)  # Số tiền của hóa đơn
    orderId = str(uuid.uuid4())  # order id của momo chứ ko phải của chúng ta
    requestId = str(uuid.uuid4())  # như trên
    requestType = "captureMoMoWallet"
    extraData = "merchantName=;merchantId="
    rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" + \
                   str(amount) + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + returnUrl + \
                   "&notifyUrl=" + notifyUrl + "&extraData=" + extraData
    h = hmac.new(serectkey.encode(), rawSignature.encode(), hashlib.sha256)
    signature = h.hexdigest()

    data = {
        'partnerCode': partnerCode,
        'accessKey': accessKey,
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'returnUrl': returnUrl,
        'notifyUrl': notifyUrl,
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    data = json.dumps(data)
    clen = len(data)
    req = urllib.request.Request(endpoint, data.encode('utf-8'),
                                 {'Content-Type': 'application/json', 'Content-Length': clen}
                                 )
    f = urllib.request.urlopen(req)
    response = f.read()
    f.close()
    return json.loads(response)


def RefundOrder(total):
    pass
