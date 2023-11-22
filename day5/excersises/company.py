# Create a class called Company with the list of all employees. Create a method
# called is_punctual to return the employees who have taken leaves of more
# than 24 per year.

class Company:
    emp={}

    def __init__(self,emp):
        self.emp=emp
        
    def is_puntual(self):
        list=[]
        for key in self.emp:
            if(self.emp[key]>24):
                list.append(key)
        return list
                
            

comp=Company({
        "soumya":20,
        "sona":45,
        "ramya":5,
        "ravi":25
        })

print("Not puntual emp list",comp.is_puntual())