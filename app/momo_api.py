import json
import urllib
import uuid
import hmac
import hashlib


# def CreateOrderReq(total):
#     data = {
#         'total': total
#     }
#     return data


# def CreateOrderByMomo(req: CreateOrderReq):
def CreateOrderByMomo(total):
    endpoint = "https://payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOEQ4F20201024"  # busssiness momo
    accessKey = "6UJmuB7yc8rrMah4"  # busssiness momo
    serectkey = "0S9J1b5u1eJtTUFEOVlYxOkIMmrQW70c"  # busssiness momo
    orderInfo = "pay with MoMo"  # hieenj lên thông tin info
    returnUrl = "http://localhost:5000/payment"  # redicrect sau đi hoàn tất thanh toán
    notifyUrl = "http://localhost:5000/"
    # amount = str(req.total)  # Số tiền của hóa đơn
    amount = str(total)
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
