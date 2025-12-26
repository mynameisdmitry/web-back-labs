from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# 10 офисов: tenant == '' -> свободен
# price: пример разной стоимости (как в методичке)
offices = [
    {"number": i, "tenant": "", "price": 900 + i * 3}
    for i in range(1, 11)
]


@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.get_json(silent=True) or {}

    jsonrpc = data.get('jsonrpc', '2.0')
    method = data.get('method')
    params = data.get('params')
    req_id = data.get('id')
    

    def err(code: int, message: str):
        return {
            "jsonrpc": jsonrpc,
            "error": {"code": code, "message": message},
            "id": req_id
        }


    def ok(result):
        return {
            "jsonrpc": jsonrpc,
            "result": result,
            "id": req_id
        }

    # info (без авторизации)
    if method == 'info':
        return ok(offices)

    # дальше нужна авторизация
    login = session.get('login')
    if not login:
        return err(1, "Unauthorized")

    # booking
    if method == 'booking':
        office_number = params

        for office in offices:
            if office["number"] == office_number:
                if office["tenant"] != "":
                    return err(2, "Already booked")
                office["tenant"] = login
                return ok("success")

        return err(5, "Office not found")

    # cancellation
    if method == 'cancellation':
        office_number = params

        for office in offices:
            if office["number"] == office_number:

                if office["tenant"] == "":
                    return err(3, "Office is not rented")
                
                if office["tenant"] != login:
                    return err(4, "Not your office")
                
                office["tenant"] = ""
                return ok("success")

        return err(5, "Office not found")

    # method not found
    return err(-32601, "Method not found")
