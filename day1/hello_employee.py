from flask import Flask
app = Flask(__name__)
employees = {
1: "Prashanth",
2: "Shiva",
3: "Phani",
4: "Pranav"
}

#path variables
@app.route("/<employeeName>", methods=["GET"])
def hello_employee(employeeName):
    return "<p>Hello, {}!</p>".format(employeeName)

#path variable with data type
@app.route("/<int:employee_id>", methods=["GET"])
def hello_employee_var(employee_id):
    return "<p>Hello, {}!</p>".format(employees.get(employee_id,"Person Not Present"))