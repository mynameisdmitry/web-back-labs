from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# Глобальный список офисов (10 офисов)
# tenant == '' -> свободен
offices = [{"number": i, "tenant": ""} for i in range(1, 11)]


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

    # helper: ошибка
    def err(code: int, message: str):
        return {
            "jsonrpc": jsonrpc,
            "error": {"code": code, "message": message},
            "id": req_id
        }

    # helper: успех
    def ok(result):
        return {
            "jsonrpc": jsonrpc,
            "result": result,
            "id": req_id
        }

    # 1) info
    if method == 'info':
        return ok(offices)

    # Ниже методы, требующие авторизацию
    login = session.get('login')
    if not login:
        return err(1, "Unauthorized")

    # 2) booking
    if method == 'booking':
        office_number = params

        for office in offices:
            if office["number"] == office_number:
                if office["tenant"] != "":
                    return err(2, "Already booked")
                office["tenant"] = login
                return ok("success")

        return err(3, "Office not found")

    # 3) cancellation
    if method == 'cancellation':
        office_number = params

        for office in offices:
            if office["number"] == office_number:
                if office["tenant"] == "":
                    return err(4, "Not booked")
                if office["tenant"] != login:
                    return err(5, "Forbidden")
                office["tenant"] = ""
                return ok("success")

        return err(3, "Office not found")

    # method not found
    return err(-32601, "Method not found")
